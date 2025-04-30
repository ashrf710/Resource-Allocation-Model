from pulp import LpProblem, LpMinimize, LpVariable, lpSum
import pandas as pd

# Define the problem for 15 zones
model = LpProblem("Flood_Response_Allocation_15_Zones", LpMinimize)

# Define zones
zones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]

# Define decision variables for each zone
ambulance_vars = {zone: LpVariable(f"Ambulances_{zone}", lowBound=1, cat="Integer") for zone in zones}
staff_vars = {zone: LpVariable(f"Staff_{zone}", lowBound=1, cat="Integer") for zone in zones}
supplies_vars = {zone: LpVariable(f"Supplies_{zone}", lowBound=10, cat="Integer") for zone in zones}

# Define deviation variables to handle absolute differences
dev_ambulances = {zone: LpVariable(f"Dev_Ambulances_{zone}", lowBound=0, cat="Continuous") for zone in zones}
dev_staff = {zone: LpVariable(f"Dev_Staff_{zone}", lowBound=0, cat="Continuous") for zone in zones}
dev_supplies = {zone: LpVariable(f"Dev_Supplies_{zone}", lowBound=0, cat="Continuous") for zone in zones}

# Define demand per zone from the latest data
demand = {
    "A": (3, 6, 50), "B": (2, 4, 30), "C": (1, 3, 20),
    "D": (3, 5, 40), "E": (4, 8, 60), "F": (1, 2, 15),
    "G": (1, 3, 20), "H": (4, 8, 70), "I": (2, 4, 35),
    "J": (1, 3, 25), "K": (3, 6, 55), "L": (2, 5, 40),
    "M": (4, 8, 65), "N": (1, 2, 15), "O": (1, 3, 20)
}

# Define the Objective Function (Minimizing Total Deviations)
model += lpSum(dev_ambulances[z] for z in zones) + \
         lpSum(dev_staff[z] for z in zones) + \
         lpSum(dev_supplies[z] for z in zones), "Total_Deviation"

# Enforce demand satisfaction per zone with deviation handling
for zone, (amb, staff, supply) in demand.items():
    model += (ambulance_vars[zone] - amb <= dev_ambulances[zone]), f"Amb_Dev_Pos_{zone}"
    model += (amb - ambulance_vars[zone] <= dev_ambulances[zone]), f"Amb_Dev_Neg_{zone}"
    
    model += (staff_vars[zone] - staff <= dev_staff[zone]), f"Staff_Dev_Pos_{zone}"
    model += (staff - staff_vars[zone] <= dev_staff[zone]), f"Staff_Dev_Neg_{zone}"
    
    model += (supplies_vars[zone] - supply <= dev_supplies[zone]), f"Sup_Dev_Pos_{zone}"
    model += (supply - supplies_vars[zone] <= dev_supplies[zone]), f"Sup_Dev_Neg_{zone}"

# Resource Constraints (Updated limits)
model += lpSum(ambulance_vars.values()) <= 30, "Max_Ambulances"
model += lpSum(staff_vars.values()) <= 70, "Max_Staff"
model += lpSum(supplies_vars.values()) <= 600, "Max_Supplies"

# Budget Constraint ($40,000)
model += (lpSum([500 * ambulance_vars[z] + 200 * staff_vars[z] + 10 * supplies_vars[z] for z in zones]) <= 40000), "Budget_Constraint"

# Solve the model
model.solve()

# Extract Results
allocation_results = {
    "Zone": zones,
    "Ambulances": [ambulance_vars[zone].varValue for zone in zones],
    "Staff": [staff_vars[zone].varValue for zone in zones],
    "Supplies": [supplies_vars[zone].varValue for zone in zones]
}

# Convert results to DataFrame
df_allocation = pd.DataFrame(allocation_results)
print(df_allocation)

# Save results to a CSV file
df_allocation.to_csv("15_zone_allocation.csv", index=False)
print("Results saved as 15_zone_allocation.csv")

import pandas as pd

# Load the allocation results from the CSV file (if running separately)
df_allocation = pd.read_csv("15_zone_allocation.csv")

# Define cost parameters
ambulance_cost = 500
staff_cost = 200
supplies_cost = 10
budget_limit = 40000

# Calculate cost per zone
df_allocation["Cost"] = (
    df_allocation["Ambulances"] * ambulance_cost +
    df_allocation["Staff"] * staff_cost +
    df_allocation["Supplies"] * supplies_cost
)

# Calculate total cost and remaining budget
total_cost = df_allocation["Cost"].sum()
remaining_budget = budget_limit - total_cost

# Print the cost results
print(df_allocation[["Zone", "Cost"]])
print(f"Total Cost: {total_cost}")
print(f"Remaining Budget: {remaining_budget}")
