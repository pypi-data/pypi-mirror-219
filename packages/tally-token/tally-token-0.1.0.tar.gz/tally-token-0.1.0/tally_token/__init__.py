from __future__ import annotations

import secrets


def _generate_random_token(size: int) -> bytes:
    # TODO: seed
    return secrets.token_bytes(size)


def split_text(clear_text: str) -> tuple[bytes, bytes]:
    clear_text_bytes = bytes(clear_text, "utf-8")
    return split1(clear_text_bytes)


def split1(source: bytes) -> tuple[bytes, bytes]:
    token = _generate_random_token(len(source))
    cipher_text = bytearray()
    for i in range(len(source)):
        cipher_text.append(source[i] ^ token[i])
    return bytes(token), bytes(cipher_text)


def merge1(token1: bytes, token2: bytes) -> bytes:
    clear_text = bytearray()
    for i in range(len(token1)):
        clear_text.append(token1[i] ^ token2[i])
    return bytes(clear_text)


def merge_text(token: bytes, cipher_text: bytes) -> str:
    return merge1(token, cipher_text).decode("utf-8")
