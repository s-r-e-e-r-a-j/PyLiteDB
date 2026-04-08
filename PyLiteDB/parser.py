# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import json
from typing import Any

class Parser:
    def parse_create(self, q: str) -> tuple[str, None]:
        parts = q.strip().split()
        return parts[2], None

    def parse_insert(self, q: str) -> tuple[str, dict[str, Any]]:
        left, right = q.split("VALUES", 1)
        parts = left.strip().split()
        name = parts[2]
        payload = json.loads(right.strip())
        return name, payload

    def parse_select(self, q: str) -> tuple[str, None]:
        parts = q.strip().split()
        return parts[-1], None

    def parse_update(self, q: str) -> tuple[str, str, dict[str, Any]]:
        parts = q.strip().split(maxsplit=3)
        name = parts[1]
        rid = parts[2]
        payload = json.loads(parts[3])
        return name, rid, payload

    def parse_delete(self, q: str) -> tuple[str, str]:
        parts = q.strip().split()
        name = parts[1]
        rid = parts[2]
        return name, rid

    def parse_filter(self, q: str) -> tuple[str, str, str]:
        parts = q.strip().split()
        name = parts[1]
        key, value = parts[2].split("=", 1)
        return name, key, value
