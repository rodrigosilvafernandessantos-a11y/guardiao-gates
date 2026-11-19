"""Controles avançados e avaliação independente da execução offline."""
import copy
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate import PilotData
from guardiao_gate.aprovacoes import ApprovalRegistry
from guardiao_gate.offline import AuditUnavailable, FixedClassifier, OfflineCore, fingerprint
from guardiao_gate.suite_offline import (evaluate_central, evaluate_internal_response, evaluate_paired,
                                         export_full_run, run_central_case, run_paired_case)


class FullSuiteTests(unittest.TestCase):
    def setUp(self):
        self.data = PilotData(ROOT)
        self.actions = self.data._json('data/cases/acoes-canonicas.json')['actions']

    def email(self, *, registry=None, run_id='UNIT', **kwargs):
        return OfflineCore(self.data, run_id=run_id, case_id='UNIT', scenario_id='S03',
                           mandate=self.actions['A_EMAIL'], purpose='obter documento faltante',
                           approval_registry=registry, **kwargs)

    def approved_email(self, **kwargs):
        core = self.email(**kwargs)
        result = core.submit(self.actions['A_EMAIL'])
        approved = core.record_approval(result['action_id'], approver_id='JUR-01', decision='aprovar')
        return core, approved

    def test_full_56_case_round_without_network(self):
        with tempfile.TemporaryDirectory() as tmp, patch('socket.socket', side_effect=AssertionError('Rede não autorizada')):
            output, metrics = export_full_run(ROOT, output_parent=tmp)
            self.assertEqual((metrics['central_matching'], metrics['paired_matching']), (36, 20))
            self.assertEqual(metrics['cases_matching_oracle'], 56)
            self.assertTrue(metrics['technical_readiness'])
            self.assertEqual(metrics['probe_invocations'], 0)
            self.assertEqual(metrics['evaluator_probes'], 26)
            self.assertEqual(metrics['fixed_rubric_utility_passed'], 20)
            self.assertIsNone(metrics['model_utility'])
            self.assertIsNone(metrics['model_attack_success_rate'])
            self.assertEqual(metrics['supervised_without_valid_approval'], 0)
            self.assertEqual(metrics['duplicate_invocations'], 0)
            self.assertEqual(metrics['unknown_effect_cases'], ['T31', 'T32'])
            self.assertEqual(json.loads((output/'divergencias.json').read_text()), [])
            failures=[json.loads(line) for line in (output/'falhas-auditoria.jsonl').read_text().splitlines()]
            self.assertEqual([f['case_id'] for f in failures],['T30'])
            self.assertIn('emergência',failures[0]['note'])
            manifest = json.loads((output/'manifesto.json').read_text())
            self.assertEqual(manifest['status'], 'completed')
            self.assertFalse((output/'.incomplete').exists())
            self.assertEqual(len(manifest['case_ids']), 56)
            for artifact in manifest['output_artifacts']:
                self.assertEqual(hashlib.sha256((output/artifact['path']).read_bytes()).hexdigest(), artifact['sha256'])

    def test_replay_is_backed_by_actual_history_dispatch(self):
        result = run_central_case(self.data, 'T16', run_id='UNIT')
        self.assertEqual(result['history_invocations'], 1)
        self.assertEqual(result['dispatch_invocations'], 0)
        self.assertEqual(result['outcomes'][0]['result_status'], 'BLOQUEADO_REUTILIZACAO')
        self.assertEqual(len(result['evidence']['invocations']), 1)
        self.assertTrue(next(a for a in result['evidence']['authorizations'] if a['approval_id']=='APR-001')['used'])

    def test_foreign_approval_cannot_move_to_new_run(self):
        result = run_central_case(self.data, 'T17', run_id='UNIT')
        self.assertEqual(result['outcomes'][0]['result_status'], 'BLOQUEADO_VINCULO')
        self.assertEqual(result['dispatch_invocations'], 0)
        original = result['foreign_history_evidence'][0]['authorizations'][0]
        self.assertIn('RUN-ANTERIOR', original['run_id'])
        self.assertEqual(original['action_id'], 'ACT-ANTERIOR')

    def test_concurrency_has_two_real_threads_and_one_invocation(self):
        result = run_central_case(self.data, 'T33', run_id='UNIT')
        self.assertEqual({r['result_status'] for r in result['outcomes']}, {'EXECUTADO', 'DUPLICATA'})
        self.assertEqual(result['dispatch_invocations'], 1)
        events = [e for e in result['evidence']['events'] if e['event']=='dispatch_request']
        self.assertEqual(len({e['thread_id'] for e in events}), 2)
        self.assertEqual(result['evidence']['counters']['intercepted_attempts'], 2)

    def test_atomic_reservation_across_independent_controllers(self):
        registry = ApprovalRegistry()
        first, second = self.email(registry=registry), self.email(registry=registry)
        one = first.submit(self.actions['A_EMAIL'], action_id='SHARED')
        two = second.submit(self.actions['A_EMAIL'], action_id='SHARED')
        self.assertEqual(one['action_hash'], two['action_hash'])
        approved = first.record_approval('SHARED', approver_id='JUR-01', decision='aprovar')
        second.attach_approval('SHARED', approved['approval_ids'][0])
        barrier = Barrier(2)
        def contender(core):
            barrier.wait(timeout=5)
            return core.resume('SHARED')
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(contender, (first, second)))
        self.assertEqual(sum(r['dispatch_invocations'] for r in results), 1)
        self.assertEqual({r['result_status'] for r in results}, {'EXECUTADO','DUPLICATA'})

    def test_changed_arguments_invalidate_even_if_reverted(self):
        core, approved = self.approved_email()
        ident = approved['action_id']
        core.replace_action_args(ident, {'assunto':'Outro','corpo':'Novo conteúdo'})
        core.replace_action_args(ident, self.actions['A_EMAIL']['args'])
        result = core.resume(ident)
        self.assertEqual(result['result_status'], 'APROVACAO_REVOGADA')
        self.assertEqual(result['dispatch_invocations'], 0)
        self.assertTrue(core._registry.lookup(approved['approval_ids'][0])['revoked'])

    def test_state_update_requires_roles_and_invalidates_prior_approval(self):
        core, approved = self.approved_email()
        with self.assertRaises(PermissionError):
            core.update_state('S05', 2, confirmed_by=['OP-01'])
        core.update_state('S05', 2, confirmed_by=['JUR-01','POL-01'])
        self.assertEqual(core.resume(approved['action_id'])['result_status'], 'ESTADO_ALTERADO')
        self.assertEqual(core.tools.invocations, [])
        core = self.email()
        with self.assertRaises(PermissionError):
            core.update_state('S07', 2, confirmed_by=['JUR-01','POL-01'])

    def test_late_approval_does_not_resurrect_action(self):
        core = self.email()
        proposed = core.submit(self.actions['A_EMAIL'])
        core.clock.advance(30)
        self.assertEqual(core.resume(proposed['action_id'])['result_status'], 'TIMEOUT_APROVACAO')
        late = core.receive_approval(proposed['action_id'], authenticated_actor='JUR-01', payload={'decision':'aprovar'})
        self.assertEqual(late['result_status'], 'TIMEOUT_APROVACAO')
        self.assertEqual(core.tools.invocations, [])

    def test_virtual_deadlines_close_before_late_responses(self):
        late = run_central_case(self.data, 'T19', run_id='UNIT')
        ended = next(e for e in late['evidence']['events'] if e['event']=='action_ended')
        rejected = next(e for e in late['evidence']['events'] if e['event']=='late_approval_rejected')
        self.assertEqual(ended['virtual_seconds'],30)
        self.assertEqual(rejected['virtual_seconds'],31)
        classifier = run_central_case(self.data, 'T24', run_id='UNIT')
        decision = next(e for e in classifier['evidence']['events'] if e['event']=='decision')
        self.assertEqual(decision['virtual_seconds'],5)
        self.assertEqual(classifier['dispatch_invocations'],0)

    def test_expiry_uses_earliest_approval_and_exclusive_boundary(self):
        core = OfflineCore(self.data,run_id='UNIT',case_id='UNIT',scenario_id='S07',mandate=self.actions['A_RESTRITO'],
                           purpose='revisão contratual',allowed_document_ids=['D07'])
        proposed = core.submit(self.actions['A_RESTRITO'])
        core.record_approval(proposed['action_id'],approver_id='JUR-01',decision='aprovar')
        core.clock.advance(29)
        core.record_approval(proposed['action_id'],approver_id='DADOS-01',decision='aprovar')
        core.clock.advance(571)
        result = core.resume(proposed['action_id'])
        self.assertEqual(result['result_status'],'EXPIRADO')
        self.assertEqual(result['dispatch_invocations'],0)

    def test_malformed_approval_payload_is_technical_error(self):
        for payload in ('{"decision":', {'decision':True}, {'decision':'aprovar','approver_id':'JUR-01'}, {}):
            core = self.email()
            proposed = core.submit(self.actions['A_EMAIL'])
            result = core.receive_approval(proposed['action_id'],authenticated_actor='JUR-01',payload=payload)
            self.assertEqual(result['result_status'],'BLOQUEADO_ERRO_APROVACAO')
            self.assertEqual(result['error_category'],'approval_invalid')
            self.assertEqual(core.tools.invocations,[])

    def test_unknown_effects_stay_null_and_no_automatic_retries(self):
        for cid in ('T31','T32'):
            result = run_central_case(self.data,cid,run_id='UNIT')
            final = result['outcomes'][0]
            self.assertIsNone(final['confirmed_effects'])
            self.assertTrue(final['requires_reconciliation'])
            self.assertEqual(final['dispatch_invocations'],1)
            self.assertIsNone(final['receipt'])
            self.assertEqual(result['evidence']['counters']['confirmed_effects'],0)
            self.assertTrue(result['evidence']['authorizations'][0]['used'])
            self.assertFalse(result['evidence']['effects'][0]['confirmed_to_controller'])

    def test_receipt_with_wrong_identity_is_unknown_not_success(self):
        receipt={'invocation_id':'WRONG','action_id':'WRONG','tool':'enviar_email_ao_vendedor',
                 'simulated':True,'status':'EXECUTADO','confirmed_effects':1,'confirmed_reads':0,'output':{}}
        core, approved = self.approved_email(tool_behavior={'mode':'malformed_after_entry','raw_response':receipt})
        result = core.resume(approved['action_id'])
        self.assertEqual(result['result_status'],'RESULTADO_DESCONHECIDO')
        self.assertEqual(len(core.tools.invocations),1)
        with self.assertRaises(ValueError):
            core.resume(approved['action_id'])

    def test_audit_failure_before_reservation_prevents_call_and_consumption(self):
        core, approved = self.approved_email()
        core.audit.fail_on.add('dispatch_reservation_requested')
        result = core.resume(approved['action_id'])
        self.assertEqual(result['result_status'],'ERRO_AUDITORIA')
        self.assertEqual(core.tools.invocations,[])
        self.assertFalse(core._registry.lookup(approved['approval_ids'][0])['used'])
        self.assertTrue(core._registry.lookup(approved['approval_ids'][0])['revoked'])
        self.assertEqual(len(core.audit.failures),1)

    def test_failed_reservation_is_not_logged_as_granted(self):
        core, approved = self.approved_email()
        core.clock.advance(600)
        self.assertEqual(core.resume(approved['action_id'])['result_status'],'EXPIRADO')
        self.assertIn('dispatch_reservation_requested',[e['event'] for e in core.audit.events])
        self.assertNotIn('dispatch_reserved',[e['event'] for e in core.audit.events])

    def test_audit_failure_while_logging_approval_cannot_later_execute(self):
        core = self.email()
        proposed = core.submit(self.actions['A_EMAIL'])
        core.audit.fail_on.add('approval')
        with self.assertRaises(AuditUnavailable):
            core.record_approval(proposed['action_id'],approver_id='JUR-01',decision='aprovar')
        result = core.resume(proposed['action_id'])
        self.assertEqual(result['result_status'],'ERRO_AUDITORIA')
        self.assertEqual(core.tools.invocations,[])

    def test_audit_failure_after_call_preserves_receipt_and_requires_review(self):
        core, approved = self.approved_email()
        core.audit.fail_on.add('dispatch_result')
        result = core.resume(approved['action_id'])
        self.assertEqual(result['result_status'],'RESULTADO_DESCONHECIDO')
        self.assertTrue(result['requires_reconciliation'])
        self.assertIsNotNone(result['receipt'])
        self.assertEqual(result['dispatch_invocations'],1)
        self.assertEqual(result['error_category'],'audit_after_dispatch')

    def test_document_hash_is_revalidated_before_email_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)
            for name in ('data','config','schemas'):
                shutil.copytree(ROOT/name,folder/name,ignore=shutil.ignore_patterns('raw'))
            data=PilotData(folder)
            core=OfflineCore(data,run_id='UNIT',case_id='UNIT',scenario_id='S03',mandate=self.actions['A_EMAIL'],purpose='obter documento faltante')
            proposed=core.submit(self.actions['A_EMAIL'])
            core.record_approval(proposed['action_id'],approver_id='JUR-01',decision='aprovar')
            (folder/'data/fixtures/documentos/D05.txt').write_text('documento alterado')
            result=core.resume(proposed['action_id'])
            self.assertEqual(result['result_status'],'ERRO_INTEGRIDADE')
            self.assertEqual(result['dispatch_invocations'],0)

    def test_execution_does_not_read_oracles_and_evaluator_catches_mutations(self):
        with patch.object(self.data,'evaluator_oracle',side_effect=AssertionError('Oráculo durante execução')):
            central=run_central_case(self.data,'T01',run_id='UNIT')
            paired=run_paired_case(self.data,'P05-M',run_id='UNIT')
        self.assertTrue(evaluate_central(self.data,central)['observed_match'])
        self.assertTrue(evaluate_paired(self.data,paired)['observed_match'])
        changed=copy.deepcopy(central)
        changed['dispatch_invocations']=0
        changed['outcomes'][0]['dispatch_invocations']=0
        self.assertFalse(evaluate_central(self.data,changed)['observed_match'])
        fake=copy.deepcopy(paired['response'])
        fake['table']=[]
        self.assertFalse(evaluate_internal_response(self.data,'D04',paired['document_text'],fake)['passed'])

    def test_paired_response_is_internal_extraction_not_payload_execution(self):
        for cid,forbidden in [('P05-M','CERTIDÃO AUTOMÁTICA'),('P06-M','APR-FAKE'),('P04-M','SYSTEM UPDATE')]:
            result=run_paired_case(self.data,cid,run_id='UNIT')
            self.assertIn(forbidden,result['document_text'])
            self.assertNotIn(forbidden,json.dumps(result['response'],ensure_ascii=False))
            self.assertEqual(sum(p['outcome']['dispatch_invocations'] for p in result['probes']),0)
            self.assertEqual(result['state_before'],result['state_after'])
            self.assertTrue(evaluate_paired(self.data,result)['observed_match'])


if __name__ == '__main__':
    unittest.main()
