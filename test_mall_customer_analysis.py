"""
Unit tests for the MallCustomerAnalysis class.
This module contains tests for loading data, performing clustering, and visualizing results.
"""

import unittest
import pandas as pd
from mall_customer_analysis import MallCustomerAnalysis

class TestMallCustomerAnalysis(unittest.TestCase):
    """
    Unit tests for the MallCustomerAnalysis class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up resources for testing.
        """
        cls.data_url = (
            "https://gist.githubusercontent.com/pravalliyaram/5c05f43d2351249927b8a3f3cc3e5ecf/raw/"
            "8bd6144a87988213693754baaa13fb204933282d/Mall_Customers.csv"
        )
        cls.analysis = MallCustomerAnalysis(cls.data_url)

    def test_load_data(self):
        """
        Test the load_data method.
        """
        self.analysis.load_data()
        self.assertIsNotNone(self.analysis.data, "Data should be loaded.")
        self.assertIsInstance(self.analysis.data, pd.DataFrame, "Data should be a DataFrame.")

    def test_perform_clustering(self):
        """
        Test the perform_clustering method.
        """
        self.analysis.load_data()
        self.assertIsNotNone(self.analysis.data, "Data should be loaded before clustering.")
        self.analysis.perform_clustering(n_clusters=5)
        self.assertIsNotNone(self.analysis.data, "Data should not be None after clustering.")
        self.assertIn(
            "Cluster", self.analysis.data.columns, "Cluster column should be added to the data."
        )
        self.assertEqual(
            len(self.analysis.data["Cluster"].unique()), 5, "There should be 5 unique clusters."
        )

    def test_visualize(self):
        """
        Test the visualize method.
        """
        self.analysis.load_data()
        self.analysis.perform_clustering(n_clusters=5)
        self.assertIsNotNone(
            self.analysis.clustered_data, "Clustered data should be available before visualization."
        )
        try:
            self.analysis.visualize()
        except ValueError as e:
            self.fail(f"Visualization failed with ValueError: {e}")
        except RuntimeError as e:
            self.fail(f"Visualization failed with RuntimeError: {e}")

if __name__ == "__main__":
    unittest.main()
