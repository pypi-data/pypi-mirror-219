import pandas as pd
import numpy as np
import pytest
from tc_uc4.datapreparation.datapreparation_utils import (PreprocessingTeleconsulto, code_to_name, Normalizer,
                                                          ReplacerNA, Detrender, Deseasoner, Differencer)
from tc_uc4.utility.exceptions import InputTypeError
from statsmodels.tsa.seasonal import seasonal_decompose


### PreprocessingTeleconsulto ###

@pytest.fixture
def sample_df():
    data = {
        'data_richiesta': pd.date_range(start='2022-01-01', end='2022-01-10'),
        'id_teleconsulto': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return pd.DataFrame(data)


def test_prophet(sample_df):
    preprocessing = PreprocessingTeleconsulto()

    # Test with default time_granularity
    expected_result = pd.DataFrame({
        'Timestamp': pd.date_range(start='2022-01-01', end='2022-01-10'),
        'Target': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    })
    result = preprocessing.prophet(sample_df, time_granularity="D")
    assert result.equals(expected_result)

    # Test with custom time_granularity
    expected_result = pd.DataFrame({
        'Timestamp': pd.date_range(start='2022-01-01', end='2022-01-10', freq='12H'),
        'Target': [1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0, np.nan, 1.0]
    })
    result = preprocessing.prophet(sample_df, time_granularity="12H")
    assert result.equals(expected_result)

    # Test with invalid input type
    with pytest.raises(InputTypeError):
        preprocessing.prophet("invalid_dataframe")

    # Test with invalid datetime_index
    with pytest.raises(InputTypeError):
        preprocessing.prophet(sample_df.rename(columns={'data_richiesta': 'invalid_index'}))

    # Test with invalid target
    with pytest.raises(InputTypeError):
        preprocessing.prophet(sample_df.rename(columns={'id_teleconsulto': 'invalid_target'}))


### code_to_name ###

# Test case for valid input
def test_code_to_name_valid_input():
    # Create a sample pd.Series and mapping dictionary for testing
    cod = pd.Series([1, 2, 3, 4, 5])
    convers_dict = {1: "Apple", 2: "Banana", 3: "Orange", 4: "Grape", 5: "Mango"}
    # Call the code_to_name function
    result = code_to_name(cod, convers_dict)
    assert isinstance(result, pd.Series) #the result should be a Series

    expected_result = pd.Series(["Apple", "Banana", "Orange", "Grape", "Mango"])
    pd.testing.assert_series_equal(result, expected_result) #the result should has the correct value

# Test case for invalid input
def test_code_to_name_invalid_input():
    # Create an invalid input (not a pd.Series)
    invalid_cod = [1, 2, 3, 4, 5]
    convers_dict = {1: "Apple", 2: "Banana", 3: "Orange", 4: "Grape", 5: "Mango"}
    # Test for InputTypeError when invalid input is provided for cod
    with pytest.raises(InputTypeError):
        code_to_name(invalid_cod, convers_dict)

    # Create an invalid input (not a dict)
    cod = pd.Series([1, 2, 3, 4, 5])
    invalid_convers_dict = [1, 2, 3, 4, 5]
    # Test for InputTypeError when invalid input is provided for convers_dict
    with pytest.raises(InputTypeError):
        code_to_name(cod, invalid_convers_dict)


### Normalizer ###

@pytest.fixture
def example_data():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_fit_normalizer(example_data):
    # Create an instance of the Normalizer class
    normalizer = Normalizer()

    # Call the fit method with the example data
    fitted_normalizer = normalizer.fit(example_data)

    # Verify that the output is the same instance of normalizer
    assert fitted_normalizer is normalizer

    # Verify that the min and max values are calculated correctly
    assert normalizer.min == 10
    assert normalizer.max == 50

def test_transform_normalizer(example_data):
    # Create an instance of the Normalizer class
    normalizer = Normalizer()

    # Call the fit method with the example data
    normalizer.fit(example_data)

    # Call the transform method with the example data
    transformed_data = normalizer.transform(example_data)
    print(transformed_data)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the DataFrame has the correct columns
    assert transformed_data.columns.tolist() == ['timestamp', 'volumes']

    # Verify that the data is correctly normalized
    assert transformed_data['volumes'].min() == 0
    assert transformed_data['volumes'].max() == 1

    # Verify that the data has not been modified in other ways
    assert example_data['timestamp'].equals(transformed_data['timestamp'])


### ReplacerNA ###

#transform function
@pytest.fixture
def example_data_transform():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, None, 30, None, 50]})
    return data

def test_fit_replace_na(example_data_transform):
    # Create an instance of the ReplacerNA class with method="mean"
    replacer = ReplacerNA(method="mean")

    # Call the fit method with the example data
    fitted_replacer = replacer.fit(example_data_transform)

    # Verify that the output is the same instance of replacer
    assert fitted_replacer is replacer

    # Verify that the value and method_for_df are calculated correctly
    assert replacer.value == 30.0
    assert replacer.method_for_df is None

def test_transform_replace_na(example_data_transform):
    # Create an instance of the ReplacerNA class with method="zero"
    replacer = ReplacerNA(method="zero")

    # Call the fit method with the example data
    replacer.fit(example_data_transform)

    # Call the transform method with the example data
    transformed_data = replacer.transform(example_data_transform)
    print(transformed_data)
    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data has missing values replaced correctly
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': [10.0, 0.0, 30.0, 0.0, 50.0]})
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_transform__replace_na_ffill(example_data_transform):
    # Create an instance of the ReplacerNA class with method="ffill"
    replacer = ReplacerNA(method="ffill")

    # Call the fit method with the example data
    replacer.fit(example_data_transform)

    # Call the transform method with the example data
    transformed_data = replacer.transform(example_data_transform)

    # Verify that the transformed data has missing values replaced correctly using forward fill
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': [10.0, 10.0, 30.0, 30.0, 50.0]})
    pd.testing.assert_frame_equal(transformed_data, expected_data)


### Detrender ###

#trend function
@pytest.fixture
def example_data_trend():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_fit_detrender(example_data_trend):
    # Create an instance of the Detrender class with period=2
    detrender = Detrender(period=2)

    # Call the fit method with the example data
    fitted_detrender = detrender.fit(example_data_trend)

    # Verify that the output is the same instance of detrender
    assert fitted_detrender is detrender

    # Verify that the trend is calculated correctly
    expected_trend = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], name='trend')
    pd.testing.assert_series_equal(detrender.trend, expected_trend)

def test_transform_detrender(example_data_trend):
    # Create an instance of the Detrender class with period=2
    detrender = Detrender(period=2)

    # Call the fit method with the example data
    detrender.fit(example_data_trend)

    # Call the transform method with the example data
    transformed_data = detrender.transform(example_data_trend)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data is detrended correctly
    expected_trend = seasonal_decompose(example_data_trend['volumes'], model='additive', period=2, extrapolate_trend='freq').trend
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': example_data_trend['volumes'] - expected_trend})
    pd.testing.assert_frame_equal(transformed_data, expected_data)


### Deseasoner ###

#season function
@pytest.fixture
def example_data_season():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_transform_deseasoner(example_data_season):
    # Create an instance of the Deseasoner class with period=2
    deseasoner = Deseasoner(period=2)

    # Call the fit method with the example data
    deseasoner.fit(example_data_season)

    # Call the transform method with the example data
    transformed_data = deseasoner.transform(example_data_season)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data is deseasonalized correctly
    expected_seasonal = seasonal_decompose(example_data_season['volumes'], model='additive', period=2, extrapolate_trend='freq').seasonal
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': example_data_season['volumes'] - expected_seasonal})
    pd.testing.assert_frame_equal(transformed_data, expected_data)


### Differencer ###

#difference function
@pytest.fixture
def example_data_difference():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_transform_differencer(example_data_difference):
    # Create an instance of the Differencer class with lag=1
    differencer = Differencer(lag=1)

    # Call the fit method with the example data
    differencer.fit(example_data_difference)

    # Call the transform method with the example data
    transformed_data = differencer.transform(example_data_difference)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data is differenced correctly
    expected_data = pd.DataFrame({'timestamp': [2, 3, 4, 5],
                                  'volumes': [10, 10, 10, 10]})
    pd.testing.assert_frame_equal(transformed_data, expected_data)
