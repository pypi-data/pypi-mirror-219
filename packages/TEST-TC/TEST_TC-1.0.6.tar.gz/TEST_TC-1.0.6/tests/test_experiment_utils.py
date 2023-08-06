import pandas as pd
import pytest
from tc_uc4.utility.experiment_utils import add_mapped_columns, generate_queries, create_zero_dataframe
from tc_uc4.utility.constants import code_to_region_name, code_to_speciality


@pytest.fixture
def sample_df():
    data = {
        'col1': ['A', 'A', 'B', 'B'],
        'col2': [30, 190, 50, 80],
        'Value': [1, 2, 3, 4]
    }
    return pd.DataFrame(data)


### add_mapped_columns ###

def test_add_mapped_columns(sample_df):
    hierarchy = {'Level1': 'col1', 'Level2': 'col2'}
    conversion = {'Level1': '', 'Level2': 'code_to_region_name'}
    expected_hierarchy = {'Level1': 'col1', 'Level2': 'col2_mapped'}
    expected_df = pd.DataFrame({
        'col1': ['A', 'A', 'B', 'B'],
        'col2': [30, 190, 50, 80],
        'Value': [1, 2, 3, 4],
        'col2_mapped': ['Lombardia', 'Sicilia', 'Veneto', 'Emilia-Romagna']
    })

    new_df, new_hierarchy = add_mapped_columns(hierarchy, sample_df, conversion)

    pd.testing.assert_frame_equal(new_df, expected_df)
    assert new_hierarchy == expected_hierarchy


### generate_queries ###

def test_generate_queries(sample_df):
    hierarchy_values = ['col1', 'col2']
    expected_dictionary = {
        'A': "(col1=='A')",
        'B': "(col1=='B')",
        'A/30': "(col1=='A' & col2==30)",
        'A/190': "(col1=='A' & col2==190)",
        'B/50': "(col1=='B' & col2==50)",
        'B/80': "(col1=='B' & col2==80)"
    }

    dictionary = generate_queries(hierarchy_values, sample_df)

    assert dictionary == expected_dictionary


### create_zero_dataframe ###

def test_create_zero_dataframe_valid_input():
    columns = ['A', 'B', 'C']
    n_rows = 3
    result = create_zero_dataframe(columns, n_rows)
    expected_result = pd.DataFrame({'A': {0: 0.0, 1: 0.0, 2: 0.0}, 
                                    'B': {0: 0.0, 1: 0.0, 2: 0.0}, 
                                    'C': {0: 0.0, 1: 0.0, 2: 0.0}})
    pd.testing.assert_frame_equal(result, expected_result)
    assert isinstance(result, pd.DataFrame)
