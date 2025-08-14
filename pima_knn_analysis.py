"""
Pima Indians Diabetes Dataset Analysis and Classification using KNN.

This script performs the following tasks:
1. Loads the Pima Indians Diabetes dataset.
2. Visualizes the data using various plots (density plot, bar chart, box and whisker plot, etc.).
3. Builds a KNN classification model.
4. Evaluates the model's accuracy.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]
data = pd.read_csv(url, names=columns)


# Data visualization
def visualize_data(data):
    """Generate important charts for the dataset."""
    # Density plot
    data.plot(
        kind="density", subplots=True, layout=(3, 3), sharex=False, figsize=(12, 10)
    )
    plt.suptitle("Density Plots")
    plt.show()

    # Bar chart
    data["Outcome"].value_counts().plot(kind="bar", color=["blue", "orange"])
    plt.title("Bar Chart of Outcome")
    plt.xlabel("Outcome")
    plt.ylabel("Count")
    plt.show()

    # Correlation matrix
    plt.figure(figsize=(10, 8))
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

    # Box and whisker plots
    data.plot(
        kind="box",
        subplots=True,
        layout=(3, 3),
        sharex=False,
        sharey=False,
        figsize=(12, 10),
    )
    plt.suptitle("Box and Whisker Plots")
    plt.show()


# Build and evaluate KNN model
def knn_model(data):
    """Build and evaluate a KNN classification model."""
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Build the KNN model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)

    # Make predictions
    y_pred = knn.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    visualize_data(data)
    knn_model(data)
