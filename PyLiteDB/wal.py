# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List

class WAL:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: Dict) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, separators=(",", ":")) + "\n")

    def read_all(self) -> List[Dict]:
        if not self.path.exists():
            return []
        out: List[Dict] = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                out.append(json.loads(line))
        return out

    def clear(self) -> None:
        try:
            self.path.unlink()
        except Exception:
            pass
