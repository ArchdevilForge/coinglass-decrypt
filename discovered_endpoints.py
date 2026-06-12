#!/usr/bin/env python3
"""
Discovered CoinGlass API Endpoints

Source: Reverse-engineered from Next.js webpack bundles
  - Main bundle: https://s3.coinglass.com/v1/cg/_next/static/chunks/pages/_app-f75bb33a408a04d3.js
  - Webpack module 12471 contains AES-ECB encryption logic, FP/xW functions, interceptors
  - Strings obfuscated via lookup table function Qt(offset, seed)

Base URLs:
  - https://capi.coinglass.com            (main API, encrypted + plain)
  - https://fapi.coinglass.com            (secondary API, mostly plain)
  - https://capi.coinglass.com/liquidity-heatmap  (liquidity heatmaps, plain)
  - https://capi.coinglass.com/coin-community     (community features)
  - https://fapi.coinglass.com/coin-community      (community features)

APIs are called via one of these wrappers from module 12471:
  - FP (exported as `FP`, function `ie`):   GET with encryption headers, decrypts response
  - xW (exported as `xW`, function `ae`):   Non-encrypted request
  - Zl (exported as `Zl`, function `se`):   POST with encryption headers

Headers for encrypted requests (set by request interceptor):
  - encryption: true
  - cache-ts-v2: <timestamp>
  - language: en (or user's language)
  - obe: <value from params.obe>
  - ua: <value from params.ua>
  - User-Agent: Mozilla/5.0 ...
  - Origin: https://www.coinglass.com
  - Referer: https://www.coinglass.com/...

Encrypted response headers:
  - user: base64-encoded user token (decrypts to actual AES key)
  - v: version indicator (55, 66, 77, or 1 for URL-based)
"""

# === ENCRYPTED ENDPOINTS (via FP wrapper) ===
# These are called with encryption: true header and return encrypted responses.
# Use fetch_and_decrypt() from decrypt.py.

ENCRYPTED_ENDPOINTS_CAPI = {
    # === SPOT ===
    "/api/spot/rsi/list": {"pageSize": 500, "pageNum": 1},
    "/api/spot/coin/category": None,
    "/api/spot/coin/markets": {"symbol": "BTC"},
    "/api/spot/coin/info": {"symbol": "BTC"},
    "/api/spot/coin/symbol": {"symbol": "BTC"},
    "/api/spot/coin/outIn": {"symbol": "BTC"},
    "/api/spot/outIn/category": None,
    "/api/spot/support/coin": None,
    "/api/spot/margin/realCrossLendingRate": None,
    "/api/spot/marketCap/data": None,
    "/api/spot/priceChange/history": {"symbol": "BTC"},
    "/api/spot/pricePerformance": {"symbol": "BTC"},

    # === FUTURES ===
    "/api/futures/liquidation/chart": {"symbol": "BTC", "interval": "1h"},
    "/api/futures/liquidation/today": None,
    "/api/futures/liquidation/order": {"symbol": "BTC"},
    "/api/futures/liquidation/maxOrder": None,
    "/api/futures/liquidation/count/heatmap": None,
    "/api/futures/liquidation/ex/info": None,
    "/api/futures/longShortRate": {"symbol": "BTC", "timeType": 1, "type": 0},
    "/api/futures/longShortChart": {"symbol": "BTC"},
    "/api/futures/home/statistics": None,
    "/api/futures/bigOrder": None,
    "/api/futures/data/distribution": {"symbol": "BTC"},
    "/api/futures/coins/heatmap": None,
    "/api/futures/coins/priceChange": None,
    "/api/futures/ticker": {"symbol": "BTC"},
    "/api/futures/v2/coins/markets": None,
    "/api/futures/v2/marginMarketCap": None,
    "/api/futures/vol/chart": {"symbol": "BTC", "type": 1, "timeType": 1},
    "/api/futures/select/coins/tickers": None,
    "/api/futures/accountAndPosition": None,
    "/api/futures/accountAndPosition/list": None,
    "/api/futures/ocPcCompare": None,
    "/api/futures/insuranceFundBalance/history": {"symbol": "BTC"},
    "/api/futures/market/category?full=true": None,

    # === FUNDING RATE ===
    "/api/fundingRate/list": {"pageSize": 100, "pageNum": 1},
    "/api/fundingRate/rank": {"pageSize": 100},
    "/api/fundingRate/avg": None,
    "/api/fundingRate/flow": None,
    "/api/fundingRate/heatmap": {"type": 1},
    "/api/fundingRate/cumulative": None,
    "/api/fundingRate/coin/detail": {"symbol": "BTC"},
    "/api/fundingRate/arbitrage-list": None,
    "/api/fundingRate/interestArbitrageV2": None,
    "/api/fundingRate/v2/history/chart": {"symbol": "BTC"},
    "/api/fundingRate/v2/home": None,

    # === OPEN INTEREST ===
    "/api/openInterest/statistics": None,
    "/api/openInterest/info": {"symbol": "BTC"},
    "/api/openInterest/change": {"symbol": "BTC"},
    "/api/openInterest/oiVolRadio": {"symbol": "BTC"},
    "/api/openInterest/v3/chart": {"symbol": "BTC", "interval": "1h"},
    "/api/openInterest/ex/info": None,

    # === OPTIONS ===
    "/api/option/statistics": None,
    "/api/option/v2/chart": {"symbol": "BTC"},
    "/api/option/oi/history": {"symbol": "BTC"},
    "/api/option/vol/history": {"symbol": "BTC"},
    "/api/option/top/oi": {"symbol": "BTC"},
    "/api/option/top/vol": {"symbol": "BTC"},
    "/api/option/strike_pain": {"symbol": "BTC"},
    "/api/option/index/chart": {"symbol": "BTC"},
    "/api/option/netPremiumStrikeHeatmap": {"symbol": "BTC"},

    # === VOLUME ===
    "/api/vol/overview": None,
    "/api/vol/history": None,
    "/api/vol/coin/top/overview": None,
    "/api/vol/coin/detail/overview": {"symbol": "BTC"},

    # === MARKET CAP ===
    "/api/marketCapRank": {"pageSize": 100},
    "/api/marketCapRank/history": {"symbol": "BTC"},
    "/api/marketCap/history": {"symbol": "BTC"},
    "/api/marketCap/stablecoin/history": {"symbol": "USDT"},
    "/api/marketCap/type/history": {"symbol": "BTC"},

    # === INDICES (CGDI/CGRI etc.) ===
    "/api/index/cgdi": None,
    "/api/index/cgdi/performance": None,
    "/api/index/cgri": {"symbol": "BTC"},
    "/api/index/cgri/performance": {"symbol": "BTC"},
    "/api/index/pi": None,
    "/api/index/macdList": None,
    "/api/index/rsiMap": {"symbol": "BTC"},
    "/api/index/history": None,
    "/api/index/priceAndOiMap": {"symbol": "BTC"},
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
    "/api/index/aggregate/liqHeatMap": None,
    "/api/index/v2/liqHeatMap": {"symbol": "BTC"},
    "/api/index/v3/aggregate/liqHeatMap": None,
    "/api/index/v5/liqHeatMap": None,
    "/api/index/2/exLiqMap": None,
    "/api/index/5/liqMap": None,

    # === ETF ===
    "/api/etf/overview": None,
    "/api/etf/flow": None,
    "/api/etf/bito": None,
    "/api/etf/bito/history/chart": None,
    "/api/etf/history/chart?type=2": None,

    # === DERIVATIVES ===
    "/api/derivative/exchange/list": None,
    "/api/derivative/exchange/info": {"exName": "Binance"},
    "/api/derivative/exchange/heatmap": None,
    "/api/derivative/exchange/dex/list": None,
    "/api/derivative/exchange/sta/history": {"exName": "Binance"},
    "/api/derivative/exchange/futures/symbolRank": None,
    "/api/derivative/exchange/pair-rank": None,

    # === TRADING DATA ===
    "/api/tradingData/accountList": None,
    "/api/tradingData/accountLSRatio": {"symbol": "BTC"},
    "/api/tradingData/positionLSRatio": {"symbol": "BTC"},
    "/api/tradingData/bitfinex/chart": None,
    "/api/tradingData/bitfinex/symbols": None,
    "/api/tradingData/whaleVsRetail": {"symbol": "BTC"},
    "/api/tradingData/sta?type=2": None,

    # === HYPERLIQUID ===
    "/api/hyperliquid/vaults": None,
    "/api/hyperliquid/topPosition": None,
    "/api/hyperliquid/topPosition/action": None,
    "/api/hyperliquid/topPosition/actionHistory": None,
    "/api/hyperliquid/topPosition/liqMap": None,
    "/api/hyperliquid/address/symbol/group": None,
    "/api/hyperliquid/position/user/count": None,

    # === GRAYSCALE ===
    "/api/grayscaleOpenInterest": None,
    "/api/grayscaleOpenInterest/history": None,
    "/api/grayscale/shareholders": None,
    "/api/grayscale/eft/gbtc/history": None,
    "/api/grayscale/market/history": None,

    # === MONEY FLOW ===
    "/api/moneyFlow/history": {"symbol": "BTC"},

    # === LIQUIDATION LEVELS ===
    "/api/liquidationLevels/v2": {"symbol": "BTC"},

    # === BASIS ===
    "/api/basis/current/chart": {"symbol": "BTC"},
    "/api/basis/v2/chart": {"symbol": "BTC"},

    # === MACRO / ECONOMIC ===
    "/api/economic/calendar/data": None,
    "/api/economic/calendar/event": None,
    "/api/economic/calendar/activities": None,

    # === MARKET ===
    "/api/marketHistory": None,
    "/api/marketVolatility": {"symbol": "BTC"},
    "/api/priceAndIndicator": None,
    "/api/bitcoinTreasuries": None,
    "/api/bull_market_peak_indicator": None,

    # === STOCK / TRADFI ===
    "/api/tradfi/overview": None,
    "/api/tradfi/market-list": None,
    "/api/tradfi/overall-distribution": None,
    "/api/tradfi/sector-statistics-list": None,
    "/api/stock/list": {"pageSize": 20},
    "/api/stock/v2/list": {"pageSize": 20},
    "/api/stock/all/list": None,
    "/api/stock/detail": {"symbol": "AAPL"},
    "/api/stock/history": {"symbol": "AAPL"},
    "/api/stock/news": None,
    "/api/stock/market/history/all": None,

    # === COINS ===
    "/api/coin/search": {"keyword": "BTC"},
    "/api/coin/tickers": {"pageSize": 100},
    "/api/coin/market": None,
    "/api/coin/all_history": None,
    "/api/coin/liquidation": {"symbol": "BTC"},
    "/api/coin/liq/heatmap": None,
    "/api/coin/hot/exs": None,
    "/api/coin/unlock/list": None,
    "/api/coin/unlock/detail": {"symbol": "BTC"},

    # === SELECT ===
    "/api/select/coins/tickers": None,
    "/api/support/symbol": None,
    "/api/v2/support/symbol": None,
    "/api/ticker": None,

    # === ESCAPE INDICES ===
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

    # === OTHERS ===
    "/api/ip/country": None,
    "/api/cexs": None,
    "/api/ls/card": None,
    "/api/ls/sentiment": None,
    "/api/utxo/list": None,
    "/api/marv/z-score/list": None,
    "/api/itbit/vol/chart": None,
    "/api/book/funding_k": None,
    "/api/sys/goto": None,
    "/api/v2/kline": None,
    "/api/price": {"symbol": "BTC", "interval": "1d"},

    # === ARTICLES / STRAPI ===
    "/api/articles": None,
    "/api/articles/related/": None,
    "/api/strapi/page": None,
    "/api/strapi/wiki_category_list": None,
}

# === ENCRYPTED ENDPOINTS (full URLs) ===
# These use the full https:// URL rather than relative path
ENCRYPTED_ENDPOINTS_FULL = [
    # --- capi.coinglass.com ---
    "https://capi.coinglass.com/api/block/transaction/analytics",
    "https://capi.coinglass.com/api/block/transaction/find",
    "https://capi.coinglass.com/api/block/transaction/history",
    "https://capi.coinglass.com/api/block/transaction/stat",
    "https://capi.coinglass.com/api/btcCompare/etfStrategy",
    "https://capi.coinglass.com/api/btcCompare/exchangeEtf",
    "https://capi.coinglass.com/api/btcCompare/exchangeStrategy",
    "https://capi.coinglass.com/api/etf/eth/flow",
    "https://capi.coinglass.com/api/etf/flow",
    "https://capi.coinglass.com/api/etf/hk/flow",
    "https://capi.coinglass.com/api/etf/hype/flow",
    "https://capi.coinglass.com/api/etf/sol/flow",
    "https://capi.coinglass.com/api/etf/xrp/flow",
    "https://capi.coinglass.com/api/futures/data/distribution/2",
    "https://capi.coinglass.com/api/futures/flow/category",
    "https://capi.coinglass.com/api/futures/flow/table",
    "https://capi.coinglass.com/api/futures/select/coins/tickers",
    "https://capi.coinglass.com/api/futures/top/coins/tickers",
    "https://capi.coinglass.com/api/grayscale/eft/gbtc",
    "https://capi.coinglass.com/api/home/category",
    "https://capi.coinglass.com/api/home/coinMarkets",
    "https://capi.coinglass.com/api/home/v2/coinMarkets",
    "https://capi.coinglass.com/api/index/optionVsFuturesByOi",
    "https://capi.coinglass.com/api/kline",
    "https://capi.coinglass.com/api/largeOrder",
    "https://capi.coinglass.com/api/largeOrder/statistics",
    "https://capi.coinglass.com/api/largeTakerOrder",
    "https://capi.coinglass.com/api/largeTakerOrder/revoke",
    "https://capi.coinglass.com/api/largeTakerOrder/statistics",
    "https://capi.coinglass.com/api/openInterest/v3/ETH-BTC/chart",
    "https://capi.coinglass.com/api/orderFlow",
    "https://capi.coinglass.com/api/price",
    "https://capi.coinglass.com/api/spot/coin/info",
    "https://capi.coinglass.com/api/spot/coin/markets",
    "https://capi.coinglass.com/api/spot/coin/outIn",
    "https://capi.coinglass.com/api/spot/coin/symbol",
    "https://capi.coinglass.com/api/spot/outIn/category",
    "https://capi.coinglass.com/api/spot/support/coin",
    "https://capi.coinglass.com/api/stock/asset/history/change",
    "https://capi.coinglass.com/api/stock/eth/list",
    "https://capi.coinglass.com/api/stock/eth/spot/inFlow",
    "https://capi.coinglass.com/api/stock/history/premium",
    "https://capi.coinglass.com/api/stock/history/premium/spot",
    "https://capi.coinglass.com/api/stock/hype/list",
    "https://capi.coinglass.com/api/stock/hype/spot/inFlow",
    "https://capi.coinglass.com/api/stock/sol/list",
    "https://capi.coinglass.com/api/stock/sol/spot/inFlow",
    "https://capi.coinglass.com/api/stock/spot/inFlow",
    "https://capi.coinglass.com/api/stock/xrp/list",
    "https://capi.coinglass.com/api/stock/xrp/spot/inFlow",
    "https://capi.coinglass.com/api/strapi/home_list_v2",
    "https://capi.coinglass.com/api/strapi/wiki_category",
    "https://capi.coinglass.com/api/strapi/wiki_related",
    "https://capi.coinglass.com/api/strapi/wiki_search",
    "https://capi.coinglass.com/api/treasury/eth/company/Detail",
    "https://capi.coinglass.com/api/treasury/eth/company/list",
    "https://capi.coinglass.com/api/treasury/eth/history",
    "https://capi.coinglass.com/api/treasury/eth/purchases/list",
    "https://capi.coinglass.com/api/treasury/eth/top",
    "https://capi.coinglass.com/api/treasury/eth/top_v2",
    "https://capi.coinglass.com/api/v2/kline",
    "https://capi.coinglass.com/coin-community/api/user/contract/ticker/collect/list",

    # --- fapi.coinglass.com ---
    "https://fapi.coinglass.com/api/calendar/liquidation/event",
    "https://fapi.coinglass.com/api/coin/history",
    "https://fapi.coinglass.com/api/coin/performance",
    "https://fapi.coinglass.com/api/coin/profile",
    "https://fapi.coinglass.com/api/coin/related",
    "https://fapi.coinglass.com/api/coin/v2/info",
    "https://fapi.coinglass.com/api/coin/vol/heatmap",
    "https://fapi.coinglass.com/api/earn/flexible",
    "https://fapi.coinglass.com/api/escape/index/microStrategyCostV2",
    "https://fapi.coinglass.com/api/flippening",
    "https://fapi.coinglass.com/api/flippening/details",
    "https://fapi.coinglass.com/api/flippening/list",
    "https://fapi.coinglass.com/api/flippening/statInfo",
    "https://fapi.coinglass.com/api/hyperliquid/address/group/count",
    "https://fapi.coinglass.com/api/hyperliquid/address/group/margin",
    "https://fapi.coinglass.com/api/hyperliquid/address/group/pnl",
    "https://fapi.coinglass.com/api/hyperliquid/address/largest/positions",
    "https://fapi.coinglass.com/api/hyperliquid/address/liquidation/risk",
    "https://fapi.coinglass.com/api/hyperliquid/address/openPerp/top",
    "https://fapi.coinglass.com/api/hyperliquid/address/user/List",
    "https://fapi.coinglass.com/api/hyperliquid/position/symbol/shortAndLong",
    "https://fapi.coinglass.com/api/index/bitcoinActiveAddresses",
    "https://fapi.coinglass.com/api/index/bitcoinNewAddresses",
    "https://fapi.coinglass.com/api/index/bitcoinPowerLaw",
    "https://fapi.coinglass.com/api/index/federalFundsRate",
    "https://fapi.coinglass.com/api/index/globalM2SupplyGrowth",
    "https://fapi.coinglass.com/api/index/terminalPrice",
    "https://fapi.coinglass.com/api/index/uSM2SupplyGrowth",
    "https://fapi.coinglass.com/api/index/v4/aggregate/liqHeatMap",
    "https://fapi.coinglass.com/api/index/v6/liqHeatMap",
    "https://fapi.coinglass.com/api/index/volatilityList",
    "https://fapi.coinglass.com/api/liqHeatMap/list",
    "https://fapi.coinglass.com/api/metrics/balanceGt0P01",
    "https://fapi.coinglass.com/api/metrics/balanceGt0P1",
    "https://fapi.coinglass.com/api/metrics/balanceGt1",
    "https://fapi.coinglass.com/api/metrics/balanceGt10",
    "https://fapi.coinglass.com/api/metrics/balanceGt100",
    "https://fapi.coinglass.com/api/metrics/balanceGt100k",
    "https://fapi.coinglass.com/api/metrics/balanceGt10k",
    "https://fapi.coinglass.com/api/metrics/balanceGt1k",
    "https://fapi.coinglass.com/api/metrics/between0P1And1",
    "https://fapi.coinglass.com/api/metrics/between100And1k",
    "https://fapi.coinglass.com/api/metrics/between10And100",
    "https://fapi.coinglass.com/api/metrics/between10kAnd100k",
    "https://fapi.coinglass.com/api/metrics/between1And10",
    "https://fapi.coinglass.com/api/metrics/between1kAnd10k",
    "https://fapi.coinglass.com/api/metrics/bitcoinBalancedPrice",
    "https://fapi.coinglass.com/api/metrics/bitcoinCDD",
    "https://fapi.coinglass.com/api/metrics/bitcoinCVDD",
    "https://fapi.coinglass.com/api/metrics/bitcoinCorrelation",
    "https://fapi.coinglass.com/api/metrics/bitcoinDeltaTop",
    "https://fapi.coinglass.com/api/metrics/bitcoinHashPriceIndex",
    "https://fapi.coinglass.com/api/metrics/bitcoinHashRate",
    "https://fapi.coinglass.com/api/metrics/bitcoinHashRibbons",
    "https://fapi.coinglass.com/api/metrics/bitcoinLTHMVRV",
    "https://fapi.coinglass.com/api/metrics/bitcoinLTHRealizedPrice",
    "https://fapi.coinglass.com/api/metrics/bitcoinLTHSOPR",
    "https://fapi.coinglass.com/api/metrics/bitcoinLiveliness",
    "https://fapi.coinglass.com/api/metrics/bitcoinNRPL",
    "https://fapi.coinglass.com/api/metrics/bitcoinNetworkBlocks",
    "https://fapi.coinglass.com/api/metrics/bitcoinSOPR",
    "https://fapi.coinglass.com/api/metrics/bitcoinSTHMVRV",
    "https://fapi.coinglass.com/api/metrics/bitcoinSTHRealizedPrice",
    "https://fapi.coinglass.com/api/metrics/bitcoinSTHSOPR",
    "https://fapi.coinglass.com/api/metrics/bitcoinSTHSupplyChange",
    "https://fapi.coinglass.com/api/metrics/bitcoinThermocap",
    "https://fapi.coinglass.com/api/metrics/bitcoinTopCap",
    "https://fapi.coinglass.com/api/metrics/bitcoinVDDMultiple",
    "https://fapi.coinglass.com/api/metrics/bitcoinWhaleShadows",
    "https://fapi.coinglass.com/api/metrics/blockHeight",
    "https://fapi.coinglass.com/api/metrics/blockRewardPerDay",
    "https://fapi.coinglass.com/api/metrics/blockSpeedTime",
    "https://fapi.coinglass.com/api/metrics/blockWeight",
    "https://fapi.coinglass.com/api/metrics/btcFeesDay",
    "https://fapi.coinglass.com/api/metrics/btcGoldCorrelation",
    "https://fapi.coinglass.com/api/metrics/btcLTHSupplyChange",
    "https://fapi.coinglass.com/api/metrics/btcMinerOutflows",
    "https://fapi.coinglass.com/api/metrics/btcSupplyInLoss",
    "https://fapi.coinglass.com/api/metrics/btcSupplyInProfit",
    "https://fapi.coinglass.com/api/metrics/btcUsEquitiesCorrelation",
    "https://fapi.coinglass.com/api/metrics/circulatingSupply",
    "https://fapi.coinglass.com/api/metrics/countryDistributionNode",
    "https://fapi.coinglass.com/api/metrics/cryptocurrencyLegality",
    "https://fapi.coinglass.com/api/metrics/dailyMinerRevenue",
    "https://fapi.coinglass.com/api/metrics/exBTCDailyMarketShare",
    "https://fapi.coinglass.com/api/metrics/exBTCDailyTotalTradingVol",
    "https://fapi.coinglass.com/api/metrics/exBTCDailyTradingVol",
    "https://fapi.coinglass.com/api/metrics/exBTCMonthlyTradingVol",
    "https://fapi.coinglass.com/api/metrics/exBTCVolumeDominance",
    "https://fapi.coinglass.com/api/metrics/exDailyMarketShare",
    "https://fapi.coinglass.com/api/metrics/exDailyTradingVol",
    "https://fapi.coinglass.com/api/metrics/exMonthlyTradingVol",
    "https://fapi.coinglass.com/api/metrics/futureBTCTrend",
    "https://fapi.coinglass.com/api/metrics/futuresTradingVolume",
    "https://fapi.coinglass.com/api/metrics/googleTrends",
    "https://fapi.coinglass.com/api/metrics/governmentTreasuries",
    "https://fapi.coinglass.com/api/metrics/gtFiveYearHODLWave",
    "https://fapi.coinglass.com/api/metrics/gtOneYearHODLWave",
    "https://fapi.coinglass.com/api/metrics/gtTenYearHODLWave",
    "https://fapi.coinglass.com/api/metrics/holdingGtXByYear",
    "https://fapi.coinglass.com/api/metrics/latestBlocksMined",
    "https://fapi.coinglass.com/api/metrics/monthlyMinerRevenue",
    "https://fapi.coinglass.com/api/metrics/nodesByASN",
    "https://fapi.coinglass.com/api/metrics/nonZeroBalance",
    "https://fapi.coinglass.com/api/metrics/numberUtxosInLoss",
    "https://fapi.coinglass.com/api/metrics/numberUtxosInProfit",
    "https://fapi.coinglass.com/api/metrics/outputPerDay",
    "https://fapi.coinglass.com/api/metrics/outputPerTx",
    "https://fapi.coinglass.com/api/metrics/outputVolPerDay",
    "https://fapi.coinglass.com/api/metrics/outputVolPerTx",
    "https://fapi.coinglass.com/api/metrics/percentAddressesInLoss",
    "https://fapi.coinglass.com/api/metrics/percentAddressesInProfit",
    "https://fapi.coinglass.com/api/metrics/percentUtxosInProfit",
    "https://fapi.coinglass.com/api/metrics/piCycleTopPrediction",
    "https://fapi.coinglass.com/api/metrics/predictions",
    "https://fapi.coinglass.com/api/metrics/priceDrawDownFromATH",
    "https://fapi.coinglass.com/api/metrics/priceForecastTools",
    "https://fapi.coinglass.com/api/metrics/pricePerfSinceHalving",
    "https://fapi.coinglass.com/api/metrics/realizedCapHODLWaves",
    "https://fapi.coinglass.com/api/metrics/redditSubscribers",
    "https://fapi.coinglass.com/api/metrics/spot2FuturesTradingVolume",
    "https://fapi.coinglass.com/api/metrics/spotETFDailyAUM",
    "https://fapi.coinglass.com/api/metrics/spotETFMarketShare",
    "https://fapi.coinglass.com/api/metrics/spotETFNetFlows",
    "https://fapi.coinglass.com/api/metrics/spotETFNetFlowsUsd",
    "https://fapi.coinglass.com/api/metrics/spotETFTradingVolume",
    "https://fapi.coinglass.com/api/metrics/spotTotalETFNetFlows",
    "https://fapi.coinglass.com/api/metrics/treasuries",
    "https://fapi.coinglass.com/api/metrics/usOffshoreTradingVolume",
    "https://fapi.coinglass.com/api/metrics/wbtcBalance",
    "https://fapi.coinglass.com/api/metrics/weeklyPricePerf",
    "https://fapi.coinglass.com/api/metrics/wikiPageViews",
    "https://fapi.coinglass.com/api/metrics/yearlyCandles",
    "https://fapi.coinglass.com/api/metrics/yearlyPricePerf",
    "https://fapi.coinglass.com/api/moneyFlow/coin",
    "https://fapi.coinglass.com/api/sys/api/config",
    "https://fapi.coinglass.com/api/treasury/BTCNetFlowWeekly",
    "https://fapi.coinglass.com/api/treasury/balanceSheetHistory",
    "https://fapi.coinglass.com/api/treasury/balanceSheetHistoryV2",
    "https://fapi.coinglass.com/api/treasury/btcStock",
    "https://fapi.coinglass.com/api/treasury/publicCompanies?top=60",
    "https://fapi.coinglass.com/api/treasury/similarCompanies",
    "https://fapi.coinglass.com/api/treasury/statInfo",
    "https://fapi.coinglass.com/api/treasury/stockDetails",
    "https://fapi.coinglass.com/api/treasury/totalHistory",
    "https://fapi.coinglass.com/api/v2/kline",
    "https://fapi.coinglass.com/coin-community/api/user/collect/hy/list",
]

# === NON-ENCRYPTED ENDPOINTS (via xW wrapper) ===
# These are called without encryption headers, plain HTTP.
NON_ENCRYPTED_ENDPOINTS = [
    # === ALARM (coin-community) ===
    "/coin-community/api/alarm/create",
    "/coin-community/api/alarm/delete",
    "/coin-community/api/alarm/list",
    "/coin-community/api/alarm/msg",
    "/coin-community/api/alarm/update",
    "/coin-community/api/alarm/update/status",

    # === USER COLLECTIONS (coin-community) ===
    "/coin-community/api/user/collect/filter/delete",
    "/coin-community/api/user/collect/filter/save",
    "/coin-community/api/user/collect/list?type=11",
    "/coin-community/api/user/billAddress/find",
    "/coin-community/api/user/billAddress/save",

    # === LS SENTIMENT (both FP and xW registered) ===
    "/api/ls/sentiment",

    # === FULL URLS (non-encrypted) ===
    "https://capi.coinglass.com/coin-community/api/user/contract/symbol/collect",
    "https://fapi.coinglass.com/coin-community/api/user/collect/update/hy/remark",
    "https://fapi.coinglass.com/coin-community/api/user/contract/symbol/collect",
]

# === SPECIAL ENDPOINTS (liquidity heatmap, non-encrypted) ===
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

# === ADDITIONAL ENDPOINTS (from bundle but not categorized into FP/xW) ===
ADDITIONAL_ENDPOINTS = {
    # BRC20 tokens
    "brc20": [
        "/api/brc20/detail", "/api/brc20/gasFee", "/api/brc20/holders",
        "/api/brc20/list", "/api/brc20/ohlc", "/api/brc20/tickers", "/api/brc20/transfer",
    ],
    # ARC20 tokens
    "arc20": [
        "/api/arc20/detail", "/api/arc20/holders", "/api/arc20/list",
        "/api/arc20/market", "/api/arc20/price", "/api/arc20/transfer",
    ],
    # CME
    "cme": [
        "/api/cme/cot/report", "/api/cme/cot/report/history",
    ],
    # Exchange assets
    "exchange_assets": [
        "/api/exchangeAssets/data", "/api/exchangeAssets/list",
        "/api/exchange/chain/v3/balance", "/api/exchange/chain/v3/balance/list",
        "/api/exchange/futures/supportCoin", "/api/exchange/futures/transactionCount",
    ],
    # BitMEX
    "bitmex": [
        "/api/bitmex/BTC/price", "/api/bitmex/leaderboard",
        "/api/bitmex/leaderboard/userHistory", "/api/bitmex/position",
    ],
    # Home
    "home": [
        "/api/home/card", "/api/home/card2", "/api/home/card4",
        "/api/home/coinMarkets",
    ],
    # Others
    "other": [
        "/api/bl/", "/api/sys/goto",
    ],
}

if __name__ == "__main__":
    print(f"ENCRYPTED (capi relative): {len(ENCRYPTED_ENDPOINTS_CAPI)}")
    print(f"ENCRYPTED (full URLs):     {len(ENCRYPTED_ENDPOINTS_FULL)}")
    print(f"NON-ENCRYPTED:            {len(NON_ENCRYPTED_ENDPOINTS)}")
    print(f"SPECIAL:                   {len(SPECIAL_ENDPOINTS)}")
    print(f"TOTAL: ~{len(ENCRYPTED_ENDPOINTS_CAPI) + len(ENCRYPTED_ENDPOINTS_FULL) + len(NON_ENCRYPTED_ENDPOINTS) + len(SPECIAL_ENDPOINTS)}")
