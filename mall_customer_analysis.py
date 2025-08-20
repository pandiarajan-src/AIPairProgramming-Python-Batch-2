"""
MallCustomerAnalysis module.
This module contains the MallCustomerAnalysis class for performing KMeans clustering and visualizing customer data.
"""

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

class MallCustomerAnalysis:
    """
    A class to perform KMeans clustering and visualize customer data.

    Attributes:
        data_url (str): URL of the dataset.
        data (DataFrame): Loaded dataset.
        clustered_data (DataFrame): Dataset with cluster labels.
    """

    def __init__(self, url):
        """
        Initializes the MallCustomerAnalysis class with the dataset URL.

        Args:
            url (str): URL of the dataset.
        """
        self.data_url = url
        self.data = None
        self.clustered_data = None

    def load_data(self):
        """
        Loads the dataset from the provided URL.

        Raises:
            ValueError: If the dataset cannot be loaded.
        """
        self.data = pd.read_csv(self.data_url)
        if self.data is None:
            raise ValueError("Data could not be loaded. Please check the URL or file path.")

    def perform_clustering(self, n_clusters=5):
        """
        Performs KMeans clustering on the dataset.

        Args:
            n_clusters (int): Number of clusters for KMeans. Default is 5.

        Raises:
            ValueError: If the dataset is not loaded.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Please call load_data() first.")
        features = self.data[['Age', 'Annual Income (k$)', 'Spending Score (1-100)']]

        # Determine the optimal number of clusters using the elbow method
        inertia = []
        for n in range(1, 11):
            kmeans = KMeans(n_clusters=n, random_state=42)
            kmeans.fit(features)
            inertia.append(kmeans.inertia_)

        # Plot the elbow curve
        plt.figure(figsize=(8, 5))
        plt.plot(
            range(1, 11), inertia, marker='o'
        )
        plt.title('Elbow Method')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia')
        plt.show()

        # Fit KMeans with the optimal number of clusters
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.data['Cluster'] = kmeans.fit_predict(features)
        self.clustered_data = self.data
        self.clustered_data.to_csv('clustered_data.csv', index=False)

    def visualize(self):
        """
        Generates various visualizations for the clustered data.

        Raises:
            ValueError: If the clustered data is not available.
        """
        if self.clustered_data is None:
            raise ValueError("Clustered data is not available. Please call perform_clustering() first.")
        # Age vs Spending Score
        plt.figure(figsize=(8, 5))
        sns.scatterplot(
            x='Age', y='Spending Score (1-100)', hue='Cluster',
            data=self.clustered_data, palette='viridis'
        )
        plt.title('Age vs Spending Score')
        plt.show()

        # Age vs Annual Income
        plt.figure(figsize=(8, 5))
        sns.scatterplot(
            x='Age', y='Annual Income (k$)', hue='Cluster',
            data=self.clustered_data, palette='viridis'
        )
        plt.title('Age vs Annual Income')
        plt.show()

        # Annual Income vs Spending Score
        plt.figure(figsize=(8, 5))
        sns.scatterplot(
            x='Annual Income (k$)', y='Spending Score (1-100)', hue='Cluster',
            data=self.clustered_data, palette='viridis'
        )
        plt.title('Annual Income vs Spending Score')
        plt.show()

        # Gender vs Annual Income
        plt.figure(figsize=(8, 5))
        sns.boxplot(
            x='Gender', y='Annual Income (k$)',
            data=self.clustered_data
        )
        plt.title('Gender vs Annual Income')
        plt.show()

        # Gender vs Spending Score
        plt.figure(figsize=(8, 5))
        sns.boxplot(
            x='Gender', y='Spending Score (1-100)',
            data=self.clustered_data
        )
        plt.title('Gender vs Spending Score')
        plt.show()

if __name__ == "__main__":
    DATA_URL = (
        "https://gist.githubusercontent.com/pravalliyaram/5c05f43d2351249927b8a3f3cc3e5ecf/raw/"
        "8bd6144a87988213693754baaa13fb204933282d/Mall_Customers.csv"
    )
    analysis = MallCustomerAnalysis(DATA_URL)
    analysis.load_data()
    analysis.perform_clustering()
    analysis.visualize()
