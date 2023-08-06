from typing import Any, Dict

import pandas as pd
from prophet import Prophet
from typing_extensions import Self

from ..analytics.evaluationMetrics import evaluations
from ..datapreparation.datapreparation_utils import logger
from ..datapreparation.prep import PreprocessingClass
from ..utility.experiment_utils import create_zero_dataframe
from ..utility.constants import predict_dataframe_columns
from .algorithm import Prophet_model, prophet_tuning
from .prophet_utils import preprocess_prophet_input, preprocess_prophet_output
from copy import deepcopy

class ProphetExperiment:
    def __init__(self):
        pass
    
    def fit(self, df_train_dict: Dict, df_val_dict: Dict, 
            hyperparameters_grid: Dict[str, Any], max_na_ratio: float = 0.5,) -> Self:
        
        count = 0
        self.models_dict = {}
        self.models_best_params = {}
        self.max_na_ratio = max_na_ratio

        # Train and tune all models for all the possible levels in the hierarchy
        tmp_df_train_dict = deepcopy(df_train_dict)
        tmp_df_val_dict = deepcopy(df_val_dict)

        for id_pred in tmp_df_train_dict.keys():
            self.models_dict[id_pred] = None
            self.models_best_params[id_pred] = {}

            logger.info(f"START training {id_pred}")
            prophet_train_df = preprocess_prophet_input(tmp_df_train_dict[id_pred], date = "Timestamp", target = "Target")
            prophet_val_df = preprocess_prophet_input(tmp_df_val_dict[id_pred], date = "Timestamp", target = "Target")

            if (prophet_train_df['y'] > 0).sum() / len(prophet_train_df) < self.max_na_ratio:
                logger.info(f"The train set for time series {id_pred} has more than {self.max_na_ratio*100}% null values, skipping it.")
                count += 1
                logger.info(f"Remaining number of iteration - {len(tmp_df_train_dict.keys())-count}")
                continue
            try:
                # Tune if we have a non-empty validation set
                best_params = prophet_tuning(hyperparameters_grid, prophet_train_df, prophet_val_df)
                Model = Prophet_model(best_params)
                # Retrain on train and val data with best parameters
                Model.fit(pd.concat([prophet_train_df, prophet_val_df]))

                self.models_best_params[id_pred] = best_params
                self.models_dict[id_pred] = Model
            except ValueError as e:
                logger.info(f"Skipping training {id_pred}, due to: {e}")
                count += 1
                logger.info(f"Remaining number of iteration - {len(tmp_df_train_dict.keys())-count}")
                continue

            logger.info(f"DONE training {id_pred}")

            count += 1
            logger.info(f"Remaining number of iteration - {len(tmp_df_train_dict.keys())-count}")

        return self
    
    def refit(self, df_dict : Dict):
                
        count = 0
        # Train and tune all models for all the possible levels in the hierarchy
        tmp_df_dict = deepcopy(df_dict)

        for id_pred in tmp_df_dict.keys():
            logger.info(f"START Re-Training {id_pred}")
            prophet_df = preprocess_prophet_input(tmp_df_dict[id_pred], date = "Timestamp", target = "Target")

            # If the models exists and have been trained, execute the retrain on the whole dataset
            if isinstance(self.models_dict[id_pred], Prophet_model):
                Model = Prophet_model(self.models_best_params[id_pred])
                # Retrain on train and val data with best parameters
                Model.fit(prophet_df)

                self.models_dict[id_pred] = Model

            logger.info(f"DONE Re-Training {id_pred}")

            count += 1
            logger.info(f"Remaining number of iteration - {len(tmp_df_dict.keys())-count}")

        return self

    def create_hyperparameters_table(
        self, hyperparameters: dict[str, Any]) -> dict[str, Any]:
        def get_params_to_log(
            model: Prophet, hyperparameters: list[str]) -> dict[str, Any]:
            return {hyper: getattr(model, hyper) for hyper in hyperparameters}

        return {id_pred.replace('/', '_') : get_params_to_log(model.model, list(hyperparameters.keys())) if model else None 
                for id_pred, model in self.models_dict.items()}

    def predict(self, df_test_dict: dict) -> pd.DataFrame:
        predictions = []
        tmp_df_test_dict = deepcopy(df_test_dict)
        for id_pred, df_test in tmp_df_test_dict.items():
            prophet_df_test = preprocess_prophet_input(df_test, date = "Timestamp", target = "Target")
            model = self.models_dict[id_pred]
            if model is None:
                logger.info(f"Skipping prediction for {id_pred}, as the model has not been trained")
                df_output = create_zero_dataframe(predict_dataframe_columns, len(prophet_df_test))
                df_output['Id_pred'] = id_pred
                df_output['Timestamp'] = list(prophet_df_test['ds'])
            else:
                try:
                    df_test_pred = model.predict(prophet_df_test)
                    df_output = preprocess_prophet_output(df_test_pred, id_pred)
                except ValueError as e:
                    logger.info(f"Skipping prediction for {id_pred}, due to: {e}")
                    df_output = create_zero_dataframe(
                        predict_dataframe_columns,
                        len(prophet_df_test),
                    )
                    df_output['Id_pred'] = id_pred
                    df_output['Timestamp'] = list(prophet_df_test['ds'])
            # Evaluate model
            predictions.append(df_output)
            logger.info(f"DONE predicting {id_pred}")

        return pd.concat(predictions)

    def evaluate(self, df_test_dict: dict) -> pd.DataFrame: 
        metrics = []
        tmp_df_test_dict = deepcopy(df_test_dict)
        predictions = self.predict(df_test_dict)
        
        for id_pred, df_test in tmp_df_test_dict.items():
            logger.info(f"START evaluating {id_pred}")           
            df_pred = predictions[predictions["Id_pred"] == id_pred]
            if df_pred.Pred_mean.sum() > 0:
                metrics.append(evaluations(df_test, df_pred, date='Timestamp' , y_true='Target', y_pred='Pred_mean'))  
        
        metrics = pd.concat(metrics).dropna()
        return metrics
