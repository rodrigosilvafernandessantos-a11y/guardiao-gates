#!/usr/bin/env python3
"""Executa o notebook em kernel Jupyter novo, por IPC local, e salva suas saídas."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import queue
import re
from urllib.parse import quote, unquote
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'notebooks/experimento-guardiao-gate.ipynb'


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _reply(client, ident, timeout):
    deadline=time.monotonic()+timeout
    while True:
        message=client.get_shell_msg(timeout=max(0.1,deadline-time.monotonic()))
        if message['parent_header'].get('msg_id')==ident:
            return message['content']
        if time.monotonic()>deadline:
            raise TimeoutError('Sem resposta do kernel')


def _execute_cell(client, cell, timeout):
    source=cell['source'] if isinstance(cell['source'],str) else ''.join(cell['source'])
    ident=client.execute(source,allow_stdin=False,stop_on_error=True,store_history=True)
    deadline=time.monotonic()+timeout
    while True:
        remaining=deadline-time.monotonic()
        if remaining<=0:
            raise TimeoutError('Célula excedeu o limite de execução')
        try:
            message=client.get_iopub_msg(timeout=remaining)
        except queue.Empty as exc:
            raise TimeoutError('Célula não concluiu no prazo') from exc
        if message['parent_header'].get('msg_id')!=ident:
            continue
        kind,content=message['msg_type'],message['content']
        if kind=='execute_input':
            cell['execution_count']=content['execution_count']
        elif kind=='stream':
            cell['outputs'].append({'output_type':'stream','name':content['name'],'text':content['text']})
        elif kind in ('display_data','execute_result'):
            output={'output_type':kind,'data':content['data'],'metadata':content.get('metadata',{})}
            if kind=='execute_result':
                output['execution_count']=content['execution_count']
            cell['outputs'].append(output)
        elif kind=='error':
            cell['outputs'].append({'output_type':'error','ename':content['ename'],'evalue':content['evalue'],'traceback':content['traceback']})
        elif kind=='clear_output':
            cell['outputs']=[]
        elif kind=='status' and content['execution_state']=='idle':
            break
    reply=_reply(client,ident,timeout)
    cell['execution_count']=reply.get('execution_count',cell['execution_count'])
    if reply['status']!='ok':
        raise RuntimeError(f"{reply.get('ename')}: {reply.get('evalue')}")


def _locate(client):
    expression=('__import__("json").dumps({"run_dir":str(globals().get("RUN_DIR","")), '
                '"analysis_dir":str(globals().get("ANALYSIS_DIR","")), '
                '"technical_readiness":bool(globals().get("METRICS",{}).get("technical_readiness",False))})')
    ident=client.execute('',silent=True,store_history=False,allow_stdin=False,user_expressions={'result':expression})
    result=_reply(client,ident,10)['user_expressions']['result']
    if result['status']!='ok':
        return {}
    return json.loads(ast.literal_eval(result['data']['text/plain']))


def _rebase_snapshot_links(notebook, destination):
    """Mantém navegáveis os links da cópia movida para a pasta da rodada."""
    def rewrite(text):
        def replace(match):
            link=match.group(2)
            if link.startswith(('http:', 'https:', 'mailto:', '#', 'data:')) or Path(link).is_absolute():
                return match.group(0)
            target,sep,fragment=link.partition('#')
            relative=os.path.relpath((SOURCE.parent/unquote(target)).resolve(),destination)
            return match.group(1)+quote(relative,safe='/.-_')+(sep+fragment if sep else '')+match.group(3)
        return re.sub(r'(\]\()([^\s)]+)(\))',replace,text)
    for cell in notebook['cells']:
        if cell['cell_type']=='markdown':
            text=cell['source'] if isinstance(cell['source'],str) else ''.join(cell['source'])
            cell['source']=rewrite(text)
        for output in cell.get('outputs',[]):
            if 'text/markdown' in output.get('data',{}):
                output['data']['text/markdown']=rewrite(output['data']['text/markdown'])
    notebook['metadata']['guardiao_gate']['snapshot_links_rebased_from']='notebooks/'


def execute_notebook(*, kernel_cwd='notebooks', timeout=60):
    if os.name=='nt':
        raise RuntimeError('O executor IPC foi preparado para Unix/macOS. Use um editor Jupyter no Windows.')
    raw=SOURCE.read_bytes()
    notebook=json.loads(raw)
    if notebook.get('nbformat')!=4 or not isinstance(notebook.get('cells'),list):
        raise ValueError('Formato de notebook inválido')
    for position,cell in enumerate(notebook['cells'],1):
        if cell['cell_type']=='code':
            code=cell['source'] if isinstance(cell['source'],str) else ''.join(cell['source'])
            compile(code,f'notebook:cell-{position}','exec')
            cell.update(execution_count=None,outputs=[])
    started=datetime.now(timezone.utc).isoformat()
    failure=None; location={}; executed=0
    cwd=ROOT if kernel_cwd=='root' else ROOT/'notebooks'
    # Diretório curto para os sockets IPC, sem tocar configurações pessoais.
    with tempfile.TemporaryDirectory(prefix='guardiao-nb-',dir='/tmp') as runtime:
        previous={key:os.environ.get(key) for key in ('IPYTHONDIR','JUPYTER_RUNTIME_DIR')}
        os.environ['IPYTHONDIR']=str(Path(runtime)/'ipython')
        os.environ['JUPYTER_RUNTIME_DIR']=runtime
        manager=client=None
        try:
            from jupyter_client import KernelManager
            manager=KernelManager(kernel_name='python3',connection_file=str(Path(runtime)/'kernel.json'),
                                  transport='ipc',ip=str(Path(runtime)/'socket'))
            manager.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}']
            manager.start_kernel(cwd=str(cwd),env=dict(os.environ),stdout=sys.stderr,stderr=sys.stderr)
            client=manager.blocking_client();client.start_channels();client.wait_for_ready(timeout=30)
            for position,cell in enumerate(notebook['cells'],1):
                if cell['cell_type']!='code':
                    continue
                _execute_cell(client,cell,timeout)
                executed+=1
                print(f'Célula {position}/{len(notebook["cells"])} concluída.',flush=True)
            location=_locate(client)
        except Exception as exc:
            failure=f'{type(exc).__name__}: {exc}'
            if client is not None:
                try:
                    location=_locate(client)
                except Exception:
                    pass
        finally:
            if manager is not None and manager.has_kernel:
                manager.shutdown_kernel(now=True)
            if client is not None:
                client.stop_channels()
            for key,value in previous.items():
                if value is None:
                    os.environ.pop(key,None)
                else:
                    os.environ[key]=value
    if failure is None and not location.get('analysis_dir'):
        failure='Notebook terminou sem publicar a análise da rodada'
    if failure:
        parent=Path(location['run_dir']) if location.get('run_dir') else ROOT/'results'
        destination=parent/('notebook-falhou-'+uuid4().hex[:12])
        destination.mkdir(parents=True,exist_ok=False)
    else:
        destination=Path(location['analysis_dir'])
    notebook.setdefault('metadata',{}).setdefault('guardiao_gate',{}).pop('source_outputs',None)
    notebook['metadata']['guardiao_gate']['execution_status']='failed' if failure else ('completed' if location.get('technical_readiness') else 'completed_with_divergences')
    notebook['metadata']['guardiao_gate']['source_notebook_sha256']=hashlib.sha256(raw).hexdigest()
    _rebase_snapshot_links(notebook,destination)
    snapshot=destination/('notebook-parcial.ipynb' if failure else 'notebook.executado.ipynb')
    with snapshot.open('x',encoding='utf-8') as handle:
        json.dump(notebook,handle,ensure_ascii=False,indent=2)
        handle.write('\n')
    result={'status':'failed' if failure else ('completed' if location.get('technical_readiness') else 'completed_with_divergences'),
            'started_at_utc':started,'ended_at_utc':datetime.now(timezone.utc).isoformat(),
            'python_executable':sys.executable,'kernel_transport':'ipc','kernel_cwd':str(cwd),
            'source_notebook_sha256':hashlib.sha256(raw).hexdigest(),
            'executed_notebook':str(snapshot),'executed_notebook_sha256':_hash(snapshot),
            'code_cells_completed':executed,'run_dir':location.get('run_dir'),
            'analysis_dir':location.get('analysis_dir'),'error':failure}
    if location.get('run_dir') and (Path(location['run_dir'])/'manifesto.json').is_file():
        result['run_manifest_sha256']=_hash(Path(location['run_dir'])/'manifesto.json')
    if not failure:
        result['analysis_manifest_sha256']=_hash(destination/'manifesto-analise.json')
    with (destination/'execucao-jupyter.json').open('x',encoding='utf-8') as handle:
        json.dump(result,handle,ensure_ascii=False,indent=2);handle.write('\n')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel-cwd',choices=['root','notebooks'],default='notebooks')
    parser.add_argument('--cell-timeout',type=int,default=60)
    args=parser.parse_args()
    if args.cell_timeout<=0:
        parser.error('--cell-timeout deve ser positivo')
    result=execute_notebook(kernel_cwd=args.kernel_cwd,timeout=args.cell_timeout)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if result['status']!='completed':
        raise SystemExit(1)


if __name__=='__main__':
    main()
