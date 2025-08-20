"""
Test module for Pima KNN Analysis.

This module contains tests for all functions in pima_knn_analysis.py.
"""

import pytest
from pima_knn_analysis import visualize_data, knn_model, data


def test_visualize_data():
    """Test the visualize_data function."""
    try:
        visualize_data(data)
    except Exception as e:
        pytest.fail(f"Visualization failed with error: {e}")


def test_knn_model(capsys):
    """Test the knn_model function."""
    try:
        knn_model(data)
        captured = capsys.readouterr()
        assert "Accuracy" in captured.out
    except Exception as e:
        pytest.fail(f"KNN model failed with error: {e}")
