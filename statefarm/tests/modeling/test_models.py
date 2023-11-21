import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from statefarm.modeling.models import (
    LogisticRegressionAnalysis,
)  # Replace with the actual import


class TestLogisticRegressionAnalysis(unittest.TestCase):
    @patch("statefarm.modeling.models.LogisticRegression")
    def test_fit_exploratory_model(self, MockLR):
        analysis = LogisticRegressionAnalysis()
        df = pd.DataFrame({"x1": [0.1, 0.2, 0.3], "x2": [1, 2, 3], "y": [0, 1, 0]})
        mock_lr_instance = MockLR.return_value
        mock_lr_instance.coef_ = [[0.4, 0.3]]  # Mock coefficients

        variables = analysis.fit_exploratory_model(df, "y")

        self.assertEqual(len(variables), 2)
        MockLR.assert_called_once()
        mock_lr_instance.fit.assert_called_once()

    @patch("statefarm.modeling.models.sm.Logit")
    def test_fit_final_model(self, MockLogit):
        analysis = LogisticRegressionAnalysis()
        df = pd.DataFrame({"x1": [0.1, 0.2, 0.3], "x2": [1, 2, 3], "y": [0, 1, 0]})
        analysis.variables = ["x1", "x2"]
        mock_logit_instance = MockLogit.return_value
        mock_logit_instance.fit.return_value.summary.return_value = "Model Summary"

        summary = analysis.fit_final_model(df, "y")

        self.assertEqual(summary, "Model Summary")
        MockLogit.assert_called_once()

    def test_evaluate_model(self):
        analysis = LogisticRegressionAnalysis()
        df = pd.DataFrame({"x1": [0.1, 0.2, 0.3], "x2": [1, 2, 3], "y": [0, 1, 0]})
        analysis.variables = ["x1", "x2"]

        analysis.final_result = MagicMock()
        analysis.final_result.predict.return_value = [0.1, 0.9, 0.5]

        outcomes, grouped_outcomes = analysis.evaluate_model(df, "y")

        self.assertEqual(len(outcomes), 3)
        self.assertTrue("prob_bin" in outcomes.columns)
        self.assertEqual(len(grouped_outcomes), 20)


if __name__ == "__main__":
    unittest.main()
