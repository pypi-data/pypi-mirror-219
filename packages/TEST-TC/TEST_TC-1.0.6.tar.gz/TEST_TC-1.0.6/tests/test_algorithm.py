import pytest
import pandas as pd
from tc_uc4.algorithms.algorithm import prophet_tuning, Prophet_model

### prophet_tuning ###

@pytest.fixture
def example_train_df():
    return pd.DataFrame({
        'ds': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'y': [10.5, 11.2, 9.8]
    })

@pytest.fixture
def example_validation_df():
    return pd.DataFrame({
        'ds': pd.to_datetime(['2023-06-04', '2023-06-05', '2023-06-06']),
        'y': [9.7, 11.0, 10.2]
    })

def test_prophet_tuning_valid(example_train_df, example_validation_df):
    param_grid = {
        'changepoint_prior_scale': [0.01],
        'seasonality_prior_scale': [0.5]
    }
    best_params = prophet_tuning(param_grid, example_train_df, example_validation_df)
    assert best_params == {'changepoint_prior_scale': 0.01, 'seasonality_prior_scale': 0.5}

def test_prophet_tuning_empty_validation_df(example_train_df):
    param_grid = {
        'changepoint_prior_scale': [0.01, 0.1, 0.5],
        'seasonality_prior_scale': [0.5, 5, 10]
    }
    empty_validation_df = pd.DataFrame(columns=['ds', 'y'])
    with pytest.raises(ValueError, match="Il dataframe di convalida con la rimozione dei valori nulli, è vuoto"):
        prophet_tuning(param_grid, example_train_df, empty_validation_df)


### Prophet_model ###

@pytest.fixture
def example_df_model():
    return pd.DataFrame({
        'ds': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'y': [10.5, 11.2, 9.8]
    })

def test_prophet_model_fit(example_df_model):
    model = Prophet_model()
    model.fit(example_df_model)
    assert model.df.equals(example_df_model)

def test_prophet_model_predict(example_df_model):
    model = Prophet_model()
    model.fit(example_df_model)
    future_df = model.future_dataset()
    predictions = model.predict(future_df)
    assert isinstance(future_df, pd.DataFrame)
    assert isinstance(predictions, pd.DataFrame)

def test_prophet_model_save_load(tmp_path, example_df_model):
    model = Prophet_model()
    model.fit(example_df_model)

    # Save the model
    save_path = tmp_path / "model.pkl"
    model.save(str(save_path))

    # Load the model
    loaded_model = Prophet_model.load(str(save_path))

    assert isinstance(loaded_model, Prophet_model)
    assert loaded_model.model is not None
    pd.testing.assert_frame_equal(loaded_model.model.history, model.model.history)
