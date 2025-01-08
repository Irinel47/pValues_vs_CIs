# Step 1: Load and Inspect the Data
import pandas as pd

# Load the dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
data = pd.read_excel(url)

# Display the first few rows to understand the structure
print(data.head())

# Check for missing values
print(data.isnull().sum())

# Check basic statistics of numerical columns
print(data.describe())



# Step 2: Filter and Preprocess the Data
# Remove missing values in key columns
data = data.dropna(subset=["InvoiceDate", "Quantity", "UnitPrice"])

# Filter out rows with non-positive quantities or unit prices
data = data[(data["Quantity"] > 0) & (data["UnitPrice"] > 0)]

# Add a TotalPrice column
data["TotalPrice"] = data["Quantity"] * data["UnitPrice"]

# Remove transactions above the 99th percentile
data = data[data["TotalPrice"] <= data["TotalPrice"].quantile(0.99)]

# Check the cleaned dataset
print(data.head())


# Step 3: Define Pre- and Post-Promotion Periods (let's assume that a promotion started halfwasy thorugh the 2011 year)
# Check the earliest and latest InvoiceDate
print("Earliest Date:", data["InvoiceDate"].min())
print("Latest Date:", data["InvoiceDate"].max())

# Convert InvoiceDate to datetime
data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])

# Define pre- and post-promotion data
promotion_date = "2011-07-01"
data_pre = data[data["InvoiceDate"] < promotion_date]
data_post = data[data["InvoiceDate"] >= promotion_date]

# Print the number of transactions in each group
print("Pre-Promotion Transactions:", len(data_pre))
print("Post-Promotion Transactions:", len(data_post))


# Step 4: Explore Key Metrics
# Calculate Average Order Value (AOV) for each period
aov_pre = data_pre.groupby("InvoiceNo")["TotalPrice"].sum()
aov_post = data_post.groupby("InvoiceNo")["TotalPrice"].sum()

print("Pre-Promotion AOV:", aov_pre.mean())
print("Post-Promotion AOV:", aov_post.mean())


# Step 5: Visualize Distribution of Order Values
import matplotlib.pyplot as plt

# Plot histograms
plt.hist(aov_pre, bins=50, alpha=0.7, label="Pre-Promotion")
plt.hist(aov_post, bins=50, alpha=0.7, label="Post-Promotion")
plt.title("Distribution of Order Values: Pre- vs. Post-Promotion")
plt.xlabel("Order Value (£)")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Step 6: Calculate mean and median AOV for each period
mean_pre = aov_pre.mean()
median_pre = aov_pre.median()
mean_post = aov_post.mean()
median_post = aov_post.median()

print(f"Pre-Promotion: Mean AOV = £{mean_pre:.2f}, Median AOV = £{median_pre:.2f}")
print(f"Post-Promotion: Mean AOV = £{mean_post:.2f}, Median AOV = £{median_post:.2f}")

# Step 7: Perform a t-test for the difference in means
from scipy import stats

t_stat, p_value = stats.ttest_ind(aov_pre, aov_post)
print(f"T-Statistic: {t_stat:.2f}, P-Value: {p_value:.4f}")

# Step 8: Compute Confidence Intervals
# Calculate confidence intervals
def calculate_ci(data):
    mean = data.mean()
    sem = stats.sem(data)  # Standard error of the mean
    ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
    return mean, ci

mean_pre, ci_pre = calculate_ci(aov_pre)
mean_post, ci_post = calculate_ci(aov_post)

print(f"Pre-Promotion: Mean = £{mean_pre:.2f}, 95% CI = {ci_pre}")
print(f"Post-Promotion: Mean = £{mean_post:.2f}, 95% CI = {ci_post}")

# Step 9: Bar plot of means with error bars for 95% CI
# Data for plotting
means = [mean_pre, mean_post]

# Plot
plt.bar(["Pre-Promotion", "Post-Promotion"], means)
plt.title("Average Order Value: Pre- vs. Post-Promotion")
plt.ylabel("Average Order Value (£)")
plt.show()