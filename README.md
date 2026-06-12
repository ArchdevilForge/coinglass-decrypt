# CoinGlass Decrypt

**Pure Python decryption of CoinGlass internal API responses. No API key, no browser required.**

CoinGlass ([coinglass.com](https://www.coinglass.com)) is a cryptocurrency data aggregator that encrypts its public API payloads with AES-128-ECB. This project reverse-engineers the encryption scheme (extracted from the CoinGlass webpack module 12471) and provides a simple Python interface to decrypt any endpoint.

## Quick Start

```bash
pip install requests pycryptodome
python example.py
```

## How It Works

CoinGlass encrypts API responses, but the decryption key is delivered alongside the encrypted data via response headers.

```
Request  ──→  GET /api/spot/rsi/list  (with `encryption: true` header)
                  │
Response  ──→  Headers: { user: <base64 token>, v: "55" }
                  │
                  ▼
            1. Lookup Key0 from internal constant table (v=55 → "170b070da9654622")
            2. AES-128-ECB decrypt(user_token, Key0) → gzip(actual_key)
            3. Gunzip → actual AES key
            4. AES-128-ECB decrypt(encrypted_body, actual_key) → gzip(JSON)
            5. Gunzip → plain JSON
```

No authentication, cookies, session, or API key is needed. Anyone can decrypt any endpoint.

### Key Constants

The `v` response header selects which constant is used to derive the first-layer key:

| `v` | Constant | Source |
|-----|----------|--------|
| 55 | `170b070da9654622` | Webpack module 12471, `Kt[22]` |
| 66 | `d6537d845a964081` | Webpack module 12471, `Kt[38]` |
| 77 | `863f08689c97435b` | Webpack module 12471, `BatcW` |
| 1  | URL path | Derived from `btoa(url_path)[:16]` |

## API Reference

### `decrypt(encrypted_body, user_token_b64, v, url="")`

Low-level decryption. Parses the encrypted JSON body, applies the two-round AES-ECB + gzip pipeline, and returns the plain Python dict.

```python
from decrypt import decrypt
import requests, json

resp = requests.get("https://capi.coinglass.com/api/spot/rsi/list", params={"pageSize": 2})
data = decrypt(resp.text, resp.headers["user"], resp.headers["v"])
print(json.dumps(data, indent=2))
```

### `fetch_and_decrypt(url, params=None, timeout=30)`

High-level convenience wrapper: sends a browser-like GET request with encryption headers, then decrypts the response.

```python
from decrypt import fetch_and_decrypt

data = fetch_and_decrypt(
    "https://capi.coinglass.com/api/spot/rsi/list",
    {"pageSize": 500, "pageNum": 1},
)
print(data["total"])  # → 413
```

## Available Data Categories

Over **280 encrypted endpoints** have been discovered and verified working. Data includes:

| Category | Sample Endpoints |
|----------|-----------------|
| **Spot RSI** | RSI values (15m/1h/4h/12h/24h) for 400+ coins |
| **Funding Rate** | Rankings, averages, flow history, heatmaps |
| **Open Interest** | Statistics, charts, OI/Volume ratio |
| **Options** | Statistics, top OI/volume, max pain strike |
| **ETF Flows** | BTC/ETH/SOL/XRP ETF inflows/outflows |
| **Long/Short Ratio** | Per-coin L/S ratio, account ratio, position ratio |
| **Liquidation** | Charts by exchange, today's data, max orders |
| **Market Cap** | Rankings, history, stablecoin dominance |
| **On-Chain Metrics** | Hash rate, SOPR, MVRV, active addresses, CDD, 50+ metrics |
| **On-Chain Indices** | CGDI, CGRI, Pi Cycle, AHR999, Puell Multiple, Mayer Multiple |
| **Escape Indices** | Altcoin season, Bitcoin dominance, reserve risk, NUPL, RHODL |
| **Macro/Stocks** | Traditional finance overview, stock data |
| **Money Flow** | Per-coin capital flow history |
| **Treasuries** | Public company BTC holdings, MicroStrategy data |
| **Hyperliquid** | Vaults, top positions, user distribution |
| **Economic Calendar** | Macro event calendar |
| **And more…** | Basis, volatility, order flow, large orders, UTXO, CME COT reports |

See [`discovered_endpoints.py`](discovered_endpoints.py) for the full catalog.

## Example

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

Run `python example.py` for a working demo.

## Disclaimer

This project is for **educational and research purposes only**. The encryption scheme was reverse-engineered from publicly accessible client-side JavaScript code. Respect CoinGlass's terms of service when using this software.

## License

MIT
