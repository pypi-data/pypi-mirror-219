"""Tally Token

This module provides a simple way to split a secret into multiple tokens.
The secret can be recovered only if all the tokens are merged together.
"""
from __future__ import annotations

import secrets


def split_text(
    clear_text: str, into: int = 2, *, encoding: str = "utf-8"
) -> list[bytes]:
    """Split a text into multiple tokens.

    Args:
        clear_text: The text to be split.
        into: The number of tokens to be generated.
        encoding: The encoding of the text.
    """
    clear_text_bytes = bytes(clear_text, encoding=encoding)
    return split_bytes_into(clear_text_bytes, into)


def _split1(source: bytes) -> tuple[bytes, bytes]:
    token = _generate_random_token(len(source))
    cipher_text = bytearray()
    for i in range(len(source)):
        cipher_text.append(source[i] ^ token[i])
    return bytes(token), bytes(cipher_text)


def split_bytes_into(source: bytes, n: int) -> list[bytes]:
    """Split a bytes into multiple token bytes.

    Args:
        source: The bytes to be split.
        n: The number of tokens to be generated.
    """
    tokens = []
    token = source
    for _ in range(n - 1):
        generated, token = _split1(token)
        tokens.append(generated)
    tokens.append(token)
    return tokens


def _merge1(token1: bytes, token2: bytes) -> bytes:
    clear_text = bytearray()
    for i in range(len(token1)):
        clear_text.append(token1[i] ^ token2[i])
    return bytes(clear_text)


def merge_bytes_into(tokens: list[bytes]) -> bytes:
    """Merge tokens into a secret bytes.

    Args:
        tokens: The tokens to be merged.
    """
    token = tokens[0]
    for i in range(1, len(tokens)):
        token = _merge1(token, tokens[i])
    return token


def merge_text(tokens: list[bytes], *, encoding: str = "utf-8") -> str:
    """Merge tokens into a text.

    Args:
        tokens: The tokens to be merged.
        encoding: The encoding of the text.
    """
    clear_text_bytes = merge_bytes_into(tokens)
    return clear_text_bytes.decode(encoding)


def _generate_random_token(size: int) -> bytes:
    return secrets.token_bytes(size)
