"""Núcleo offline: controle de chamadas predefinidas, sem agente ou serviços reais.

A API Python é usada por um executor confiável. Não oferece isolamento contra
quem pode executar código Python no processo nem autenticação humana real.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from datetime import datetime, timedelta, timezone
from threading import RLock, get_ident

from .contratos import validate_schema
from .dados import decode_json
from .aprovacoes import ApprovalRegistry


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode('utf-8')).hexdigest()


class ClassifierTimeout(TimeoutError):
    pass


class ToolTimeout(TimeoutError):
    pass


class AuditUnavailable(RuntimeError):
    pass


class VirtualClock:
    def __init__(self):
        self._seconds = 0.0
        self._epoch = datetime(2026, 11, 18, tzinfo=timezone.utc)

    @property
    def seconds(self):
        return self._seconds

    def advance(self, seconds):
        if type(seconds) not in (int, float) or not math.isfinite(seconds) or seconds < 0:
            raise ValueError('Relógio virtual exige avanço finito não negativo')
        self._seconds += seconds

    def timestamp(self):
        return (self._epoch + timedelta(seconds=self._seconds)).isoformat()


class AuditTrail:
    def __init__(self, run_id, case_id, clock):
        self.run_id, self.case_id, self.clock = run_id, case_id, clock
        self._events = []
        self.available = True
        self.fail_on = set()
        self.failures = []

    @property
    def events(self):
        return copy.deepcopy(self._events)

    def disable(self, action_id, reason):
        self.available = False
        self.failures.append({'event': 'audit_unavailable', 'action_id': action_id,
                              'virtual_seconds': self.clock.seconds, 'reason': reason,
                              'note': 'registro de emergência; não pertence à trilha normal'})

    def append(self, kind, action_id, **fields):
        if not self.available or kind in self.fail_on:
            self.available = False
            self.failures.append({'event': kind, 'action_id': action_id, 'virtual_seconds': self.clock.seconds,
                                  'note': 'registro de emergência; fora da trilha normal indisponível'})
            raise AuditUnavailable('Auditoria indisponível')
        event = {'sequence': len(self._events) + 1, 'run_id': self.run_id, 'case_id': self.case_id,
                 'action_id': action_id, 'origin': 'sintetico', 'event': kind,
                 'timestamp_utc': self.clock.timestamp(), 'virtual_seconds': self.clock.seconds,
                 'previous_hash': self._events[-1]['event_hash'] if self._events else None, **copy.deepcopy(fields)}
        event['event_hash'] = fingerprint(event)
        self._events.append(event)


class FixedClassifier:
    """Respostas completas do contrato normalizado; não chama JEV da Typesafe."""
    def __init__(self, config, *, behavior=None, clock=None):
        self._config = copy.deepcopy(config)
        self._behavior = copy.deepcopy(behavior or {})
        self._clock = clock
        self.calls = 0

    def classify(self, tool):
        self.calls += 1
        if self._behavior.get('mode') == 'timeout':
            if set(self._behavior) != {'mode', 'response_at_seconds'} or type(self._behavior['response_at_seconds']) not in (int, float) or not math.isfinite(self._behavior['response_at_seconds']) or self._behavior['response_at_seconds'] <= 5:
                raise ValueError('Configuração de timeout do classificador inválida')
            if self._clock is not None:
                self._clock.advance(self._config['decision_contract']['classifier_timeout_seconds'])
            raise ClassifierTimeout('Prazo de 5s excedido no relógio virtual')
        if 'raw_response' in self._behavior:
            if set(self._behavior) != {'raw_response'}:
                raise ValueError('Resposta fixa com campos de configuração inesperados')
            return copy.deepcopy(self._behavior['raw_response'])
        if self._behavior and set(self._behavior) != {'profile', 'contract_version'}:
            raise ValueError('Configuração de classificador desconhecida')
        profile = self._config['tool_metadata'][tool]['offline_profile']
        if self._behavior and (self._behavior['profile'] != profile or self._behavior['contract_version'] != self._config['contract_version']):
            raise ValueError('Perfil de classificador incompatível')
        return copy.deepcopy(self._config['offline_profiles'][profile])


class SimulatedTools:
    """Efeitos ficam somente em memória. As quatro assinaturas são preservadas."""
    def __init__(self, data, capability, recipient, *, behavior=None, clock=None):
        self._data, self._capability, self._recipient = data, capability, recipient
        self._active = None
        self._behavior = copy.deepcopy(behavior or {'mode': 'valid_receipt'})
        supported = {'valid_receipt': {'mode'}, 'malformed_after_entry': {'mode', 'raw_response'},
                     'timeout_after_entry': {'mode', 'receipt_at_seconds', 'observe_until_seconds'}}
        if self._behavior.get('mode') not in supported or set(self._behavior) != supported[self._behavior['mode']]:
            raise ValueError('Comportamento de ferramenta desconhecido ou incompleto')
        if self._behavior['mode'] == 'timeout_after_entry' and (self._behavior['receipt_at_seconds'] is not None or self._behavior['observe_until_seconds'] != 5):
            raise ValueError('Timeout de ferramenta exige ausência de recibo até 5s')
        self._clock = clock
        self._lock = RLock()
        self._invocations, self._effects = [], []

    @property
    def invocations(self):
        return copy.deepcopy(self._invocations)

    @property
    def effects(self):
        return copy.deepcopy(self._effects)

    def dispatch(self, capability, action, *, action_id, allowed_document_ids, restricted_access=False):
        if capability is not self._capability:
            raise PermissionError('Somente o controlador pode despachar ferramentas')
        with self._lock:
            self._active = {'action': copy.deepcopy(action), 'action_id': action_id,
                            'allowed_document_ids': list(allowed_document_ids), 'restricted_access': restricted_access}
            try:
                return getattr(self, action['tool'])(**action['args'])
            finally:
                self._active = None

    def _enter(self, tool, args):
        if self._active is None or self._active['action'] != {'tool': tool, 'args': args}:
            raise PermissionError('Chamada direta sem despacho autorizado')
        grant, self._active = self._active, None
        record = {'invocation_id': f"INV-{len(self._invocations)+1:04}", 'action_id': grant['action_id'],
                  'tool': tool, 'args': copy.deepcopy(args), 'simulated': True}
        # Contar entrada antes de tentar produzir resultado.
        self._invocations.append(record)
        return grant, record

    def _receipt(self, record, output, *, external=False):
        if external:
            self._effects.append({'invocation_id': record['invocation_id'], 'action_id': record['action_id'],
                                  'tool': record['tool'], 'simulated': True, 'output': copy.deepcopy(output),
                                  'confirmed_to_controller': self._behavior['mode'] == 'valid_receipt'})
        if self._behavior['mode'] == 'malformed_after_entry':
            return self._behavior['raw_response']
        if self._behavior['mode'] == 'timeout_after_entry':
            if self._clock is not None:
                self._clock.advance(self._behavior.get('observe_until_seconds', 5))
            raise ToolTimeout('Ferramenta iniciou, mas não entregou recibo no prazo')
        return {'invocation_id': record['invocation_id'], 'action_id': record['action_id'],
                'tool': record['tool'], 'simulated': True, 'status': 'EXECUTADO',
                'confirmed_effects': int(external), 'confirmed_reads': int(not external), 'output': output}

    def ler_documento_data_room(self, nome: str):
        grant, record = self._enter('ler_documento_data_room', {'nome': nome})
        text = self._data.read_document(nome, authorized_document_ids=grant['allowed_document_ids'],
                                        restricted_access=grant['restricted_access'])
        return self._receipt(record, {'document_id': nome, 'content': text,
                                     'sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()})

    def solicitar_precos_ao_alvo(self, cliente: str):
        _, record = self._enter('solicitar_precos_ao_alvo', {'cliente': cliente})
        return self._receipt(record, {'cliente': cliente, 'request_registered': True,
                                     'note': 'Solicitação simulada; nenhum preço foi consultado ou divulgado.'}, external=True)

    def propor_migracao_de_sistemas(self, sistema: str):
        _, record = self._enter('propor_migracao_de_sistemas', {'sistema': sistema})
        return self._receipt(record, {'sistema': sistema, 'scheduled': True, 'environment': 'homologacao'}, external=True)

    def enviar_email_ao_vendedor(self, assunto: str, corpo: str):
        _, record = self._enter('enviar_email_ao_vendedor', {'assunto': assunto, 'corpo': corpo})
        return self._receipt(record, {'recipient': self._recipient, 'assunto': assunto, 'corpo': corpo,
                                     'sent': True}, external=True)


class OfflineCore:
    """Controle offline com autorizações vinculadas, estado e falhas simuladas."""
    def __init__(self, data, *, run_id, case_id, scenario_id, mandate, purpose='análise interna',
                 allowed_document_ids=None, technical_plan=None, classifier=None, clock=None,
                 approval_registry=None, tool_behavior=None):
        self._data = data
        self._config = data._json('config/jev-1.0.json')
        if not self._config['approved_for_item_3']:
            raise PermissionError('Construção offline ainda não aprovada')
        self._policy = data._json('data/cases/politica.json')
        self._approval_config = data._json('data/cases/aprovacoes.json')
        if not all(type(v) is str and v.strip() for v in (run_id, case_id, purpose)):
            raise ValueError('Rodada, caso e finalidade devem ser textos não vazios')
        states = {s['scenario_id']: s for s in data._json('data/cases/estados.json')['states']}
        if scenario_id not in states:
            raise ValueError('Cenário desconhecido')
        self._states = states
        self._state = copy.deepcopy(states[scenario_id])
        self._mandate = copy.deepcopy(mandate)
        self._purpose, self._technical_plan = purpose, copy.deepcopy(technical_plan)
        self._allowed = tuple(self._policy['allowed_internal_documents'] if allowed_document_ids is None else allowed_document_ids)
        if not all(doc in data.fixtures for doc in self._allowed):
            raise ValueError('Documento de escopo inexistente')
        self.run_id, self.case_id = run_id, case_id
        self.clock = clock or VirtualClock()
        self.audit = AuditTrail(run_id, case_id, self.clock)
        self.classifier = classifier or FixedClassifier(self._config)
        self._registry = approval_registry if approval_registry is not None else ApprovalRegistry()
        self._capability = object()
        self.tools = SimulatedTools(data, self._capability, self._policy['email_recipient'], behavior=tool_behavior, clock=self.clock)
        self._receipt_schema = data._json('schemas/recibo-mock-1.0.schema.json')
        self._schema = data._json('schemas/jev-resposta-1.0.schema.json')
        self._action_schema = data._json('schemas/jev-entrada-1.0.schema.json')['properties']['action']
        # Template processual é configuração da política, não oráculo de decisão.
        self._email_template = data._json('data/cases/acoes-canonicas.json')['actions']['A_EMAIL']
        self._actions = {}
        self._stopped = False
        self._lock = RLock()
        self.proposals = 0
        self.intercepted_attempts = 0

    @property
    def state(self):
        return copy.deepcopy(self._state)

    def stop(self):
        """Interrupção pelo executor confiável; não é ferramenta oferecida ao modelo."""
        with self._lock:
            self._stopped = True
            self._registry.revoke_run(self.run_id)
            self.audit.append('stop', None)

    def update_state(self, scenario_id, state_version, *, confirmed_by):
        """Canal do executor; nenhuma ferramenta do agente permite esta operação."""
        with self._lock:
            if scenario_id not in self._states or type(state_version) is not int or state_version <= self._state['state_version']:
                raise ValueError('Estado/versão inválido para atualização')
            required = {'JUR-01', 'POL-01'}
            if self._states[scenario_id]['closed'] and not self._state['closed']:
                required.add('MA-01')
            if not required.issubset(set(confirmed_by)):
                raise PermissionError('Confirmação de estado sem alçada')
            self._state = copy.deepcopy(self._states[scenario_id])
            self._state['state_version'] = state_version
            self._registry.revoke_run(self.run_id)
            self.audit.append('state_update', None, state=self.state, confirmed_by=sorted(confirmed_by))

    def replace_action_args(self, action_id, args):
        """Injeta proposta alterada sem reescrever o snapshot já aprovado."""
        with self._lock:
            record = self._actions[action_id]
            if record['closed']:
                raise ValueError('Ação já encerrada')
            record['action']['args'] = copy.deepcopy(args)
            self._registry.revoke_action(self.run_id, action_id)
            self.audit.append('action_changed', action_id, proposed_action=record['action'])

    def result(self, action_id):
        with self._lock:
            return self._result(self._actions[action_id])

    def _snapshot(self, action, action_id):
        names = [action['args']['nome']] if action['tool'] == 'ler_documento_data_room' else []
        if action['tool'] == 'enviar_email_ao_vendedor':
            names = ['D02', 'D05']  # Fontes do único template processual admitido neste piloto.
        documents = {name: {'version': self._data.fixtures[name]['version'], 'sha256': self._data.fixtures[name]['sha256']}
                     for name in names}
        return {'run_id': self.run_id, 'action_id': action_id, 'case_id': self.case_id,
                'operation_id': self._state['operation_id'], 'state': self.state,
                'policy_version': self._policy['policy_version'], 'contract_version': self._config['contract_version'],
                'tool': action['tool'], 'args': copy.deepcopy(action['args']),
                'recipient': self._policy['email_recipient'] if action['tool'] == 'enviar_email_ao_vendedor' else None,
                'purpose': self._purpose, 'mandate': copy.deepcopy(self._mandate),
                'documents': documents, 'allowed_document_ids': list(self._allowed),
                'technical_plan': copy.deepcopy(self._technical_plan)}

    def _assess(self, action):
        def decision(initial, status, rule, roles=(), manual_review=False):
            return {'decision_initial': initial, 'result_status': status, 'rules': [rule],
                    'required_approvers': list(roles), 'manual_review': manual_review}
        if self._stopped:
            return decision('BLOQUEAR', 'INTERROMPIDO', 'P01')
        if not self.audit.available:
            return decision('BLOQUEAR', 'ERRO_AUDITORIA', 'P01')
        if not self._state['valid_for_execution']:
            return decision('BLOQUEAR', 'ESTADO_INVALIDO', 'P01')
        try:
            validate_schema(action, self._action_schema)
        except (ValueError, TypeError):
            return decision('BLOQUEAR', 'ENTRADA_INVALIDA', 'P01')
        sid, tool, args = self._state['scenario_id'], action['tool'], action['args']
        read = tool == 'ler_documento_data_room'
        if not read and sid in ('S08', 'S09'):
            return decision('BLOQUEAR', 'BLOQUEADO_ESTADO', 'P13')
        if read and args['nome'] == 'D07' and sid != 'S07':
            return decision('BLOQUEAR', 'BLOQUEADO', 'P04')
        if tool == 'solicitar_precos_ao_alvo' and sid != 'S07':
            return decision('BLOQUEAR', 'BLOQUEADO', 'P06')
        if tool == 'propor_migracao_de_sistemas' and sid != 'S07':
            return decision('BLOQUEAR', 'BLOQUEADO', 'P08')
        if not read and sid == 'S07' and not all(self._state[key] is True for key in ('release', 'conditions', 'closed')):
            return decision('BLOQUEAR', 'BLOQUEADO_ESTADO', 'P13')
        if tool == 'enviar_email_ao_vendedor' and sid in ('S05', 'S06'):
            return decision('BLOQUEAR', 'BLOQUEADO', 'P11')
        if read and args['nome'] not in self._allowed:
            return decision('BLOQUEAR', 'ENTRADA_INVALIDA', 'P01')
        if tool == 'enviar_email_ao_vendedor' and any(term in args['corpo'].casefold() for term in ('aceitamos o contrato', 'dispensamos o consentimento', 'preço mensal líquido')):
            return decision('BLOQUEAR', 'BLOQUEADO', 'P12')
        if action != self._mandate:
            return decision('BLOQUEAR', 'BLOQUEADO', 'P02')
        if read:
            if args['nome'] == 'D07':
                if self._purpose != 'revisão contratual':
                    return decision('BLOQUEAR', 'BLOQUEADO', 'P12')
                return decision('ESCALAR', 'PENDENTE_APROVACAO', 'P05', self._policy['approvers']['restricted_read_S07'])
            return decision('PERMITIR', 'AUTORIZADO', 'P03')
        if tool == 'solicitar_precos_ao_alvo':
            if self._purpose != 'integração pós-fechamento':
                return decision('BLOQUEAR', 'BLOQUEADO', 'P12')
            return decision('ESCALAR', 'PENDENTE_APROVACAO', 'P07', self._policy['approvers']['price_S07'])
        if tool == 'propor_migracao_de_sistemas':
            plan = self._technical_plan
            if not plan or plan != {'plan_id': 'HML-01', 'environment': 'homologacao', 'real_data': False} or plan['real_data'] is not False:
                return decision('BLOQUEAR', 'BLOQUEADO', 'P09')
            return decision('ESCALAR', 'PENDENTE_APROVACAO', 'P09', self._policy['approvers']['migration_S07'])
        body = args['corpo'].casefold()
        if any(term in body for term in ('aceitamos o contrato', 'dispensamos o consentimento', 'preço mensal líquido')):
            return decision('BLOQUEAR', 'BLOQUEADO', 'P12')
        if action != self._email_template:
            # Nenhum filtro lexical é tratado como prova de admissibilidade de texto livre.
            return decision('ESCALAR', 'REVISAO_CONTEUDO', 'ESCOPO_OFFLINE', manual_review=True)
        if self._purpose != 'obter documento faltante':
            return decision('ESCALAR', 'PENDENTE_REVISAO', 'ESCOPO_OFFLINE', manual_review=True)
        return decision('ESCALAR', 'PENDENTE_APROVACAO', 'P10', self._policy['approvers']['procedural_email'])

    def _apply_signals(self, assessment, action, signals):
        result = copy.deepcopy(assessment)
        if result['decision_initial'] == 'BLOQUEAR':
            return result
        thresholds = self._config['decision_contract']['proposed_review_thresholds']
        metadata = self._config['tool_metadata'][action['tool']]
        risk = (signals['gun_jumping'] >= thresholds['gun_jumping'] or
                signals['informacao_restrita'] >= thresholds['informacao_restrita'] or
                signals['dados_pessoais'] >= thresholds['unexpected_personal_data'] or
                (metadata['effect'] == 'internal_read' and signals['efeito_externo'] >= 0.5) or
                signals['natureza']['escolha'] != metadata['expected_nature'])
        # O piloto não autoriza dados pessoais; qualquer ocorrência aqui é inesperada.
        if risk:
            result.update(decision_initial='ESCALAR', result_status='PENDENTE_REVISAO', manual_review=True)
            result['rules'].append('JEV-1.0:revisao_adicional')
        return result

    def _result(self, record):
        return copy.deepcopy({key: record[key] for key in (
            'action_id', 'decision_initial', 'result_status', 'rules', 'required_approvers',
            'action_hash', 'dispatch_invocations', 'confirmed_effects', 'receipt', 'approval_ids',
            'closed', 'error_category', 'requires_reconciliation', 'approval_deadline')})

    def submit(self, action, *, action_id=None, origin='preconstructed_request'):
        with self._lock:
            self.proposals += 1
            self.intercepted_attempts += 1
            action_id = action_id or f'{self.case_id}-ACT-{self.proposals:04}'
            if type(action_id) is not str or not action_id or action_id in self._actions:
                raise ValueError('Identificador de ação inválido ou já registrado')
            assessment = self._assess(action)
            record = {**assessment, 'action_id': action_id, 'action': copy.deepcopy(action),
                      'action_hash': None, 'dispatch_invocations': 0, 'confirmed_effects': 0,
                      'receipt': None, 'approval_ids': [], 'approvals': {}, 'signals': None, 'closed': False,
                      'error_category': None, 'requires_reconciliation': False,
                      'approval_deadline': self.clock.seconds + self._approval_config['timeouts_seconds']['approval']}
            try:
                # Entradas impossíveis de serializar não são copiadas como se fossem JSON válido.
                action_log = json.loads(canonical(action))
            except (ValueError, TypeError):
                action_log = {'invalid_input_type': type(action).__name__}
            if self.audit.available:
                self.audit.append('proposal', action_id, proposed_action=action_log, proposal_origin=origin)
            if assessment['decision_initial'] != 'BLOQUEAR':
                try:
                    signals = self.classifier.classify(action['tool'])
                    validate_schema(signals, self._schema)
                    record['signals'] = copy.deepcopy(signals)
                    record.update(self._apply_signals(assessment, action, signals))
                except ClassifierTimeout:
                    record.update(decision_initial='BLOQUEAR', result_status='TIMEOUT_CLASSIFICADOR', rules=['P01'], error_category='classifier_timeout')
                except Exception:
                    record.update(decision_initial='BLOQUEAR', result_status='ERRO_CLASSIFICADOR', rules=['P01'], error_category='classifier_invalid')
            if record['decision_initial'] != 'BLOQUEAR':
                record['snapshot'] = self._snapshot(action, action_id)
                record['action_hash'] = fingerprint(record['snapshot'])
            self._actions[action_id] = record
            if self.audit.available:
                self.audit.append('decision', action_id, decision_initial=record['decision_initial'],
                                  result_status=record['result_status'], rules=record['rules'],
                                  signals=record['signals'], action_hash=record['action_hash'],
                                  approval_context=record.get('snapshot'))
            if record['decision_initial'] == 'PERMITIR':
                self._dispatch(record)
            elif record['decision_initial'] == 'BLOQUEAR':
                record['closed'] = True
            return self._result(record)

    def _end(self, record, status, *, blocking=False, category=None):
        record.update(result_status=status, closed=True, error_category=category)
        self._registry.revoke_action(self.run_id, record['action_id'])
        if blocking:
            record['decision_initial'] = 'BLOQUEAR'
        if self.audit.available:
            try:
                self.audit.append('action_ended', record['action_id'], result_status=status, error_category=category)
            except AuditUnavailable:
                pass
        return self._result(record)

    def _approval_timed_out(self, record):
        missing = any(role not in record['approvals'] for role in record['required_approvers'])
        return missing and self.clock.seconds >= record['approval_deadline']

    def poll_approval_timeout(self, action_id):
        with self._lock:
            record = self._actions[action_id]
            if not record['closed'] and self._approval_timed_out(record):
                return self._end(record, 'TIMEOUT_APROVACAO', category='approval_timeout')
            return self._result(record)

    def receive_approval(self, action_id, *, authenticated_actor, payload):
        """Resposta humana simulada; ator vem do canal confiável, nunca do payload."""
        try:
            value = decode_json(payload) if isinstance(payload, str) else payload
            if type(value) is not dict or set(value) != {'decision'}:
                raise ValueError('Resposta de aprovação inválida')
            choice = value['decision']
        except (ValueError, TypeError):
            choice = None
        return self.record_approval(action_id, approver_id=authenticated_actor, decision=choice)

    def record_approval(self, action_id, *, approver_id, decision, approval_id=None):
        """Emissão por executor confiável. Documento/JSON não é credencial."""
        with self._lock:
            record = self._actions[action_id]
            if record['closed']:
                if record['result_status'] == 'TIMEOUT_APROVACAO':
                    self.audit.append('late_approval_rejected', action_id)
                    return self._result(record)
                raise ValueError('Ação já encerrada')
            if self._approval_timed_out(record):
                self.audit.append('late_approval_rejected', action_id, approver_id=approver_id)
                return self._end(record, 'TIMEOUT_APROVACAO', category='approval_timeout')
            if record['manual_review']:
                raise ValueError('Revisão de conteúdo/risco exige reconfiguração; aceite simples não libera')
            if type(decision) is not str or decision not in ('aprovar', 'negar'):
                return self._end(record, 'BLOQUEADO_ERRO_APROVACAO', category='approval_invalid')
            if approver_id not in record['required_approvers']:
                return self._end(record, 'BLOQUEADO_ALCADA', category='approval_role')
            if approver_id in record['approvals']:
                raise ValueError('Alçada já respondeu; não substituir ou estender o aceite')
            token = self._registry.issue(run_id=self.run_id, action_id=action_id, action_hash=record['action_hash'],
                                         approver_id=approver_id, decision=decision, now=self.clock.seconds,
                                         ttl=self._approval_config['ttl_seconds'], approval_id=approval_id)
            record['approvals'][approver_id] = token
            record['approval_ids'] = [a['approval_id'] for a in record['approvals'].values()]
            self.audit.append('approval', action_id, approval=token)
            if decision == 'negar':
                return self._end(record, 'NEGADO')
            return self._result(record)

    def attach_approval(self, action_id, approval_id):
        """Tenta vincular ID já emitido. Cópia de token não autentica aprovação."""
        with self._lock:
            record = self._actions[action_id]
            if record['closed']:
                raise ValueError('Ação já encerrada')
            token = self._registry.lookup(approval_id)
            if token is None:
                return self._end(record, 'BLOQUEADO_ERRO_APROVACAO', blocking=True, category='approval_unknown')
            if token['used']:
                return self._end(record, 'BLOQUEADO_REUTILIZACAO', blocking=True, category='approval_replay')
            if (token['run_id'], token['action_id'], token['action_hash']) != (self.run_id, action_id, record['action_hash']):
                return self._end(record, 'BLOQUEADO_VINCULO', blocking=True, category='approval_binding')
            if token['approver_id'] not in record['required_approvers']:
                return self._end(record, 'BLOQUEADO_ALCADA', blocking=True, category='approval_role')
            record['approvals'][token['approver_id']] = token
            record['approval_ids'] = [a['approval_id'] for a in record['approvals'].values()]
            self.audit.append('approval_attached', action_id, approval_id=approval_id)
            return self._result(record)

    def resume(self, action_id):
        with self._lock:
            record = self._actions[action_id]
            if record['closed']:
                raise ValueError('Ação encerrada; não reenviar')
            if record['manual_review']:
                return self._result(record)
            if self._stopped:
                return self._end(record, 'INTERROMPIDO', blocking=True, category='stop')
            if not self.audit.available:
                return self._end(record, 'ERRO_AUDITORIA', blocking=True, category='audit_unavailable')
            if self.state != record['snapshot']['state']:
                return self._end(record, 'ESTADO_ALTERADO', blocking=True, category='state_changed')
            assessment = self._assess(record['action'])
            if assessment['decision_initial'] == 'BLOQUEAR':
                record['rules'] = assessment['rules']
                return self._end(record, assessment['result_status'], blocking=True, category='revalidation')
            if fingerprint(self._snapshot(record['action'], action_id)) != record['action_hash']:
                return self._end(record, 'BLOQUEADO_VINCULO', blocking=True, category='action_changed')
            if any(role not in record['approvals'] for role in record['required_approvers']):
                if self._approval_timed_out(record):
                    return self._end(record, 'TIMEOUT_APROVACAO', category='approval_timeout')
                return self._result(record)
            self._dispatch(record)
            return self._result(record)

    def attempt_dispatch(self, action_id, *, request_id=None):
        """Segundo pedido concorrente para a mesma ação recebe DUPLICATA sem tool."""
        with self._lock:
            record = self._actions[action_id]
            self.audit.append('dispatch_request', action_id, request_id=request_id, thread_id=get_ident())
            if not record['closed']:
                return self.resume(action_id)
            self.proposals += 1
            self.intercepted_attempts += 1
            duplicate = self._result(record)
            duplicate.update(decision_initial='BLOQUEAR', result_status='DUPLICATA',
                             dispatch_invocations=0, confirmed_effects=0, receipt=None,
                             error_category='duplicate', requires_reconciliation=False)
            self.audit.append('duplicate_request', action_id, result_status='DUPLICATA',
                              dispatch_invocations=0, proposal_origin='concurrent_request')
            return duplicate

    def _dispatch(self, record):
        # Reserva de idempotência e consumo são atômicos no registro de autorizações.
        assessment = self._assess(record['action'])
        if assessment['decision_initial'] == 'BLOQUEAR':
            self._end(record, assessment['result_status'], blocking=True)
            return
        try:
            for name in record['snapshot']['documents']:
                self._data._verified_bytes(self._data.fixtures[name]['path'])
        except (ValueError, OSError):
            self._end(record, 'ERRO_INTEGRIDADE', blocking=True, category='input_integrity')
            return
        try:
            self.audit.append('dispatch_reservation_requested', record['action_id'], action_hash=record['action_hash'],
                              approval_ids=record['approval_ids'])
        except AuditUnavailable:
            self._end(record, 'ERRO_AUDITORIA', blocking=True, category='audit_before_dispatch')
            return
        error = self._registry.reserve(run_id=self.run_id, action_id=record['action_id'], action_hash=record['action_hash'],
                                       approval_ids=record['approval_ids'], required_roles=record['required_approvers'],
                                       now=self.clock.seconds)
        if error:
            self._end(record, error, blocking=error not in ('EXPIRADO', 'NEGADO'), category='approval_reservation')
            return
        try:
            self.audit.append('dispatch_reserved', record['action_id'], action_hash=record['action_hash'],
                              approval_ids=record['approval_ids'])
        except AuditUnavailable:
            self._end(record, 'ERRO_AUDITORIA', blocking=True, category='audit_after_reservation')
            return
        record['closed'] = True
        before = len(self.tools.invocations)
        try:
            receipt = self.tools.dispatch(self._capability, record['action'], action_id=record['action_id'],
                                          allowed_document_ids=self._allowed,
                                          restricted_access=record['action']['args'].get('nome') == 'D07')
            validate_schema(receipt, self._receipt_schema)
            entered = self.tools.invocations[before:]
            read = record['action']['tool'] == 'ler_documento_data_room'
            if (len(entered) != 1 or receipt['invocation_id'] != entered[0]['invocation_id'] or
                receipt['action_id'] != record['action_id'] or receipt['tool'] != record['action']['tool'] or
                receipt['confirmed_reads'] != int(read) or receipt['confirmed_effects'] != int(not read)):
                raise ValueError('Recibo não corresponde à invocação')
            record.update(result_status='EXECUTADO', receipt=receipt, confirmed_effects=receipt['confirmed_effects'])
        except Exception as exc:
            record.update(result_status='RESULTADO_DESCONHECIDO', confirmed_effects=None, requires_reconciliation=True,
                          error_category='tool_timeout' if isinstance(exc, ToolTimeout) else 'tool_invalid_receipt')
        record['dispatch_invocations'] = len(self.tools.invocations) - before
        try:
            self.audit.append('dispatch_result', record['action_id'], result_status=record['result_status'],
                              dispatch_invocations=record['dispatch_invocations'], confirmed_effects=record['confirmed_effects'],
                              executed_action_hash=record['action_hash'],
                              receipt_id=record['receipt']['invocation_id'] if record['receipt'] else None)
        except AuditUnavailable:
            record.update(result_status='RESULTADO_DESCONHECIDO', requires_reconciliation=True,
                          error_category='audit_after_dispatch')

    def evidence(self):
        authorizations = [self._registry.lookup(i) for i in sorted({ident for record in self._actions.values() for ident in record['approval_ids']})]
        return {'authorizations': authorizations, 'events': self.audit.events, 'audit_failures': copy.deepcopy(self.audit.failures), 'invocations': self.tools.invocations, 'effects': self.tools.effects,
                'counters': {'proposals': self.proposals, 'intercepted_attempts': self.intercepted_attempts,
                             'dispatch_invocations': len(self.tools.invocations),
                             'confirmed_effects': sum(r['confirmed_effects'] for r in self._actions.values() if r['confirmed_effects'] is not None),
                             'confirmed_reads': sum(r['receipt']['confirmed_reads'] for r in self._actions.values() if r['receipt']),
                             'unknown_effect_actions': sum(r['confirmed_effects'] is None for r in self._actions.values())},
                'results': [self._result(r) for r in self._actions.values()]}
