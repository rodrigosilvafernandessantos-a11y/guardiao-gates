#!/usr/bin/env python3
"""Executa 36 casos centrais e vinte pareados; não importa clientes de modelos."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate.suite_offline import export_full_run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-parent', type=Path)
    args = parser.parse_args()
    output, summary = export_full_run(ROOT, output_parent=args.output_parent)
    print(json.dumps({'output': str(output), **summary}, ensure_ascii=False, indent=2))
    if not summary['technical_readiness']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
