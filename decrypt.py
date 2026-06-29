#!/usr/bin/env python3
"""
CoinGlass API Response Decryption — Pure Python, no browser, no API key.

Reverse-engineered from CoinGlass webpack module 12471 (CryptoJS AES-ECB).

Algorithm:
  Layer 1: AES-128-ECB(user_token, Key0)   → Gzip(actual_key)
  Layer 2: Gunzip                          → 16-char hex actual key
  Layer 3: AES-128-ECB(encrypted_body, key) → Gzip(JSON)
  Layer 4: Gunzip                          → plain JSON

Key derivation (v=1, universal since 2025):
  Key0 = base64(url_path)[:16]

Old v=55/66/77 constants (deprecated, no longer in use):
  v=55 → base64("170b070da9654622")[:16]
  v=66 → base64("d6537d845a964081")[:16]
  v=77 → base64("863f08689c97435b")[:16]

Usage:
  from decrypt import fetch_and_decrypt
  data = fetch_and_decrypt("https://capi.coinglass.com/api/spot/rsi/list")
"""

import json
import gzip
import base64
import time
from typing import Any, Dict
from urllib.parse import urlparse

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# Historical key constants (found in webpack module 12471).
# Modern CoinGlass (2025+) uses v=1 universally — these are kept for
# backward compatibility with old archive data.
_KEY_TABLE = {
    "55": "170b070da9654622",
    "66": "d6537d845a964081",
    "77": "863f08689c97435b",
}


def _derive_key0(v: str, url: str = "") -> str:
    """Derive the first-layer decryption key from the `v` response header.

    All current CoinGlass endpoints (100% as of 2025+) return v=1:
      Key0 = base64(url_path)[:16]

    Legacy v=55/66/77 (no longer in use):
      Key0 = base64(constant_from_table)[:16]
    """
    if v == "1":
        constant = urlparse(url).path or url.split("?")[0]
    else:
        constant = _KEY_TABLE.get(v)
        if constant is None:
            raise ValueError(f"Unknown v={v}, known: {list(_KEY_TABLE)} + [1]")
    return base64.b64encode(constant.encode()).decode()[:16]


def decrypt(
    encrypted_body: str, user_token_b64: str, v: str, url: str = ""
) -> Dict[str, Any]:
    """
    Decrypt a CoinGlass encrypted API response.

    Args:
        encrypted_body: Raw HTTP response body (JSON with "data" field).
        user_token_b64: Value of the 'user' response header.
        v: Value of the 'v' response header.
        url: API URL (needed when v="1").

    Returns:
        Decrypted JSON as Python dict.
    """
    outer = json.loads(encrypted_body)
    payload = base64.b64decode(outer["data"])
    token = base64.b64decode(user_token_b64)

    key0 = _derive_key0(v, url)

    # Layer 1-2: decrypt user token → gunzip → actual key
    step1 = unpad(AES.new(key0.encode(), AES.MODE_ECB).decrypt(token), 16)
    actual_key = gzip.decompress(step1).decode()

    # Layer 3-4: decrypt payload → gunzip → JSON
    step2 = unpad(AES.new(actual_key.encode(), AES.MODE_ECB).decrypt(payload), 16)
    plain = gzip.decompress(step2).decode()

    return json.loads(plain)


def fetch_and_decrypt(url: str, params: dict = None, timeout: int = 30) -> Dict[str, Any]:
    """Fetch an encrypted CoinGlass API endpoint and return the decrypted data.

    Args:
        url: Full API URL (e.g. https://capi.coinglass.com/api/spot/rsi/list)
        params: Optional query parameters as a dict.
        timeout: Request timeout in seconds (default 30).

    Returns:
        Decrypted JSON as a Python dict or list.

    Raises:
        ValueError: If the response is missing the required encryption headers.
        requests.HTTPError: On non-200 HTTP status.
    """
    import requests

    resp = requests.get(
        url,
        params=params or {},
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-ts-v2": str(int(time.time() * 1000)),
            "encryption": "true",
            "language": "en",
            "Origin": "https://www.coinglass.com",
            "Referer": "https://www.coinglass.com",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Linux"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/125.0.0.0 Safari/537.36",
        },
        timeout=timeout,
    )
    resp.raise_for_status()

    user = resp.headers.get("user")
    v = resp.headers.get("v")
    if not user or not v:
        # Plain (non-encrypted) endpoint — return JSON directly
        return resp.json()

    return decrypt(resp.text, user, v, url)
