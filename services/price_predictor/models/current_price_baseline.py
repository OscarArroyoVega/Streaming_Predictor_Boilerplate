import pandas as pd

class CurrentPriceBaseline:
    """
    Class for a model that predicts the price in the next "window_size" minutes
    by using the current price and the current price change rate
    """
    
    def __init__(self, ohlc_window_sec: int):
        self.ohlc_window_sec = ohlc_window_sec
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fit the model to the data.
        """
        pass
    
    def predict(self, X: pd.DataFrame) -> pd.Series:
        """
        Predicts the price in the next "window_size" minutes by using the current price.
        """
        return X["close"]