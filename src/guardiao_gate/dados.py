"""Leitura explícita de entradas, configurações confiáveis e oráculos separados.

Este módulo não autentica aprovadores nem implementa a política MA-SIM-1.0.
As listas de acesso devem vir do futuro controlador, nunca do modelo.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

from .contratos import validate_schema


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Chave JSON duplicada: {key}')
        result[key] = value
    return result


def decode_json(text):
    def invalid_constant(value):
        raise ValueError(f'Constante JSON inválida: {value}')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=invalid_constant)


def index_unique(records, key):
    result = {}
    for record in records:
        ident = record[key]
        if ident in result:
            raise ValueError(f'ID duplicado: {ident}')
        result[ident] = record
    return result


class PilotData:
    """Interface de dados para um notebook, sem carregar respostas no contexto."""

    def __init__(self, root):
        self.root = Path(root).resolve()
        self.manifest = decode_json((self.root / 'data/cases/manifesto.json').read_text(encoding='utf-8'))
        self.hashes = index_unique(self.manifest['artifacts'], 'path')
        self.fixtures = index_unique(self._json('data/fixtures/manifesto.json')['fixtures'], 'document_id')
        self.central = index_unique(self._jsonl('data/cases/casos-centrais.jsonl'), 'case_id')
        self.paired = index_unique(self._jsonl('data/cases/casos-pareados.jsonl'), 'case_id')

    def _verified_bytes(self, relative):
        if relative not in self.hashes:
            raise ValueError(f'Artefato fora do manifesto: {relative}')
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('Caminho fora do projeto')
        data = path.read_bytes()
        if sha256(data) != self.hashes[relative]['sha256']:
            raise ValueError(f'Hash divergente: {relative}')
        return data

    def _json(self, relative):
        return decode_json(self._verified_bytes(relative).decode('utf-8'))

    def _jsonl(self, relative):
        return [decode_json(line) for line in self._verified_bytes(relative).decode('utf-8').splitlines() if line.strip()]

    def trusted_case(self, case_id):
        """Somente para o executor: condições e falhas, sem oráculo."""
        cases = self.central if case_id in self.central else self.paired
        return copy.deepcopy(cases[case_id])

    def agent_request(self, case_id):
        """Somente tarefa e canal. Documento será fornecido pela ferramenta LER."""
        case = self.paired[case_id]
        return {'task': case['task'], 'response_channel': case['response_channel']}

    def read_document(self, document_id, *, authorized_document_ids, restricted_access=False):
        """Leitura de fixture para o futuro mock, com escopo fornecido pelo controlador.

        restricted_access é uma decisão confiável do chamador, não uma aprovação
        autenticada. O controlador futuro deve verificar as alçadas antes de usá-lo.
        Não expor este método diretamente como ferramenta do modelo.
        """
        if not isinstance(document_id, str) or not re.fullmatch(r'(?:D0[1-7]|P(?:0[1-9]|10)-[BM])', document_id):
            raise ValueError('Identificador de documento inválido')
        if not isinstance(authorized_document_ids, (list, tuple, set, frozenset)) or not all(isinstance(value, str) for value in authorized_document_ids):
            raise ValueError('Escopo deve ser uma coleção explícita de IDs')
        if type(restricted_access) is not bool:
            raise ValueError('Autorização restrita deve ser booleana')
        if document_id not in authorized_document_ids:
            raise PermissionError('Documento fora do escopo de leitura')
        fixture = self.fixtures[document_id]
        if fixture['access'] == 'restricted' and not restricted_access:
            raise PermissionError('Documento restrito exige autorização verificada pelo controlador')
        data = self._verified_bytes(fixture['path'])
        if sha256(data) != fixture['sha256']:
            raise ValueError('Hash da fixture diverge do catálogo')
        return data.decode('utf-8')

    def evaluator_oracle(self, case_id):
        """Somente para o avaliador; nunca incluir no pedido do agente."""
        name = 'centrais' if case_id in self.central else 'pareados'
        oracles = index_unique(self._jsonl(f'data/cases/oraculos/{name}.jsonl'), 'case_id')
        return copy.deepcopy(oracles[case_id])

    def validate(self):
        """Valida o pacote de dados; não executa os 56 casos do experimento."""
        for relative in self.hashes:
            data = self._verified_bytes(relative)
            if relative.endswith('.json'):
                decode_json(data.decode('utf-8'))
            elif relative.endswith('.jsonl'):
                self._jsonl(relative)
        for source in self.manifest['sources']:
            if sha256((self.root / source['path']).read_bytes()) != source['sha256']:
                raise ValueError(f"Fonte alterada desde a exportação: {source['path']}")
        doc_ids = {f'D{i:02}' for i in range(1, 8)}
        pair_ids = {f'P{i:02}-{v}' for i in range(1, 11) for v in ('B', 'M')}
        if set(self.fixtures) != doc_ids | pair_ids:
            raise ValueError('Inventário de documentos incompleto')
        if set(self.central) != {f'T{i:02}' for i in range(1, 37)} or set(self.paired) != pair_ids:
            raise ValueError('Inventário de casos incompleto')
        states = index_unique(self._json('data/cases/estados.json')['states'], 'scenario_id')
        actors = index_unique(self._json('data/cases/atores.json')['actors'], 'actor_id')
        rules = index_unique(self._json('data/cases/politica.json')['rules'], 'rule_id')
        if set(states) != {f'S{i:02}' for i in range(1, 11)}:
            raise ValueError('Inventário de estados incompleto')
        if len(actors) != 8 or set(rules) != {f'P{i:02}' for i in range(1, 15)}:
            raise ValueError('Inventário de atores ou regras incompleto')
        for name, cases in [('centrais', self.central), ('pareados', self.paired)]:
            oracle_ids = index_unique(self._jsonl(f'data/cases/oraculos/{name}.jsonl'), 'case_id')
            if set(oracle_ids) != set(cases):
                raise ValueError('Oráculos não correspondem aos casos')
            for case in cases.values():
                if case['scenario_id'] not in states:
                    raise ValueError('Cenário inexistente')
                if any(key in case for key in ('expected', 'reference_answer', 'reason', 'outcomes_unordered')):
                    raise ValueError('Oráculo misturado à entrada')
        for doc_id, fixture in self.fixtures.items():
            text = self.read_document(doc_id, authorized_document_ids=[doc_id], restricted_access=doc_id == 'D07')
            if '\r' in text or text.endswith('\n') or '**Resposta de referência:**' in text or '**Tarefa e resposta de referência:**' in text:
                raise ValueError(f'Texto ou normalização indevidos: {doc_id}')
            if doc_id in pair_ids:
                case = self.paired[doc_id]
                if case['allowed_document_ids'] != [doc_id] or case['mandate'] != {'tool': 'ler_documento_data_room', 'args': {'nome': doc_id}}:
                    raise ValueError('Escopo de par inválido')
                base = self.read_document(fixture['base_document_id'], authorized_document_ids=[fixture['base_document_id']])
                if fixture['variant'] == 'B' and text != base:
                    raise ValueError('Variante normal diverge da base')
                if fixture['variant'] == 'M' and not text.startswith(base + '\n\n'):
                    raise ValueError('Variante maliciosa diverge da construção especificada')
        if states['S10']['release'] is not None or states['S10']['conditions'] is not None or states['S10']['valid_for_execution']:
            raise ValueError('S10 deve preservar desconhecidos e invalidade')
        if not states['S08']['exceptional'] or not states['S08']['closed'] or states['S08']['release']:
            raise ValueError('S08 perdeu a inconsistência deliberada')
        signals = self._json('data/cases/sinais-offline.json')
        config = self._json('config/jev-1.0.json')
        schema = self._json(signals['response_schema'])
        if signals['contract_version'] != config['contract_version'] or signals['profiles'] != config['offline_profiles']:
            raise ValueError('Perfis JEV divergem da configuração canônica')
        if signals['approved_for_item_3'] != config['approved_for_item_3'] or signals['contract_status'] != config['status']:
            raise ValueError('Estado de aprovação JEV diverge da configuração')
        if not signals['executable'] or set(signals['profiles']) != {'leitura', 'email', 'preco', 'migracao'}:
            raise ValueError('Perfis JEV completos ausentes')
        for profile in signals['profiles'].values():
            validate_schema(profile, schema)
        for case in self.central.values():
            classifier = case['setup']['classifier']
            if 'profile' in classifier:
                tool_profile = config['tool_metadata'][case['action']['tool']]['offline_profile']
                if classifier['profile'] != tool_profile or classifier['contract_version'] != config['contract_version']:
                    raise ValueError('Perfil JEV incompatível com ferramenta ou versão')
        for case in self.paired.values():
            if case['classifier_profile'] != 'leitura':
                raise ValueError('A leitura inicial dos pares deve usar perfil de leitura')
        return {'base_documents': 7, 'paired_documents': 20, 'states': len(states),
                'central_cases': len(self.central), 'paired_cases': len(self.paired),
                'data_integrity': 'validada', 'agent_tests_executed': False,
                'signals_contract': signals['contract_version'],
                'item_3_status': 'aprovado' if signals['approved_for_item_3'] else 'aguardando_aprovacao_do_pesquisador'}
