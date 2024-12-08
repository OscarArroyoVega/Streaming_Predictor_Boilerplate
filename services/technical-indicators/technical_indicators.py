import numpy as np
from quixstreams import State
from talib import stream


def compute_technical_indicators(candle: dict, state: State) -> dict:
    """
    Computes the technical indicators
    """

    candles = state.get('candles', default=[])

    # extract open, high, low, close, volume from the candles
    open = np.array([candle['open'] for candle in candles])
    high = np.array([candle['high'] for candle in candles])
    low = np.array([candle['low'] for candle in candles])
    close = np.array([candle['close'] for candle in candles])
    volume = np.array([candle['volume'] for candle in candles])

    indicators = {}

    # compute the technical indicators
    sma_14 = stream.SMA(close, timeperiod=14)
    indicators['sma_14'] = sma_14

    rsi_9 = stream.RSI(close, timeperiod=9)
    indicators['rsi_9'] = rsi_9

    rsi_14 = stream.RSI(close, timeperiod=14)
    indicators['rsi_14'] = rsi_14

    rsi_21 = stream.RSI(close, timeperiod=21)
    indicators['rsi_21'] = rsi_21

    rsi_28 = stream.RSI(close, timeperiod=28)
    indicators['rsi_28'] = rsi_28

    macd_10 = stream.MACD(close, fastperiod=10, slowperiod=24, signalperiod=9)
    indicators['macd_10'] = macd_10

    upper_band_10, middle_band_10, lower_band_10 = stream.BBANDS(
        close, timeperiod=10, nbdevup=2, nbdevdn=2
    )
    indicators['upper_band_10'] = upper_band_10
    indicators['middle_band_10'] = middle_band_10
    indicators['lower_band_10'] = lower_band_10

    upper_band_15, middle_band_15, lower_band_15 = stream.BBANDS(
        close, timeperiod=15, nbdevup=2, nbdevdn=2
    )
    indicators['upper_band_15'] = upper_band_15
    indicators['middle_band_15'] = middle_band_15
    indicators['lower_band_15'] = lower_band_15

    upper_band_20, middle_band_20, lower_band_20 = stream.BBANDS(
        close, timeperiod=20, nbdevup=2, nbdevdn=2
    )
    indicators['upper_band_20'] = upper_band_20
    indicators['middle_band_20'] = middle_band_20
    indicators['lower_band_20'] = lower_band_20

    adx_14 = stream.ADX(high, low, close, timeperiod=14)
    indicators['adx_14'] = adx_14

    ema_10 = stream.EMA(close, timeperiod=10)
    indicators['ema_10'] = ema_10

    atr_14 = stream.ATR(high, low, close, timeperiod=14)
    indicators['atr_14'] = atr_14

    price_roc_10 = stream.ROC(close, timeperiod=10)
    indicators['price_roc_10'] = price_roc_10

    mfi_14 = stream.MFI(high, low, close, volume, timeperiod=14)
    indicators['mfi_14'] = mfi_14

    willr_14 = stream.WILLR(high, low, close, timeperiod=14)
    indicators['willr_14'] = willr_14

    cdl_pattern = stream.CDL2CROWS(open, high, low, close)
    indicators['cdl_pattern'] = cdl_pattern

    final_message = {
        **candle,
        **indicators,
    }  # TODO: debub this message

    return final_message
