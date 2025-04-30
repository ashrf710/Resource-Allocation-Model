import pandas as pd
import matplotlib.pyplot as plt

# Load the allocation results from the CSV file (simulating the data here)
allocation_data = {
    "Zone": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
    "Ambulances": [3, 1, 1, 3, 4, 1, 1, 4, 2, 1, 3, 2, 2, 1, 1],
    "Staff": [6, 4, 3, 5, 8, 2, 3, 8, 4, 3, 6, 5, 8, 2, 3],
    "Supplies": [50, 30, 20, 40, 60, 15, 20, 70, 35, 25, 55, 40, 65, 15, 20],
    "Cost": [3200, 1600, 1300, 2900, 4200, 1050, 1300, 4300, 2150, 1350, 3250, 2400, 3250, 1050, 1300]
}

df_allocation = pd.DataFrame(allocation_data)

# Plot 1: Bar Chart - Resource Allocation Per Zone
plt.figure(figsize=(12, 6))
df_allocation.set_index("Zone")[["Ambulances", "Staff", "Supplies"]].plot(kind="bar", figsize=(12, 6))
plt.title("Resource Allocation Per Zone")
plt.ylabel("Number of Resources")
plt.xlabel("Zones")
plt.legend(title="Resources")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle="--", alpha=0.7)
plt.show()

# Plot 2: Pie Chart - Budget Distribution
plt.figure(figsize=(8, 8))
plt.pie(df_allocation["Cost"], labels=df_allocation["Zone"], autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
plt.title("Budget Allocation Per Zone")
plt.show()

# Plot 3: Bar Chart - Cost per Zone
plt.figure(figsize=(12, 6))
plt.bar(df_allocation["Zone"], df_allocation["Cost"], color="cornflowerblue", edgecolor="black")
plt.xlabel("Zones")
plt.ylabel("Cost (USD)")
plt.title("Cost Allocation Per Zone")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
