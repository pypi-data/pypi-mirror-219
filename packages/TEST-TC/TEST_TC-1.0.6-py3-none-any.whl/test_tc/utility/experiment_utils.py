import numpy as np
import pandas as pd
import os
import shutil

from .constants import code_to_region_name, code_to_speciality
from ..datapreparation.datapreparation_utils import logger

from ..algorithms.prophet_utils import train_val_test_split
from ..datapreparation.prep import PreprocessingClass
from ..datahandler.datahandler import DataHandler


def add_mapped_columns(
    hierarchy: dict[str, str], df: pd.DataFrame, conversion: dict[str, str]
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Adds columns in the dataframe "df" according to a given hierarchy and conversion dictionary.

    Parameters
    ----------
    hierarchy : dict[str, str]
        A dictionary mapping levels to column names in the DataFrame.
    df : pd.DataFrame
        The input DataFrame to be mapped.
    conversion : dict[str, str]
        A dictionary mapping levels to conversion names.

    Returns
    -------
    tuple[pd.DataFrame, dict[str, str]]
        A tuple containing the modified DataFrame and the updated hierarchy dictionary.
    """
    for conversion_level in conversion.keys():
        if conversion[conversion_level]:
            name_column = hierarchy[conversion_level]
            dict_mapping = eval(conversion[conversion_level])
            df[name_column] = df[name_column].apply(
                lambda x: dict_mapping[x]
            )
            # hierarchy[conversion_level] = name_column
    return df #, hierarchy


def generate_queries(hierarchy_values: list[str], df: pd.DataFrame) -> dict[str, str]:
    """Generate a dictionary of ids and queries based on the given hierarchy values and DataFrame.

    Parameters
    ----------
    hierarchy_values : list[str]
        A list of hierarchy levels in the DataFrame.
    df : pd.DataFrame
        The DataFrame containing the data.


    Returns
    -------
    dict[str, str]
        Dictionary where the keys are unique identifiers and the values are queries.
    """
    dictionary = {}
    for n in range(1, len(hierarchy_values) + 1):
        df_aggregate = df.loc[:, hierarchy_values[:n]].drop_duplicates()
        for i in df_aggregate.itertuples(index=False):
            query = str(i)[6:].replace("=", "==").replace(",", " &")
            id_pred = "/".join([f"{i[j]}" for j in range(len(i))])
            dictionary[id_pred] = query
    return dictionary


def create_zero_dataframe(columns: list[str], n_rows: int) -> pd.DataFrame:
    """Creates a dataframe with the given columns and rows full of zeros.

    Parameters
    ----------
    columns : list[str]
        column names
    n_rows : int
        Number of rows

    Returns
    -------
    pd.DataFrame
        dataframe
    """
    # Create a dictionary with the column names and values
    data = {col: np.zeros(n_rows) for col in columns}

    # Create the dataframe
    df = pd.DataFrame(data)

    return df


def check_val_test_size(val_size: int, test_size: int):
    """Check the validation and test sizes to ensure they meet the minimum requirement.

    Parameters
    ----------
    val_size : int
        The size of the validation set.
    test_size : int
        The size of the test set.
    """
    if val_size == 0 or test_size == 0:
        logger.info(
            f"Be aware that either validation size {val_size} or test size {test_size} is equal to 0"
        )
    
    if test_size >= val_size:
         logger.error(f'Validation Set size MUST be greater than Test Size. Inputs given were: Validation Size -> {val_size} / Test Size -> {test_size}')
         raise ValueError(f'Validation Set size MUST be greater than Test Size. Inputs given were: Validation Size -> {val_size} / Test Size -> {test_size}')


def get_prophetexperiment_datasets(df: pd.DataFrame, dict_id_pred_queries: dict[str, str],
                                   preprocessor: PreprocessingClass,
                                   preprocessing_dict: dict
                                #    , time_granularity: str,
                                #    date_col: str
                                   ) -> dict:
    """
    _summary_

    Parameters
    ----------
    df
        _description_
    dict_id_pred_queries
        _description_
    preprocessor
        _description_
    preproc_details
        _description_

    Returns
    -------
        _description_
    """
    dict_preprocessed_df = {} 
    for id_pred, query in dict_id_pred_queries.items():
            filtered_df = df.query(query)
            filtered_df = filtered_df.reset_index(drop = True)
            filtered_df = allign_dates(filtered_df, preprocessing_dict['date_col'], df)
            full_df = preprocessor.fit_transform(filtered_df, **preprocessing_dict)
            dict_preprocessed_df[id_pred] = full_df
    return dict_preprocessed_df


def split_prophetexperiment_datasets(dict_preprocessed_df: dict, val_size: float, test_size: float = None) -> dict:
    """
    _summary_

    Parameters
    ----------
    dict_preprocessed_df
        _description_
    val_size
        _description_
    test_size, optional
        _description_, by default None

    Returns
    -------
        _description_
    """
    df_train_dict, df_val_dict, df_test_dict = {}, {}, {}
    for id_pred, dataset in dict_preprocessed_df.items():
        df_train, df_val, df_test = train_val_test_split(dataset, val_size, test_size)
        df_train_dict[id_pred] = df_train
        df_val_dict[id_pred] = df_val
        df_test_dict[id_pred] = df_test
    return {'train_dict': df_train_dict, 'val_dict' : df_val_dict, 'test_dict' : df_test_dict}


def allign_dates(filtered_df : pd.DataFrame, date_col: str, df: pd.DataFrame) -> pd.DataFrame:
    num = filtered_df.dtypes[filtered_df.dtypes.isin([int, float])].index
    obj = filtered_df.dtypes[filtered_df.dtypes == object].index
    max = df[date_col].max()
    min = df[date_col].min()
    if max not in filtered_df[date_col].values:
        new_line = len(filtered_df) # 0 based
        filtered_df.loc[new_line, num] = 0
        filtered_df.loc[new_line, obj] = filtered_df.loc[new_line-1, obj]
        filtered_df.loc[new_line, date_col] = max

    if min not in filtered_df[date_col].values:
        new_line = len(filtered_df) # 0 based
        filtered_df.loc[new_line, num] = 0
        filtered_df.loc[new_line, obj] = filtered_df.loc[new_line-1, obj]
        filtered_df.loc[new_line, date_col] = min
        filtered_df = filtered_df.sort_values(date_col).reset_index(drop = True)

    return filtered_df


def write_dataframes_locally(filenames_list, dataframes_list, save_data_folder):
            os.makedirs(save_data_folder, exist_ok=True)
            DH = DataHandler(data_folder = save_data_folder)
            for index in range(len(filenames_list)):
                DH.write(dataframes_list[index], filename = filenames_list[index], folder = '')
        
def remove_dataframe_locally(folder_to_remove):
     shutil.rmtree(folder_to_remove)