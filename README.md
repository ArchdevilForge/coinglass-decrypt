# CoinGlass Decrypt

**Pure Python decryption of CoinGlass internal API responses. No API key, no browser required.**

CoinGlass ([coinglass.com](https://www.coinglass.com)) is a cryptocurrency data aggregator that encrypts its public API payloads with AES-128-ECB. This project reverse-engineers the encryption scheme (extracted from the CoinGlass webpack module 12471) and provides a simple Python interface to decrypt any endpoint.

---

## Quick Start

```bash
pip install requests pycryptodome
python example.py
```

Or with uv:

```bash
uv sync
uv run python example.py
```

---

## How It Works

CoinGlass encrypts API responses, but the decryption key is delivered alongside the encrypted data via response headers.

```
Request  ──→  GET /api/spot/rsi/list  (with `encryption: true` header)
                  │
Response  ──→  Headers: { user: <base64 token>, v: "1" }
                  │
                  ▼
            1. Key0 = base64(url_path)[:16]    (v=1 scheme)
            2. AES-128-ECB decrypt(user_token, Key0) → gzip(actual_key)
            3. Gunzip → 16-char hex AES key
            4. AES-128-ECB decrypt(encrypted_body, key) → gzip(JSON)
            5. Gunzip → plain JSON
```

No authentication, cookies, session, or API key is needed. Anyone can decrypt any endpoint.

### Key Derivation (v=1, universal)

All current CoinGlass endpoints use **`v=1`** (confirmed across 136 endpoints). The first-layer key is derived from the URL path:

| `v` | Key0 = `base64(…)[:16]` | Example |
|-----|--------------------------|---------|
| 1   | URL path | `/api/futures/home/statistics` → `L2FwaS9mdXR1cmVz` |

**Legacy** `v=55/66/77` constants (extracted from webpack module 12471, **no longer returned by any endpoint**):

| `v` | Constant | Key0 |
|-----|----------|------|
| 55  | `170b070da9654622` | `MTcwYjA3MGRhOTY1NDYyMg==`[:16] = `MTcwYjA3MGRhOTY1` |
| 66  | `d6537d845a964081` | `ZDY1MzdkODQ1YTk2NDA4MQ==`[:16] = `ZDY1MzdkODQ1YTk2` |
| 77  | `863f08689c97435b` | `ODYzZjA4Njg5Yzk3NDM1Yg==`[:16] = `ODYzZjA4Njg5Yzk3` |

### Request Format

Every encrypted endpoint requires these request headers:

```http
GET /api/spot/rsi/list?pageSize=500&pageNum=1
Host: capi.coinglass.com
Accept: application/json, text/plain, */*
encryption: true
language: en
cache-ts-v2: <current_time_ms>
Origin: https://www.coinglass.com
Referer: https://www.coinglass.com/
User-Agent: Mozilla/5.0 (X11; Linux x86_64) Chrome/125.0.0.0 Safari/537.36
```

### Response Format

Encrypted endpoints return:

```http
HTTP/1.1 200 OK
v: 1
user: <base64_encoded_token>
encryption: true
ev: 2
content-type: application/json

{"code":"0","msg":"success","data":"<base64_encrypted_payload>"}
```

Non-encrypted endpoints return plain JSON (no `v` or `user` headers).

---

## API Reference

### `decrypt(encrypted_body, user_token_b64, v, url="")`

Low-level decryption. Applies the two-round AES-ECB + gzip pipeline and returns the plain Python dict.

```python
from decrypt import decrypt
import requests

resp = requests.get("https://capi.coinglass.com/api/spot/rsi/list", params={"pageSize": 2})
data = decrypt(resp.text, resp.headers["user"], resp.headers["v"])
```

### `fetch_and_decrypt(url, params=None, timeout=30)`

High-level convenience wrapper: sends a browser-like GET request with encryption headers, then decrypts.

```python
from decrypt import fetch_and_decrypt

data = fetch_and_decrypt(
    "https://capi.coinglass.com/api/spot/rsi/list",
    {"pageSize": 500, "pageNum": 1},
)
print(data["total"])  # → 413
```

---

## Available Data Categories

All **136 encrypted endpoints** verified working. Summary by category:

| Category | Count | What you get |
|----------|------|-------------|
| **Spot** | 10 | RSI (15m/1h/4h/12h/24h) for 400+ coins, markets, info, out/in flows, market cap |
| **Futures** | 16 | Liquidation charts/today, L/S ratio, big orders, data distribution, OI, volume |
| **Funding Rate** | 8 | Rankings, averages, flow history, arbitrage, interest arbitrage |
| **Open Interest** | 3 | Statistics, info, OI/Volume ratio |
| **Options** | 6 | Statistics, top OI/volume, strike pain, net premium heatmap |
| **Volume** | 3 | Overview, history, per-coin detail |
| **Market Cap** | 5 | Rankings, history, stablecoin history |
| **Indices** | 20 | CGDI, CGRI, Pi Cycle, AHR999, Puell Multiple, Mayer Multiple, RSI map, MACD, volatility, + 12 more |
| **ETF** | 5 | Overview, flow, BITO, ETF history charts |
| **Derivatives** | 3 | Exchange list/info, DEX list |
| **Trading Data** | 3 | Account list, Bitfinex symbols, STA |
| **Hyperliquid** | 5 | Vaults, top positions, address groups, user count |
| **Grayscale** | 5 | Open interest, history, shareholders, GBTC history |
| **Money Flow** | 1 | Per-coin capital flow history |
| **Basis** | 1 | Current basis chart |
| **Macro/Economic** | 3 | Calendar data/events/activities |
| **Market** | 4 | Market history, volatility, treasuries, peak indicator |
| **TradFi** | 3 | TradFi overview, distribution, sector stats |
| **Stock** | 4 | Stock list, market history, v2 list |
| **Coins** | 4 | Search, liquidation, hot exchanges, unlock schedule |
| **Select** | 1 | Coin tickers |
| **Home** | 4 | Dashboard cards, coin markets sorted by RSI/OI/liq |
| **Escape Indices** | 12 | Altcoin season, BTC dominance, LTH/STH supply, NUPL, RHODL, + 7 more |
| **Other** | 7 | IP/country, sentiment, UTXO, Z-score, ITBIT volume, funding K, price |

> See [`discovered_endpoints.py`](discovered_endpoints.py) for the full endpoint catalog with parameters.

### Endpoint Status Legend

| Status | Count | Meaning |
|--------|-------|---------|
| ✅ `ENCRYPTED_ENDPOINTS_CAPI` | 136 | Encrypted (v=1), verified working, decryptable |
| ⚪ `EMPTY_RESPONSE_ONLY` | 57 | Responds with `{success:true}` but no data (needs session/params) |
| ✅ `NON_ENCRYPTED_ENDPOINTS` | 16 | Plain JSON, no encryption |
| ✅ `SPECIAL_ENDPOINTS` | 2 | Heatmap v3/v4 (non-encrypted, special routes) |
| 🟢 `ENCRYPTED_ENDPOINTS_FULL` (active) | 4 | From webpack — still alive; some encrypted, some not |
| ❌ `DEAD_ENDPOINTS` | 81 | From webpack — **all return 404** (block chain, mining, defi, overview routes removed by CoinGlass) |
| **Total active** | **~215** | |

---

## Examples

### RSI Ranking (top 10 by 4h)

```python
from decrypt import fetch_and_decrypt

data = fetch_and_decrypt(
    "https://capi.coinglass.com/api/spot/rsi/list",
    {"pageSize": 500, "pageNum": 1},
)

sorted_4h = sorted(data["list"], key=lambda x: float(x.get("rsi4h", 0)), reverse=True)
for coin in sorted_4h[:10]:
    print(f"#{coin['rank']:<4} {coin['symbol']:<10} RSI 4h={coin['rsi4h']}")
```

### Futures Home Statistics

```python
data = fetch_and_decrypt("https://capi.coinglass.com/api/futures/home/statistics")
print(data.keys())  # → volH24Chain, shortRate, oiH24Chain, openInterest, ...
```

### CGDI (CoinGlass Digital Currency Index)

```python
data = fetch_and_decrypt("https://capi.coinglass.com/api/index/cgdi")
print(f"Latest CGDI: {data['prices'][-1]:.2f}")
```

### ETF Flows

```python
data = fetch_and_decrypt("https://capi.coinglass.com/api/etf/flow")
print(f"{len(data)} ETF flow records")
```

See [`example.py`](example.py) for a working demo.

---

## Project Files

| File | Purpose |
|------|---------|
| [`decrypt.py`](decrypt.py) | Core decryption library |
| [`discovered_endpoints.py`](discovered_endpoints.py) | Full endpoint catalog with params and status |
| [`example.py`](example.py) | Usage examples |
| [`test_endpoints.py`](test_endpoints.py) | 45-endpoint automated test suite |
| [`PROBE_REPORT.md`](PROBE_REPORT.md) | Reverse engineering probe report (v values, headers, full analysis) |
| [`pyproject.toml`](pyproject.toml) | Python package config |

---

## Full Probe Report

See [`PROBE_REPORT.md`](PROBE_REPORT.md) for the complete reverse engineering probe results, including:

- v value distribution across all endpoints
- JSHook browser traffic capture analysis
- Request/response header breakdown
- Encrypted vs non-encrypted endpoint classification
- 93-endpoint bulk verification results

---

## Disclaimer

This project is for **educational and research purposes only**. The encryption scheme was reverse-engineered from publicly accessible client-side JavaScript code. Respect CoinGlass's terms of service when using this software.

## License

MIT