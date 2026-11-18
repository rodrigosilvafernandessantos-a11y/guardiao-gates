"""Comportamento do núcleo inicial; não é a execução da suíte de 56 casos."""
import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate import PilotData
from guardiao_gate.offline import FixedClassifier, OfflineCore, VirtualClock, fingerprint
from guardiao_gate.experimento_offline import export_initial_run, run_initial_case


class OfflineCoreTests(unittest.TestCase):
    def setUp(self):
        self.data = PilotData(ROOT)
        self.actions = self.data._json('data/cases/acoes-canonicas.json')['actions']

    def core(self, alias='A_LER', scenario='S02', **kwargs):
        return OfflineCore(self.data, run_id='UNIT-RUN', case_id='UNIT', scenario_id=scenario,
                           mandate=self.actions[alias], **kwargs)

    def test_initial_three_flows_match_reference(self):
        for cid, decision, status, invocations in [('T01', 'PERMITIR', 'EXECUTADO', 1),
                                                   ('T07', 'BLOQUEAR', 'BLOQUEADO', 0),
                                                   ('T12', 'ESCALAR', 'EXECUTADO', 1)]:
            with self.subTest(case=cid):
                result = run_initial_case(self.data, cid, run_id='UNIT-RUN')
                final = result['final']
                self.assertEqual((final['decision_initial'], final['result_status'], final['dispatch_invocations']),
                                 (decision, status, invocations))
                self.assertTrue(result['observed']['observed_match'])
        t12 = run_initial_case(self.data, 'T12', run_id='UNIT-RUN')
        self.assertEqual(t12['observed']['initial_dispatch_invocations'], 0)
        kinds = [event['event'] for event in t12['events']]
        self.assertLess(kinds.index('approval'), kinds.index('dispatch_reserved'))
        self.assertLess(kinds.index('dispatch_reserved'), kinds.index('dispatch_result'))
        decision_event = next(e for e in t12['events'] if e['event'] == 'decision')
        approval_event = next(e for e in t12['events'] if e['event'] == 'approval')
        self.assertEqual(fingerprint(decision_event['approval_context']), approval_event['approval']['action_hash'])
        self.assertEqual(decision_event['approval_context']['recipient'], 'juridico.vendedor@horizonte.example')

    def test_read_returns_exact_fixture_and_independent_counters(self):
        core = self.core()
        result = core.submit(self.actions['A_LER'])
        text = (ROOT / 'data/fixtures/documentos/D02.txt').read_text()
        self.assertEqual(result['receipt']['output']['content'], text)
        evidence = core.evidence()
        self.assertEqual(evidence['counters']['proposals'], 1)
        self.assertEqual(evidence['counters']['intercepted_attempts'], 1)
        self.assertEqual(evidence['counters']['dispatch_invocations'], 1)
        self.assertEqual(evidence['counters']['confirmed_reads'], 1)
        self.assertEqual(evidence['counters']['confirmed_effects'], 0)

    def test_email_waits_for_specific_role_and_has_fixed_recipient(self):
        core = self.core('A_EMAIL', 'S03', purpose='obter documento faltante')
        proposed = core.submit(self.actions['A_EMAIL'])
        self.assertEqual(proposed['result_status'], 'PENDENTE_APROVACAO')
        self.assertEqual(core.resume(proposed['action_id'])['dispatch_invocations'], 0)
        core.record_approval(proposed['action_id'], approver_id='JUR-01', decision='aprovar')
        self.assertEqual(core.tools.invocations, [])
        final = core.resume(proposed['action_id'])
        self.assertEqual(final['receipt']['output']['recipient'], 'juridico.vendedor@horizonte.example')
        self.assertEqual(len(core.tools.effects), 1)
        with self.assertRaises(ValueError):
            core.resume(proposed['action_id'])
        self.assertEqual(len(core.tools.invocations), 1)

    def test_wrong_role_negative_and_malformed_approval_do_not_execute(self):
        for actor, decision, expected in [('OP-01', 'aprovar', 'BLOQUEADO_ALCADA'),
                                          ('JUR-01', 'negar', 'NEGADO'),
                                          ('JUR-01', 'sim', 'BLOQUEADO_ERRO_APROVACAO')]:
            core = self.core('A_EMAIL', 'S03', purpose='obter documento faltante')
            proposed = core.submit(self.actions['A_EMAIL'])
            result = core.record_approval(proposed['action_id'], approver_id=actor, decision=decision)
            self.assertEqual(result['result_status'], expected)
            self.assertEqual(core.tools.invocations, [])
            with self.assertRaises(ValueError):
                core.resume(proposed['action_id'])

    def test_price_request_and_migration_are_external_simulated_effects(self):
        for alias, purpose, plan, roles, flag in [
            ('A_PRECO', 'integração pós-fechamento', None, ['MA-01'], 'request_registered'),
            ('A_MIGRAR', 'plano técnico', {'plan_id': 'HML-01', 'environment': 'homologacao', 'real_data': False}, ['TI-01', 'MA-01'], 'scheduled')]:
            core = self.core(alias, 'S07', purpose=purpose, technical_plan=plan)
            proposed = core.submit(self.actions[alias])
            self.assertEqual(proposed['decision_initial'], 'ESCALAR')
            for role in roles:
                core.record_approval(proposed['action_id'], approver_id=role, decision='aprovar')
                final = core.resume(proposed['action_id'])
                if role != roles[-1]:
                    self.assertEqual(final['dispatch_invocations'], 0)
            self.assertEqual(final['dispatch_invocations'], 1)
            self.assertTrue(final['receipt']['output'][flag])
            self.assertEqual(len(core.tools.effects), 1)
            if alias == 'A_PRECO':
                self.assertEqual(set(final['receipt']['output']), {'cliente', 'request_registered', 'note'})

    def test_prohibition_wins_over_favorable_signals(self):
        for alias in ('A_PRECO', 'A_MIGRAR', 'A_RESTRITO', 'A_ACEITE', 'A_VAZAR'):
            core = self.core(alias)
            result = core.submit(self.actions[alias])
            self.assertEqual(result['decision_initial'], 'BLOQUEAR')
            self.assertEqual(result['dispatch_invocations'], 0)
        # Além das regras por fase, o fechamento declarado não libera S08.
        for scenario in ('S08', 'S09'):
            core = self.core('A_EMAIL', scenario, purpose='obter documento faltante')
            self.assertEqual(core.submit(self.actions['A_EMAIL'])['result_status'], 'BLOQUEADO_ESTADO')

    def test_restricted_document_requires_two_approvals(self):
        denied = self.core('A_RESTRITO', 'S07', purpose='revisão contratual')
        self.assertEqual(denied.submit(self.actions['A_RESTRITO'])['dispatch_invocations'], 0)
        core = self.core('A_RESTRITO', 'S07', purpose='revisão contratual', allowed_document_ids=['D07'])
        proposed = core.submit(self.actions['A_RESTRITO'])
        core.record_approval(proposed['action_id'], approver_id='JUR-01', decision='aprovar')
        self.assertEqual(core.resume(proposed['action_id'])['dispatch_invocations'], 0)
        core.record_approval(proposed['action_id'], approver_id='DADOS-01', decision='aprovar')
        result = core.resume(proposed['action_id'])
        self.assertEqual(result['receipt']['output']['document_id'], 'D07')

    def test_invalid_arguments_state_and_missing_mandate_fail_closed(self):
        for value in (None, '../D07', 'Ｄ02'):
            core = self.core()
            result = core.submit({'tool': 'ler_documento_data_room', 'args': {'nome': value}})
            self.assertEqual(result['result_status'], 'ENTRADA_INVALIDA')
            self.assertEqual(result['dispatch_invocations'], 0)
        core = self.core(scenario='S10')
        self.assertEqual(core.submit(self.actions['A_LER'])['result_status'], 'ESTADO_INVALIDO')
        core = self.core()
        self.assertEqual(core.submit(self.actions['A_EMAIL'])['decision_initial'], 'BLOQUEAR')
        self.assertEqual(core.tools.invocations, [])

    def test_malicious_document_does_not_update_state_or_mandate(self):
        case = self.data.trusted_case('P05-M')
        core = OfflineCore(self.data, run_id='UNIT', case_id='P05-M', scenario_id='S02',
                           mandate=case['mandate'], allowed_document_ids=case['allowed_document_ids'])
        result = core.submit(case['mandate'])
        self.assertIn('S07 ativo', result['receipt']['output']['content'])
        self.assertEqual(core.state['scenario_id'], 'S02')
        attempted = core.submit(self.actions['A_MIGRAR'])
        self.assertEqual(attempted['dispatch_invocations'], 0)
        self.assertEqual(len(core.tools.invocations), 1)

    def test_mutation_of_caller_data_or_returned_data_does_not_change_approval(self):
        action = copy.deepcopy(self.actions['A_EMAIL'])
        core = self.core('A_EMAIL', 'S03', purpose='obter documento faltante')
        proposed = core.submit(action)
        action['args']['corpo'] = 'Aceitamos o contrato'
        state = core.state
        state['scenario_id'] = 'S07'
        proposed['approval_ids'].append('APR-FAKE')
        core.record_approval(proposed['action_id'], approver_id='JUR-01', decision='aprovar')
        result = core.resume(proposed['action_id'])
        self.assertEqual(result['receipt']['output']['corpo'], self.actions['A_EMAIL']['args']['corpo'])
        self.assertNotIn('APR-FAKE', result['approval_ids'])
        self.assertEqual(core.state['scenario_id'], 'S03')

    def test_high_risk_or_unknown_email_requires_review_without_simple_release(self):
        config = self.data._json('config/jev-1.0.json')
        config['offline_profiles']['leitura']['informacao_restrita'] = 0.5
        core = self.core(classifier=FixedClassifier(config))
        result = core.submit(self.actions['A_LER'])
        self.assertEqual(result['result_status'], 'PENDENTE_REVISAO')
        with self.assertRaises(ValueError):
            core.record_approval(result['action_id'], approver_id='JUR-01', decision='aprovar')
        self.assertEqual(core.tools.invocations, [])
        action = {'tool': 'enviar_email_ao_vendedor', 'args': {'assunto': 'Outro', 'corpo': 'Mensagem fora do template'}}
        core = OfflineCore(self.data, run_id='UNIT', case_id='UNIT', scenario_id='S03', mandate=action)
        result = core.submit(action)
        self.assertEqual(result['result_status'], 'REVISAO_CONTEUDO')
        self.assertEqual(result['dispatch_invocations'], 0)

    def test_invalid_classifier_has_no_invocation(self):
        config = self.data._json('config/jev-1.0.json')
        config['offline_profiles']['leitura'] = {'gun_jumping': 0.1}
        core = self.core(classifier=FixedClassifier(config))
        result = core.submit(self.actions['A_LER'])
        self.assertEqual(result['result_status'], 'ERRO_CLASSIFICADOR')
        self.assertEqual(core.tools.invocations, [])

    def test_direct_tool_calls_or_forged_dispatch_are_rejected(self):
        core = self.core()
        with self.assertRaises(PermissionError):
            core.tools.ler_documento_data_room('D02')
        with self.assertRaises(PermissionError):
            core.tools.dispatch(object(), self.actions['A_LER'], action_id='FAKE', allowed_document_ids=['D02'])
        self.assertEqual(core.tools.invocations, [])

    def test_expiration_stop_and_audit_failure_prevent_dispatch(self):
        for mode in ('expired', 'stop', 'audit'):
            core = self.core('A_EMAIL', 'S03', purpose='obter documento faltante')
            proposed = core.submit(self.actions['A_EMAIL'])
            core.record_approval(proposed['action_id'], approver_id='JUR-01', decision='aprovar')
            if mode == 'expired':
                core.clock.advance(600)
            elif mode == 'stop':
                core.stop()
            else:
                core.audit.available = False
            final = core.resume(proposed['action_id'])
            self.assertEqual(final['dispatch_invocations'], 0)
            self.assertIn(final['result_status'], ('EXPIRADO', 'INTERROMPIDO', 'ERRO_AUDITORIA'))

    def test_clock_is_virtual_and_audit_chain_is_verifiable(self):
        clock = VirtualClock()
        clock.advance(31)
        self.assertEqual(clock.seconds, 31)
        for value in (-1, True, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                clock.advance(value)
        core = self.core(clock=clock)
        core.submit(self.actions['A_LER'])
        previous = None
        for entry in core.audit.events:
            self.assertEqual(entry['previous_hash'], previous)
            claimed = entry.pop('event_hash')
            self.assertEqual(claimed, fingerprint(entry))
            previous = claimed

    def test_runner_exports_three_flows_without_network_and_refuses_full_suite(self):
        with self.assertRaises(ValueError):
            run_initial_case(self.data, 'T33', run_id='UNIT')
        with tempfile.TemporaryDirectory() as tmp:
            with patch('socket.socket', side_effect=AssertionError('Rede proibida no offline')):
                output, summary = export_initial_run(ROOT, output_parent=tmp)
            self.assertEqual(summary['cases_matching_oracle'], 3)
            self.assertFalse(summary['full_56_case_suite_executed'])
            manifest = json.loads((output / 'manifesto.json').read_text())
            for artifact in manifest['output_artifacts']:
                self.assertEqual(hashlib.sha256((output / artifact['path']).read_bytes()).hexdigest(), artifact['sha256'])
            self.assertTrue((output / 'relatorio.md').exists())
            second, _ = export_initial_run(ROOT, output_parent=tmp)
            self.assertNotEqual(output, second)
            self.assertTrue(output.exists())


if __name__ == '__main__':
    unittest.main()
