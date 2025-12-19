# Developer: Sreeraj
# GitHub: https://github.com/s-r-e-e-r-a-j

from __future__ import annotations
import os, base64
from typing import Dict
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class Crypto:
    def __init__(self, passphrase: str, salt_file: str | None = None, iterations: int = 200_000) -> None:
        self.iterations = iterations
        self.salt_file = salt_file or "pylitedb.salt"
        if os.path.exists(self.salt_file):
            with open(self.salt_file, "r", encoding="utf-8") as f:
                self.salt = base64.b64decode(f.read().strip())
        else:
            self.salt = os.urandom(16)
            with open(self.salt_file, "w", encoding="utf-8") as f:
                f.write(base64.b64encode(self.salt).decode())
        kdf = PBKDF2HMAC(algorithm=hashes.SHA3_256(), length=32, salt=self.salt, iterations=self.iterations)
        self.key = kdf.derive(passphrase.encode())

    def encrypt(self, plaintext: bytes) -> Dict[str, str]:
        aes = AESGCM(self.key)
        nonce = os.urandom(12)
        ct = aes.encrypt(nonce, plaintext, None)
        return {"nonce": base64.b64encode(nonce).decode(), "ct": base64.b64encode(ct).decode()}

    def decrypt(self, entry: Dict[str, str]) -> bytes:
        aes = AESGCM(self.key)
        nonce = base64.b64decode(entry["nonce"].encode())
        ct = base64.b64decode(entry["ct"].encode())
        return aes.decrypt(nonce, ct, None)

    def meta(self) -> str:
        return base64.b64encode(self.salt).decode()
