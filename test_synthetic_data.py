"""
Unit tests for the synthetic_data module.
"""

import os
import csv
import unittest
from synthetic_data import generate_synthetic_data, read_csv


class TestSyntheticData(unittest.TestCase):
    """Test cases for the synthetic_data module."""

    def setUp(self):
        """Set up a temporary file for testing."""
        self.test_file = "test_synthetic_data.csv"

    def tearDown(self):
        """Clean up the temporary file after testing."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_generate_synthetic_data(self):
        """Test the generate_synthetic_data function."""
        generate_synthetic_data(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 21)  # 1 header + 20 data rows
            self.assertEqual(len(rows[0]), 5)  # 5 columns

    def test_read_csv(self):
        """Test the read_csv function."""
        generate_synthetic_data(self.test_file)
        with open(self.test_file, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            expected_rows = list(reader)

        # Capture printed output
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        read_csv(self.test_file)
        sys.stdout = sys.__stdout__

        printed_output = captured_output.getvalue().strip().split("\n")
        printed_rows = [
            row.strip("[]").replace("'", "").split(", ") for row in printed_output
        ]
        self.assertEqual(printed_rows, expected_rows)


if __name__ == "__main__":
    unittest.main()
