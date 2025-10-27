# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import json, uuid, os
from typing import Any, Dict, List, Optional
from .storage import StorageEngine
from .btree import BTree
from .wal import WAL
from .crypto import Crypto

class Database:
    def __init__(self, path: str, passphrase: str | None = None) -> None:
        self.path = path
        self.passphrase = passphrase or ""
        salt_file = f"{os.path.splitext(path)[0]}.salt"
        self.crypto = Crypto(self.passphrase, salt_file=salt_file) if passphrase else None
        self.store = StorageEngine(path, self.crypto)
        self.wal = WAL(path + ".wal")
        self.tables: Dict[str, BTree] = {}
        self._load_tables()
        self._replay_wal()

    def _load_tables(self) -> None:
        if not self.store.meta_path.exists():
            self.store.meta_path.write_text(json.dumps({"tables": {}}), encoding="utf-8")
        cfg = json.loads(self.store.meta_path.read_text(encoding="utf-8"))
        for name, info in cfg.get("tables", {}).items():
            b = BTree()
            for rid, page in info.get("rows", {}).items():
                b.insert(rid, page)
            self.tables[name] = b

    def _replay_wal(self) -> None:
        for rec in self.wal.read_all():
            self._apply(rec)
        self.wal.clear()

    def create_table(self, name: str) -> None:
        self.store.write_table_meta(name, {"rows": {}})
        self.tables[name] = BTree()

    def insert(self, table: str, row: Dict[str, Any]) -> str:
        rid = uuid.uuid4().hex
        page_no = self.store.write_row(row)
        rec = {"op": "insert", "table": table, "id": rid, "page": page_no}
        self.wal.append(rec)
        self._apply(rec)
        return rid

    def get(self, table: str, rid: str) -> Optional[Dict[str, Any]]:
        t = self.tables.get(table)
        if not t:
            return None
        page = t.get(rid)
        if page is None:
            return None
        return self.store.read_row(page)

    def delete(self, table: str, rid: str) -> bool:
        rec = {"op": "delete", "table": table, "id": rid}
        self.wal.append(rec)
        return self._apply(rec)

    def update(self, table: str, rid: str, new_data: Dict[str, Any]) -> bool:
        t = self.tables.get(table)
        if not t:
            return False
        page = t.get(rid)
        if page is None:
            return False
        current_row = self.store.read_row(page)
        current_row.update(new_data)
        self.store.update_page(page, current_row)
        rec = {"op": "update", "table": table, "id": rid, "page": page}
        self.wal.append(rec)
        return self._apply(rec)

    def find_all(self, table: str) -> List[Dict[str, Any]]:
        t = self.tables.get(table)
        if not t:
            return []
        out: List[Dict[str, Any]] = []
        for rid in t.all_keys():
            out.append(self.get(table, rid))
        return out

    def find_by_filter(self, table: str, key: str, value: Any) -> List[Dict[str, Any]]:
        t = self.tables.get(table)
        if not t:
            return []
        result: List[Dict[str, Any]] = []
        for rid in t.all_keys():
            row = self.get(table, rid)
            if row and key in row and row[key] == value:
                result.append(row)
        return result

    def _apply(self, record: Dict[str, Any]) -> bool:
        op = record.get("op")
        table = record.get("table")
        if op == "insert":
            rid = record["id"]
            page = record["page"]
            self.tables.setdefault(table, BTree()).insert(rid, page)
            info = self.store.read_table_meta(table)
            rows = info.get("rows", {})
            rows[rid] = page
            self.store.write_table_meta(table, {"rows": rows})
            return True
        if op == "delete":
            rid = record["id"]
            t = self.tables.get(table)
            if not t:
                return False
            ok = t.delete(rid)
            if ok:
                info = self.store.read_table_meta(table)
                rows = info.get("rows", {})
                rows.pop(rid, None)
                self.store.write_table_meta(table, {"rows": rows})
            return ok
        if op == "update":
            return True
        return False

    def commit(self) -> None:
        self.wal.clear()
