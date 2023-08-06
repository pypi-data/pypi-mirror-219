from typing import Dict, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
# Hierarchical Forecast
from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.utils import aggregate

from ..utility.tele_logger import logger
from ..analytics.evaluationMetrics import evaluations



def get_hierarchical_df(df: pd.DataFrame, hierarchy: Dict[str, str],
                        time_granularity: str, date_col: str, target_col: str) -> pd.DataFrame:
    """
    The function generates the dataframe suitable for obtaining 
    HierarchicalForecast info. It generates this dataframe
    starting from the input dataframe by using the information
    of the configuration file.

    Parameters
    ----------
    df: pd.DataFrame
        The input dataframe (typically inside .../data/input)
    preprocessor: PreprocessingClass
        The initialized preprocessing class
    hierarchy: dict
        Dictionary retrieved from the configuration file.
        it contains the hierarchy columns ordered by levels
    time_granularity: str
        string referring to the time granularity.
        Information retrieved from the configuration file.

    Returns
    -------
        pd.DataFrame
        A dataframe of columns: ds|y|level0|level1|level2|level3
        level0 refers to Italia
        level1, level2, level3 are obtained from the hierarchy dict
    """
    
    output_df = df[[date_col, target_col]]
    output_df['level0'] = 'Italia'
    output_df['y'] = 1
    output_df[date_col] = output_df[date_col].dt.to_period(time_granularity).dt.to_timestamp()
    for level, col_name in hierarchy.items():
        output_df[level] = df[col_name]
    output_df = output_df.rename(columns={date_col:'ds'})
    return output_df

def get_hierarchical_info(hier_df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """
    The function generates the hierarchical aggregation info
    starting from the hierarchical dataframe obtained by <get_hierarchical_df>

    Parameters
    ----------
    hier_df: pd.DataFrame
        Dataframe obtained by <get_hierarchical_df>

    Returns
    -------
        Tuple(S_df: pd.DataFrame, tags: dict)
        S_df binary matrix to understand the hierarchy levels
        tags maps the hierarchy level to the hierarchy values 

    """
    filtered_columns = [col for col in hier_df.columns if 'level' in col]
    filtered_columns.sort()
    spec = [filtered_columns[:i] for i in range(1, len(filtered_columns) + 1)]
    Y_df, S_df, tags = aggregate(df = hier_df, spec = spec)
    return Y_df, S_df, tags

def get_hier_pred(test_pred):
    """
    _summary_

    Parameters
    ----------
    test_pred
        _description_

    Returns
    -------
        _description_
    """
    hier_pred = test_pred.rename(columns = {
        'Timestamp' : 'ds', 'Pred_mean' : 'Prophet'
    })

    hier_pred = hier_pred.set_index('Id_pred')
    hier_pred = hier_pred.rename_axis('unique_id')
    for col in hier_pred.columns:
        if col not in ['ds', 'Prophet']:
            hier_pred = hier_pred.drop(col, axis = 1)
    return hier_pred

def rename_index(df):
    """
    _summary_

    Parameters
    ----------
    df
        _description_

    Returns
    -------
        _description_
    """
    unique_indexes = list(df.index.unique())
    for index in unique_indexes:
        if index != 'Italia':
            new_index = 'Italia/' + index
            df.rename(index = {index : new_index}, inplace = True)
    return df

def concat_dataframes(dict_dataframe):
    """
    _summary_

    Parameters
    ----------
    dict_dataframe
        _description_

    Returns
    -------
        _description_
    """
    dataframes_to_concat = []
    for id_pred, df in dict_dataframe.items():
        df['Id_pred'] = id_pred
        dataframes_to_concat.append(df)
    concat_dataframe = pd.concat(dataframes_to_concat)
    concat_dataframe = concat_dataframe.set_index('Id_pred')
    concat_dataframe = concat_dataframe.rename_axis('unique_id')
    return concat_dataframe

def check_date_consistency(hier_train, concat_df_train):
    return np.all(pd.to_datetime(hier_train['ds']).values == pd.to_datetime(concat_df_train['Timestamp']).values)

def hierarchical_reconcilers(hier_pred, hier_train, sum_df, tags, 
                             reconcilers, confidence_level = 95, method = 'bootstrap'):
    
    hrec = HierarchicalReconciliation(reconcilers=reconcilers)
    Y_rec_df = hrec.reconcile(Y_hat_df = hier_pred, Y_df = hier_train, S = sum_df,
                            tags = tags, level=[confidence_level],
                            intervals_method = method)
    
    numeric_columns = Y_rec_df.select_dtypes(include=[np.number]).columns
    Y_rec_df[numeric_columns] = Y_rec_df[numeric_columns].round().astype(int) # update a round before astype (as astype is like "floor")
    return Y_rec_df, hrec.reconcilers

def best_reconcile(concat_df_test, reconciled_df, y_true,
                     model_name, weight_rmse = 0.5, weights_mape = 0.0):
    
    # TODO -> funzione che riallinea le colonne di output di predizione (Id_pred)
    concat_df_test = concat_df_test.dropna()
    reconciled_df = reconciled_df.dropna()
    joined_df = reconciled_df.join(concat_df_test, how='inner')

    if len(joined_df) > 0:
        interest_columns = [col for col in reconciled_df.columns if col.startswith(f'{model_name}'.title()) and 'lo' not in col[-7:] and 'hi' not in col]
        
        metrics_methods = {}
        for pred_col in interest_columns:
            mape = round(mean_absolute_percentage_error(joined_df[y_true], joined_df[pred_col]), 2)
            rmse = round(mean_squared_error(joined_df[y_true], joined_df[pred_col], squared = False), 2)
            weighted_metric = weight_rmse * rmse + weights_mape * mape
            metrics_methods[pred_col] = weighted_metric

        # Check if the best reconciler is the base one
        # If that's the case, log a warning and calculate the second best reconciler
        best_reconciler = min(metrics_methods, key=lambda k: metrics_methods[k])
        if best_reconciler == f'{model_name}'.title():
            logger.warning('None of the reconcilers is better than the base model. Returns the second best reconciler')
            del metrics_methods[best_reconciler]
            interest_columns.pop(interest_columns.index(best_reconciler))
            best_reconciler = min(metrics_methods, key=lambda k: metrics_methods[k])
        # If that's not the case, return the proper index of the reconciler by removing the model_name
        else:
            del metrics_methods[f'{model_name}'.title()]
            interest_columns.pop(interest_columns.index(f'{model_name}'.title()))
        
        return interest_columns.index(best_reconciler), best_reconciler
    else:
        raise ValueError('There are no common indexes between the two dataframes')