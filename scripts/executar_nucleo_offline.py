#!/usr/bin/env python3
"""Executa e exporta apenas T01/T07/T12. Não importa clientes de modelos."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate.experimento_offline import export_initial_run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-parent', type=Path, help='Pasta para novas rodadas; padrão: results/')
    args = parser.parse_args()
    output, summary = export_initial_run(ROOT, output_parent=args.output_parent)
    print(json.dumps({'output': str(output), **summary}, ensure_ascii=False, indent=2))
    if not summary['all_initial_flows_match']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
