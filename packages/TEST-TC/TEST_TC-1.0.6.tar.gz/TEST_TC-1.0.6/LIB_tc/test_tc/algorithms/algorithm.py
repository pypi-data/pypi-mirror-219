import pandas as pd
import pickle
import itertools
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
from prophet import Prophet
from typing_extensions import Self

from .prophet_utils import check_prophet_fit_df, check_prophet_predict_df, check_prophet_save, check_prophet_load
from ..utility.tele_logger import logger


class Prophet_model:
    def __init__(self, dic_param: dict = {
                  "changepoint_prior_scale": 0.5,
                  "seasonality_prior_scale": 0.1,
                  "yearly_seasonality": 10,
                  "weekly_seasonality": 3, 
                  "daily_seasonality": 10,
                  }) -> Self:
        """
        Istanciate the Prophet_model class

        Parameters
        ----------
        dic_param: dict        
            Dictionary representing the model parameters 

        Returns
        -------
        """
        logger.info('Initializing the model class', important = True)
        self.model = Prophet(**dic_param)

    def fit(self,
            df: pd.DataFrame) -> Self:
        """
        fit method: train the prophet model on df
        Parameters
        ----------
        df: pd.DataFrame
            DataFrame in the prophet format two columns: ['ds', 'y'])
        
        Returns
        -------
        """
        # The input dataset must be in the prophet format: it must contain the two columns ['ds', 'y']
        
        check_prophet_fit_df(df)
        self.df = df
        logger.info('Training the model', important = True)
        self.model.fit(self.df)
  
    def future_dataset(self,
                dic_param: dict = {'periods': 100,
                                   'freq': 'D'}):

        """
        Generation of the dataset for future forecasting

        Parameters
        ----------
        dic_param: dict
            Dictionary of the future parameters (e.g. 'periods', 'freq')

        Returns
        -------
            pd.DataFrame
            The dataframe for the forecasting in the future
        """
        logger.info('Creation of the future dataset for forecasting')
        return self.model.make_future_dataframe(**dic_param)
    
    def predict(self,
                df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict method: prediction on df 

        Parameters
        ----------
        df: pd.DataFrame
        The dataframe on which the prediction is applied. 
            
        Returns
        -------
            pd.DataFrame
            The prophet dataframe for predictions
        """
        # The dataset should be either 2 columns ('ds','y') or 1 column ('ds')
        check_prophet_predict_df(df)

        logger.info('Prediction phase')
        return self.model.predict(df)
    
    def save(self,
             path: str) -> None:
        r"""Store algorithm to file.
        Parameters
        ----------
        path : str
            path of the file where the algorithm must be stored.
        """

        check_prophet_save(model = self.model, file_path = path)

        logger.info('Saving the model in the ".pkl" format', important = True)
        with open(path, 'wb') as file:
            pickle.dump(self.model, file)

    @classmethod
    def load(cls,
             path: str) -> Self:
        r"""Load algorithm from file.
        Parameters
        ----------
        path : str
            Path to the file where the algorithm must be stored.
        """
        check_prophet_load(file_path = path)

        logger.info('Loading the model', important = True)
        with open(path, 'rb') as file:
            model_file = pickle.load(file)
        loaded_model = cls({})
        loaded_model.model = model_file
        return loaded_model


def prophet_tuning(param_grid: dict, train_df: pd.DataFrame, validation_df: pd.DataFrame,
                   weight_rmse = 0.5, weight_mape = 0.5) -> dict:
    """
    Performs the parameters selection on a given set of parameters grid

    Parameters
    ----------
    param_grid: dict
        The parameters grid space

    train_df: pd.DataFrame
        The dataframe on which the model fit is applied 

    validation_df: pd.DataFrame
        The dataframe on which the model evaluation is applied 

    weight_rmse: numeric, optional
        weight of the rmse, by default 0.5

    weight_mape: numeric, optional
        weight of the mape, by default 0.5

    Returns
    -------
        dictionary of the best parameters

    Raises
    ------
    ValueError
        if the validation set is empty, after cleaning
    """
    rmse_mape = []
    keys, values = zip(*param_grid.items())
    permutations_dicts = [dict(zip(keys, v)) for v in itertools.product(*values)]
    for params in permutations_dicts:
        m =  Prophet_model(params)
        m.fit(train_df)
        validation_df_clean = validation_df.dropna()
        if len(validation_df_clean) > 0:
            val_predictions = m.model.predict(validation_df_clean)
            rmse = mean_squared_error(validation_df_clean['y'], val_predictions['yhat'], squared = False)
            mape = mean_absolute_error(validation_df_clean['y'], val_predictions['yhat'])
            rmse_mape.append(weight_rmse * rmse + weight_mape * mape)
        else:
            raise ValueError("Il dataframe di convalida con la rimozione dei valori nulli, è vuoto")

    best_params_index = np.argmin(rmse_mape)
    best_params = permutations_dicts[best_params_index]
    return best_params
