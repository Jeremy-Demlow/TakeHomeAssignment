__all__ = ["LogisticRegressionAnalysis"]

import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import logging


class LogisticRegressionAnalysis:
    """
    A class for conducting logistic regression analysis.

    This class simplifies the process of fitting a logistic regression model,
    selecting important variables based on coefficients, and evaluating the model's
    performance using the C-statistic (ROC AUC score).

    Attributes:
        exploratory_LR (LogisticRegression): The initial logistic regression model.
        variables (list): List of selected variables based on the model's coefficients.
        final_model (statsmodels.Logit): The final logistic regression model after variable selection.
        final_result (statsmodels.LogitResults): Results of the final logistic regression model.
    """

    def __init__(self):
        """Initializes the LogisticRegressionAnalysis class with default values."""
        self.exploratory_LR = None
        self.variables = []
        self.final_model = None
        self.final_result = None

    def fit_exploratory_model(self, df, target_column):
        """
        Fits an exploratory logistic regression model to identify important variables.

        Args:
            df (pandas.DataFrame): The dataset to fit the model on.
            target_column (str): The name of the target variable in the dataset.

        Returns:
            list: The list of top 25 variables selected based on the coefficients.
        """
        self.exploratory_LR = LogisticRegression(
            penalty="l1", fit_intercept=False, solver="liblinear"
        )
        self.exploratory_LR.fit(df.drop(columns=[target_column]), df[target_column])

        # Extract coefficients
        results = pd.DataFrame(df.drop(columns=[target_column]).columns).rename(
            columns={0: "name"}
        )
        results["coefs"] = self.exploratory_LR.coef_[0]
        results["coefs_squared"] = results["coefs"] ** 2

        # Select top 25 variables
        self.variables = results.nlargest(25, "coefs_squared")["name"].tolist()

        logging.info("Selected Variables: %s", self.variables)
        return self.variables

    def fit_final_model(self, df, target_column):
        """
        Fits the final logistic regression model using selected variables.

        Args:
            df (pandas.DataFrame): The dataset to fit the model on.
            target_column (str): The name of the target variable in the dataset.

        Returns:
            str: The summary of the final logistic regression model.
        """
        self.final_model = sm.Logit(df[target_column], df[self.variables])
        self.final_result = self.final_model.fit()

        logging.info(self.final_result.summary())
        return self.final_result.summary()

    def evaluate_model(self, df, target_column):
        """
        Evaluates the model's performance using the C-statistic (ROC AUC score).

        Args:
            df (pandas.DataFrame): The dataset to evaluate the model on.
            target_column (str): The name of the target variable in the dataset.

        Returns:
            pandas.Series: Sum of target variable in each probability bin.
        """
        outcomes = pd.DataFrame(self.final_result.predict(df[self.variables])).rename(
            columns={0: "probs"}
        )
        outcomes["y"] = df[target_column]

        roc_auc = roc_auc_score(outcomes["y"], outcomes["probs"])
        logging.info("The C-Statistics is %s", roc_auc)

        outcomes["prob_bin"] = pd.qcut(outcomes["probs"], q=20)
        grouped_outcomes = outcomes.groupby(["prob_bin"])["y"].sum()
        return outcomes, grouped_outcomes
