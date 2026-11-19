"""Registro de autorizações do simulador, separado do conteúdo dos documentos."""
from __future__ import annotations

import copy
from threading import RLock
from uuid import uuid4


class ApprovalRegistry:
    """Autoridade local do executor confiável; não autentica pessoas reais.

    O modelo recebe somente nomes de ferramentas de negócio. Não recebe este
    registro nem acesso aos métodos de emissão/revogação.
    """
    def __init__(self):
        self._lock = RLock()
        self._tokens = {}
        self._reservations = set()

    def issue(self, *, run_id, action_id, action_hash, approver_id, decision, now, ttl, approval_id=None):
        with self._lock:
            ident = approval_id or f'{action_id}-APR-{approver_id}-{uuid4().hex[:12]}'
            if ident in self._tokens:
                raise ValueError('Identificador de aprovação já emitido')
            token = {'approval_id': ident, 'run_id': run_id, 'action_id': action_id,
                     'action_hash': action_hash, 'approver_id': approver_id, 'decision': decision,
                     'issued_at_seconds': now, 'expires_at_seconds': now + ttl,
                     'max_invocations': 1, 'used': False, 'revoked': False,
                     'source': 'trusted_test_harness'}
            self._tokens[ident] = token
            return copy.deepcopy(token)

    def lookup(self, approval_id):
        with self._lock:
            return copy.deepcopy(self._tokens.get(approval_id))

    def revoke_run(self, run_id):
        with self._lock:
            for token in self._tokens.values():
                if token['run_id'] == run_id and not token['used']:
                    token['revoked'] = True

    def revoke_action(self, run_id, action_id):
        with self._lock:
            for token in self._tokens.values():
                if (token['run_id'], token['action_id']) == (run_id, action_id) and not token['used']:
                    token['revoked'] = True

    def reserve(self, *, run_id, action_id, action_hash, approval_ids, required_roles, now):
        """Reserva idempotência e consome todas as alçadas em uma seção atômica."""
        with self._lock:
            key = (run_id, action_id)
            if key in self._reservations:
                return 'DUPLICATA'
            tokens = [self._tokens.get(ident) for ident in approval_ids]
            if any(token is None for token in tokens):
                return 'BLOQUEADO_ERRO_APROVACAO'
            if {t['approver_id'] for t in tokens} != set(required_roles):
                return 'BLOQUEADO_ALCADA'
            for token in tokens:
                if token['used']:
                    return 'BLOQUEADO_REUTILIZACAO'
                if token['run_id'] != run_id or token['action_id'] != action_id or token['action_hash'] != action_hash:
                    return 'BLOQUEADO_VINCULO'
                if token['revoked']:
                    return 'APROVACAO_REVOGADA'
                if not token['issued_at_seconds'] <= now < token['expires_at_seconds']:
                    return 'EXPIRADO'
                if token['decision'] != 'aprovar' or token['max_invocations'] != 1:
                    return 'NEGADO'
            self._reservations.add(key)
            for token in tokens:
                token['used'] = True
            return None
