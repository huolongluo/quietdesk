import os
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def tmp_data(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("QUIETDESK_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("QUIETDESK_ENGINE", "fixture")
    os.environ["QUIETDESK_DATA_DIR"] = str(tmp_path)
    from quietdesk import store

    store.DATA_DIR = tmp_path
