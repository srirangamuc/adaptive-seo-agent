from __future__ import annotations

from pathlib import Path


class LanceDBService:
    def __init__(self, db_path: Path):
        self.db_path = db_path

    def connect(self) -> None:
        self.db_path.mkdir(parents=True, exist_ok=True)
