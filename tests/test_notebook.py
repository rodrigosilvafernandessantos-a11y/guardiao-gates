"""Preparação, integridade e análise do notebook; kernels reais são validados pelo executor CLI."""
import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from guardiao_gate.notebook import (analyze_run,compare_runs,html_table,load_notebook_config,
                                    persist_analysis,pinned_requirements,prepare_notebook,run_from_notebook,verify_run)
from guardiao_gate.suite_offline import export_full_run


class NotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.first,_=export_full_run(ROOT,output_parent=cls.temp.name)
        cls.second,_=export_full_run(ROOT,output_parent=cls.temp.name)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_source_is_clean_and_all_cells_compile(self):
        notebook=json.loads((ROOT/'notebooks/experimento-guardiao-gate.ipynb').read_text())
        self.assertEqual((notebook['nbformat'],notebook['nbformat_minor']),(4,5))
        self.assertEqual(len({c['id'] for c in notebook['cells']}),len(notebook['cells']))
        codes=[c for c in notebook['cells'] if c['cell_type']=='code']
        self.assertEqual(len(codes),12)
        for cell in codes:
            compile(cell['source'],cell['id'],'exec')
            self.assertIsNone(cell['execution_count'])
            self.assertEqual(cell['outputs'],[])

    def test_offline_only_preflight_rejects_mode_and_unsafe_output(self):
        for key,value in [('mode','model'),('model_enabled',True),('output_parent','../fora'),('output_parent','/tmp')]:
            params=load_notebook_config(ROOT);params[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):
                prepare_notebook(ROOT,params)

    def test_versions_are_checked_before_execution(self):
        params=load_notebook_config(ROOT)
        expected=pinned_requirements(ROOT/'requirements-notebook.txt')
        with patch('guardiao_gate.notebook.importlib.metadata.version',side_effect=lambda name:expected[name]):
            prepared=prepare_notebook(ROOT,params)
            self.assertFalse(prepared['dependency_mismatches'])
        with patch('guardiao_gate.notebook.importlib.metadata.version',return_value='0.0.0'):
            with self.assertRaisesRegex(RuntimeError,'versões fixadas'):
                prepare_notebook(ROOT,params)

    def test_changed_source_rejected_before_creating_round(self):
        params=load_notebook_config(ROOT)
        expected=pinned_requirements(ROOT/'requirements-notebook.txt')
        with patch('guardiao_gate.notebook.importlib.metadata.version',side_effect=lambda name:expected[name]):
            prepared=prepare_notebook(ROOT,params)
            prepared['source_notebook_sha256']='0'*64
            with patch('guardiao_gate.notebook.export_full_run') as execute:
                with self.assertRaisesRegex(ValueError,'mudou'):
                    run_from_notebook(ROOT,prepared)
                execute.assert_not_called()

    def test_repeat_rounds_preserve_both_and_match_semantically(self):
        result=compare_runs(self.first,self.second)
        self.assertNotEqual(result['first_run'],result['second_run'])
        self.assertTrue(result['same_inputs'])
        self.assertTrue(result['same_code'])
        self.assertTrue(result['same_metrics'])
        self.assertTrue(result['reproduced'])
        self.assertTrue((self.first/'manifesto.json').exists())
        self.assertTrue((self.second/'manifesto.json').exists())

    def test_analysis_preserves_unknown_effects_and_counts(self):
        analysis=analyze_run(self.first)
        self.assertEqual(sum(g['total'] for g in analysis['groups']),56)
        for case in analysis['critical']:
            if case['caso'] in ('T31','T32'):
                self.assertEqual(case['efeitos_confirmados_por_tentativa'],[None])
                self.assertTrue(case['reconciliacao'])
        self.assertEqual([p['casos'] for p in analysis['paired_groups']],[10,10])

    def test_analysis_saved_separately_and_not_overwritten(self):
        analysis=analyze_run(self.second)
        parent_bytes=(self.second/'manifesto.json').read_bytes()
        target=persist_analysis(self.second,analysis)
        self.assertTrue((target/'analise.md').exists())
        self.assertEqual((self.second/'manifesto.json').read_bytes(),parent_bytes)
        with self.assertRaises(FileExistsError):
            persist_analysis(self.second,analysis)
        tampered=copy.deepcopy(analysis);tampered['metrics']['case_count']=1
        with self.assertRaisesRegex(ValueError,'diverge'):
            persist_analysis(self.first,tampered)

    def test_tampered_outputs_cannot_be_presented_as_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'rodada';shutil.copytree(self.first,folder)
            (folder/'metricas.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'alterado'):
                verify_run(folder)

    def test_html_is_escaped_and_absence_is_not_zero(self):
        output=html_table([{'a':'<script>alert(1)</script>','b':None,'c':True}])
        self.assertNotIn('<script>',output)
        self.assertIn('&lt;script&gt;',output)
        self.assertIn('—',output)
        self.assertIn('sim',output)

    def test_divergences_are_preserved_and_analysis_still_completes(self):
        import guardiao_gate.suite_offline as suite
        actual=suite.evaluate_central
        def divergent(data,result):
            evaluated=actual(data,result)
            if result['case_id']=='T01':
                evaluated['checks']['injected_regression']=False
                evaluated['observed_match']=False
            return evaluated
        with tempfile.TemporaryDirectory() as tmp,patch.object(suite,'evaluate_central',side_effect=divergent):
            folder,summary=export_full_run(ROOT,output_parent=tmp)
            self.assertFalse(summary['technical_readiness'])
            analysis=analyze_run(folder)
            self.assertEqual(len(analysis['divergences']),1)
            saved=persist_analysis(folder,analysis)
            self.assertIn('não atendidos',(saved/'analise.md').read_text())


if __name__=='__main__':
    unittest.main()
