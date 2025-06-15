
# =================================================================
# 這個模組包含了交易策略的配置和優化建議。
# =================================================================

class StrategyConfig:
    """交易策略的配置"""

    # 技術指標參數
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    RSI_LENGTH = 14
    KDJ_LENGTH = 9
    KDJ_SIGNAL = 3

    MA_TREND_LENGTH = 200  # ma趨勢線的長度
    

    # 風險管理參數
    RISK_PER_TRADE = 0.02  # 每次交易的風險比例 (2%)
    MAX_POSITION_RATIO = 0.95  # 最大持倉比例 (95%)

    # ATR參數
    ATR_LENGTH = 14  # ATR計算的長度
    ATR_MULTIPLIER = 2.0  # ATR乘數，用於計算止損距離

    # 交易信號閾值
    MIN_SIGNAL_STRENGTH = 2  # 最小交易信號強度

    # RSI閾值
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30

    # KDJ閾值
    KDJ_OVERBOUGHT = 80
    KDJ_OVERSOLD = 20

    # 交易參數
    INITIAL_CASH = 10000
    COMMISSION = 0.002  # 0.2% �讠�鞎�

# =================================================================
# 優化建議
# =================================================================

class OptimizationSuggestions:
    """交易策略的優化建議"""

    MACD_FAST_RANGE = [8, 10, 12, 15]
    MACD_SLOW_RANGE = [21, 26, 30, 35]
    MACD_SIGNAL_RANGE = [6, 9, 12]

    RSI_LENGTH_RANGE = [10, 14, 18, 21]

    KDJ_LENGTH_RANGE = [6, 9, 12, 15]
    KDJ_SIGNAL_RANGE = [2, 3, 4, 5]

    MA_TREND_RANGE = [150, 200, 250]

    RISK_RANGE = [0.01, 0.015, 0.02, 0.025, 0.03]

    ATR_MULTIPLIER_RANGE = [1.5, 2.0, 2.5, 3.0]

# =================================================================
# 市場狀態參數
# =================================================================

class MarketRegimeParams:
    """市場狀態參數"""
彍
    BULL_MARKET = {
        'min_signals': 2,
        'rsi_overbought': 75,
        'rsi_oversold': 35,
        'atr_multiplier': 2.5,
        'risk_per_trade': 0.025
    }

    BEAR_MARKET = {
        'min_signals': 2,
        'rsi_overbought': 65,
        'rsi_oversold': 25,
        'atr_multiplier': 1.5,
        'risk_per_trade': 0.015
    }

    SIDEWAYS_MARKET = {
        'min_signals': 3, 
        'rsi_overbought': 70,
        'rsi_oversold': 30,
        'atr_multiplier': 2.0,
        'risk_per_trade': 0.02
    }