import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "Impact_of_Remote_Work_on_Mental_Health.csv"
data = pd.read_csv(file_path)

# Display basic info about the dataset
print("Dataset Info:")
print(data.info())

# Display the first few rows of the dataset
print("\nFirst 5 rows of the dataset:")
print(data.head())

# Calculate summary statistics
summary_stats = data.describe()
print("\nSummary Statistics:")
print(summary_stats)

# Calculate median and standard deviation for numerical columns
medians = data.median(numeric_only=True)
std_devs = data.std(numeric_only=True)
print("\nMedians:")
print(medians)
print("\nStandard Deviations:")
print(std_devs)