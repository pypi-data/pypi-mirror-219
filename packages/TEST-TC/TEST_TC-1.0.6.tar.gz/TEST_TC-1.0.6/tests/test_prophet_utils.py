import pandas as pd
import pytest
import os
from tc_uc4.algorithms.prophet_utils import (check_prophet_fit_df, check_prophet_predict_df,
                                      check_prophet_predict_df, check_prophet_save,
                                      check_prophet_load, check_split_input, train_val_test_split,
                                      save_model_results, preprocess_prophet_output,
                                      check_preprocess_prophet_input, preprocess_prophet_input,
                                      is_not_convertible_to_int_float, literal_evaluation, generate_values,
                                      grid_values_hyperparameters)

### check_prophet_fit_df ###

# Test case for a valid input DataFrame
def test_check_prophet_fit_df_valid_input():
    input_data = pd.DataFrame({'ds': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')],
                              'y': [10, 20]})
    assert check_prophet_fit_df(input_data) is None

# Test case for invalid input (not a DataFrame)
def test_check_prophet_fit_df_invalid_input():
    input_data = 'invalid'
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)

def test_check_prophet_fit_df_empty_dataframe():
    input_data = pd.DataFrame({'ds': []})
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)

# Test case for DataFrame with less than two columns
def test_check_prophet_fit_df_less_than_two_columns():
    input_data = pd.DataFrame({'ds': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')]})
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)

# Test case for DataFrame missing 'ds' column
def test_check_prophet_fit_df_missing_ds_column():
    input_data = pd.DataFrame({'y': [10, 20]})
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)

# Test case for DataFrame missing 'y' column
def test_check_prophet_fit_df_missing_y_column():
    input_data = pd.DataFrame({'ds': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')]})
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)

# Test case for non-datetime 'ds' column
def test_check_prophet_fit_df_non_datetime_ds_column():
    input_data = pd.DataFrame({'ds': ['2023-01-01', '2023-01-02'],
                              'y': [10, 20]})
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)

# Test case for non-numeric 'y' column
def test_check_prophet_fit_df_non_numeric_y_column():
    input_data = pd.DataFrame({'ds': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')],
                              'y': ['10', '20']})
    with pytest.raises(ValueError):
        check_prophet_fit_df(input_data)



### check_prophet_predict_df ###

# Test case for a valid input DataFrame
def test_check_prophet_predict_df_valid_input():
    input_data = pd.DataFrame({'ds': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')]})
    assert check_prophet_predict_df(input_data) is None

# Test case for invalid input (not a DataFrame)
def test_check_prophet_predict_df_invalid_input():
    input_data = 'invalid'
    with pytest.raises(ValueError):
        check_prophet_predict_df(input_data)

# Test case for DataFrame with no columns
def test_check_prophet_predict_df_no_columns():
    input_data = pd.DataFrame()
    with pytest.raises(ValueError):
        check_prophet_predict_df(input_data)

# Test case for an empty DataFrame
def test_check_prophet_predict_df_empty_dataframe():
    input_data = pd.DataFrame({'ds': []})
    with pytest.raises(ValueError):
        check_prophet_predict_df(input_data)

# Test case for DataFrame missing 'ds' column
def test_check_prophet_predict_df_missing_ds_column():
    input_data = pd.DataFrame({'y': [10, 20]})
    with pytest.raises(ValueError):
        check_prophet_predict_df(input_data)

# Test case for non-datetime 'ds' column
def test_check_prophet_predict_df_non_datetime_ds_column():
    input_data = pd.DataFrame({'ds': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')]})
    input_data['ds'] = pd.to_numeric(input_data['ds'])
    with pytest.raises(ValueError):
        check_prophet_predict_df(input_data)


### check_prophet_save ###

class DummyModel:
    def __init__(self, history):
        if history:
            history = pd.DataFrame()
        else:
            history = 'Not valid history'

        self.history = history

# Test case for a valid model and file path
def test_check_prophet_save_valid_input(tmpdir):
    model = DummyModel(history=True)
    file_path = os.path.join(tmpdir, 'model.pkl')
    assert check_prophet_save(model, file_path) is None

# Test case for invalid file extension
def test_check_prophet_save_invalid_file_extension(tmpdir):
    model = DummyModel(history=True)
    file_path = os.path.join(tmpdir, 'model.txt')
    with pytest.raises(ValueError):
        check_prophet_save(model, file_path)

# Test case for saving an untrained model
def test_check_prophet_save_untrained_model(tmpdir):
    model = DummyModel(history=False)
    file_path = os.path.join(tmpdir, 'model.pkl')
    with pytest.raises(ValueError):
        check_prophet_save(model, file_path)

# Test case for non-existent directory
def test_check_prophet_save_nonexistent_directory(tmpdir):
    model = DummyModel(history=True)
    file_path = os.path.join(tmpdir, 'subdir/model.pkl')
    with pytest.raises(ValueError):
        check_prophet_save(model, file_path)


### check_prophet_load ###

# Test case for a valid file path
def test_check_prophet_load_valid_input(tmpdir):
    file_path = os.path.join(tmpdir, 'model.pkl')
    open(file_path, 'a').close()  # Create an empty file
    assert check_prophet_load(file_path) is None

# Test case for non-existent file path
def test_check_prophet_load_nonexistent_file(tmpdir):
    file_path = os.path.join(tmpdir, 'nonexistent.pkl')
    with pytest.raises(ValueError):
        check_prophet_load(file_path)

# Test case for invalid file extension
def test_check_prophet_load_invalid_file_extension(tmpdir):
    file_path = os.path.join(tmpdir, 'model.txt')
    open(file_path, 'a').close()  # Create an empty file
    with pytest.raises(ValueError):
        check_prophet_load(file_path)


### check_split_input ###

# Test case for a valid input DataFrame and validation size
def test_check_split_input_valid_input():
    df = pd.DataFrame({'datetime': pd.date_range(start='2022-01-01', periods=5)})
    val_size = 0.2
    assert check_split_input(df, val_size) is None

# Test case for an empty DataFrame
def test_check_split_input_empty_dataframe():
    df = pd.DataFrame()
    val_size = 0.2
    with pytest.raises(ValueError):
        check_split_input(df, val_size)

# Test case for DataFrame missing datetime column
def test_check_split_input_missing_datetime_column():
    df = pd.DataFrame({'col1': [1, 2, 3]})
    val_size = 0.2
    with pytest.raises(ValueError):
        check_split_input(df, val_size)

# Test case for non-monotonic datetime column
def test_check_split_input_non_monotonic_datetime_column():
    df =pd.DataFrame({'datetime': [pd.Timestamp('2022-01-01'), pd.Timestamp('2021-01-03'), pd.Timestamp('2021-01-05'),
                                    pd.Timestamp('2021-01-03'), pd.Timestamp('2021-01-01')]})
    val_size = 0.2
    with pytest.raises(ValueError):
        check_split_input(df, val_size)

# Test case for invalid validation size
def test_check_split_input_invalid_val_size():
    df = pd.DataFrame({'datetime': pd.date_range(start='2022-01-01', periods=5)})
    val_size = -0.2
    with pytest.raises(ValueError):
        check_split_input(df, val_size)

# Test case for invalid test size
def test_check_split_input_invalid_test_size():
    df = pd.DataFrame({'datetime': pd.date_range(start='2022-01-01', periods=5)})
    val_size = 0.2
    test_size = 1.5
    with pytest.raises(ValueError):
        check_split_input(df, val_size, test_size)


### train_val_test_split ###

@pytest.fixture
def example_df_split():
    return pd.DataFrame({'datetime': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']), 'col1': [1, 2, 3, 4, 5]})

# Test case for a valid input DataFrame and validation size
def test_train_val_test_split_valid_input(example_df_split):
    # df = pd.DataFrame({'datetime': [pd.Timestamp('2022-01-01'), pd.Timestamp('2022-01-02'), pd.Timestamp('2022-01-03'),
    #                                 pd.Timestamp('2022-01-04'), pd.Timestamp('2022-01-05')], 'col1': [1, 2, 3, 4, 5]})
    val_size = 0.2
    test_size = 0.1
    train_set, val_set, test_set = train_val_test_split(example_df_split, val_size, test_size)
    
    assert len(train_set) == 3
    assert len(val_set) == 1
    assert len(test_set) == 1

# Test case for a valid input DataFrame and validation size only
def test_train_val_test_split_valid_input_without_test_size(example_df_split):
    # df = pd.DataFrame({'datetime': [pd.Timestamp('2022-01-01'), pd.Timestamp('2022-01-02'), pd.Timestamp('2022-01-03'),
    #                                 pd.Timestamp('2022-01-04'), pd.Timestamp('2022-01-05')],'col1': [1, 2, 3, 4, 5]})
    val_size = 0.2
    train_set, val_set = train_val_test_split(example_df_split, val_size)
    
    assert len(train_set) == 4
    assert len(val_set) == 1

# Test case for invalid validation size
def test_train_val_test_split_invalid_val_size(example_df_split):
    # df = pd.DataFrame({'datetime': [pd.Timestamp('2022-01-01'), pd.Timestamp('2022-01-02'), pd.Timestamp('2022-01-03'),
    #                                 pd.Timestamp('2022-01-04'), pd.Timestamp('2022-01-05')],'col1': [1, 2, 3, 4, 5]})
    val_size = -0.2
    test_size = 0.1
    with pytest.raises(ValueError):
        train_val_test_split(example_df_split, val_size, test_size)

# Test case for invalid test size
def test_train_val_test_split_invalid_test_size(example_df_split):
    # df = pd.DataFrame({'datetime': [pd.Timestamp('2022-01-01'), pd.Timestamp('2022-01-02'), pd.Timestamp('2022-01-03'),
    #                                 pd.Timestamp('2022-01-04'), pd.Timestamp('2022-01-05')],'col1': [1, 2, 3, 4, 5]})
    val_size = 0.2
    test_size = 1.5
    with pytest.raises(ValueError):
        train_val_test_split(example_df_split, val_size, test_size)


### save_model_results, preprocess_prophet_output ###

@pytest.fixture
def example_df_output():
    return pd.DataFrame({
        'ds':  pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'yhat': [10.5, 11.2, 9.8],
        'yhat_lower': [9.5, 10.8, 9.0],
        'yhat_upper': [11.5, 11.6, 10.5]
    })

def test_preprocess_prophet_output(example_df_output):
    id_pred = 'Lombardia'
    expected_output = pd.DataFrame({
        'Timestamp': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'Id_pred': ['Lombardia', 'Lombardia', 'Lombardia'],
        'Pred_mean': [10, 11, 9],
        'Sigma': [1, 0, 0],
        'Pi_lower_95': [9, 10, 9],
        'Pi_upper_95': [11, 11, 10]
    })

    output = preprocess_prophet_output(example_df_output, id_pred)
    pd.testing.assert_frame_equal(output, expected_output)

def test_save_model_results(example_df_output, tmp_path):
    path = str(tmp_path)
    id_pred = 'Lombardia'
    save_model_results(example_df_output, path, id_pred, 'TEST.parquet')

    assert 'TEST.parquet' in os.listdir(str(tmp_path))


### check_preprocess_prophet_input, preprocess_prophet_input ###

@pytest.fixture
def example_df_input():
    return pd.DataFrame({
        'Timestamp': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'Target': [10.5, 11.2, 9.8]
    })

def test_check_preprocess_prophet_input_invalid_dataframe():
    with pytest.raises(ValueError, match="Input is not a DataFrame."):
        check_preprocess_prophet_input('not_a_dataframe', 'Timestamp', 'Target')

def test_check_preprocess_prophet_input_invalid_empty_dataframe():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="Il DataFrame è vuoto."):
        check_preprocess_prophet_input(empty_df, 'Timestamp', 'Target')

def test_check_preprocess_prophet_input_invalid_less_than_two_columns():
    df = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-01'])})
    with pytest.raises(ValueError, match="DataFrame must have at least two columns."):
        check_preprocess_prophet_input(df, 'Timestamp', 'Target')

def test_check_preprocess_prophet_input_invalid_missing_columns():
    df = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']), 'z': [10.5, 11.2, 9.8]})
    with pytest.raises(ValueError, match="Specified columns are not present in the DataFrame."):
        check_preprocess_prophet_input(df, 'Timestamp', 'Target')

def test_check_preprocess_prophet_input_invalid_inconsistent_columns():
    df = pd.DataFrame({'Timestamp': [1, 2, 3], 'Target': [10.5, 11.2, 9.8]})
    with pytest.raises(ValueError, match="The column Timestamp must have datetime type"):
        check_preprocess_prophet_input(df, 'Timestamp', 'Target')
    
    df = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']), 'Target': ['A', 'B', 'C']})
    with pytest.raises(ValueError, match="The column Target must have numeric type"):
        check_preprocess_prophet_input(df, 'Timestamp', 'Target')

def test_preprocess_prophet_input(example_df_input, capsys):
    processed_df = preprocess_prophet_input(example_df_input, 'Timestamp', 'Target')
    captured = capsys.readouterr()
    assert captured.out == ""

    expected_df = pd.DataFrame({
        'ds': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'y': [10.5, 11.2, 9.8]
    })
    pd.testing.assert_frame_equal(processed_df, expected_df)

def test_preprocess_prophet_input_invalid(example_df_input):
    with pytest.raises(ValueError, match="Specified columns are not present in the DataFrame."):
        preprocess_prophet_input(example_df_input, 'invalid_date', 'invalid_target')

    processed_df = preprocess_prophet_input(example_df_input, 'Timestamp', 'Target')
    expected_df = pd.DataFrame({
        'ds': pd.to_datetime(['2023-06-01', '2023-06-02', '2023-06-03']),
        'y': [10.5, 11.2, 9.8]
    })
    pd.testing.assert_frame_equal(processed_df, expected_df)


### is_not_convertible_to_int_float ###

def test_is_not_convertible_to_int_float():
    assert is_not_convertible_to_int_float("abc") == True
    assert is_not_convertible_to_int_float("1.23.4") == True
    assert is_not_convertible_to_int_float("123") == False
    assert is_not_convertible_to_int_float("1.23") == False


### literal_evaluation ###

def test_literal_evaluation():
    values_list = ['True', 'False', '123', '12.3']
    assert literal_evaluation(values_list) == [True, False, 123, 12.3]

    values_list = ['True', 'False', '1.23', 'abc']
    with pytest.raises(ValueError):
        literal_evaluation(values_list)


### generate_values ###

def test_generate_values():
    dictionary = {'min': 0, 'max': 5, 'step': 1}
    assert generate_values(dictionary) == [0, 1, 2, 3, 4, 5]

    dictionary = {'min': 0, 'max': 5, 'step': 0.5}
    assert generate_values(dictionary) == [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    # min is 0 so i get the default_step
    dictionary = {'min': 0, 'max': 5, 'step': -1}
    assert generate_values(dictionary) == [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    # min is not 0 so i get the min as step
    dictionary = {'min': 1, 'max': 5, 'step': -1}
    assert generate_values(dictionary) == [1, 2, 3, 4, 5]

    dictionary = {'min': 0, 'max': 5, 'step': 10}
    with pytest.raises(ValueError):
        generate_values(dictionary)


### grid_values_hyperparameters ###

def test_grid_values_hyperparameters():
    config_toml = {
        'param1': ['True', 'False'],
        'changepoint_prior_scale': {'min': 0, 'max': 5, 'step': 1},
        'seasonality_prior_scale': {'min': 0, 'max': 5, 'step': 0.5}
    }
    expected_result = {
        'param1': [True, False],
        'changepoint_prior_scale': [0, 1, 2, 3, 4, 5],
        'seasonality_prior_scale': [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    }
    assert grid_values_hyperparameters(config_toml) == expected_result

    config_toml = {
        'param1': ['True', 'False'],
        'changepoint_prior_scale': {'min': 0, 'max': 5, 'step': 10},
        'seasonality_prior_scale': {'min': 0, 'max': 5, 'step': 0.1}
    }
    with pytest.raises(ValueError):
        grid_values_hyperparameters(config_toml)
