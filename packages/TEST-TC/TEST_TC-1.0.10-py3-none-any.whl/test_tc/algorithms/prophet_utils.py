import pandas as pd
import numpy as np
import os
import ast

from ..datahandler.datahandler import DataHandler
from ..utility.tele_logger import logger

def check_prophet_fit_df(input_data):
    """
    Esegue i controlli sull'input fornito per il metodo fit() di Prophet.

    Parameters
    ----------
    input_data
        L'input fornito per il metodo fit() di Prophet.

    Raises
    ------
    ValueError
        Se l'input non è del tipo pd.DataFrame.
    ValueError
        Se il dataframe non ha almeno due colonne.
    ValueError
        Se il dataframe non contiene le colonne 'ds' e 'y'.
    ValueError
        Se la colonna 'ds' non è di tipo datetime.
    ValueError
        Se la colonna 'y' non è di tipo numerico
    """

    # Controllo se l'input è un DataFrame
    if not isinstance(input_data, pd.DataFrame):
        raise ValueError("L'input deve essere un DataFrame.")

    # Controllo se il DataFrame ha almeno due colonne
    if len(input_data.columns) < 2:
        raise ValueError("Il DataFrame deve avere almeno due colonne.")

    if len(input_data) == 0:
        raise ValueError("Il DataFrame è vuoto.")
    
    # Controllo se 'ds' e 'y' sono presenti nel DataFrame
    if 'ds' not in input_data.columns or 'y' not in input_data.columns:
        raise ValueError("Il DataFrame deve contenere le colonne 'ds' e 'y'.")

    # Controllo il tipo delle colonne
    if not pd.core.dtypes.common.is_datetime64_any_dtype(input_data['ds']):
        raise ValueError("La colonna 'ds' deve essere di tipo datetime.")

    if not pd.core.dtypes.common.is_numeric_dtype(input_data['y']):
        raise ValueError("La colonna 'y' deve essere di tipo numerico.")

def check_prophet_predict_df(input_data):
    """
    Esegue i controlli sull'input fornito per il metodo predict() di Prophet.

    Parameters
    ----------
    input_data
        L'input fornito per il metodo predict() di Prophet.

    Raises
    ------
    ValueError
        Se l'input fornito non è del tipo pd.DataFrame
    ValueError
        Se il dataframe non ha almeno una colonna
    ValueError
        Se la colonna 'ds' non è presente nel dataframe
    ValueError
        Se la colonna 'ds' non è del tipo datetime
    """
    # Controllo se l'input è un DataFrame
    if not isinstance(input_data, pd.DataFrame):
        raise ValueError("L'input deve essere un DataFrame.")

    # Controllo se il DataFrame ha almeno una colonna
    if len(input_data.columns) < 1:
        raise ValueError("Il DataFrame deve avere almeno una colonna.")

    if len(input_data) == 0:
        raise ValueError("Il DataFrame è vuoto.")
    
    # Controllo se 'ds' è presente nel DataFrame
    if 'ds' not in input_data.columns:
        raise ValueError("Il DataFrame deve contenere la colonna 'ds'.")
    # Controllo sul tipo della colonna ds
    if not pd.core.dtypes.common.is_datetime64_any_dtype(input_data['ds']):
        raise ValueError("La colonna 'ds' deve essere di tipo datetime.")
    
def check_prophet_save(model, file_path):
    """
    Esegue i controlli sull'input fornito per il metodo save() di Prophet.

    Parameters
    ----------
    model
        fitted prophet model
    file_path: str
        The complete file path where to save the model

    Raises
    ------
    ValueError
        Se il file non ha un' estensione pkl
    ValueError
        Se provi a salvare un modello non addestrato
    ValueError
        Se la cartella di destinazione per il salvataggio non esiste.
    """


    # Controllo sull'estensione del file
    if not file_path.endswith(".pkl"):
        raise ValueError("Il file deve avere un'estensione '.pkl' per il salvataggio del modello.")

    # Controllo se il modello è stato addestrato correttamente
    if not isinstance(model.history, pd.DataFrame):
        raise ValueError("Il modello non è stato addestrato correttamente. Esegui il metodo fit() prima del salvataggio.")

    # Controllo se il percorso del file esiste
    file_dir = os.path.dirname(file_path)
    if file_dir and not os.path.exists(file_dir):
        raise ValueError("La cartella di destinazione per il salvataggio non esiste.")

def check_prophet_load(file_path):
    """
    Esegue i controlli sull'input fornito per il metodo load() di Prophet.

    Parameters
    ----------
    file_path
        Il percorso del file contenente il modello da caricare.
    Raises
    ------
    ValueError
        Se il percorso del file non esiste.
    ValueError
        Se il file che provi a caricare non ha estensione pkl
    """

    # Controllo se il percorso del file esiste
    if not os.path.exists(file_path):
        raise ValueError("Il percorso del file non esiste.")

    # Controllo sull'estensione del file
    if not file_path.endswith(".pkl"):
        raise ValueError("Il file deve avere un'estensione '.pkl' per il caricamento del modello.")

def check_split_input(df, val_size, test_size=None):
    """
    Check the input parameters for split train, validation, test

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe that needs to be split
    val_size:
        Percentage of validation set
    test_size:
        Percentage of test set (optional)
    Raises
    ------
    ValueError
        If the DataFrame is empty.
    ValueError
        If the dataframe does not contain a datetime column.
    ValueError
        If the datetime column is not sorted.
    ValueError
        If val_size is not between 0 and 1.
    ValueError
        If test_size is provided and not between 0 and 1.
    """
    if len(df) == 0:
        raise ValueError("Il DataFrame è vuoto.")

    # Controllo se esiste una colonna di tipo datetime
    datetime_columns = [col for col in df.columns if pd.api.types.is_datetime64_any_dtype(df[col])]
    if len(datetime_columns) == 0:
        raise ValueError("Il dataframe non contiene una colonna di tipo datetime")

    # Controllo se la colonna temporale è ordinata in modo monotono
    for col in datetime_columns:
        if not df[col].is_monotonic_increasing and not df[col].is_monotonic_decreasing:
            raise ValueError(f"La colonna '{col}' non è ordinata in modo monotono")

    if not (val_size > 0):
        raise ValueError("val_size must be greater or equal than 1")

    if test_size is not None and not (test_size > 0):
        raise ValueError("test_size must be greater or equal than 1")

def train_val_test_split(df: pd.DataFrame, val_size: float, test_size: float = None) -> tuple:
    """
    Create train, validation, test dataframes

    Parameters
    ----------
    df: pd.DataFrame
        The dataframe that needs to be split
    train_size: float, optional
        Percentage of training set
    val_size: float, optional
        Percentage of validation set
    test_size: float, optional
        Percentage of test set

    Returns
    -------
        Tuple: (train_set, val_set, test_set)
    """
    # Parameters check
    check_split_input(df = df, val_size = val_size, test_size = test_size)

    total_rows = len(df)

    # Effettua lo split dei dati
    train_set = df.iloc[:-(val_size+test_size)]
    val_set = df.iloc[(total_rows-val_size-test_size):(-1)*test_size]
    test_set = df.iloc[(total_rows-test_size):]

    return train_set, val_set, test_set
    
def preprocess_prophet_output(df: pd.DataFrame, id_pred: str) -> pd.DataFrame:
    """
    The function generates the results table from the Prophet table.
    The results table has columns (Timestamp, Id_pred, Pred_mean, Sigma, Pi_lower_95, Pi_upper_95)

    Parameters
    ----------
    df: pd.DataFrame
        Dataframe representing the Prophet results
    id_pred: str
        String referring to the id_pred (e.g. Lombardia, Lombardia/ASL*)

    Returns
    -------
    pd.DataFrame
        The dataframe in the format (Timestamp, Id_pred, Pred_mean, Sigma, Pi_lower_95, Pi_upper_95)
    """
    preproc_df = df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    preproc_df['Id_pred'] = id_pred
    preproc_df.columns = ['Timestamp', 'Pred_mean', 'Pi_lower_95', 'Pi_upper_95', 'Id_pred']
    preproc_df['Sigma'] = (preproc_df['Pi_upper_95'] - preproc_df['Pi_lower_95']) / (2 * 1.96)
    preproc_df[['Pred_mean', 'Pi_lower_95', 'Pi_upper_95', 'Sigma']] = preproc_df[['Pred_mean', 'Pi_lower_95', 'Pi_upper_95', 'Sigma']].astype(int)
    return preproc_df[['Timestamp', 'Id_pred', 'Pred_mean', 'Sigma', 'Pi_lower_95', 'Pi_upper_95']]

def save_model_results(df: pd.DataFrame, path_to_folder: str, id_pred: str, filename: str = 'output.parquet') -> None:
    """
    Method to save the prophet dataframe

    Parameters
    ----------
    df: pd.DataFrame
    Prophet dataframe that needs to be changed for saving

    path_to_folder: str
        path where to the folder where save the output '.parquet'
    
    filename: str, optional
        filename of the '.parquet' file

    id_pred: str
    String referring to the id_pred (e.g. Lombardia, Lombardia/ASL*)

    Returns
    -------
        None
"""
    DH = DataHandler(path_to_folder)
    try:
        result_df = preprocess_prophet_output(df, id_pred)
    except Exception as e:
        raise ValueError(f"Error occurred during the generation of the output file: {str(e)}. Make sure the dataset is the one resulted from Prophet predict.")
    
    logger.info(' Saving the model result')
    DH.write(result_df, folder='', filename = filename)

def check_preprocess_prophet_input(df, date, target):
    """
    Check the consistency of the dataframe
    Parameters
    ----------
    df
        input dataframe
    date
        date column name to check
    target
        target column name to check

    Returns
    -------
        the two columns ordered by type (datetime, numeric)

    Raises
    ------
    ValueError
        if df is not a dataframe
    ValueError
        if the dataframe has less than two columns
    ValueError
        if col1 and col2 are not dataframe columns
    ValueError
        if the columns are not datetime and numeric
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a DataFrame.")
    
    if len(df) == 0:
        raise ValueError("Il DataFrame è vuoto.")

    if len(df.columns) < 2:
        raise ValueError("DataFrame must have at least two columns.")

    if date not in df.columns or target not in df.columns:
        raise ValueError("Specified columns are not present in the DataFrame.")

    if not pd.api.types.is_datetime64_any_dtype(df[date]):
        raise ValueError(f"The column {date} must have datetime type")
        
    if not pd.api.types.is_numeric_dtype(df[target]):
        raise ValueError(f"The column {target} must have numeric type")

def preprocess_prophet_input(df: pd.DataFrame, date: str, target: str):
    """
    Convert the date column name into 'ds' and the target column name in 'y'

    Parameters
    ----------
    df: pd.DataFrame
        Input DataFrame to check
    date: str
        Name of the date column
    target: str
        Name of the target column

    Returns
    -------
        the processed df
    """
    
    check_preprocess_prophet_input(df = df, date = date, target = target)
    df_ = df.rename(columns={date: 'ds', target: 'y'})
    return df_

def is_not_convertible_to_int_float(string_: str):
    """
    check if the string cannot be converted into float or int

    Parameters
    ----------
    string_
        the string to be parsed

    Returns
    -------
        False if the string cannot be converted, True otherwise
    """
    try:
        ast.literal_eval(string_)
        return False
    except ValueError:
        return True
    except SyntaxError:
        return True
    
def literal_evaluation(values_list: list) -> list:
    """
    The function evaluates the list values for the parameters: 'weekly_seasonality', 'yearly_seasonality'

    Parameters
    ----------
    values_list
        list of strings to be evaluates

    Returns
    -------
        list of evaluated values
    """
    for j in values_list:
        if j not in ['True', 'False'] and is_not_convertible_to_int_float(j):
            raise ValueError(f'The following value {j} is not a valid parameter')
    return [ast.literal_eval(val) for val in values_list]

def generate_values(dictionary, default_step = 0.5):
    """
    The function generates the possible values of the numeric prophet parameters

    Parameters
    ----------
    dictionary
        dictionary formt he config file with min, max and step
    default_step, optional
        the default step used if it's not specified in the config file

    Returns
    -------
        list of possible values

    Raises
    ------
    ValueError
        if the step is greater than the values range
    """

    min_value = dictionary.get('min')
    max_value = dictionary.get('max')
    step = dictionary.get('step')
    if step == 'None':
        step = default_step  # Valore di default dello step

    if not isinstance(min_value, (float, int)) or not isinstance(max_value, (float, int)) or not isinstance(step, (float, int)):
        raise ValueError(f' One of the dtypes of {min_value}, {max_value}, {step} is not valid')
    
    if step == -1 and min_value>0:
        step = min_value  # Utilizza min value come step
    elif step == -1 and min_value==0:
        step = default_step
    elif step > (max_value - min_value):
        raise ValueError(f'The step {step} must be lower than the difference between max {max_value} and min {min_value}')

    values = list(np.arange(min_value,max_value,step))

    # Verifica se il valore massimo è già incluso nella lista
    if max_value not in values:
        values.append(max_value)

    return values

def grid_values_hyperparameters(config_toml: dict) -> dict:
    """
    The function takes as input the dictionary of the config file
    and generates the combination of grid search parameters

    Parameters
    ----------
    config_toml
        the dictionary form the config file

    Returns
    -------
        the grid search parameter dictionary
    """
    grid_parameters = {}
    for param in config_toml.keys():
        if (type(config_toml[param]) == list):
            grid_parameters[param] = literal_evaluation(config_toml[param])

        elif (type(config_toml[param]) == dict):
            if param.lower() == 'changepoint_prior_scale':
                grid_parameters[param] = generate_values(config_toml[param], default_step = 0.1)

            if param.lower() == 'seasonality_prior_scale':
                grid_parameters[param] = generate_values(config_toml[param], default_step = 1.0)
        else:
            raise ValueError(f' The value datetype of {param} is not valid')
    return grid_parameters