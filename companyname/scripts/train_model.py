__all__ = ["train_model"]

import argparse
import logging
import os
import pandas as pd
import joblib

from companyname.data.data_preparation import DataSplitter, DataPreprocessor
from companyname.modeling.models import LogisticRegressionAnalysis


def train_model(data_path, model_save_path, preprocessor_save_path):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the data processing and model training pipeline.")

    df = pd.read_csv(data_path)

    data_splitter = DataSplitter(df=df, y_vars=["y"])
    data_splitter.split_data(
        test_size=4000, val_size=0.1, random_state=13, create_test_set=True
    )

    columns_to_convert = ["x12", "x63"]
    columns_to_impute = [
        col
        for col in df.columns
        if col not in ["y", "x5", "x31", "x81", "x82"] + columns_to_convert
    ]
    columns_to_dummy = ["x5", "x31", "x81", "x82"]
    preprocessor = DataPreprocessor(
        columns_to_convert, columns_to_impute, columns_to_dummy, target_column="y"
    )

    X_train = preprocessor.fit_transform(data_splitter.X_train)
    X_valid = preprocessor.transform(data_splitter.X_valid)
    X_test = preprocessor.transform(data_splitter.X_test)

    train_df = pd.concat([X_train, data_splitter.y_train], axis=1).reset_index(
        drop=True
    )
    valid_df = pd.concat([X_valid, data_splitter.y_valid], axis=1).reset_index(
        drop=True
    )
    test_df = pd.concat([X_test, data_splitter.y_test], axis=1).reset_index(drop=True)

    lr_analysis = LogisticRegressionAnalysis()
    lr_analysis.fit_exploratory_model(train_df, "y")
    combined_df = pd.concat([train_df, valid_df, test_df])
    lr_analysis.fit_final_model(combined_df, "y")
    lr_analysis.evaluate_model(combined_df, "y")

    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(preprocessor_save_path), exist_ok=True)
    joblib.dump(lr_analysis, model_save_path)
    joblib.dump(preprocessor, preprocessor_save_path)

    logging.info("Data processing and model training pipeline completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a logistic regression model.")
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to the training data CSV file",
    )
    parser.add_argument(
        "--model_save_path",
        type=str,
        required=True,
        help="Path to save the trained model",
    )
    parser.add_argument(
        "--preprocessor_save_path",
        type=str,
        required=True,
        help="Path to save the data preprocessor",
    )

    args = parser.parse_args()
    train_model(args.data_path, args.model_save_path, args.preprocessor_save_path)
