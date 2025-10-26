# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import os
from pathlib import Path

PAGE_SIZE: int = 4096

class Pager:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(self.path), os.O_RDWR | os.O_CREAT)

    def read_page(self, page_no: int) -> bytes:
        os.lseek(self.fd, page_no * PAGE_SIZE, os.SEEK_SET)
        return os.read(self.fd, PAGE_SIZE)

    def write_page(self, page_no: int, data: bytes) -> None:
        if len(data) > PAGE_SIZE:
            raise ValueError("page too large")
        os.lseek(self.fd, page_no * PAGE_SIZE, os.SEEK_SET)
        os.write(self.fd, data.ljust(PAGE_SIZE, b"\x00"))

    def file_size_pages(self) -> int:
        size = os.fstat(self.fd).st_size
        return (size + PAGE_SIZE - 1) // PAGE_SIZE

    def allocate_page(self) -> int:
        n = self.file_size_pages()
        self.write_page(n, b"")
        return n
