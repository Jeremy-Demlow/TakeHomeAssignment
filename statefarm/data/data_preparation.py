__all__ = ["DataSplitter", "DataPreprocessor"]

import pandas as pd
import logging
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


class DataSplitter:
    """
    A class for splitting data into training, validation, and optionally test sets.

    Attributes:
        df (pandas.DataFrame): The complete dataset.
        y_vars (list of str): Column names of the target variables.
        splits (list of lists): Indices for training, validation, and test sets.
        X_train, X_valid, X_test (pandas.DataFrame): Training, validation, and test features.
        y_train, y_valid, y_test (pandas.DataFrame): Training, validation, and test targets.
    """

    def __init__(self, df, y_vars):
        self.df = df
        self.y_vars = y_vars
        self.splits = {"train": None, "valid": None, "test": None}
        self.X_train = self.X_valid = self.X_test = None
        self.y_train = self.y_valid = self.y_test = None

    def split_data(
        self, test_size=0.2, val_size=0.1, random_state=13, create_test_set=False
    ):
        """
        Splits the dataset into training, validation, and optionally test sets.

        The method first splits the dataset into training plus temporary set and validation set.
        If a test set is requested, it further splits the training plus temporary set into
        the final training set and test set. The 'test_size' parameter can be either a float
        to represent the proportion of the dataset to include in the test split or an
        absolute number of samples.

        Parameters:
            test_size (float or int): If float, represents the proportion of the dataset
                                      to include in the test split. If int, represents
                                      the absolute number of samples to include in the test split.
            val_size (float): Proportion of the dataset to include in the validation split.
            random_state (int): Controls the shuffling applied to the data before applying the split.
            create_test_set (bool): Whether to create a separate test set. If False,
                                    the test set-related attributes (X_test, y_test) remain None.

        Note:
            - The 'test_size' is interpreted as a proportion if it is a float less than 1,
              otherwise, it is interpreted as the absolute number of samples.
            - The actual size of the test set might be slightly different from the specified 'test_size'
              when it is given as a proportion, due to rounding.
        """
        x_train_full, x_val, y_train_full, y_val = train_test_split(
            self.df.drop(columns=self.y_vars),
            self.df[self.y_vars],
            test_size=val_size,
            random_state=random_state,
        )

        if create_test_set:
            x_train, x_test, y_train, y_test = train_test_split(
                x_train_full,
                y_train_full,
                test_size=test_size,
                random_state=random_state,
            )
            self.splits["test"] = (x_test.index, y_test.index)
        else:
            x_train, y_train = x_train_full, y_train_full
            self.X_test, self.y_test = (
                None,
                None,
            )  # Explicitly set to None when not creating a test set

        self.splits["train"] = (x_train.index, y_train.index)
        self.splits["valid"] = (x_val.index, y_val.index)

        self._extract_splits()

    def _extract_splits(self):
        """Internal method to extract features and targets for each set based on splits."""
        self.X_train, self.y_train = (
            self.df.drop(columns=self.y_vars).iloc[self.splits["train"][0]],
            self.df[self.y_vars].iloc[self.splits["train"][1]],
        )
        self.X_valid, self.y_valid = (
            self.df.drop(columns=self.y_vars).iloc[self.splits["valid"][0]],
            self.df[self.y_vars].iloc[self.splits["valid"][1]],
        )

        logging.info(f"Training set: {self.X_train.shape}, {self.y_train.shape}")
        logging.info(f"Validation set: {self.X_valid.shape}, {self.y_valid.shape}")

        if self.splits["test"]:
            self.X_test, self.y_test = (
                self.df.drop(columns=self.y_vars).iloc[self.splits["test"][0]],
                self.df[self.y_vars].iloc[self.splits["test"][1]],
            )
            logging.info(f"Test set: {self.X_test.shape}, {self.y_test.shape}")
        else:
            logging.info("No test set created.")


class DataPreprocessor:
    """
    A class for preprocessing data for machine learning tasks.

    This class handles the conversion of monetary and percentage string values to floats,
    imputation of missing values, scaling of features, and the creation of dummy variables
    for categorical columns. It can be used for both fitting and transforming training data,
    as well as transforming new data with the same transformations applied to the training data.

    Attributes:
        columns_to_convert (list of str): Columns that contain monetary or percentage string values.
        columns_to_impute (list of str): Columns for which missing values will be imputed.
        columns_to_dummy (list of str): Categorical columns to be converted to dummy variables.
        target_column (str, optional): The name of the target variable column. Default is None.
        imputer (SimpleImputer): The imputer object used for missing value imputation.
        scaler (StandardScaler): The scaler object used for feature scaling.
        dummy_columns (dict): A dictionary to store the columns created after dummy encoding.

    Methods:
        fit_transform(df): Fits the preprocessor to the data and transforms the data.
        transform(df): Transforms a new dataset using the transformations fitted on the training data.
    """

    def __init__(
        self,
        columns_to_convert,
        columns_to_impute,
        columns_to_dummy,
        target_column=None,
    ):
        """
        Initializes the DataPreprocessor with specified columns for conversion, imputation,
        dummy variable creation, and optionally a target column.

        Parameters:
            columns_to_convert (list of str): Columns with monetary or percentage string values to convert.
            columns_to_impute (list of str): Columns for which missing values will be imputed.
            columns_to_dummy (list of str): Categorical columns to be converted into dummy variables.
            target_column (str, optional): The name of the target variable column. Default is None.
        """
        self.columns_to_convert = columns_to_convert
        self.columns_to_impute = columns_to_impute
        self.columns_to_dummy = columns_to_dummy
        self.target_column = target_column
        self.imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
        self.scaler = StandardScaler()
        self.dummy_columns = {}

    def _convert_columns(self, df):
        """
        Converts monetary and percentage values in specified columns from string to float.

        Parameters:
            df (pandas.DataFrame): The dataframe to process.

        Returns:
            pandas.DataFrame: The dataframe with converted columns.
        """

        for col in self.columns_to_convert:
            if df[col].dtype == object:
                df[col] = (
                    df[col]
                    .replace(
                        {r"\$": "", ",": "", "%": "", r"\(": "-", r"\)": ""}, regex=True
                    )
                    .astype(float)
                )
            else:
                logging.warning(
                    f"Column {col} is not of string type and will not be converted."
                )
        return df

    def fit_transform(self, df):
        """
        Fits the preprocessor to the data and transforms the data.
        This includes converting specified columns, imputing missing values,
        scaling, and creating dummy variables.

        Parameters:
            df (pandas.DataFrame): The training dataset to fit and transform.

        Returns:
            pandas.DataFrame: The transformed dataframe.
        """
        df = self._convert_columns(df)
        columns_to_drop = self.columns_to_dummy[:]
        if self.target_column and self.target_column in df.columns:
            columns_to_drop.append(self.target_column)

        df_imputed = pd.DataFrame(
            self.imputer.fit_transform(df.drop(columns=columns_to_drop)),
            columns=df.drop(columns=columns_to_drop).columns,
            index=df.index,
        )
        df_imputed_std = pd.DataFrame(
            self.scaler.fit_transform(df_imputed),
            columns=df_imputed.columns,
            index=df.index,
        )

        for col in self.columns_to_dummy:
            dummies = pd.get_dummies(
                df[col], drop_first=True, prefix=col, prefix_sep="_", dummy_na=True
            )
            dummies = dummies.reindex(df.index, fill_value=0)
            self.dummy_columns[col] = dummies.columns.tolist()
            df_imputed_std = pd.concat([df_imputed_std, dummies], axis=1, sort=False)

        return df_imputed_std

    def transform(self, df):
        """
        Transforms a dataset using the transformations fitted on the training data.
        This includes converting specified columns, imputing missing values,
        scaling, and creating dummy variables based on the training data.

        Parameters:
            df (pandas.DataFrame): The new dataset to transform.

        Returns:
            pandas.DataFrame: The transformed dataframe.
        """
        df = self._convert_columns(df)
        columns_to_drop = self.columns_to_dummy[:]
        if self.target_column and self.target_column in df.columns:
            columns_to_drop.append(self.target_column)
        df_imputed = pd.DataFrame(
            self.imputer.transform(df.drop(columns=columns_to_drop)),
            columns=df.drop(columns=columns_to_drop).columns,
            index=df.index,
        )
        df_imputed_std = pd.DataFrame(
            self.scaler.transform(df_imputed),
            columns=df_imputed.columns,
            index=df.index,
        )

        for col in self.columns_to_dummy:
            dummies = pd.get_dummies(
                df[col], drop_first=True, prefix=col, prefix_sep="_", dummy_na=True
            )
            dummies = dummies.reindex(columns=self.dummy_columns[col], fill_value=0)
            df_imputed_std = pd.concat([df_imputed_std, dummies], axis=1, sort=False)

        return df_imputed_std
