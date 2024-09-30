from typing import Optional

from loguru import logger
import optuna
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error

class XGBoostModel:

    def __init__(self):
        self.model: XGBRegressor = None
    
    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        n_search_trials: Optional[int] = 0,
        n_splits: Optional[int] = 3,
    ):
        """
        Trains an XGBoost model on the given training data.

        Args:
            X_train: pd.DataFrame, the training data
            y_train: pd.Series, the target variable
            n_search_trials: int, the number of trials to run for hyperparameter optimization
            n_splits: int, the number of splits to use for cross-validation
        """
        logger.info(f"Training XGBoost model with n_search_trials={n_search_trials} and n_splits={n_splits}")
        
        # check that n_search_trials is not negative
        assert n_search_trials >= 0, "n_search_trials must be non-negative"

        if n_search_trials == 0:
            # train a model with default parameters
            # this is what we have been using so far
            self.model = XGBRegressor()
            self.model.fit(X_train, y_train)
            logger.info(f"Model trained with default hyperparameters")
        else:
            # we do cross-validation with the number of splits specified
            # and we search for the best hyperparameters using Bayesian optimization
            best_hyperparams = self._find_best_hyperparams(
                X_train,
                y_train,
                n_search_trials,
                n_splits
            )
            logger.info(f"Best hyperparameters: {best_hyperparams}")

            # we train the model with the best hyperparameters
            self.model = XGBRegressor(**best_hyperparams)
            self.model.fit(X_train, y_train)
            logger.info(f"Model trained with best hyperparameters")

    def predict(self, X_test):
        return self.model.predict(X_test)
    
    def _find_best_hyperparams(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        n_search_trials: int,
        n_splits: int
    ):  
        """
        Finds the best hyperparameters for the model using Bayesian optimization.

        Args:
            X_train: pd.DataFrame, the training data
            y_train: pd.Series, the target variable
            n_search_trials: int, the number of trials to run
            n_splits: int, the number of splits to use for cross-validation

        Returns:
            dict, the best hyperparameters
        """
        def objective(trial: optuna.Trial) -> float:
            """
            Objective function for Optuna that returns the mean absolute error we
            want to minimize.

            Args:
                trial: optuna.Trial, the trial object

            Returns:
                float, the mean absolute error
            """
            # we ask Optuna to sample the next set of hyperparameters
            # these are our candidates for this trial
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
                "max_depth": trial.suggest_int("max_depth", 3, 10),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                
                # TODO: there is room to improve the search space
            }

            # let's split our X_train into n_splits folds with a time-series split
            # we want to keep the time-series order in each fold
            # we will use the time-series split from sklearn
            from sklearn.model_selection import TimeSeriesSplit
            tscv = TimeSeriesSplit(n_splits=n_splits)
            mae_scores = []
            for train_index, val_index in tscv.split(X_train):

                # split the data into training and validation sets
                X_train_fold, X_val_fold = X_train.iloc[train_index], X_train.iloc[val_index]
                y_train_fold, y_val_fold = y_train.iloc[train_index], y_train.iloc[val_index]

                # train the model on the training set
                model = XGBRegressor(**params)
                model.fit(X_train_fold, y_train_fold)

                # evaluate the model on the validation set
                y_pred = model.predict(X_val_fold)
                mae = mean_absolute_error(y_val_fold, y_pred)
                mae_scores.append(mae)

            # return the average MAE across all folds
            import numpy as np
            return np.mean(mae_scores)

        # we create a study object that minimizes the objective function
        study = optuna.create_study(direction="minimize")
        
        # we run the trials
        study.optimize(objective, n_trials=n_search_trials)

        # we return the best hyperparameters
        return study.best_trial.params

    def get_model_obj(self):
        return self.model