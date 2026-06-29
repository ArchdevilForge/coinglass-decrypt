#!/usr/bin/env python3
"""Test multiple CoinGlass encrypted endpoints — comprehensive."""

from decrypt import fetch_and_decrypt
import sys

BASE = "https://capi.coinglass.com"

TO_TEST = [
    # Spot
    ("/api/spot/coin/category", None, "Spot Coin Category"),
    ("/api/spot/coin/info", {"symbol": "BTC"}, "Spot BTC Info"),
    ("/api/spot/coin/markets", {"symbol": "BTC"}, "Spot BTC Markets"),
    ("/api/spot/coin/symbol", {"symbol": "BTC"}, "Spot BTC Symbol"),
    ("/api/spot/marketCap/data", None, "Spot Market Cap"),
    ("/api/spot/priceChange/history", {"symbol": "BTC"}, "Spot BTC Price Change"),
    # Futures
    ("/api/futures/liquidation/chart", {"symbol": "BTC", "interval": "1h"}, "Futures Liq Chart"),
    ("/api/futures/liquidation/today", {"symbol": "BTC"}, "Futures Liq Today"),
    ("/api/futures/longShortRate", {"symbol": "BTC", "timeType": 1, "type": 0}, "Futures L/S Rate"),
    ("/api/futures/home/statistics", None, "Futures Home Stats"),
    ("/api/futures/bigOrder", {"symbol": "BTC"}, "Futures Big Order"),
    ("/api/futures/data/distribution", {"symbol": "BTCUSDT", "exName": "Binance"}, "Futures Data Dist"),
    ("/api/futures/ticker", {"symbol": "BTC"}, "Futures Ticker"),
    ("/api/futures/v2/coins/markets", None, "Futures V2 Coin Mkts"),
    # Funding Rate
    ("/api/fundingRate/list", {"pageSize": 5, "pageNum": 1}, "FR List"),
    ("/api/fundingRate/avg", None, "FR Avg"),
    ("/api/fundingRate/heatmap", {"type": 1}, "FR Heatmap"),
    ("/api/fundingRate/v2/home", None, "FR V2 Home"),
    # Open Interest
    ("/api/openInterest/statistics", None, "OI Statistics"),
    ("/api/openInterest/info", {"symbol": "BTC"}, "OI BTC Info"),
    ("/api/openInterest/change", {"symbol": "BTC"}, "OI BTC Change"),
    ("/api/openInterest/v3/chart", {"symbol": "BTC", "interval": "1h"}, "OI V3 Chart"),
    # Options
    ("/api/option/statistics", None, "Option Statistics"),
    ("/api/option/v2/chart", {"symbol": "BTC"}, "Option V2 Chart"),
    # Volume
    ("/api/vol/overview", None, "Vol Overview"),
    ("/api/vol/history", None, "Vol History"),
    # Market Cap
    ("/api/marketCapRank", {"pageSize": 10}, "Mkt Cap Rank"),
    ("/api/marketCap/history", {"symbol": "BTC"}, "Mkt Cap BTC Hist"),
    # Indices
    ("/api/index/cgdi", None, "CGDI Index"),
    ("/api/index/cgri", {"symbol": "BTC"}, "CGRI Index"),
    ("/api/index/pi", None, "PI Index"),
    # ETF
    ("/api/etf/overview", None, "ETF Overview"),
    ("/api/etf/flow", None, "ETF Flow"),
    # Macro
    ("/api/economic/calendar/data", None, "Economic Calendar"),
    # Trading Data
    ("/api/tradingData/accountLSRatio", {"symbol": "BTC"}, "TradingData L/S"),
    ("/api/tradingData/whaleVsRetail", {"symbol": "BTC"}, "Whale vs Retail"),
    # Money Flow
    ("/api/moneyFlow/history", {"symbol": "BTC"}, "Money Flow Hist"),
    # Liquidation Levels
    ("/api/liquidationLevels/v2", {"symbol": "BTC"}, "Liq Levels V2"),
    # Basis
    ("/api/basis/current/chart", {"symbol": "BTC"}, "Basis Chart"),
    # Grayscale
    ("/api/grayscaleOpenInterest", None, "Grayscale OI"),
    # Coin
    ("/api/coin/search", {"keyword": "BTC"}, "Coin Search"),
    ("/api/coin/tickers", {"pageSize": 10}, "Coin Tickers"),
    # Stock
    ("/api/stock/detail", {"symbol": "AAPL"}, "Stock AAPL"),
    # Escape Indices
    ("/api/escape/index/altCoinSeason", None, "Altcoin Season"),
    ("/api/escape/index/bitcoinDominance", None, "BTC Dominance"),
]

ok = 0
fail = 0

for path, params, label in TO_TEST:
    url = f"{BASE}{path}"
    try:
        data = fetch_and_decrypt(url, params, timeout=15)
        if isinstance(data, dict):
            keys = list(data.keys())[:3]
        elif isinstance(data, list):
            keys = f"list[{len(data)} items]"
        else:
            keys = type(data).__name__
        print(f"  \033[32m✓\033[0m {label:30s} keys={keys}")
        ok += 1
    except Exception as e:
        print(f"  \033[31m✗\033[0m {label:30s} {e}")
        fail += 1

print(f"\n\033[32m✓ {ok} passed\033[0m, \033[31m{fail} failed\033[0m / {ok+fail} total")
sys.exit(0 if fail == 0 else 1)
