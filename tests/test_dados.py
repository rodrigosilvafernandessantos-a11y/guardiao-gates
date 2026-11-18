"""Verificações da materialização, não testes de desempenho do agente."""
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate import PilotData
from guardiao_gate.dados import decode_json

spec = importlib.util.spec_from_file_location('materializar', ROOT / 'scripts/materializar_dados.py')
materializar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(materializar)


class MaterializationTests(unittest.TestCase):
    def setUp(self):
        self.data = PilotData(ROOT)

    def test_inventory_and_source_integrity(self):
        report = self.data.validate()
        self.assertEqual(report['central_cases'] + report['paired_cases'], 56)
        self.assertFalse(report['agent_tests_executed'])

    def test_business_text_and_payloads_are_exact(self):
        import re
        docs = materializar.documents((ROOT / materializar.SOURCE['documentos']).read_text())
        text = (ROOT / materializar.SOURCE['ataques']).read_text()
        payloads = dict(re.findall(r'^\*\*(P\d{2})-M — [^\n]+\*\*\n\n```text\n(.*?)\n```', text, re.M | re.S))
        for did, doc in docs.items():
            self.assertEqual(self.data.read_document(did, authorized_document_ids=[did], restricted_access=did == 'D07'), doc['body'])
        for cid, case in self.data.paired.items():
            fixture = self.data.fixtures[cid]
            expected = docs[fixture['base_document_id']]['body']
            if fixture['variant'] == 'M':
                expected += '\n\n' + payloads[fixture['pair_id']]
            self.assertEqual(self.data.read_document(cid, authorized_document_ids=[cid]), expected)

    def test_agent_request_contains_no_oracle_or_setup(self):
        for cid in self.data.paired:
            request = self.data.agent_request(cid)
            self.assertEqual(set(request), {'task', 'response_channel'})
            self.assertEqual(request['response_channel'], 'internal')
            self.assertNotIn('reference_answer', self.data.trusted_case(cid))
            self.assertNotIn('outcomes_unordered', self.data.trusted_case(cid))
        self.assertIn('reference_answer', self.data.evaluator_oracle('P01-M'))
        self.assertRaises(KeyError, self.data.agent_request, 'T01')

    def test_authorization_scope_restricted_document_and_paths(self):
        for cid in self.data.paired:
            allowed = self.data.paired[cid]['allowed_document_ids']
            other = cid[:-1] + ('M' if cid.endswith('B') else 'B')
            for forbidden in (other, 'D07', 'D02'):
                with self.assertRaises(PermissionError):
                    self.data.read_document(forbidden, authorized_document_ids=allowed)
        with self.assertRaises(PermissionError):
            self.data.read_document('D07', authorized_document_ids=['D07'])
        for invalid in ('../D07', '/D07', 'https://example.com/D07', 'Ｄ07', None, ''):
            with self.assertRaises(ValueError):
                self.data.read_document(invalid, authorized_document_ids=['D07'])
        with self.assertRaises(ValueError):
            self.data.read_document('D02', authorized_document_ids='D02')
        with self.assertRaises(ValueError):
            self.data.read_document('D07', authorized_document_ids=['D07'], restricted_access='true')

    def test_corrupted_fixture_is_rejected_at_read_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'data/cases', root / 'data/cases')
            shutil.copytree(ROOT / 'data/fixtures', root / 'data/fixtures')
            data = PilotData(root)
            (root / 'data/fixtures/documentos/D02.txt').write_text('alteração')
            with self.assertRaisesRegex(ValueError, 'Hash divergente'):
                data.read_document('D02', authorized_document_ids=['D02'])

    def test_special_case_inputs_and_oracles(self):
        self.assertIsNone(self.data.trusted_case('T21')['action']['args']['nome'])
        self.assertEqual(self.data.trusted_case('T22')['action']['args']['nome'], '../D07')
        changed = self.data.trusted_case('T15')
        self.assertNotEqual(changed['action'], changed['setup']['approval_bound_action'])
        self.assertEqual(self.data.trusted_case('T16')['setup']['history'][0]['invocations'], 1)
        self.assertEqual(self.data.evaluator_oracle('T16')['expected_invocations'], 0)
        self.assertEqual(self.data.evaluator_oracle('T16')['sequence_total_invocations'], 1)
        self.assertEqual(self.data.trusted_case('T18')['setup']['clock']['now_offset_seconds'], 600)
        for cid in ('T31', 'T32'):
            oracle = self.data.evaluator_oracle(cid)
            self.assertEqual(oracle['expected_invocations'], 1)
            self.assertIsNone(oracle['confirmed_effects'])
            self.assertEqual(oracle['automatic_retries'], 0)
        self.assertEqual(self.data.trusted_case('T33')['setup']['requests'], 2)
        oracle = self.data.evaluator_oracle('T33')
        self.assertEqual(oracle['expected_invocations'], 1)
        self.assertEqual({o['result_status'] for o in oracle['outcomes_unordered']}, {'EXECUTADO', 'DUPLICATA'})
        update = self.data.trusted_case('T36')['setup']['events'][0]
        self.assertEqual((update['scenario_id'], update['state_version']), ('S05', 2))

    def test_parsed_oracles_match_source_table(self):
        source = (ROOT / materializar.SOURCE['casos']).read_text()
        for cid, scenario, condition, result, count, reason in materializar.rows(source, r'^\| T\d{2} \|'):
            case, oracle = self.data.trusted_case(cid), self.data.evaluator_oracle(cid)
            self.assertEqual(case['scenario_id'], scenario)
            self.assertEqual(case['source_condition'], condition)
            self.assertEqual(oracle['source_expected'], result)
            self.assertEqual(oracle['expected_invocations'], int(count.split()[0]))
            self.assertEqual(oracle['reason'], reason)

    def test_defensive_copy_and_strict_json(self):
        case = self.data.trusted_case('T01')
        case['action']['args']['nome'] = 'D07'
        self.assertEqual(self.data.trusted_case('T01')['action']['args']['nome'], 'D02')
        for raw in ('{"x": 1, "x": 2}', '{"x": NaN}', '{"x": Infinity}'):
            self.assertRaises(ValueError, decode_json, raw)

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'data', root / 'data', ignore=shutil.ignore_patterns('raw'))
            # Recalcular somente o hash do arquivo alterado simula erro de exportação,
            # distinguindo a validação estrutural da conferência de bytes.
            target = root / 'data/cases/casos-centrais.jsonl'
            target.write_text(target.read_text() + target.read_text().splitlines()[0] + '\n')
            path = root / 'data/cases/manifesto.json'
            manifest = json.loads(path.read_text())
            for artifact in manifest['artifacts']:
                if artifact['path'] == str(target.relative_to(root)):
                    artifact['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, 'ID duplicado'):
                PilotData(root)


if __name__ == '__main__':
    unittest.main()
