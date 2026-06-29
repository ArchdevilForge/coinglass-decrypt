#!/usr/bin/env python3
"""Example: fetch CoinGlass encrypted API data (Spot RSI, Futures, ETF, Indices)."""

from decrypt import fetch_and_decrypt
import json

BASE = "https://capi.coinglass.com"

def show(label, data):
    if isinstance(data, dict):
        keys = list(data.keys())[:5]
        print(f"  keys={keys}")
    elif isinstance(data, list):
        print(f"  list[{len(data)} items]")
    else:
        print(f"  type={type(data).__name__}")

# --- RSI List (Spot) ---
print("=== RSI List (top 10 by 4h) ===\n")
data = fetch_and_decrypt(f"{BASE}/api/spot/rsi/list", {"pageSize": 500, "pageNum": 1})
sorted_4h = sorted(data["list"], key=lambda x: float(x.get("rsi4h", 0)), reverse=True)
for coin in sorted_4h[:10]:
    print(f"  #{coin['rank']:<4} {coin['symbol']:<10} "
          f"${float(coin['price']):>10,.4f}  "
          f"RSI 4h={coin['rsi4h']:<7}  1h={coin['rsi1h']:<7}  15m={coin['rsi15m']}")

high = [c for c in data["list"] if float(c.get("rsi4h", 0)) >= 70]
low = [c for c in data["list"] if float(c.get("rsi4h", 0)) <= 30]
print(f"\nRSI 4h ≥ 70 ({len(high)} coins) / ≤ 30 ({len(low)} coins)\n")

# --- Futures Home Stats ---
print("=== Futures Home Statistics ===")
data = fetch_and_decrypt(f"{BASE}/api/futures/home/statistics")
show("futures/home/statistics", data)

# --- CGDI Index ---
print("\n=== CGDI Index ===")
data = fetch_and_decrypt(f"{BASE}/api/index/cgdi")
show("index/cgdi", data)
print(f"  Latest CGDI: {data['prices'][-1]:.2f}")

# --- ETF Overview ---
print("\n=== ETF Overview ===")
data = fetch_and_decrypt(f"{BASE}/api/etf/overview")
show("etf/overview", data)

# --- Home Card (market overview) ---
print("\n=== Market Overview Cards ===")
data = fetch_and_decrypt(f"{BASE}/api/home/card")
show("home/card", data)

# --- Home V2 Coin Markets ---
print("\n=== Home V2 Coin Markets (sorted by RSI 4h) ===")
data = fetch_and_decrypt(f"{BASE}/api/home/v2/coinMarkets",
                          {"sort": "rsi4h", "order": "desc", "pageNum": 1, "pageSize": 5, "ex": "all"})
for c in data.get("list", [])[:5]:
    print(f"  {c['symbol']:<10} price=${float(c.get('price',0)):,.4f}  "
          f"rsi4h={c.get('rsi4h','-')}  fundingRate={c.get('fundingRate','-')}")
