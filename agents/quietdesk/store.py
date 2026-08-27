from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Shift

DATA_DIR = Path(os.getenv("QUIETDESK_DATA_DIR", ".data"))


def _path(shift_id: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR / f"{shift_id}.json"


def save(shift: Shift) -> Shift:
    _path(shift.id).write_text(shift.model_dump_json(indent=2), encoding="utf-8")
    return shift


def load(shift_id: str) -> Shift:
    return Shift.model_validate_json(_path(shift_id).read_text(encoding="utf-8"))


def list_shifts() -> list[Shift]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    items: list[Shift] = []
    for p in sorted(DATA_DIR.glob("*.json"), reverse=True):
        try:
            items.append(Shift.model_validate_json(p.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError, ValueError):
            continue
    return items
