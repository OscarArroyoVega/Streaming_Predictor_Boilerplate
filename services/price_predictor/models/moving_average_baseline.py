import pandas as pd

class MovingAverageBaseline:
    """
    Class for a model that predicts the price in the next "window_size" minutes
    by using the moving average of the last "window_size" minutes
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
        Predicts the price in the next "window_size" minutes by using the moving average of the last "window_size" minutes.
        """
        return X["close"]
    
    