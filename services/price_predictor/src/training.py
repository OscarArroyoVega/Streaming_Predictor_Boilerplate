from typing import Optional
from comet_ml import Experiment
from loguru import logger
from sklearn.metrics import mean_absolute_error

from src.config import HopsworksConfig
from src.config import CometConfig




def train_model(
    comet_config: CometConfig,
    hopsworks_config: HopsworksConfig,
    feature_view_name: str,
    feature_view_version: int,
    feature_group_name: str,
    feature_group_version: int,
    ohlc_window_sec: int,
    product_id: str,
    last_n_days: int,
    forecast_steps: int,
    comet_api_key: str,
    comet_project_name: str,
    
):
    """
    Reads features from the Feature Store 
    Trains a predictive model,
    Saves the model to the model registry
    
    Args:
        comet_config: CometConfig
        hopsworks_config: HopsworksConfig
        feature_view_name: str
        feature_view_version: int
        feature_group_name: str
        feature_group_version: int
        ohlc_window_sec: int
        product_id: str
        last_n_days: int
        forecast_steps: int
    
    Returns:
        None
    
    """
     # create a comet experiment
    experiment = Experiment(
        api_key=comet_api_key,
        project_name=comet_project_name,
    )
    
    #load features from the feature store
    from src.ohlc_data_reader import OhlcDataReader
    
    ohlc_data_reader = OhlcDataReader(
        ohlc_window_sec=ohlc_window_sec,
        hopsworks_config=hopsworks_config,
        feature_view_name=feature_view_name,
        feature_view_version=feature_view_version,
        feature_group_name=feature_group_name,
        feature_group_version=feature_group_version,
    )
    
    # read the sorted data from the offline store
    ohlc_df = ohlc_data_reader.read_from_offline_store(
        product_id=product_id,
        last_n_days=last_n_days
    )
  
    logger.debug(f"Data loaded: {ohlc_df.head()}")
    experiment.log_parameter("n_raw_feature_rows", len(ohlc_df))
      
    # Split the data into train and test sets
    prop_test_data = 0.3  # 30% for test data
    test_size = int(len(ohlc_df) * prop_test_data)
    train_df = ohlc_df[:-test_size]
    test_df = ohlc_df[-test_size:]
    logger.debug(f"Train set start date: {train_df.index[0]}, end date: {train_df.index[-1]}, length: {len(train_df)}")
    logger.debug(f"Test set start date: {test_df.index[0]}, end date: {test_df.index[-1]}, length: {len(test_df)}")
    experiment.log_parameter("n_train_rows_before_dropna", len(train_df))
    experiment.log_parameter("n_test_rows_before_dropna", len(test_df))
    
    # first dumb model!
    # add a column with the target price we want our model to predict
    # for both train and test data
    train_df['target_price'] = train_df['close'].shift(-forecast_steps)
    test_df['target_price'] = test_df['close'].shift(-forecast_steps)
    logger.debug(f"Target price added to train_df: {train_df[['close', 'target_price']].head()}")
    logger.debug(f"Target price added to test_df: {test_df[['close', 'target_price']].head()}")
   
    
    #remove the rows with NaN values
    train_df = train_df.dropna()
    test_df = test_df.dropna()
    logger.debug(f"NaN values dropped from train_df: {train_df.shape}")
    logger.debug(f"NaN values dropped from test_df: {test_df.shape}")
    experiment.log_parameter("n_train_rows_after_dropna", len(train_df))
    experiment.log_parameter("n_test_rows_after_dropna", len(test_df))
    
    # split data into features and targets
    X_train = train_df.drop(columns=['target_price'])
    y_train = train_df['target_price']
    X_test = test_df.drop(columns=['target_price'])
    y_test = test_df['target_price']
    
    #log the shape of the data
    logger.debug(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    logger.debug(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    
     # log the shapes to Comet ML
    experiment.log_parameter("X_train_shape", X_train.shape)
    experiment.log_parameter("y_train_shape", y_train.shape)
    experiment.log_parameter("X_test_shape", X_test.shape)
    experiment.log_parameter("y_test_shape", y_test.shape)

    
    #build a model
    from models.current_price_baseline import CurrentPriceBaseline
    model = CurrentPriceBaseline(ohlc_window_sec=ohlc_window_sec)
    model.fit(X_train, y_train)
    logger.debug(f"Model trained: {model}")
    experiment.log_metric("mae", mae)
        
    #evaluate the model
    y_pred = model.predict(X_test)
   
    
    mae = mean_absolute_error(y_test, y_pred)
    logger.debug(f"Mean absolute error: {mae}")     
    experiment.log_metric("mae", mae)
    breakpoint()
    
    #train an XGBoost model
    from xgboost import XGBRegressor
    xgb_model = XGBRegressor()
    xgb_model.fit(X_train, y_train)
    y_pred = xgb_model.predict(X_test)
    xgb_mae = mean_absolute_error(y_test, y_pred)
    logger.debug(f"XGBoost Mean absolute error: {xgb_mae}")
    experiment.log_metric("xgb_mae", xgb_mae)
    
    #save model to the model registry
    

    experiment.end()

if __name__ == "__main__":

    from src.config import config, hopsworks_config, comet_config
    
    train_model(
        comet_config=comet_config,
        hopsworks_config=hopsworks_config,
        feature_view_name=config.feature_view_name,
        feature_view_version=config.feature_view_version,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,    
        ohlc_window_sec=config.ohlc_window_sec,
        product_id=config.product_id,
        last_n_days=config.last_n_days,
        forecast_steps=config.forecast_steps,
    )
    
