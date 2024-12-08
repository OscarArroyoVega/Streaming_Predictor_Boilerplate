import numpy as np
from quixstreams import State
from talib import stream


def compute_technical_indicators(candle: dict, state: State) -> dict:
    """
    Computes the technical indicators
    """

    candles = state.get('candles', default=[])

    # extract open, high, low, close, volume from the candles
    # open = np.array([candle['open'] for candle in candles])
    high = np.array([candle['high'] for candle in candles])
    low = np.array([candle['low'] for candle in candles])
    close = np.array([candle['close'] for candle in candles])
    volume = np.array([candle['volume'] for candle in candles])

    indicators = {}

    # compute the technical indicators
    # Simple Moving Average - Shows average price over period
    indicators['sma_14'] = stream.SMA(close, timeperiod=14)

    # Relative Strength Index - Momentum indicator showing overbought/oversold conditions
    indicators['rsi_9'] = stream.RSI(close, timeperiod=9)
    indicators['rsi_14'] = stream.RSI(close, timeperiod=14)
    indicators['rsi_21'] = stream.RSI(close, timeperiod=21)
    indicators['rsi_28'] = stream.RSI(close, timeperiod=28)

    # Moving Average Convergence Divergence - Trend-following momentum indicator
    indicators['macd_10'] = stream.MACD(
        close, fastperiod=10, slowperiod=24, signalperiod=9
    )

    # Bollinger Bands - Shows volatility channels around moving average
    for period in [10, 15, 20]:
        upper, middle, lower = stream.BBANDS(
            close, timeperiod=period, nbdevup=2, nbdevdn=2
        )
        indicators[f'upper_band_{period}'] = upper
        indicators[f'middle_band_{period}'] = middle
        indicators[f'lower_band_{period}'] = lower

    # Average Directional Index - Measures trend strength
    indicators['adx_14'] = stream.ADX(high, low, close, timeperiod=14)

    # Exponential Moving Average - Weighted moving average emphasizing recent prices
    indicators['ema_10'] = stream.EMA(close, timeperiod=10)

    # Average True Range - Measures market volatility
    indicators['atr_14'] = stream.ATR(high, low, close, timeperiod=14)

    # Price Rate of Change - Momentum indicator showing price changes over time
    indicators['price_roc_10'] = stream.ROC(close, timeperiod=10)

    # Money Flow Index - Volume-weighted RSI
    indicators['mfi_14'] = stream.MFI(high, low, close, volume, timeperiod=14)

    # Williams %R - Momentum indicator similar to RSI but scaled -100 to 0
    indicators['willr_14'] = stream.WILLR(high, low, close, timeperiod=14)

    final_message = {
        **candle,
        **indicators,
    }  # TODO: debub this message

    return final_message
