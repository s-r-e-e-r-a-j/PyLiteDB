# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
from .pager import Pager
from .crypto import Crypto

class StorageEngine:
    def __init__(self, file_path: str, crypto: Crypto | None = None) -> None:
        self.file_path = Path(file_path)
        self.pager = Pager(str(self.file_path))
        self.crypto = crypto
        self.meta_path = self.file_path.with_suffix(".meta.json")
        if not self.meta_path.exists():
            self.meta_path.write_text(json.dumps({"tables": {}}))

    def read_table_meta(self, name: str) -> Dict:
        m = json.loads(self.meta_path.read_text(encoding="utf-8"))
        return m["tables"].get(name, {})

    def write_table_meta(self, name: str, meta: Dict) -> None:
        m = json.loads(self.meta_path.read_text(encoding="utf-8"))
        m["tables"][name] = meta
        self.meta_path.write_text(json.dumps(m, indent=2))

    def read_row(self, page_no: int) -> Dict:
        raw = self.pager.read_page(page_no)
        raw = raw.rstrip(b"\x00")
        if not raw:
            return {}
        if self.crypto:
            entry = json.loads(raw.decode("utf-8"))
            pt = self.crypto.decrypt(entry)
            return json.loads(pt.decode("utf-8"))
        return json.loads(raw.decode("utf-8"))

    def write_row(self, obj: Dict) -> int:
        data = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if self.crypto:
            entry = self.crypto.encrypt(data)
            payload = json.dumps(entry, separators=(",", ":")).encode("utf-8")
        else:
            payload = data
        page_no = self.pager.allocate_page()
        self.pager.write_page(page_no, payload)
        return page_no

    def update_page(self, page_no: int, obj: Dict) -> None:
        data = json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        if self.crypto:
            entry = self.crypto.encrypt(data)
            payload = json.dumps(entry, separators=(",", ":")).encode("utf-8")
        else:
            payload = data
        self.pager.write_page(page_no, payload)
