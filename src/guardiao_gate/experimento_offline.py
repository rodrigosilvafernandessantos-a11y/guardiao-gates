"""Executor limitado aos três fluxos iniciais aprovados para o item 3."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .dados import PilotData
from .offline import OfflineCore

INITIAL_CASES = ('T01', 'T07', 'T12')


def run_initial_case(data, case_id, *, run_id):
    if case_id not in INITIAL_CASES:
        raise ValueError('Executor do item 3 aceita somente T01, T07 e T12; suíte completa pertence ao item 4')
    case = data.trusted_case(case_id)
    setup = case['setup']
    # Evitar que futuras alterações da preparação sejam silenciosamente ignoradas.
    if (setup['events'] or setup['history'] or setup['requests'] != 1 or
        setup['tool_response'] != {'mode': 'valid_receipt'} or setup['clock']['now_offset_seconds'] != 0 or
        setup['stop'] or not setup['audit_available'] or setup['operator_id'] != 'OP-01'):
        raise ValueError('Condição do caso fora do escopo do executor inicial')
    expected_profile = data._json('config/jev-1.0.json')['tool_metadata'][case['action']['tool']]['offline_profile']
    if setup['classifier'] != {'profile': expected_profile, 'contract_version': 'JEV-1.0'}:
        raise ValueError('Classificador do caso fora do escopo inicial')
    core = OfflineCore(data, run_id=run_id, case_id=case_id, scenario_id=case['scenario_id'],
                       mandate=setup['mandate'],
                       purpose='obter documento faltante' if case['action']['tool'] == 'enviar_email_ao_vendedor' else 'análise interna')
    initial = core.submit(case['action'])
    final = copy.deepcopy(initial)
    for approval in setup['approval_events']:
        if approval['source'] != 'trusted_test_harness' or approval['at_offset_seconds'] != 0:
            raise ValueError('Aprovação fora do escopo inicial')
        core.record_approval(initial['action_id'], approver_id=approval['approver_id'], decision=approval['decision'])
        final = core.resume(initial['action_id'])
    # Avaliar somente depois do resultado observado. O controlador não consulta o oráculo.
    oracle = data.evaluator_oracle(case_id)
    outcome = {'decision_initial': final['decision_initial'], 'result_status': final['result_status']}
    matched = (outcome in oracle['outcomes_unordered'] and final['dispatch_invocations'] == oracle['expected_invocations'])
    observed = {'case_id': case_id, 'scenario_id': case['scenario_id'],
                'decision_initial': initial['decision_initial'], 'result_status': final['result_status'],
                'initial_dispatch_invocations': initial['dispatch_invocations'],
                'dispatch_invocations': final['dispatch_invocations'], 'confirmed_effects': final['confirmed_effects'],
                'expected_invocations': oracle['expected_invocations'], 'observed_match': matched,
                'action_hash': final['action_hash'], 'approval_ids': final['approval_ids']}
    return {'observed': observed, 'initial': initial, 'final': final, **core.evidence()}


def _write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def _write_jsonl(path, values):
    path.write_text(''.join(json.dumps(v, ensure_ascii=False, allow_nan=False) + '\n' for v in values), encoding='utf-8')


def export_initial_run(root, *, output_parent=None):
    root = Path(root).resolve()
    data = PilotData(root)
    integrity = data.validate()
    run_id = 'offline-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:8]
    output = Path(output_parent) / run_id if output_parent is not None else root / 'results' / run_id
    output.mkdir(parents=True, exist_ok=False)
    (output / '.incomplete').write_text('Rodada incompleta até a finalização do manifesto.\n', encoding='utf-8')
    cases = [run_initial_case(data, case_id, run_id=run_id) for case_id in INITIAL_CASES]
    observed = [c['observed'] for c in cases]
    _write_jsonl(output / 'casos-observados.jsonl', observed)
    _write_jsonl(output / 'eventos.jsonl', [e for c in cases for e in c['events']])
    _write_jsonl(output / 'invocacoes.jsonl', [i for c in cases for i in c['invocations']])
    _write_jsonl(output / 'efeitos.jsonl', [e for c in cases for e in c['effects']])
    _write_json(output / 'recibos.json', {c['observed']['case_id']: c['final']['receipt'] for c in cases})
    with (output / 'casos-observados.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(observed[0]))
        writer.writeheader()
        writer.writerows(observed)
    summary = {'run_id': run_id, 'mode': 'offline', 'scope': 'item_3_initial_flows',
               'cases_executed': len(cases), 'cases_matching_oracle': sum(c['observed_match'] for c in observed),
               'all_initial_flows_match': all(c['observed_match'] for c in observed),
               'proposals': sum(c['counters']['proposals'] for c in cases),
               'intercepted_attempts': sum(c['counters']['intercepted_attempts'] for c in cases),
               'dispatch_invocations': sum(c['counters']['dispatch_invocations'] for c in cases),
               'confirmed_reads': sum(c['counters']['confirmed_reads'] for c in cases),
               'confirmed_simulated_external_effects': sum(c['counters']['confirmed_effects'] for c in cases),
               'real_model_calls': 0, 'real_external_actions': 0, 'full_56_case_suite_executed': False,
               'human_domain_review': 'pendente'}
    _write_json(output / 'metricas.json', summary)
    sources = sorted(set([p.relative_to(root).as_posix() for p in (root / 'src/guardiao_gate').glob('*.py')] +
                         ['scripts/executar_nucleo_offline.py', 'data/cases/manifesto.json', 'config/jev-1.0.json']))
    try:
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True))
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    manifest = {'run_id': run_id, 'status': 'running', 'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'python_version': platform.python_version(), 'code_revision': revision, 'working_tree_dirty': dirty,
                'case_ids': list(INITIAL_CASES), 'policy_version': 'MA-SIM-1.0', 'contract_version': 'JEV-1.0',
                'clock': 'virtual; época sintética 2026-11-18T00:00:00Z', 'integrity': integrity,
                'code_and_configuration': [{'path': p, 'sha256': hashlib.sha256((root / p).read_bytes()).hexdigest()} for p in sources],
                'data_artifacts': copy.deepcopy(data.manifest['artifacts'])}
    _write_json(output / 'manifesto.json', manifest)
    lines = ['# Rodada inicial do núcleo offline', '', f'Rodada: `{run_id}`.', '',
             'Somente T01/T07/T12, com sinais fixos e efeitos simulados. Nenhuma chamada a modelo ou ação real.', '',
             '| Caso | Decisão inicial | Estado final | Invocações | Referência coincide |',
             '|---|---|---|---:|---|']
    lines += [f"| {c['case_id']} | {c['decision_initial']} | {c['result_status']} | {c['dispatch_invocations']} | {'sim' if c['observed_match'] else 'não'} |" for c in observed]
    lines += ['', 'T12 teve zero invocações antes da aprovação simulada e uma depois. A aprovação veio do executor confiável, não de documento.', '',
              'Uma leitura confirmada e um efeito externo simulado confirmado são contados separadamente. O mock de preços não foi invocado em T07.', '',
              'Esta rodada verifica os três fluxos iniciais. Não avalia os 56 casos, utilidade de respostas de um modelo, eficácia geral ou validação jurídica.', '']
    (output / 'relatorio.md').write_text('\n'.join(lines), encoding='utf-8')
    manifest['output_artifacts'] = [{'path': p.name, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                                    for p in sorted(output.iterdir()) if p.name not in ('manifesto.json', '.incomplete')]
    manifest['status'] = 'completed'
    _write_json(output / 'manifesto.json', manifest)
    (output / '.incomplete').unlink()
    return output, summary
