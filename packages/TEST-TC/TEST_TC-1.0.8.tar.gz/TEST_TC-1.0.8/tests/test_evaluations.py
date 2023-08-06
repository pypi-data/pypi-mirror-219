import pandas as pd
import numpy as np
import pytest
from tc_uc4.analytics.evaluationMetrics import evaluations
from tc_uc4.utility.exceptions import ColumnNotFound

def test_evaluations():
     # Sample data 
     real_df = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-26', '2023-06-27', '2023-06-28', '2023-06-29']),
                             'Target': [10, 20, 30, 40]})
     prophet_df = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-26', '2023-06-27', '2023-06-28', '2023-06-29']),
                                'Id_pred' : ['TEST', 'TEST', 'TEST', 'TEST'],
                                'Pred_mean': [12, 18, 32, 37],
                                'Pi_upper_95': [14, 19, 37, 40],
                                'Pi_lower_95': [10, 15, 29, 33]})

     # Calculate evaluation metrics
     result = evaluations(real_df, prophet_df)

     expected_result = pd.DataFrame({'Id_pred': {0: 'TEST'},
                                     'MAE': {0: 2.25},
                                     'MAPE': {0: 0.11},
                                     'RMSE': {0: 2.29},
                                     'MSE': {0: 5.25},
                                     'R2': {0: 0.96},
                                     'Percentage Coverage': {0: 75.0}})

     # Verify the content of the evaluation dataframe
     assert isinstance(result, pd.DataFrame)  # The result should be a DataFrame
     assert result.shape == (1,7)  # The DataFrame should have 4 rows
     assert set(result.columns) == {'Id_pred', 'MAE', 'MAPE', 'MSE', 'R2', 'RMSE', 'Percentage Coverage'}  # The DataFrame should have the correct columns
     pd.testing.assert_frame_equal(result, expected_result)

def test_evaluations_column_not_found():
    # Sample data without the 'Pred_mean' column in the pred dataframe
     df_real = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-27', '2023-06-28', '2023-06-29']),
                             'Target': [10, 20, 30]})
     df_pred = pd.DataFrame({'Timestamp': pd.to_datetime(['2023-06-27', '2023-06-28', '2023-06-29']),
                             'Id_pred' : ['TEST', 'TEST', 'TEST'],
                             'Value': [12, 18, 32]})

     # Sample data without the 'Timestamp' column in the real dataframe
     df_real2 = pd.DataFrame({'timestamp': pd.to_datetime(['2023-06-27', '2023-06-28', '2023-06-29']),
                              'Target': [10, 20, 30]})

     # Check if the ColumnNotFound exception is raised
     with pytest.raises(ColumnNotFound):
          evaluations(df_real, df_pred)
     
     with pytest.raises(ColumnNotFound):
          evaluations(df_real2, df_pred)
