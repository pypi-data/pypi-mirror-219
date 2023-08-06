import pandas as pd
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from typing import Any, Dict
from prophet import Prophet
from sklearn.utils.estimator_checks import check_transformer_general
from tc_uc4.algorithms.experiment_model import preprocess_and_split_df, PreprocessingClass, ExperimentModel, Prophet_model
from tc_uc4.datapreparation.prep import PreprocessingClass


@pytest.fixture
def sample_df():
    data = {
        'data_richiesta': pd.date_range(start='2022-01-01', end='2022-01-10'),
        'id_teleconsulto': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return pd.DataFrame(data)


### preprocess_and_split_df ###

def test_preprocess_and_split_df(sample_df):
    preprocessor = PreprocessingClass(usecase="teleconsulto", model="prophet")
    time_granularity = "D"
    val_size = 0.2
    test_size = 0.1

    # Test preprocess_and_split_df function
    result = preprocess_and_split_df(preprocessor, sample_df, time_granularity, val_size, test_size)

    # Check the returned tuple
    assert isinstance(result, tuple)
    assert len(result) == 4
    df_preproc, df_train, df_val, df_test = result

    # Check DataFrame types
    assert isinstance(df_preproc, pd.DataFrame)
    assert isinstance(df_train, pd.DataFrame)
    assert isinstance(df_val, pd.DataFrame)
    assert isinstance(df_test, pd.DataFrame)

    # Check DataFrame shapes
    assert df_preproc.shape == (10, 2)
    assert df_train.shape == (7, 2)
    assert df_val.shape == (2, 2)
    assert df_test.shape == (1, 2)


# def test_transformer_checks():
#     preprocessor = PreprocessingClass(usecase="teleconsulto", model="prophet")
#     check_transformer_general(preprocessor, enforce_estimator_tags=True)


### ExperimentModel ###

@pytest.fixture
def experiment_model():
    preprocessor = PreprocessingClass()
    return ExperimentModel(preprocessor)


def test_experiment_model(experiment_model):
    df = pd.DataFrame({
        'data_richiesta': pd.date_range(start='2023-01-01', end='2023-01-31'),
        'id_teleconsulto': [i for i in range(31)]
    })
    dict_id_pred_queries = {'id1': 'index>16', 'id2': 'index<15'}
    hyperparameters = {'weekly_seasonality':[True], 'yearly_seasonality':[True]}
    time_granularity = 'D'
    val_size = 0.2
    test_size = 0.1
    max_na_ratio = 0.5

    experiment_model.fit(
        df,
        dict_id_pred_queries,
        hyperparameters,
        time_granularity,
        val_size,
        test_size,
        max_na_ratio
    )

    assert len(experiment_model.models_dict) == 2 # Number of dataframes from dict_id_pred_queries

    # test create_hyperparameters_table

    result = experiment_model.create_hyperparameters_table(hyperparameters)

    assert len(result) == 2 # number of dataframes from dict_id_pred_queries
    assert 'id1' in result # key number 1 from dict_id_pred_queries
    assert 'id2' in result # key number 2 from dict_id_pred_queries
    # params ffrom models
    assert result['id1'] == {'weekly_seasonality':True, 'yearly_seasonality':True} # params for model from id1
    assert result['id2'] == {'weekly_seasonality':True, 'yearly_seasonality':True} # params for model from id2


    #test predict
    result = experiment_model.predict(
        df,
        dict_id_pred_queries,
        time_granularity,
        val_size,
        test_size
    )

    assert len(result) == 5 # len of the two test sets (3+2)
    assert result['Id_pred'].nunique() == 2 # number of dataframes (id1 and id2)

    # test evaluate

    result = experiment_model.evaluate(
        df,
        dict_id_pred_queries,
        time_granularity,
        val_size,
        test_size
    )

    assert len(result) == 2 # number of dataframes (id1 and id2)
    assert result.shape == (2,7)
    assert 'id1' in result['Id_pred'].unique()
    assert list(result.columns) == ['Id_pred', 'MAE', 'MAPE', 'RMSE', 'MSE', 'R2', 'Percentage Coverage']
    