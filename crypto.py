"""Шифрование юзернеймов: AES-128-CBC, формат <iv_hex>:<ct_hex>.

Шифруем при входе в бота и заново — только когда юзернейм реально сменился.
Расшифровать может лишь владелец SECRET_KEY, то есть овнер.
"""

from __future__ import annotations

import hashlib
import os
from typing import Optional

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import config

_KEY = hashlib.sha256(config.SECRET_KEY.encode()).digest()[:16]


def encrypt(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    data = padder.update(value.encode()) + padder.finalize()
    enc = Cipher(algorithms.AES(_KEY), modes.CBC(iv)).encryptor()
    return f"{iv.hex()}:{(enc.update(data) + enc.finalize()).hex()}"


def decrypt(blob: Optional[str]) -> Optional[str]:
    if not blob or ":" not in blob:
        return None
    try:
        iv_hex, ct_hex = blob.split(":", 1)
        dec = Cipher(algorithms.AES(_KEY), modes.CBC(bytes.fromhex(iv_hex))).decryptor()
        raw = dec.update(bytes.fromhex(ct_hex)) + dec.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        return (unpadder.update(raw) + unpadder.finalize()).decode()
    except Exception:  # noqa: BLE001
        return None


def fingerprint(value: Optional[str]) -> Optional[str]:
    """Хеш юзернейма — по нему ищем упоминания, не расшифровывая базу."""
    if not value:
        return None
    return hashlib.sha256(value.strip().lower().lstrip("@").encode()).hexdigest()