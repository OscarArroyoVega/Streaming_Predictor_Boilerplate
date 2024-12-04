import pandas as pd

def keep_only_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keeps only the numeric columns in the given DataFrame.
    """
    return df[['open', 'high', 'low', 'close', 'volume']]
