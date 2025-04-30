# Importing necessary libraries
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import pandas as pd

# Step 1: Define the Goal Programming Problem
model = LpProblem("Flood_Emergency_Resource_Allocation", LpMinimize)

# Step 2: Define Decision Variables (Resources allocated per zone)
ambulances_A = LpVariable("Ambulances_A", lowBound=0, cat="Integer")
ambulances_B = LpVariable("Ambulances_B", lowBound=0, cat="Integer")
ambulances_C = LpVariable("Ambulances_C", lowBound=0, cat="Integer")

staff_A = LpVariable("Staff_A", lowBound=0, cat="Integer")
staff_B = LpVariable("Staff_B", lowBound=0, cat="Integer")
staff_C = LpVariable("Staff_C", lowBound=0, cat="Integer")

supplies_A = LpVariable("Supplies_A", lowBound=0, cat="Integer")
supplies_B = LpVariable("Supplies_B", lowBound=0, cat="Integer")
supplies_C = LpVariable("Supplies_C", lowBound=0, cat="Integer")

# Step 3: Define Deviation Variables for Goal Programming
d1_plus = LpVariable("d1_plus", lowBound=0, cat="Continuous")  # Overachievement of response time goal
d1_minus = LpVariable("d1_minus", lowBound=0, cat="Continuous") # Underachievement of response time goal

d2_plus = LpVariable("d2_plus", lowBound=0, cat="Continuous")  # Overachievement of resource availability
d2_minus = LpVariable("d2_minus", lowBound=0, cat="Continuous") # Underachievement of resource availability

d3_plus = LpVariable("d3_plus", lowBound=0, cat="Continuous")  # Over-budgeting
d3_minus = LpVariable("d3_minus", lowBound=0, cat="Continuous") # Under-budgeting

# Step 4: Define the Objective Function (Minimizing Total Deviations)
model += lpSum([d1_plus, d1_minus, d2_plus, d2_minus, d3_plus, d3_minus]), "Total_Deviation"

# Step 5: Define Constraints

# Demand Fulfillment Goals (Meeting required resources)
model += (ambulances_A == 3), "Ambulance_Requirement_A"
model += (ambulances_B == 2), "Ambulance_Requirement_B"
model += (ambulances_C == 1), "Ambulance_Requirement_C"

model += (staff_A == 6), "Staff_Requirement_A"
model += (staff_B == 4), "Staff_Requirement_B"
model += (staff_C == 3), "Staff_Requirement_C"

model += (supplies_A == 50), "Supplies_Requirement_A"
model += (supplies_B == 30), "Supplies_Requirement_B"
model += (supplies_C == 20), "Supplies_Requirement_C"

# Cost Constraint: Total cost must not exceed $10,000
model += (500 * (ambulances_A + ambulances_B + ambulances_C) +
          200 * (staff_A + staff_B + staff_C) +
          10 * (supplies_A + supplies_B + supplies_C) +
          d3_minus - d3_plus == 10000), "Budget_Goal"

# Resource Constraints (Ensuring allocations do not exceed available resources)
model += (ambulances_A + ambulances_B + ambulances_C <= 8), "Max_Ambulances"
model += (staff_A + staff_B + staff_C <= 20), "Max_Staff"
model += (supplies_A + supplies_B + supplies_C <= 400), "Max_Supplies"

# Solve the Model
model.solve()

# Step 6: Output Results
allocation_results = {
    "Ambulances": {
        "Zone A": ambulances_A.varValue,
        "Zone B": ambulances_B.varValue,
        "Zone C": ambulances_C.varValue,
    },
    "Staff": {
        "Zone A": staff_A.varValue,
        "Zone B": staff_B.varValue,
        "Zone C": staff_C.varValue,
    },
    "Supplies": {
        "Zone A": supplies_A.varValue,
        "Zone B": supplies_B.varValue,
        "Zone C": supplies_C.varValue,
    },
    "Deviations": {
        "Response Time (+)": d1_plus.varValue,
        "Response Time (-)": d1_minus.varValue,
        "Resources (+)": d2_plus.varValue,
        "Resources (-)": d2_minus.varValue,
        "Costs (+)": d3_plus.varValue,
        "Costs (-)": d3_minus.varValue,
    }
}

# Convert results to DataFrame and display
df_results = pd.DataFrame(allocation_results)
print(df_results)

