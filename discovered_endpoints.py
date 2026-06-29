#!/usr/bin/env python3
"""
CoinGlass API 端点清单（完整测试版）。

分类:
  - ENCRYPTED_ENDPOINTS_CAPI:  加密端点，实测可用（136 个）
  - EMPTY_RESPONSE_ONLY:       端点存在但返回空 success（57 个）
  - ENCRYPTED_ENDPOINTS_FULL:  完整 URL 列表（from webpack）（85 个）
     实测结果：仅 1 个加密活跃 + 1 个加密有数据 + 3 个非加密，其余 80 个返回 404
  - NON_ENCRYPTED_ENDPOINTS:   非加密端点（16 个）
  - SPECIAL_ENDPOINTS:         特殊端点（2 个）
  - DEAD_ENDPOINTS:            返回 404 的废弃端点（80 个）
"""

# === 实测可用的加密端点 (136) ===
ENCRYPTED_ENDPOINTS_CAPI = {
    # SPOT
    "/api/spot/rsi/list": {"pageSize": 500, "pageNum": 1},
    "/api/spot/coin/markets": {"symbol": "BTC"},
    "/api/spot/coin/info": {"symbol": "BTC"},
    "/api/spot/coin/symbol": {"symbol": "BTC"},
    "/api/spot/coin/outIn": {"symbol": "BTC"},
    "/api/spot/outIn/category": None,
    "/api/spot/support/coin": None,
    "/api/spot/margin/realCrossLendingRate": None,
    "/api/spot/marketCap/data": None,
    "/api/spot/pricePerformance": {"symbol": "BTC"},

    # FUTURES
    "/api/futures/liquidation/chart": {"symbol": "BTC", "interval": "1h"},
    "/api/futures/liquidation/today": {"symbol": "BTC"},
    "/api/futures/liquidation/maxOrder": None,
    "/api/futures/liquidation/ex/info": None,
    "/api/futures/longShortRate": {"symbol": "BTC", "timeType": 1, "type": 0},
    "/api/futures/home/statistics": None,
    "/api/futures/bigOrder": {"symbol": "BTC"},
    "/api/futures/data/distribution": {"symbol": "BTCUSDT", "exName": "Binance"},
    "/api/futures/coins/priceChange": None,
    "/api/futures/v2/coins/markets": None,
    "/api/futures/v2/marginMarketCap": None,
    "/api/futures/vol/chart": {"symbol": "BTC", "type": 1, "timeType": 1},
    "/api/futures/select/coins/tickers": None,
    "/api/futures/accountAndPosition/list": None,
    "/api/futures/ocPcCompare": None,
    "/api/futures/market/category?full=true": None,

    # FUNDING RATE
    "/api/fundingRate/list": {"pageSize": 100, "pageNum": 1},
    "/api/fundingRate/rank": {"pageSize": 100},
    "/api/fundingRate/avg": None,
    "/api/fundingRate/flow": None,
    "/api/fundingRate/coin/detail": {"symbol": "BTC"},
    "/api/fundingRate/arbitrage-list": None,
    "/api/fundingRate/interestArbitrageV2": None,
    "/api/fundingRate/v2/home": None,

    # OPEN INTEREST
    "/api/openInterest/statistics": None,
    "/api/openInterest/info": {"symbol": "BTC"},
    "/api/openInterest/oiVolRadio": {"symbol": "BTC"},

    # OPTIONS
    "/api/option/statistics": None,
    "/api/option/vol/history": {"symbol": "BTC"},
    "/api/option/top/oi": {"symbol": "BTC"},
    "/api/option/top/vol": {"symbol": "BTC"},
    "/api/option/strike_pain": {"symbol": "BTC"},
    "/api/option/netPremiumStrikeHeatmap": {"symbol": "BTC"},

    # VOLUME
    "/api/vol/overview": None,
    "/api/vol/history": None,
    "/api/vol/coin/detail/overview": {"symbol": "BTC"},

    # MARKET CAP
    "/api/marketCapRank": {"pageSize": 100},
    "/api/marketCapRank/history": {"symbol": "BTC"},
    "/api/marketCap/history": {"symbol": "BTC"},
    "/api/marketCap/stablecoin/history": {"symbol": "USDT"},
    "/api/marketCap/type/history": {"symbol": "BTC"},

    # INDICES
    "/api/index/cgdi": None,
    "/api/index/cgdi/performance": None,
    "/api/index/cgri": {"symbol": "BTC"},
    "/api/index/cgri/performance": {"symbol": "BTC"},
    "/api/index/pi": None,
    "/api/index/macdList": None,
    "/api/index/rsiMap": {"symbol": "BTC"},
    "/api/index/history": None,
    "/api/index/bitcoinBubbleIndex": None,
    "/api/index/bitcoinProfitableDays": None,
    "/api/index/goldenRatioMultiplier": None,
    "/api/index/stockFlow": None,
    "/api/index/puellMultiple": None,
    "/api/index/logLogRegression": None,
    "/api/index/v2/ahr999": None,
    "/api/index/towYearMAMultiplier": None,
    "/api/index/towHundredWeekMovingAvgHeatmap": None,
    "/api/index/volatilityHistory": {"symbol": "BTC"},

    # ETF
    "/api/etf/overview": None,
    "/api/etf/flow": None,
    "/api/etf/bito": None,
    "/api/etf/bito/history/chart": None,
    "/api/etf/history/chart?type=2": None,

    # DERIVATIVES
    "/api/derivative/exchange/list": None,
    "/api/derivative/exchange/info": {"exName": "Binance"},
    "/api/derivative/exchange/dex/list": None,

    # TRADING DATA
    "/api/tradingData/accountList": None,
    "/api/tradingData/bitfinex/symbols": None,
    "/api/tradingData/sta?type=2": None,

    # HYPERLIQUID
    "/api/hyperliquid/vaults": None,
    "/api/hyperliquid/topPosition": None,
    "/api/hyperliquid/topPosition/action": None,
    "/api/hyperliquid/address/symbol/group": None,
    "/api/hyperliquid/position/user/count": None,

    # GRAYSCALE
    "/api/grayscaleOpenInterest": None,
    "/api/grayscaleOpenInterest/history": None,
    "/api/grayscale/shareholders": None,
    "/api/grayscale/eft/gbtc/history": None,
    "/api/grayscale/market/history": None,

    # MONEY FLOW
    "/api/moneyFlow/history": {"symbol": "BTC"},

    # BASIS
    "/api/basis/current/chart": {"symbol": "BTC"},

    # MACRO / ECONOMIC
    "/api/economic/calendar/data": None,
    "/api/economic/calendar/event": None,
    "/api/economic/calendar/activities": None,

    # MARKET
    "/api/marketHistory": None,
    "/api/marketVolatility": {"symbol": "BTC"},
    "/api/bitcoinTreasuries": None,
    "/api/bull_market_peak_indicator": None,

    # TRADFI
    "/api/tradfi/overview": None,
    "/api/tradfi/overall-distribution": None,
    "/api/tradfi/sector-statistics-list": None,

    # STOCK
    "/api/stock/list": None,
    "/api/stock/v2/list": {"type": 2},
    "/api/stock/all/list": None,
    "/api/stock/market/history/all": None,

    # COINS
    "/api/coin/search": {"keyword": "BTC"},
    "/api/coin/liquidation": {"symbol": "BTC"},
    "/api/coin/hot/exs": None,
    "/api/coin/unlock/list": None,

    # SELECT
    "/api/select/coins/tickers": None,
    "/api/support/symbol": None,
    "/api/v2/support/symbol": None,

    # HOME
    "/api/home/v2/coinMarkets": {"sort": "rsi4h", "order": "desc", "pageNum": 1, "pageSize": 5, "ex": "all"},
    "/api/home/card": None,
    "/api/home/card2": None,
    "/api/home/card4": None,

    # ESCAPE INDICES
    "/api/escape/index/altCoinSeason": None,
    "/api/escape/index/bitcoinDominance": None,
    "/api/escape/index/longTermHolderSupply": None,
    "/api/escape/index/shortTermHolderSupply": None,
    "/api/escape/index/reserveRisk": None,
    "/api/escape/index/nupl": None,
    "/api/escape/index/rhodlRatio": None,
    "/api/escape/index/oscillator": None,
    "/api/escape/index/fourYearMovingAverage": None,
    "/api/escape/index/cBBIIndex": None,
    "/api/escape/index/mayerMultiple": None,
    "/api/escape/index/aHR999Escape": None,

    # OTHER (plain, return real data)
    "/api/ip/country": None,
    "/api/ls/sentiment": None,
    "/api/utxo/list": None,
    "/api/marv/z-score/list": None,
    "/api/itbit/vol/chart": None,
    "/api/book/funding_k": None,
    "/api/price": {"symbol": "BTC", "interval": "1d"},
}

# === 端点存在但返回空 success (57) ===
# 这些端点无崩溃，但返回 {"code":"0","msg":"success","success":true} 无数据。
# 可能需要额外参数或浏览器会话认证。
EMPTY_RESPONSE_ONLY = [
    "/api/spot/coin/category",
    "/api/spot/priceChange/history",
    "/api/futures/liquidation/order",
    "/api/futures/liquidation/count/heatmap",
    "/api/futures/longShortChart",
    "/api/futures/coins/heatmap",
    "/api/futures/ticker",
    "/api/futures/accountAndPosition",
    "/api/futures/insuranceFundBalance/history",
    "/api/fundingRate/heatmap",
    "/api/fundingRate/cumulative",
    "/api/fundingRate/v2/history/chart",
    "/api/openInterest/change",
    "/api/openInterest/v3/chart",
    "/api/openInterest/ex/info",
    "/api/option/v2/chart",
    "/api/option/oi/history",
    "/api/option/index/chart",
    "/api/vol/coin/top/overview",
    "/api/index/priceAndOiMap",
    "/api/index/aggregate/liqHeatMap",
    "/api/index/v2/liqHeatMap",
    "/api/index/v3/aggregate/liqHeatMap",
    "/api/index/v5/liqHeatMap",
    "/api/index/2/exLiqMap",
    "/api/index/5/liqMap",
    "/api/derivative/exchange/heatmap",
    "/api/derivative/exchange/sta/history",
    "/api/derivative/exchange/futures/symbolRank",
    "/api/derivative/exchange/pair-rank",
    "/api/tradingData/accountLSRatio",
    "/api/tradingData/positionLSRatio",
    "/api/tradingData/bitfinex/chart",
    "/api/tradingData/whaleVsRetail",
    "/api/hyperliquid/topPosition/actionHistory",
    "/api/hyperliquid/topPosition/liqMap",
    "/api/liquidationLevels/v2",
    "/api/basis/v2/chart",
    "/api/priceAndIndicator",
    "/api/tradfi/market-list",
    "/api/stock/detail",
    "/api/stock/history",
    "/api/stock/news",
    "/api/coin/tickers",
    "/api/coin/market",
    "/api/coin/all_history",
    "/api/coin/liq/heatmap",
    "/api/coin/unlock/detail",
    "/api/ticker",
    "/api/cexs",
    "/api/ls/card",
    "/api/sys/goto",
    "/api/v2/kline",
    "/api/articles",
    "/api/articles/related/",
    "/api/strapi/page",
    "/api/strapi/wiki_category_list",
]

# === ENCRYPTED ENDPOINTS (full URLs, from webpack) ===
# 实测结果 (2025+):
#   ✅ 活跃加密: /api/block/transaction/analytics, /fapi/api/treasury/totalHistory
#   ✅ 非加密:   /fapi/api/treasury/stockDetails, /fapi/api/v2/kline, /fapi/coin-community/...
#   ❌ 已废弃:  其余 80 个均返回 404（block chain, mining, defi, overview 系列）
#
# 说明: CoinGlass 已将 on-chain 数据分析功能迁移或下线，
#       旧的 /api/block/, /api/block/mining/, /api/block/defi/ 等路由不再可用。
#
# 注意: /api/block/transaction/analytics 返回 NoneType data（可能需额外参数），
#       /fapi/api/treasury/totalHistory 可用，v=1 加密。
ENCRYPTED_ENDPOINTS_FULL = [
    # 活跃加密端点
    {"url": "https://capi.coinglass.com/api/block/transaction/analytics",
     "status": "encrypted_working", "params": {"symbol": "BTC"},
     "note": "返回 NoneType data，可能需要在页面上下文中调用"},
    {"url": "https://fapi.coinglass.com/api/treasury/totalHistory",
     "status": "encrypted_working", "params": None,
     "note": "v=1 加密，返回 list[3103] treasury 历史数据"},
    # 非加密但仍活跃
    {"url": "https://fapi.coinglass.com/api/treasury/stockDetails",
     "status": "non_encrypted", "params": None},
    {"url": "https://fapi.coinglass.com/api/v2/kline",
     "status": "non_encrypted", "params": {"symbol": "BTC", "interval": "1h", "limit": 100},
     "note": "返回 success 但无 data→kline 需交易对参数"},
]

# === 已废弃的 /api/block/* 端点（全部返回 404） ===
# CoinGlass 已移除以下 on-chain / block / mining / defi / overview 路由。
# 保留在此以便参考，不再遍历测试。
DEAD_ENDPOINTS = [
    # /api/block/transaction/*
    "https://capi.coinglass.com/api/block/transaction/analytics/history",
    "https://capi.coinglass.com/api/block/transaction/chart",
    "https://capi.coinglass.com/api/block/transaction/overview",
    "https://capi.coinglass.com/api/block/transaction/list",
    # /api/block/adress/analytics (typo preserved from webpack)
    "https://capi.coinglass.com/api/block/adress/analytics",
    # /api/block/address/*
    "https://capi.coinglass.com/api/block/address/active/list",
    "https://capi.coinglass.com/api/block/address/new/list",
    "https://capi.coinglass.com/api/block/address/balance/list",
    "https://capi.coinglass.com/api/block/address/active/top",
    "https://capi.coinglass.com/api/block/address/topHolder",
    "https://capi.coinglass.com/api/block/address/accumulation",
    "https://capi.coinglass.com/api/block/address/balance",
    "https://capi.coinglass.com/api/block/address/topHolder/balance",
    "https://capi.coinglass.com/api/block/address/whale/netflow",
    "https://capi.coinglass.com/api/block/address/exchange/netflow",
    "https://capi.coinglass.com/api/block/address/topHolder/details",
    "https://capi.coinglass.com/api/block/address/topHolder/change",
    # /api/block/mining/*
    "https://capi.coinglass.com/api/block/mining/hashRate",
    "https://capi.coinglass.com/api/block/mining/difficulty",
    "https://capi.coinglass.com/api/block/mining/hashPrice",
    "https://capi.coinglass.com/api/block/mining/hashRate/distribution",
    "https://capi.coinglass.com/api/block/mining/pool/hashRate/list",
    "https://capi.coinglass.com/api/block/mining/miner/flow",
    "https://capi.coinglass.com/api/block/mining/miner/position",
    "https://capi.coinglass.com/api/block/mining/txFee",
    "https://capi.coinglass.com/api/block/mining/txFee/chart",
    "https://capi.coinglass.com/api/block/mining/txFee/eth",
    "https://capi.coinglass.com/api/block/mining/uncleRate",
    "https://capi.coinglass.com/api/block/mining/minerRevenue",
    "https://capi.coinglass.com/api/block/mining/costAvg",
    "https://capi.coinglass.com/api/block/mining/costAvg/chart",
    "https://capi.coinglass.com/api/block/mining/tokenUnlock",
    "https://capi.coinglass.com/api/block/mining/cds",
    "https://capi.coinglass.com/api/block/mining/cds/chart",
    "https://capi.coinglass.com/api/block/mining/energyConsumption",
    # /api/block/stableCoin/*
    "https://capi.coinglass.com/api/block/stableCoin/overview",
    "https://capi.coinglass.com/api/block/stableCoin/marketCap",
    "https://capi.coinglass.com/api/block/stableCoin/supply",
    "https://capi.coinglass.com/api/block/stableCoin/volume",
    "https://capi.coinglass.com/api/block/stableCoin/transferVolume",
    "https://capi.coinglass.com/api/block/stableCoin/transferCount",
    "https://capi.coinglass.com/api/block/stableCoin/addressCount",
    "https://capi.coinglass.com/api/block/stableCoin/velocity",
    "https://capi.coinglass.com/api/block/stableCoin/reserve",
    "https://capi.coinglass.com/api/block/stableCoin/flow",
    "https://capi.coinglass.com/api/block/stableCoin/liquidity",
    "https://capi.coinglass.com/api/block/stableCoin/stableCoinList",
    "https://capi.coinglass.com/api/block/stableCoin/ratio/history",
    # /api/block/derivative/*
    "https://capi.coinglass.com/api/block/derivative/overview",
    "https://capi.coinglass.com/api/block/derivative/oiCap",
    "https://capi.coinglass.com/api/block/derivative/oiChart",
    "https://capi.coinglass.com/api/block/derivative/liquidation/list",
    "https://capi.coinglass.com/api/block/derivative/liquidation/chart",
    "https://capi.coinglass.com/api/block/derivative/liquidation/count",
    "https://capi.coinglass.com/api/block/derivative/volumeChart",
    "https://capi.coinglass.com/api/block/derivative/rateChart",
    "https://capi.coinglass.com/api/block/derivative/longShortChart",
    "https://capi.coinglass.com/api/block/derivative/liquidation/exchange",
    # /api/block/defi/*
    "https://capi.coinglass.com/api/block/defi/overview",
    "https://capi.coinglass.com/api/block/defi/marketCapChart",
    "https://capi.coinglass.com/api/block/defi/tvlChart",
    "https://capi.coinglass.com/api/block/defi/volumeChart",
    "https://capi.coinglass.com/api/block/defi/dexVolumeChart",
    "https://capi.coinglass.com/api/block/defi/dexVolumeRateChart",
    "https://capi.coinglass.com/api/block/defi/lending",
    "https://capi.coinglass.com/api/block/defi/tvl/list",
    "https://capi.coinglass.com/api/block/defi/tvl/chain",
    # /api/block/publicChart
    "https://capi.coinglass.com/api/block/publicChart/history",
    # /api/block/overview/*
    "https://capi.coinglass.com/api/block/overview/compare",
    "https://capi.coinglass.com/api/block/overview/active",
    "https://capi.coinglass.com/api/block/overview/transaction",
    "https://capi.coinglass.com/api/block/overview/volume",
    "https://capi.coinglass.com/api/block/overview/volumeChart",
    "https://capi.coinglass.com/api/block/overview/fee",
    "https://capi.coinglass.com/api/block/overview/defi",
    "https://capi.coinglass.com/api/block/overview/stableCoin",
    "https://capi.coinglass.com/api/block/overview/derivative",
    "https://capi.coinglass.com/api/block/overview/coin",
    # /api/overview
    "https://capi.coinglass.com/api/overview/list",
    # fapi 废弃
    "https://fapi.coinglass.com/api/treasury/overview",
    "https://fapi.coinglass.com/coin-community/api/user/collect/hy/list",
]

# === NON-ENCRYPTED ENDPOINTS ===
NON_ENCRYPTED_ENDPOINTS = {
    "plain_working": {
        "/api/support/symbol": {"desc": "支持的交易对列表（明文）", "params": None},
        "/api/v2/support/symbol": {"desc": "v2 支持的交易对（实测是加密的，v=1）", "params": None},
    },
    "xW_wrapper": [
        "/coin-community/api/alarm/create",
        "/coin-community/api/alarm/delete",
        "/coin-community/api/alarm/list",
        "/coin-community/api/alarm/msg",
        "/coin-community/api/alarm/update",
        "/coin-community/api/alarm/update/status",
        "/coin-community/api/user/collect/filter/delete",
        "/coin-community/api/user/collect/filter/save",
        "/coin-community/api/user/collect/list?type=11",
        "/coin-community/api/user/billAddress/find",
        "/coin-community/api/user/billAddress/save",
    ],
    "full_urls": [
        "https://capi.coinglass.com/coin-community/api/user/contract/symbol/collect",
        "https://fapi.coinglass.com/coin-community/api/user/collect/update/hy/remark",
        "https://fapi.coinglass.com/coin-community/api/user/contract/symbol/collect",
    ],
}

NON_ENCRYPTED_ENDPOINTS_FLAT = []
for group in NON_ENCRYPTED_ENDPOINTS.values():
    if isinstance(group, dict):
        NON_ENCRYPTED_ENDPOINTS_FLAT.extend(group.keys())
    elif isinstance(group, list):
        NON_ENCRYPTED_ENDPOINTS_FLAT.extend(group)

# === SPECIAL ENDPOINTS ===
SPECIAL_ENDPOINTS = {
    "liquidity_heatmap_v3": {
        "url": "https://capi.coinglass.com/liquidity-heatmap/api/liquidity/v3/heatmap",
        "description": "Liquidity heatmap v3 (non-encrypted)",
        "params": {"symbol": "BTC", "interval": "1h", "level": 3},
    },
    "liquidity_heatmap_v4": {
        "url": "https://capi.coinglass.com/liquidity-heatmap/api/liquidity/v4/heatmap",
        "description": "Liquidity heatmap v4 (non-encrypted, has extra auth)",
        "params": {"symbol": "BTC", "interval": "1h"},
        "note": "Requires auth token - sends t={auth_token} in POST body",
    },
}

if __name__ == "__main__":
    total_enc = len(ENCRYPTED_ENDPOINTS_CAPI)
    total_full_alive = sum(1 for e in ENCRYPTED_ENDPOINTS_FULL
                           if isinstance(e, dict) and e.get("status") in ("encrypted_working", "non_encrypted"))
    total_dead = len(DEAD_ENDPOINTS)
    total_empty = len(EMPTY_RESPONSE_ONLY)
    total_non = len(NON_ENCRYPTED_ENDPOINTS_FLAT)
    total_special = len(SPECIAL_ENDPOINTS)
    print(f"ENCRYPTED (实测可用):                    {total_enc}")
    print(f"ENCRYPTED (webpack 完整 URL，活跃):      {total_full_alive}")
    print(f"ENCRYPTED (webpack 完整 URL，已废弃):    {total_dead}")
    print(f"EMPTY_RESPONSE (存在但无数据):           {total_empty}")
    print(f"NON-ENCRYPTED:                           {total_non}")
    print(f"SPECIAL:                                 {total_special}")
    print(f"TOTAL (活跃端点):                       ~{total_enc + total_full_alive + total_empty + total_non + total_special}")
