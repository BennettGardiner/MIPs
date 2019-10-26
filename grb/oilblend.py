# Solves a problem of minimising production costs associated with an
# oil refining and blending process.

# A food manufacturer refines raw oils and blends them together.
# The raw oils come in two categories – vegetable oils, of which there are two types;
# and non-vegetable oils, of which there are three types.

# The oils are refined on different production lines.
# In any month it is not possible to refine more than 200 tonnes of vegetable oil
# and more than 250 tonnes of non-vegetable oils.
# There is no loss of mass in the refining process and the cost of refining may be ignored.

# There is a technological restriction on the “hardness” of the final product.
# In the units in which hardness is measured it must lie between 3 and 6.
# The hardness of a blended product is the weighted average of its components.
# The hardness of the raw oils are:

# Oil	        Veg 1	Veg 2	Oil 1	Oil 2	Oil 3
# Hardness	    8.8	    6.1	    2.0     4.2	    5.0

# The raw oils may be purchased for immediate delivery (January)
# or bought on the futures market for delivery in subsequent months.
# Prices now and in future months are given by the following table:

# Oil	    Jan	    Feb	    Mar	    Apr	    May	    Jun
# Veg 1	    $110	$130	$110	$120	$100	$90
# Veg 2	    $120	$130	$140	$110	$120	$100
# Oil 1	    $130	$110	$130	$120	$150	$140
# Oil 2 	$110	$90	    $100	$120	$110	$80
# Oil 3	    $115	$115	$95	    $125	$105	$135

# It is possible to store up to 1000 tonnes of each raw oil for use later.
# The cost of storage is 5 per tonne per month.The final product sells for 150 per tonne.
# There are currently 500 tonnes of each raw oil in storage.
# What buying and manufacturing policy should the company pursue in order to maximise profit?

from gurobipy import *

# Problem initiate and setup
m = Model("OilBlend")

Oils = ['Veg 1', 'Veg 2', 'Oil 1', 'Oil 2', 'Oil 3']
Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June']

# Data
Hardness = [8.8, 6.1, 2.0, 4.2, 5.0]

Prices = [[110, 130, 110, 120, 100, 90],
          [120, 130, 140, 110, 120, 100],
          [130, 110, 130, 120, 150, 140],
          [110, 90, 100, 120, 110, 80],
          [115, 115, 95, 125, 105, 135]]  # Cost to buy oils each month

# Add variables
X = {}  # Purchases
Y = {}  # Usage
S = {}  # Storage
for oil in range(len(Oils)):
    for month in range(len(Months)):
        X[oil, month] = m.addVar()  # How many tonnes to purchase of each oil per month
        Y[oil, month] = m.addVar()  # How many tonnes to use of each oil per month
        S[oil, month] = m.addVar()  # How many tonnes to store of each oil per month

# Set objective
m.setObjective(quicksum(150 * Y[oil, month] - 5 * S[oil, month] - Prices[oil][month] * X[oil, month]
                        for oil in range(len(Oils)) for month in range(len(Months))), GRB.MAXIMIZE)

# Add the constraints
# Refining constraints
for month in range(len(Months)):
    m.addConstr(quicksum(Y[oil, month] for oil in range(2)) <= 200)  # Refining limit for veg oils
    m.addConstr(quicksum(Y[oil, month] for oil in range(2, len(Oils))) <= 250)  # Refining limit for normal oils

# Hardness constraints
for month in range(len(Months)):
    m.addConstr(quicksum((Hardness[oil] - 6) * Y[oil, month] for oil in range(len(Oils))) <= 0)
for month in range(len(Months)):
    m.addConstr(quicksum((Hardness[oil] - 3) * Y[oil, month] for oil in range(len(Oils))) >= 0)

# Storage constraints
for oil in range(len(Oils)):
    m.addConstr(S[oil, 0] == 500 + X[oil, 0] - Y[oil, 0])
    # m.addConstr(S[oil, len(Months) - 1] >= 500)  # optional ending constraint
for oil in range(len(Oils)):
    for month in range(1, len(Months)):
        m.addConstr(S[oil, month] == S[oil, month - 1] + X[oil, month] - Y[oil, month])
        m.addConstr(S[oil, month] <= 1000)
        # m.addConstr(S[oil, month] >= 500)  # optional made up constraint

# Optimize
m.optimize()

# Print answer
# print("Objective value is", m.objVal)
for month in range(len(Months)):
    print(f'{Months[month]} Purchases:', [X[oil, month].x for oil in range(len(Oils))])
    print(f'{Months[month]} Usages:', [Y[oil, month].x for oil in range(len(Oils))])
    print(f'{Months[month]} Storage:', [S[oil, month].x for oil in range(len(Oils))])
    print('-' * 40)