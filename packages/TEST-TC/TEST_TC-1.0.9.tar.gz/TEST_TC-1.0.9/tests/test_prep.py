import pandas as pd
import pytest
from sklearn.utils.estimator_checks import check_estimator

from tc_uc4.datapreparation.prep import PreprocessingClass


test_with_data = [
    ('teleconsulto','prophet','data_richiesta','id_teleconsulto')
]
test_no_data = [
    ('teleconsulto','prophet')
]


@pytest.mark.parametrize("usecase,model,col1,col2", test_with_data)
def test_preprocessing_class_fit_transform(usecase,model,col1,col2):
  
    # Test the fit() and transform() methods of PreprocessingClass
    example_data = pd.DataFrame({col1: pd.to_datetime(['2023-06-01 12:00:00', '2023-06-02 14:30:00', '2023-06-03 15:25:00']), col2: ['A', 'B', 'C']})
    example_data_num2 = pd.DataFrame({col1: pd.to_datetime(['2023-06-01 12:00:00', '2023-06-02 12:40:00', '2023-06-02 12:00:00']), col2: ['A', 'B', 'C']})


    # Create an instance of PreprocessingClass
    preprocessing = PreprocessingClass(usecase=usecase, model=model)

    # Fit the PreprocessingClass on the example data
    result = preprocessing.fit_transform(X=example_data, time_granularity="D")

    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)
    # Check if the result has the same shape as the input data
    assert result.shape == example_data.shape

    # Fit the PreprocessingClass on the second example data
    result = preprocessing.fit_transform(X=example_data_num2, time_granularity="D")
    expected = pd.DataFrame({'Timestamp':  pd.to_datetime(['2023-06-01', '2023-06-02']), 'Target': [1.0,2.0]})

    # Check if the result has the same shape as the input data
    print(result)
    assert result.shape == (2,2)
    # Check if the data is equal to the expected dataframe
    pd.testing.assert_frame_equal(result, expected)

@pytest.mark.parametrize("usecase,model", test_no_data)
def test_preprocessing_class_save_load(tmp_path,usecase,model):
    # Test the save() and load() methods of PreprocessingClass

    # Create an instance of PreprocessingClass
    preprocessing = PreprocessingClass(usecase=usecase, model=model)

    # Save the PreprocessingClass instance to a file
    file_path = tmp_path / "preprocessing.pkl"
    preprocessing.save(file_path)

    # Load the PreprocessingClass instance from the file
    loaded_preprocessing = PreprocessingClass.load(file_path)

    # Check if the loaded instance is of the same type as the original instance
    assert isinstance(loaded_preprocessing, PreprocessingClass)

@pytest.mark.parametrize("usecase,model", test_no_data)
def test_preprocessing_class_estimator_compatibility(usecase,model):
    # Test the estimator compatibility of PreprocessingClass using sklearn's check_estimator

    # Create an instance of PreprocessingClass
    preprocessing = PreprocessingClass(usecase=usecase, model=model)

    # Check if PreprocessingClass meets the requirements of an estimator
    assert check_estimator(preprocessing, generate_only=True)
