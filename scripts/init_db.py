from __future__ import annotations

from pathlib import Path

from config.settings import Settings
from core.services.lancedb_service import LanceDBService


def main() -> None:
    settings = Settings()
    service = LanceDBService(Path(settings.lancedb_path))
    service.connect()
    print("LanceDB initialized at", settings.lancedb_path)


if __name__ == "__main__":
    main()
