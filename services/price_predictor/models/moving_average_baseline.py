iimport pandas as pd

class MovingAverageBaseline:
    """
    A simple baseline model that predicts the next price using the moving average of the last `window_size` prices.
    """
    def __init__(self, window_size: int):
        self.window_size = window_size

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """
        Fits the model to the data.
        """
        pass
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Talk to Shadrack and he will help you implement this method")
        pass