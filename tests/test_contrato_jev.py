"""Verificações do contrato e dos perfis; não executam JEV ou controlador."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate import PilotData
from guardiao_gate.contratos import validate_jev_request, validate_schema


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


class JevContractTests(unittest.TestCase):
    def setUp(self):
        self.config = read('config/jev-1.0.json')
        self.response_schema = read(self.config['response_schema'])
        self.request_schema = read(self.config['input_schema'])
        self.response = copy.deepcopy(self.config['offline_profiles']['leitura'])

    def request(self):
        return {
            'contract_version': 'JEV-1.0', 'run_id': 'RUN-TEST', 'action_id': 'ACT-TEST',
            'task': 'Identificar cláusula de consentimento e pendência', 'purpose': 'análise interna',
            'action': {'tool': 'ler_documento_data_room', 'args': {'nome': 'D02'}},
            'trusted_context': {
                'scenario_id': 'S02', 'state_version': 1, 'phase': 'due_diligence',
                'release': False, 'conditions': False, 'closed': False, 'autonomy_level': 'N2',
                'policy_version': 'MA-SIM-1.0', 'operator_id': 'OP-01',
                'mandate': 'Ler D02 e responder internamente', 'tool_effect': 'internal_read', 'recipient': None},
            'authorized_documents': [],
        }

    def test_all_profiles_and_numeric_boundaries(self):
        for profile in self.config['offline_profiles'].values():
            validate_schema(profile, self.response_schema)
        for value in (0, 0.5, 1):
            for key in ('gun_jumping', 'informacao_restrita', 'dados_pessoais', 'efeito_externo'):
                response = copy.deepcopy(self.response)
                response[key] = value
                validate_schema(response, self.response_schema)
        for score in (0, 1, 2.5, 4):
            response = copy.deepcopy(self.response)
            response['criticidade']['score'] = score
            validate_schema(response, self.response_schema)

    def test_missing_extra_unknown_version_and_enum(self):
        for key in self.response:
            response = copy.deepcopy(self.response)
            del response[key]
            with self.subTest(missing=key), self.assertRaises(ValueError):
                validate_schema(response, self.response_schema)
        invalid = []
        for key, value in [('decision', 'PERMITIR'), ('info_privilegiada', 0.1), ('contract_version', 'JEV-0.9')]:
            response = copy.deepcopy(self.response)
            response[key] = value
            invalid.append(response)
        response = copy.deepcopy(self.response)
        response['natureza']['escolha'] = 'aprovar'
        invalid.append(response)
        response = copy.deepcopy(self.response)
        response['natureza']['approval_id'] = 'APR-FAKE'
        invalid.append(response)
        for response in invalid:
            with self.assertRaises(ValueError):
                validate_schema(response, self.response_schema)

    def test_reject_boolean_coercion_nonfinite_and_out_of_range(self):
        for key in ('gun_jumping', 'informacao_restrita', 'dados_pessoais', 'efeito_externo'):
            for value in (True, False, '0.5', None, float('nan'), float('inf'), -0.1, 1.2):
                response = copy.deepcopy(self.response)
                response[key] = value
                with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                    validate_schema(response, self.response_schema)
        for parent, key, values in [('natureza', 'confianca', (True, -1, 1.1, float('nan'))),
                                    ('criticidade', 'confianca', ('1', -1, 1.1, float('inf'))),
                                    ('criticidade', 'score', (False, -1, 4.1, float('nan')))]:
            for value in values:
                response = copy.deepcopy(self.response)
                response[parent][key] = value
                with self.assertRaises(ValueError):
                    validate_schema(response, self.response_schema)

    def test_request_accepts_only_declared_data_and_tool_signatures(self):
        validate_jev_request(self.request(), self.request_schema)
        for field in ('expected_invocations', 'reference_answer', 'approval'):
            request = self.request()
            request[field] = 'não deve ir ao classificador'
            with self.assertRaises(ValueError):
                validate_jev_request(request, self.request_schema)
        for args in ({'nome': None}, {'nome': 'D02', 'destinatario': 'outro'}, {}):
            request = self.request()
            request['action']['args'] = args
            with self.assertRaises(ValueError):
                validate_jev_request(request, self.request_schema)
        request = self.request()
        request['trusted_context']['state_version'] = True
        with self.assertRaises(ValueError):
            validate_jev_request(request, self.request_schema)
        request = self.request()
        request['authorized_documents'] = [{'document_id': 'D02', 'version': 1, 'sha256': 'inválido', 'content': 'teste'}]
        with self.assertRaises(ValueError):
            validate_jev_request(request, self.request_schema)

    def test_data_profiles_match_operational_effects(self):
        data = PilotData(ROOT)
        profiles = read('data/cases/sinais-offline.json')['profiles']
        for case in data.central.values():
            classifier = case['setup']['classifier']
            if 'profile' not in classifier:
                continue
            response = profiles[classifier['profile']]
            internal = case['action']['tool'] == 'ler_documento_data_room'
            self.assertEqual(response['efeito_externo'], 0 if internal else 1)
        with self.assertRaises(ValueError):
            validate_schema(data.trusted_case('T23')['setup']['classifier']['raw_response'], self.response_schema)
        self.assertEqual(data.trusted_case('T24')['setup']['classifier']['mode'], 'timeout')

    def test_advisory_fields_and_approval_status_are_explicit(self):
        rules = self.config['decision_contract']
        self.assertFalse(rules['criticidade_controls_decision'])
        self.assertFalse(rules['confidence_controls_decision'])
        self.assertTrue(rules['risk_does_not_grant_access'])
        self.assertEqual(rules['threshold_comparison'], '>=')
        if self.config['status'] == 'candidato_aguardando_aprovacao_do_pesquisador':
            self.assertFalse(self.config['approved_for_item_3'])

    def test_schema_changes_cannot_silently_disable_validation(self):
        schema = copy.deepcopy(self.response_schema)
        schema['allOf'] = []
        with self.assertRaisesRegex(ValueError, 'não suportada'):
            validate_schema(self.response, schema)


if __name__ == '__main__':
    unittest.main()
