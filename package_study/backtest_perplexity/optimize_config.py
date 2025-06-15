
# =================================================================
# 蝑𣇉裦��彍�滨蔭��辣
# =================================================================

class StrategyConfig:
    """蝑𣇉裦��彍�滨蔭憿�"""

    # �箇������彍
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    RSI_LENGTH = 14
    KDJ_LENGTH = 9
    KDJ_SIGNAL = 3

    # 頞典𨋍�擧蕪�典���
    MA_TREND_LENGTH = 200  # �瑟�頞典𨋍蝘餃�撟喳�

    # 憸券麬蝞∠���彍
    RISK_PER_TRADE = 0.02  # 瘥讐�鈭斗�憸券麬瘥𥪯� (2%)
    MAX_POSITION_RATIO = 0.95  # ��憭批�劐�瘥𥪯� (95%)

    # 甇Ｘ���彍
    ATR_LENGTH = 14  # ATR閮���望�
    ATR_MULTIPLIER = 2.0  # ATR甇Ｘ��齿彍

    # 靽∟�撘瑕漲��彍
    MIN_SIGNAL_STRENGTH = 2  # ��撠煾�閬�Ⅱ隤滨�����賊� (2/3)

    # RSI頞�眺頞�都瘞游像
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30

    # KDJ頞�眺頞�都瘞游像
    KDJ_OVERBOUGHT = 80
    KDJ_OVERSOLD = 20

    # �墧葫��彍
    INITIAL_CASH = 10000
    COMMISSION = 0.002  # 0.2% �讠�鞎�

# =================================================================
# ��彍�芸�撱箄降
# =================================================================

class OptimizationSuggestions:
    """��彍�芸�撱箄降"""

    # MACD��彍�芸�蝭��
    MACD_FAST_RANGE = [8, 10, 12, 15]
    MACD_SLOW_RANGE = [21, 26, 30, 35]
    MACD_SIGNAL_RANGE = [6, 9, 12]

    # RSI��彍�芸�蝭��
    RSI_LENGTH_RANGE = [10, 14, 18, 21]

    # KDJ��彍�芸�蝭��
    KDJ_LENGTH_RANGE = [6, 9, 12, 15]
    KDJ_SIGNAL_RANGE = [2, 3, 4, 5]

    # 頞典𨋍�擧蕪�典��𣇉���
    MA_TREND_RANGE = [150, 200, 250]

    # 憸券麬蝞∠��芸�蝭��
    RISK_RANGE = [0.01, 0.015, 0.02, 0.025, 0.03]

    # ATR甇Ｘ��芸�蝭��
    ATR_MULTIPLIER_RANGE = [1.5, 2.0, 2.5, 3.0]

# =================================================================
# 撣�聦�啣��拇���彍
# =================================================================

class MarketRegimeParams:
    """銝滚�撣�聦�啣�����詨遣霅�"""

    # �𥕦���彍
    BULL_MARKET = {
        'min_signals': 2,
        'rsi_overbought': 75,
        'rsi_oversold': 35,
        'atr_multiplier': 2.5,
        'risk_per_trade': 0.025
    }

    # �𠰴���彍
    BEAR_MARKET = {
        'min_signals': 2,
        'rsi_overbought': 65,
        'rsi_oversold': 25,
        'atr_multiplier': 1.5,
        'risk_per_trade': 0.015
    }

    # ��䪸撣����
    SIDEWAYS_MARKET = {
        'min_signals': 3,  # �游𠂔�潛�蝣箄�
        'rsi_overbought': 70,
        'rsi_oversold': 30,
        'atr_multiplier': 2.0,
        'risk_per_trade': 0.02
    }