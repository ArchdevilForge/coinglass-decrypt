#!/usr/bin/env python3
"""Example: fetch CoinGlass RSI data."""

from decrypt import fetch_and_decrypt
import json

# --- RSI List ---
print("=== RSI List (top 10 by 4h) ===\n")

data = fetch_and_decrypt(
    "https://capi.coinglass.com/api/spot/rsi/list",
    {"pageSize": 500, "pageNum": 1},
)

sorted_4h = sorted(data["list"], key=lambda x: float(x.get("rsi4h", 0)), reverse=True)
for coin in sorted_4h[:10]:
    print(
        f"  #{coin['rank']:<4} {coin['symbol']:<10} "
        f"${float(coin['price']):>10,.4f}  "
        f"RSI 4h={coin['rsi4h']:<7}  "
        f"1h={coin['rsi1h']:<7}  15m={coin['rsi15m']}"
    )

# --- Extreme values ---
high = [c for c in data["list"] if float(c.get("rsi4h", 0)) >= 70]
low = [c for c in data["list"] if float(c.get("rsi4h", 0)) <= 30]
print(f"\nRSI 4h ≥ 70 ({len(high)} coins):")
for c in sorted(high, key=lambda x: float(x["rsi4h"]), reverse=True):
    print(f"  {c['symbol']:<10} RSI={c['rsi4h']}  ${float(c['price']):,.4f}")
print(f"\nRSI 4h ≤ 30 ({len(low)} coins):")
for c in sorted(low, key=lambda x: float(x["rsi4h"])):
    print(f"  {c['symbol']:<10} RSI={c['rsi4h']}  ${float(c['price']):,.4f}")
