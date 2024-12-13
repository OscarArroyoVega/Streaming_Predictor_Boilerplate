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

    # Check if input arrays contain any null values
    arrays = {'high': high, 'low': low, 'close': close, 'volume': volume}
    if any(np.isnan(arr).any() for arr in arrays.values()):
        return candle

    indicators = {}

    # Helper function to safely add indicator
    def add_indicator(name: str, value) -> None:
        if isinstance(value, tuple):
            # Handle multi-value indicators like MACD and BBANDS
            if not any(np.isnan(v) if v is not None else True for v in value):
                indicators[name] = value
        elif not np.isnan(value) if value is not None else True:
            indicators[name] = value

    # compute the technical indicators
    # Simple Moving Average - Shows average price over period
    add_indicator('sma_14', stream.SMA(close, timeperiod=14))

    # Relative Strength Index - Momentum indicator showing overbought/oversold conditions
    for period in [9, 14, 21]:
        add_indicator(f'rsi_{period}', stream.RSI(close, timeperiod=period))

    # Moving Average Convergence Divergence - Trend-following momentum indicator
    macd = stream.MACD(close, fastperiod=10, slowperiod=24, signalperiod=9)
    if all(v is not None and not np.isnan(v) for v in macd if v is not None):
        macd_line, signal_line, hist = macd
        add_indicator('macd_10_line', macd_line)
        add_indicator('macd_10_signal', signal_line)
        add_indicator('macd_10_hist', hist)

    # Bollinger Bands - Shows volatility channels around moving average
    for period in [10, 15, 20]:
        bbands = stream.BBANDS(close, timeperiod=period, nbdevup=2, nbdevdn=2)
        if all(band is not None for band in bbands):
            upper, middle, lower = bbands
            add_indicator(f'upper_band_{period}', upper)
            add_indicator(f'middle_band_{period}', middle)
            add_indicator(f'lower_band_{period}', lower)

    # Average Directional Index - Measures trend strength
    add_indicator('adx_14', stream.ADX(high, low, close, timeperiod=14))

    # Exponential Moving Average - Weighted moving average emphasizing recent prices
    add_indicator('ema_10', stream.EMA(close, timeperiod=10))

    # Average True Range - Measures market volatility
    add_indicator('atr_14', stream.ATR(high, low, close, timeperiod=14))

    # Price Rate of Change - Momentum indicator showing price changes over time
    add_indicator('price_roc_10', stream.ROC(close, timeperiod=10))

    # Money Flow Index - Volume-weighted RSI
    add_indicator('mfi_14', stream.MFI(high, low, close, volume, timeperiod=14))

    # Williams %R - Momentum indicator similar to RSI but scaled -100 to 0
    add_indicator('willr_14', stream.WILLR(high, low, close, timeperiod=14))

    # Only merge indicators if we have valid values
    final_message = {**candle}
    if indicators:
        final_message.update(indicators)

    return final_message  # FIXME many technical indicators have NaN values, many of them in offline store!
