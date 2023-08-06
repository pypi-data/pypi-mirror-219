import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self
from typing import Union, Dict, List

from ..utility.tele_logger import logger
from ..utility.exceptions import InputTypeError

class ModelPreprocess: 

    def generate_time_series(self,
                df: pd.DataFrame,
                date_col: str,
                target_col: str,
                time_granularity: str = "D",
                missing_data_strategy: Union[str,int,dict] = ""
                ) -> pd.DataFrame:
        """
        Sequential execution of transformations to obtain a DataFrame with a time series structure

        Parameters
        ----------
        df: pd.DataFrame
            raw dataframe from which generates timeseries
        date_col: str
            column name identifying the columns to index on
        target_col: str
            column name identifying column from which to generate target
        missing_data_strategy: str or int
            Identifies whether to impute missing values and if so using which strategy/value
            Allowed parameters: 
                if str:
                    "mean" : missing values are replaced with the mean of the known values in the dataset.
                    "median": missing values are replaced with the median of the known values in the dataset.
                    "zero": missing values are replaced with the 0.
                    "bfill": missing values are replaced with the next available value in the dataset.
                    "ffill": missing values are replaced with the most recent preceding value in the dataset.
                if int:
                    replace NaN with the specified integer
                if dict:
                    replace NaN using the specified interpolation method (allowed "polynomial" or "spline") and its order.
        time_granularity: str 
           specifies temporal granularity

        Returns:
            pd.DataFrame: DataFrame identifying the timeseries generated according to specified hierarchies and time span
        """

         # Verify that df is of type pd.DataFrame
        if not isinstance(df, pd.DataFrame):
            logger.info("Input 'df' must be of type pd.DataFrame", important=True)
            raise InputTypeError('datapreparation_utils.generate_time_series')
        # Verify that datetime_index is a non-empty string and a column in df
        if  date_col not in df.columns:
            logger.info("Invalid value for 'date_col'. It must be a column in 'df'", important=True)
            raise InputTypeError('datapreparation_utils.generate_time_series')
        # Verify that target is a non-empty string and a column in df
        if target_col not in df.columns:
            logger.info("Invalid value for 'target'. It must be a column in 'df'", important=True)
            raise InputTypeError('datapreparation_utils.generate_time_series')
        if missing_data_strategy != "":
            if isinstance(missing_data_strategy, str):
                allowed_strategies = ["mean", "median", "zero", "bfill", "ffill", "interpolate"]
                if missing_data_strategy not in allowed_strategies:
                    logger.info("Invalid value for 'missing_data_strategy'. Allowed values: {}".format(allowed_strategies), important=True)
                    raise ValueError("Invalid value for 'missing_data_strategy' in 'datapreparation_utils.generate_time_series'. Allowed values: {}".format(allowed_strategies))
            elif isinstance(missing_data_strategy, int):
                pass
            elif isinstance(missing_data_strategy, dict):
                allowed_interpolation_method = ['polynomial', "spline"]
                if missing_data_strategy['interpolation'] not in allowed_interpolation_method:
                    logger.info("Invalid value for 'missing_data_strategy - interpolation method'. Allowed values: {}".format(allowed_interpolation_method), important=True)
                    raise ValueError("Invalid value for 'missing_data_strategy' in 'datapreparation_utils.generate_time_series'. Allowed values: {}".format(allowed_interpolation_method))
                if not isinstance(missing_data_strategy['order'], int):
                    logger.info("Invalid value for 'missing_data_strategy - order'. It must be int", important=True)
                    raise ValueError("Invalid value for 'missing_data_strategy - order' in 'datapreparation_utils.generate_time_series'. It must be int")
            else:
                logger.info("Invalid type for 'missing_data_strategy'. It must be str or int", important=True)
                raise TypeError("Invalid type for 'missing_data_strategy' in 'datapreparation_utils.generate_time_series'. It must be str or int or dict")
        
        # Raw dataset from which to generate the time serie
        self.df = df.copy()

        logger.info('Generating the timeseries target')

        df_ts = self.df.set_index(date_col).resample(time_granularity.upper()).size().reset_index()
        df_ts.columns = ["Timestamp", "Target"]
        df_ts.loc[df_ts.Target==0, "Target"] = np.nan

        if missing_data_strategy != "":
            if isinstance(missing_data_strategy,dict):
                if missing_data_strategy['interpolation']=="spline" and (df_ts['Target'].notna().sum() < missing_data_strategy['order'] or missing_data_strategy['order'] >5):
                    logger.error('The number of data points must be larger than the spline degree k or k should be 1<=k<=5.')
                    raise ValueError("Invalid value for spline order in 'datapreparation_utils.generate_time_series'")

            fillna = ReplacerNA(missing_data_strategy)
            df_ts = fillna.fit_transform(df_ts)
            df_ts['Target'] = df_ts['Target'].clip(lower=0)

        return df_ts

def code_to_name(cod: pd.Series, convers_dict: Dict) -> pd.Series:

    """
    The function generates a new column converting the code number into a meaningful string

    Parameters
    ----------
    cod: pd.Series
       The code number column
    convers_dict: dict
        The mapping dictionary from code to string

    Returns
    -------
        pd.Series
        Returns the modified column based on the mapping dictionary
    """
    if not isinstance(cod, pd.Series):
        logger.info("Input 'cod' must be of type pd.Series")
        raise InputTypeError('datapreparation_utils.cod_to_name')
    if not isinstance(convers_dict, dict):
        logger.info("Input 'convers_dict' must be of type dict")
        raise InputTypeError('datapreparation_utils.cod_to_name')
                  
    return cod.apply(lambda i: convers_dict[int(i)])


class Normalizer(TransformerMixin, BaseEstimator):

    """Normalization class for time series (between 0 and 1)
    """

    def __init__(self):
        pass

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value min and max useful to normalize data

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted normalizer
        """

        self.min = X.iloc[:,1].min()
        self.max = X.iloc[:,1].max()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform normalization between 0 and 1

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        normalized = (X.iloc[:,1] - self.min) / (self.max - self.min)
        ris = pd.concat([X.iloc[:,0],normalized],axis=1)
        ris.columns = X.columns
        
        return ris
    
class ReplacerNA(TransformerMixin, BaseEstimator):

    def __init__(self, method: Union[str,int, dict] = "") -> Self:

        """class for handling of NA

        Parameters
        ----------
        method : str | int | dict 
            if str specify the method to replace NA value (mean,median,zero), if int specify the value to replace NA value
            if dict specify which interpolation method to use between polynomial and spline and its order
        Returns
        -------
        self : object
        """
        
        self.method = method

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful for replacing NA

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted replacer
        """
        
        if self.method == "mean":
            self.value = X.iloc[:,1].mean()
            self.method_for_df = None
        elif self.method == "median":
            self.value = X.iloc[:,1].median()
            self.method_for_df = None
        elif self.method == "zero":
            self.value = 0
            self.method_for_df = None
        elif self.method == "bfill":
            self.value = None
            self.method_for_df = "bfill"
        elif self.method == "ffill":
            self.value = None
            self.method_for_df = "ffill"
        elif self.method == "interpolate":
            self.value = None
            self.method_for_df = "interpolate"
        elif isinstance(self.method, dict):
            self.value = self.method["order"]
            self.method_for_df = self.method["interpolation"].lower()

        else:
            self.value = self.method
            self.method_for_df = None

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform replacement of missing values

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """
        if self.method_for_df in ["polynomial", "spline"]:
            # Create a temporary DataFrame with a DatetimeIndex
            temp_df = pd.DataFrame({X.columns[1]: X.iloc[:, 1]})
            temp_df.index = pd.to_datetime(X.iloc[:, 0])

            # Perform time-based interpolation in the temporary DataFrame
            temp_df.iloc[:, 0] = temp_df.iloc[:, 0].interpolate(method=self.method_for_df, order = self.value)

            # Assign the interpolated values to the original column in the X DataFrame
            X.iloc[:, 1] = temp_df.iloc[:, 0].values
        else:
            X.fillna(self.value, method=self.method_for_df, inplace=True)
        return X
    
class Detrender(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Detrending time series

        Parameters
        ----------
        period : int
            specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to detrend time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted detrender
        """

        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.trend = additive_decomp.trend

        return self

    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """Perform detrending of time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        detrend_time_series = X.iloc[:,1] - self.trend
        ris = pd.concat([X.iloc[:,0],detrend_time_series],axis=1)
        ris.columns = X.columns

        return  ris
    
class Deseasoner(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Deseasonalises time series

        Parameters
        ----------
        period : int
            specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to deseasonalises time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted deseasoner
        """
        
        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.seasonal = additive_decomp.seasonal

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform deseasonalises of time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        deseason_time_series = X.iloc[:,1] - self.seasonal
        ris = pd.concat([X.iloc[:,0],deseason_time_series],axis=1)
        ris.columns = X.columns

        return ris

class Differencer(TransformerMixin, BaseEstimator):

    def __init__(self, lag: int) -> Self:

        """Differencing time series
        
        Parameters
        ----------
        lag : int
            differencing time series lag

        Returns
        -------
        self : object
        """

        self.lag = lag

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful to compute differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted normalizer
        """

        self.shape = X.shape[0]
        self.lag_time_series = X.iloc[:self.shape-self.lag,1]
        self.timestamp = X.iloc[self.lag:,0].reset_index(drop=True)

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        time_series_lagged = X.iloc[self.lag:,1].reset_index(drop=True) - self.lag_time_series
        ris = pd.concat([self.timestamp,time_series_lagged], axis=1)
        ris.columns = X.columns
        
        return ris
     
class OutlierRemover(BaseEstimator, TransformerMixin):
    def __init__(self, lower_threshold_percentile=5, upper_threshold_percentile=95):
        """
        Remove outliers from a dataset by capping values above and below thresholds.

        Parameters:
        -----------
        upper_threshold_percentile : int or float, optional (default=95)
            Percentile threshold above which values will be capped.
        lower_threshold_percentile : int or float, optional (default=5)
            Percentile threshold below which values will be capped.
        """
        self.upper_threshold_percentile = upper_threshold_percentile
        self.lower_threshold_percentile = lower_threshold_percentile
        self.upper_threshold = None
        self.lower_threshold = None

    def fit(self, X, y=None):
        """
        Compute the upper and lower thresholds based on percentiles of the input data.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted OutlierRemover object.
        """
        self.upper_threshold = np.percentile(X, self.upper_threshold_percentile)
        self.lower_threshold = np.percentile(X, self.lower_threshold_percentile)
        return self

    def transform(self, X):
        """
        Cap the values above the upper threshold and below the lower threshold.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_transformed : array-like
            Transformed data with capped outlier values.
        """
        X[X > self.upper_threshold] = self.upper_threshold
        X[X < self.lower_threshold] = self.lower_threshold
        return X
    

class Smoother(BaseEstimator, TransformerMixin):
    def __init__(self, window_size):
        """
        Smoothes a time series by applying a moving average window.

        Parameters:
        -----------
        window_size : int
            Size of the moving average window.
        """
        self.window_size = window_size

    def fit(self, X, y=None):
        """
        Fit the Smoother to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted Smoother object.
        """
        return self

    def transform(self, X):
        """
        Smooth the input data by applying a moving average window.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_smoothed : array-like
            Smoothed data obtained by applying the moving average window.
        """
        
        X_smoothed = X.rolling(window=self.window_size, min_periods=1).mean()
        return X_smoothed


class Differentiator(BaseEstimator, TransformerMixin):
    def __init__(self, order):
        """
        Differentiates "order" times a time series by taking differences between consecutive values.

        Parameters:
        -----------
        order : int
            Order of differentiation.
        """
        self.order = order

    def fit(self, X, y=None):
        
        """
        Fit the Differentiator to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted Differentiator object.
        """
        return self

    def transform(self, X):
        """
        Apply differentiation to the input data by taking differences between consecutive values.
 

        Parameters:
        -----------
        X : array-like
            Input data.


        Returns:
        --------
        X_transformed : array-like
            Transformed data obtained by taking differences between consecutive values.
        """
        X_transformed = X.copy()
        for _ in range(self.order):
            X_transformed = X_transformed.diff()
        X_transformed = np.nan_to_num(X_transformed, nan=0.0)
        return X_transformed


class LogTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        """
        Logarithmic transformation of data.

        Parameters:
        -----------
        None
        """
        pass

    def fit(self, X, y=None):
        """
        Fit the LogTransformer to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted LogTransformer object.
        """
        return self

    def transform(self, X):
        """
        Apply the logarithmic transformation to the input data.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_transformed : array-like
            Transformed data obtained by applying the logarithmic transformation.
        """
        X_transformed = np.log1p(X)
        return X_transformed

    def inverse_transform(self, X_transformed):
        """
        Reconstruct the original data from the transformed data by applying the inverse logarithmic transformation.

        Parameters:
        -----------
        X_transformed : array-like
            Transformed data.

        Returns:
        --------
        X_reconstructed : array-like
            Reconstructed data obtained by applying the inverse logarithmic transformation.
        """
        X_reconstructed = np.expm1(X_transformed)
        return X_reconstructed


class Normalizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        """
        Normalize data to the range [0, 1].

        Parameters:
        -----------
        None
        """
        pass

    def fit(self, X, y=None):
        """
        Fit the Normalizer to the data. No computations are needed in this case.

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        self : object
            Fitted Normalizer object.
        """
        
        self.min = np.min(X)
        self.max = np.max(X)
        return self

    def transform(self, X):
        """
        Normalize the input data to the range [0, 1].

        Parameters:
        -----------
        X : array-like
            Input data.

        Returns:
        --------
        X_normalized : array-like
            Normalized data obtained by scaling the values to the range [0, 1].
        """
        X_normalized = (X - self.min) / (self.max - self.min)
        return X_normalized

    def inverse_transform(self, X_normalized):
        """
        Reconstruct the original data from the normalized data by applying the inverse transformation.

        Parameters:
        -----------
        X_normalized : array-like
            Normalized data.

        Returns:
        --------
        X : array-like
            Reconstructed data obtained by applying the inverse transformation.
        """
        X = X_normalized * (self.max -self.min) + self.min
        return X
