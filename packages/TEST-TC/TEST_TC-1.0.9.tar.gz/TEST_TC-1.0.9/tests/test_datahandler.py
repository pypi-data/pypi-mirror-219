import pytest
import pandas as pd
import geopandas as gpd
import os

from tc_uc4.datahandler.datahandler import DataHandler
from tc_uc4.utility.exceptions import InputTypeError

@pytest.fixture
def data_handler(tmp_path):
    return DataHandler(data_folder=str(tmp_path))

def test_data_handler_configured_init_read(tmp_path):
    # Create a Pandas DataFrame
    data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)

    # Write DataFrame to a Parquet file
    file_path = tmp_path / 'test.parquet'
    df.to_parquet(file_path)

    DH = DataHandler(data_folder=str(tmp_path))
    df_check = DH.read(filename='test.parquet', folder='')
    df_check2 = DH.read(filename='test.parquet', folder='.')

    assert type(df_check) == pd.DataFrame
    assert type(df_check2) == pd.DataFrame
    assert df.equals(df_check)
    assert df.equals(df_check2)

    # Can't find the file
    with pytest.raises(SystemExit):
        DH.read(filename='test.parquet', folder='/')
    
    # Can't find the file
    with pytest.raises(SystemExit):
        DH.read(filename='test.parquet', folder='-')


def test_datahandler_wrong_init():
    with pytest.raises(InputTypeError):
        DH = DataHandler(data_folder=123)

def test_datahandler_read_wrong_input_types(data_handler):
    with pytest.raises(SystemExit):
        data_handler.read(123,'string ok',True)

def test_datahandler_read_geodataframe_wrong_input_types(data_handler):
    with pytest.raises(SystemExit):
        data_handler.read_geodataframe('string ok', 123, True)

def test_datahandler_write_wrong_input_types(data_handler):
    with pytest.raises(SystemExit):
        data_handler.write(pd.Series, 'string ok', 'not a bool')

def test_datahandler_read_not_supp_extension(data_handler):
    df = pd.DataFrame([1])
    with pytest.raises(SystemExit):
        data_handler.read('this_is_a_file.txt')

def test_datahandler_read_geodataframe_not_supp_extension(data_handler):
    df = pd.DataFrame([1])
    with pytest.raises(SystemExit):
        data_handler.read_geodataframe('this_is_a_file.txt')

def test_datahandler_write_not_supp_extension(data_handler):
    df = pd.DataFrame([1])
    with pytest.raises(SystemExit):
        data_handler.write(df, 'this_is_a_file.txt')

def test_datahandler_write_folder(data_handler):
    df = pd.DataFrame([1])
    with pytest.raises(SystemExit):
        data_handler.write(df, 'test.parquet', 'pippo')

def test_datahandler_outputs(tmp_path, data_handler):
    data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)

    data_geo = {
    'City': ['New York', 'Los Angeles', 'Chicago'],
    'Latitude': [40.7128, 34.0522, 41.8781],
    'Longitude': [-74.0060, -118.2437, -87.6298]
    }
    # Create GeoDataFrame
    geo_df = gpd.GeoDataFrame(data_geo, geometry=gpd.points_from_xy(data_geo['Longitude'], data_geo['Latitude']))
    
    os.mkdir(os.path.join(tmp_path, 'regions'))
    file_path_geo = tmp_path / 'regions/test.parquet'
    geo_df.to_parquet(file_path_geo)

    file_path_pd = tmp_path / 'test.parquet'
    df.to_parquet(file_path_pd)

    df = data_handler.read('test.parquet', folder='')
    assert type(df) == pd.DataFrame

    df = data_handler.read_geodataframe('test.parquet', folder='regions')
    assert type(df) == gpd.GeoDataFrame
