"""
Module to generate and read synthetic data in CSV format.

Prompt given:
# write a new python program to generate synthetic data as a csv
#   with 5 columns and 20 rows with a mixuture of stirngs and integers
# write a python method to read the csv file
# Call them in the same main function

"""

import csv
import random


def generate_synthetic_data(file_path):
    """Generate a CSV file with 5 columns and 20 rows of mixed strings and integers."""
    headers = ["Name", "Age", "City", "Score", "Category"]
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    categories = ["A", "B", "C", "D", "E"]

    with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)
        for _ in range(20):
            row = [
                random.choice(names),
                random.randint(18, 60),
                random.choice(cities),
                random.randint(0, 100),
                random.choice(categories),
            ]
            writer.writerow(row)


def read_csv(file_path):
    """Read and print the contents of a CSV file."""
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)


if __name__ == "__main__":
    FILE_PATH = "synthetic_data.csv"
    generate_synthetic_data(FILE_PATH)
    print("Synthetic data generated:")
    read_csv(FILE_PATH)
