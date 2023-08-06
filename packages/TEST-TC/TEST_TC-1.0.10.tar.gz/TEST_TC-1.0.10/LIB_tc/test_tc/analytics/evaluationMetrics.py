import warnings;
warnings.simplefilter('ignore')
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error

from ..utility.exceptions import ColumnNotFound
from ..utility.tele_logger import logger


def forecast_coverage(df_real : pd.DataFrame, df_pred : pd.DataFrame) -> float:
    """
    Calculate the forecast coverage metric.

    Parameters:
    ----------
    df_real: pd.DataFrame
        DataFrame of real values with columns 'Timestamp' and 'Target'.
    df_pred: pd.DataFrame
        DataFrame of predicted values with columns 'Timestamp', 'Pred_mean',
        'Pi_lower_95', and 'Pi_upper_95'.

    Returns:
    -------
    Float
        Forecast coverage as a percentage.
    """
    # Check if the actual values fall within the prediction intervals
    within_interval = (df_real['Target'] >= df_pred['Pi_lower_95']) & (df_real['Target'] <= df_pred['Pi_upper_95'])
    
    # Calculate the forecast coverage as the percentage of actual values within the prediction intervals
    forecast_coverage = within_interval.mean() * 100
    
    return forecast_coverage


def evaluations(df_real: pd.DataFrame, df_pred: pd.DataFrame, date: str = 'Timestamp' , y_true: str = 'Target', y_pred: str = 'Pred_mean') -> pd.DataFrame:
    """
    Create a DataFrame representing the evaluation metrics

    Parameters
    ----------
    df_real: pd.DataFrame
        the dataframes containing the real values
    df_pred: pd.DataFrame
        the dataframes containing the predicted values
    date: str
        the column name for the timestamp
    y_true: str
        the target column name for the real datasets
    y_pred: str
        the target column name for the predict datasets

    Returns
    -------
        A pd.DataFrame containing the results for MAE, RMSE, MSE and R2
    """
    if date not in df_real.columns:
        raise ColumnNotFound(func='evaluations', column=date, data=df_real)
    if date not in df_pred.columns:
        raise ColumnNotFound(func='evaluations', column=date, data=df_pred)
    if y_true not in df_real.columns:
        raise ColumnNotFound(func='evaluations', column=y_true, data=df_real)
    if y_pred not in df_pred.columns:
        raise ColumnNotFound(func='evaluations', column=y_pred, data=df_pred)

    logger.info('START Ealuating results')

    df_real= df_real.set_index(date).dropna()
    df_pred= df_pred.set_index(date).dropna()
    inter = df_real.index.intersection(df_pred.index)

    if len(inter) == 0:
        logger.warning(f'Length of intersection between Predictions and Ground Truth Datasets for {df_pred["Id_pred"][0]} is Null. Probably one of the two Datasets has not available data (all NaN).')
        scores = {'Id_pred': df_pred["Id_pred"][0], 'MAE':[np.nan], 'MAPE':[np.nan], 'RMSE': [np.nan], 'MSE':[np.nan], 'R2':[np.nan], 'Percentage Coverage':[np.nan]}
    else:    
        df_real = df_real.loc[inter]
        df_pred = df_pred.loc[inter]

        # Mean Absolute Error
        logger.info('Evaluating MAE')
        mae = round(mean_absolute_error(df_real[y_true], df_pred[y_pred]),2)
        # Mean Absolute Error
        logger.info('Evaluating MAPE')
        mape = round(mean_absolute_percentage_error(df_real[y_true], df_pred[y_pred]),2)
        # Root Mean Square Error
        logger.info('Evaluating RMSE')
        rmse = round(mean_squared_error(df_real[y_true], df_pred[y_pred], squared = False),2)
        # Mean Square Error
        logger.info('Evaluating MSE')
        mse = round(mean_squared_error(df_real[y_true], df_pred[y_pred]),2)
        # Coefficient of Determination
        logger.info('Evaluating R2')
        r2 = round(r2_score(df_real[y_true], df_pred[y_pred]),2)
        # Forecast Coverage Percentage
        logger.info('Evaluating Forecast Coverage Percentage')
        coverage = forecast_coverage(df_real=df_real, df_pred=df_pred)

        scores = {'Id_pred': df_pred["Id_pred"][0], 'MAE':[mae], 'MAPE':[mape], 'RMSE': [rmse], 'MSE':[mse], 'R2':[r2], 'Percentage Coverage':[coverage]}

        logger.info('DONE Evaluating results')

    # Saving the scores in a DF
    return pd.DataFrame(scores)
