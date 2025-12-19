# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
from bisect import bisect_left
from typing import Any, List

class BTree:
    def __init__(self) -> None:
        self.keys: List[Any] = []
        self.values: List[Any] = []

    def insert(self, key: Any, value: Any) -> None:
        i = bisect_left(self.keys, key)
        if i < len(self.keys) and self.keys[i] == key:
            self.values[i] = value
        else:
            self.keys.insert(i, key)
            self.values.insert(i, value)

    def get(self, key: Any) -> Any | None:
        i = bisect_left(self.keys, key)
        if i < len(self.keys) and self.keys[i] == key:
            return self.values[i]
        return None

    def delete(self, key: Any) -> bool:
        i = bisect_left(self.keys, key)
        if i < len(self.keys) and self.keys[i] == key:
            del self.keys[i]
            del self.values[i]
            return True
        return False

    def all_keys(self) -> List[Any]:
        return list(self.keys)
