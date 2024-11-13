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

# Summary statistics
mean_values = data.mean(numeric_only=True)  # Calculate mean for numeric columns
median_values = data.median(numeric_only=True)  # Calculate median for numeric columns
std_dev_values = data.std(numeric_only=True)  # Calculate standard deviation for numeric columns

print("\nMean Values:\n", mean_values)
print("\nMedian Values:\n", median_values)
print("\nStandard Deviation Values:\n", std_dev_values)

data.dropna(subset=["Sleep_Quality", "Company_Support_for_Remote_Work"], inplace=True)


# Visualization
column_to_visualize = "Work_Life_Balance_Rating" 
if column_to_visualize in data.columns:
    sns.countplot(x=column_to_visualize, data=data)
    plt.title(f"Distribution of {column_to_visualize}")
    plt.xlabel(column_to_visualize)
    plt.ylabel("Count")
    plt.show()
else:
    print(f"Column '{column_to_visualize}' not found in the dataset.")

# Visualization for Sleep_Quality
column_to_visualize = "Sleep_Quality"

if column_to_visualize in data.columns:
    sns.countplot(x=column_to_visualize, data=data)
    plt.title(f"Distribution of {column_to_visualize}")
    plt.xlabel(column_to_visualize)
    plt.ylabel("Count")
    plt.show()
else:
    print(f"Column '{column_to_visualize}' not found in the dataset.")

# Relationship between Sleep_Quality and Company_Support_for_Remote_Work
if "Sleep_Quality" in data.columns and "Company_Support_for_Remote_Work" in data.columns:
    grouped_data = data.groupby(["Company_Support_for_Remote_Work", "Sleep_Quality"]).size().reset_index(name="Count")
    sns.barplot(x="Company_Support_for_Remote_Work", y="Count", hue="Sleep_Quality", data=grouped_data)
    plt.title("Sleep Quality by Company Support for Remote Work")
    plt.xlabel("Company Support for Remote Work")
    plt.ylabel("Count")
    plt.legend(title="Sleep Quality")
    plt.show()
else:
    print("Required columns are not found in the dataset.")
