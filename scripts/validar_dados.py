#!/usr/bin/env python3
"""Confere integridade e separação de dados; não executa o experimento."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from guardiao_gate import PilotData

if __name__ == '__main__':
    print(json.dumps(PilotData(ROOT).validate(), ensure_ascii=False, indent=2))
