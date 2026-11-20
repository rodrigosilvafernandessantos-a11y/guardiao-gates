"""Preparação e análise do notebook; regras de decisão ficam no controlador."""
from __future__ import annotations

import copy
import hashlib
import html
import importlib.metadata
import json
import platform
import re
import sys
from collections import Counter
from pathlib import Path

from .dados import PilotData, decode_json
from .suite_offline import export_full_run


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_notebook_config(root):
    return decode_json((Path(root)/'config/notebook-offline-1.0.json').read_text(encoding='utf-8'))


def pinned_requirements(path):
    requirements = {}
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        package, sep, marker = line.partition(';')
        if sep:
            if marker.strip() != 'platform_system == "Darwin"':
                raise ValueError(f'Marcador não suportado: {marker}')
            if platform.system() != 'Darwin':
                continue
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)==([A-Za-z0-9_.+!-]+)', package.strip())
        if not match:
            raise ValueError(f'Dependência sem versão exata: {package}')
        name, version = match.groups()
        if name in requirements:
            raise ValueError(f'Dependência repetida: {name}')
        requirements[name] = version
    return requirements


def prepare_notebook(root, parameters):
    root = Path(root).resolve()
    params = copy.deepcopy(parameters)
    baseline = load_notebook_config(root)
    if set(params) != set(baseline):
        raise ValueError('Configuração do notebook tem campos ausentes ou extras')
    if params['mode'] != 'offline' or params['model_enabled'] is not False:
        raise ValueError('Somente o modo offline está implementado. Integração real pertence ao item 6.')
    if params['config_version'] != 'NB-OFFLINE-1.0' or type(params['strict_dependency_versions']) is not bool:
        raise ValueError('Versão ou verificação de dependências inválida')
    # Parâmetros científicos não são alterados por controles de apresentação.
    for key in set(params) - {'mode', 'model_enabled', 'output_parent', 'strict_dependency_versions'}:
        if params[key] != baseline[key]:
            raise ValueError(f'Parâmetro não editável no notebook: {key}')
    if tuple(sys.version_info[:2]) < tuple(params['python_minimum']):
        raise RuntimeError('Notebook requer Python 3.11+; referência validada: Python 3.12.8.')
    output_relative = Path(params['output_parent'])
    output = (root/output_relative).resolve()
    if output_relative.is_absolute() or not output.is_relative_to(root/'results'):
        raise ValueError('Saídas devem ficar em results/ ou em uma de suas subpastas')
    for relative in (params['requirements_file'], params['notebook_file'], 'data/cases/manifesto.json'):
        if not (root/relative).is_file():
            raise FileNotFoundError(f'Arquivo necessário ausente: {relative}')
    rows, mismatches = [], []
    for name, expected in pinned_requirements(root/params['requirements_file']).items():
        try:
            observed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            observed = None
        matches = observed == expected
        rows.append({'pacote': name, 'versao_referencia': expected, 'versao_observada': observed, 'coincide': matches})
        if not matches:
            mismatches.append(name)
    if mismatches and params['strict_dependency_versions']:
        raise RuntimeError('Ambiente difere das versões fixadas: '+', '.join(mismatches)+'. Instale requirements-notebook.txt no ambiente do kernel.')
    data = PilotData(root)
    inventory = data.validate()
    expected = params['expected_cases']
    if len(data.central) != expected['central'] or len(data.paired) != expected['paired'] or len(data.central)+len(data.paired) != expected['total']:
        raise ValueError('Inventário diverge do conjunto de 56 casos definido')
    return {'parameters': params, 'python_version': platform.python_version(), 'python_executable': sys.executable,
            'platform': platform.platform(), 'dependencies': rows, 'dependency_mismatches': mismatches,
            'source_notebook_sha256': sha256(root/params['notebook_file']),
            'requirements_sha256': sha256(root/params['requirements_file']),
            'config_sha256': sha256(root/'config/notebook-offline-1.0.json'), 'inventory': inventory}


def run_from_notebook(root, preparation):
    root = Path(root).resolve()
    # Repetir a preparação detecta edição de entradas/configuração desde a inspeção.
    verified = prepare_notebook(root, preparation['parameters'])
    for key in ('source_notebook_sha256','requirements_sha256','config_sha256'):
        if verified[key] != preparation[key]:
            raise ValueError('Arquivo mudou desde a preparação: '+key)
    context = {'entrypoint': 'notebook', 'config_version': 'NB-OFFLINE-1.0', **verified}
    return export_full_run(root, output_parent=root/preparation['parameters']['output_parent'], execution_context=context)


def verify_run(run_dir):
    run_dir = Path(run_dir).resolve()
    manifest = decode_json((run_dir/'manifesto.json').read_text(encoding='utf-8'))
    if manifest['status'] != 'completed' or (run_dir/'.incomplete').exists():
        raise ValueError('Rodada incompleta; não apresentar como avaliação concluída')
    names = set()
    for artifact in manifest['output_artifacts']:
        target = (run_dir/artifact['path']).resolve()
        if not target.is_relative_to(run_dir) or artifact['path'] in names:
            raise ValueError('Artefato fora da rodada ou repetido no manifesto')
        names.add(artifact['path'])
        if sha256(target) != artifact['sha256']:
            raise ValueError('Artefato da rodada alterado: '+artifact['path'])
    return manifest


def _jsonl(path):
    return [decode_json(line) for line in Path(path).read_text(encoding='utf-8').splitlines() if line.strip()]


def analyze_run(run_dir):
    run_dir = Path(run_dir).resolve()
    manifest = verify_run(run_dir)
    metrics = decode_json((run_dir/'metricas.json').read_text(encoding='utf-8'))
    observations = _jsonl(run_dir/'casos-observados.jsonl')
    complete = _jsonl(run_dir/'casos-completos.jsonl')
    divergent = decode_json((run_dir/'divergencias.json').read_text(encoding='utf-8'))
    if len(observations) != metrics['case_count'] or len(complete) != len(observations):
        raise ValueError('Registros e contagem da rodada divergem')
    groups = [{'grupo': 'Centrais', 'coincidentes': metrics['central_matching'], 'total': metrics['central_count']},
              {'grupo': 'Pareados', 'coincidentes': metrics['paired_matching'], 'total': metrics['paired_count']}]
    statuses = [{'estado_final_por_caso': status, 'casos': count}
                for status,count in sorted(Counter(o['result_status'] for o in observations).items())]
    controls = [{'indicador': label, 'observado': metrics[key]} for label,key in [
        ('Chamadas acima da referência','invocations_above_reference'),('Duplicatas','duplicate_invocations'),
        ('Sondagens executadas','probe_invocations'),('Invocações sem aprovação válida','supervised_without_valid_approval'),
        ('Erros do executor','execution_errors')]]
    critical_ids = {'T15','T16','T17','T18','T19','T23','T24','T29','T30','T31','T32','T33','T34','T36'}
    critical = []
    for case in complete:
        if case['case_id'] not in critical_ids:
            continue
        outcomes = case.get('outcomes',[])
        critical.append({'caso':case['case_id'], 'estados':[o['result_status'] for o in outcomes],
                         'invocacoes_atuais':case.get('dispatch_invocations'), 'historico':case.get('history_invocations'),
                         'efeitos_confirmados_por_tentativa':[o['confirmed_effects'] for o in outcomes],
                         'reconciliacao':any(o['requires_reconciliation'] for o in outcomes)})
    pairs = []
    for variant in ('B','M'):
        selected = [c for c in complete if c['kind']=='paired' and c['case_id'].endswith('-'+variant)]
        pairs.append({'variante':'Normal (B)' if variant=='B' else 'Maliciosa (M)', 'casos':len(selected),
                      'coincidentes':sum(c['evaluation']['observed_match'] for c in selected),
                      'rubrica_fixa_atendida':sum(c['evaluation'].get('utility',{}).get('passed',False) for c in selected),
                      'sondagens_injetadas':sum(len(c.get('probes',[])) for c in selected)})
    return {'run_id':manifest['run_id'], 'metrics':metrics, 'groups':groups,'statuses':statuses,'controls':controls,
            'central':[o for o in observations if o['kind']=='central'],
            'paired':[o for o in observations if o['kind']=='paired'], 'paired_groups':pairs,
            'critical':critical, 'divergences':divergent,
            'limits':['Sinais fixos e dados sintéticos conhecidos de desenvolvimento.',
                      'Extração e rubrica fixa não medem utilidade de modelo.',
                      'Sondagens do avaliador não são tentativas espontâneas de ataque.',
                      'T31/T32 mantêm efeito desconhecido; T30 mantém falha de auditoria.',
                      'B0/B1 e integração com JEV real não foram executados.',
                      'Revisão humana de domínio permanece pendente.']}


def html_table(rows, columns=None):
    if not rows:
        return '<p>Nenhum registro.</p>'
    columns = columns or list(rows[0])
    def cell(value):
        if value is None:
            text = '—'
        elif isinstance(value,bool):
            text = 'sim' if value else 'não'
        elif isinstance(value,(dict,list)):
            text = json.dumps(value,ensure_ascii=False)
        else:
            text = str(value)
        return html.escape(text)
    head=''.join('<th>'+cell(c)+'</th>' for c in columns)
    body=''.join('<tr>'+''.join('<td>'+cell(row.get(c))+'</td>' for c in columns)+'</tr>' for row in rows)
    return ('<div style="overflow-x:auto"><table style="border-collapse:collapse; text-align:left">'
            '<thead><tr>'+head+'</tr></thead><tbody>'+body+'</tbody></table></div>')


def _outcome_key(outcome):
    return json.dumps({key:outcome.get(key) for key in ('decision_initial','result_status','dispatch_invocations',
                                                      'confirmed_effects','error_category','requires_reconciliation')},
                      sort_keys=True,ensure_ascii=False)


def compare_runs(first, second):
    first,second=Path(first).resolve(),Path(second).resolve()
    manifests=[verify_run(path) for path in (first,second)]
    inputs=[{item['path']:item['sha256'] for item in manifest['data_artifacts']} for manifest in manifests]
    def normalized(path):
        results={}
        for case in _jsonl(path/'casos-completos.jsonl'):
            row={key:copy.deepcopy(case.get(key)) for key in ('case_id','kind','scenario_id','dispatch_invocations',
                                                            'history_invocations','response','execution_error','evaluation')}
            row['outcomes']=sorted(_outcome_key(o) for o in case.get('outcomes',[]))
            row['reading']=_outcome_key(case['reading']) if 'reading' in case else None
            row['probes']=[(p['alias'],_outcome_key(p['outcome'])) for p in case.get('probes',[])]
            results[case['case_id']]=row
        return results
    outputs=[normalized(path) for path in (first,second)]
    changed=sorted(cid for cid in set(outputs[0])|set(outputs[1]) if outputs[0].get(cid)!=outputs[1].get(cid))
    metrics=[decode_json((path/'metricas.json').read_text(encoding='utf-8')) for path in (first,second)]
    for metric in metrics:
        metric.pop('run_id',None)
    codes=[{item['path']:item['sha256'] for item in manifest['code_and_configuration']} for manifest in manifests]
    contexts=[manifest.get('execution_context') or {} for manifest in manifests]
    environments=[{'python':manifest['python_version'],
                   'platform':context.get('platform'),
                   'dependencies':{d['pacote']:d['versao_observada'] for d in context.get('dependencies',[])}}
                  for manifest,context in zip(manifests,contexts)]
    same_parameters=contexts[0].get('parameters')==contexts[1].get('parameters')
    return {'first_run':manifests[0]['run_id'],'second_run':manifests[1]['run_id'],
            'same_inputs':inputs[0]==inputs[1],'same_code':codes[0]==codes[1],
            'same_environment':environments[0]==environments[1],'same_parameters':same_parameters,
            'same_case_outcomes':not changed,'changed_cases':changed,
            'same_metrics':metrics[0]==metrics[1],
            'reproduced':inputs[0]==inputs[1] and codes[0]==codes[1] and environments[0]==environments[1] and same_parameters and not changed and metrics[0]==metrics[1],
            'ignored_expected_variation':['identificadores','timestamps','hashes vinculados à rodada','ordem do vencedor e IDs de threads em T33']}


def persist_analysis(run_dir, analysis):
    run_dir=Path(run_dir).resolve()
    parent=verify_run(run_dir)
    if analysis != analyze_run(run_dir):
        raise ValueError('Análise diverge dos arquivos preservados da rodada')
    destination=run_dir/'analise-notebook'
    destination.mkdir(exist_ok=False)
    metrics=analysis['metrics']
    status='atendidos' if metrics['technical_readiness'] else 'não atendidos'
    lines=['# Análise do notebook — Guardião Gate','',f"Rodada: `{analysis['run_id']}`.",'',
           f"Critérios locais: **{status}**. Coincidência: **{metrics['cases_matching_oracle']}/{metrics['case_count']}**.",'',
           f"Centrais: {metrics['central_matching']}/{metrics['central_count']}; pareados: {metrics['paired_matching']}/{metrics['paired_count']}.",'',
           f"Chamadas acima da referência: {metrics['invocations_above_reference']}; duplicatas: {metrics['duplicate_invocations']}; sem aprovação válida: {metrics['supervised_without_valid_approval']}.",'',
           f"Efeitos desconhecidos: {', '.join(metrics['unknown_effect_cases']) or 'nenhum'}. Falha de auditoria: {', '.join(metrics['audit_unavailable_cases']) or 'nenhuma'}.",'',
           '## Limites','',*['- '+text for text in analysis['limits']],'',
           'Os casos com falhas previstas só coincidem quando produzem os estados e contagens corretos. Nada nesta análise transforma desconhecido em zero.', '',
           'Arquivos completos: [relatório](../relatorio.md), [casos](../casos-observados.csv), [divergências](../divergencias.json), [manifesto](../manifesto.json).','']
    (destination/'analise.md').write_text('\n'.join(lines),encoding='utf-8')
    (destination/'analise.json').write_text(json.dumps(analysis,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    record={'status':'completed','run_id':analysis['run_id'],'parent_manifest_sha256':sha256(run_dir/'manifesto.json'),
            'parent_run_status':parent['status'],
            'outputs':[{'path':p.name,'sha256':sha256(p)} for p in sorted(destination.iterdir())]}
    (destination/'manifesto-analise.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return destination
