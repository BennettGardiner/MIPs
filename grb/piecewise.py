"""Solves a problem using linear programming in Gurobi"""

from gurobipy import *

# Problem initiate and setup
m = Model("PWL")

# Data
# Insert problem specific data here

# Add variables

# Amounts of each oil
A = {(oil, blend): m.addVar(vtype=GRB.CONTINUOUS)
     for oil in range(1, 3)
     for blend in range(1, 3)}

# Indicators for price levels
U = {level: m.addVar(vtype=GRB.BINARY)
     for level in range(1, 4)}

# Amounts bought in each price level
X = {level: m.addVar(vtype=GRB.CONTINUOUS, ub=500)
     for level in range(1, 4)}

# Set objective
m.setObjective(1.2 * (A[1, 1] + A[2, 1])
               + 1.4 * (A[1, 2] + A[2, 2])
               - 2.5 * X[1]
               - 2 * X[2]
               - 1.5 * X[3], GRB.MAXIMIZE)

# Add the constraints

# Blending percentage constraints
m.addConstr(A[1, 1] >= A[2, 1])
m.addConstr(A[1, 2] >= 1.5 * A[2, 2])

# Oil usage constraint
m.addConstr(A[2, 1] + A[2, 2] <= 1000)
m.addConstr(A[1, 1] + A[1, 2]
            <= 500 + X[1] + X[2] + X[3])

# Linking and order constraints
m.addConstr(U[1] <= X[1] / 500)
m.addConstr(U[1] >= X[2] / 500)
m.addConstr(U[2] <= X[2] / 500)
m.addConstr(U[2] >= X[3] / 500)
m.addConstr(U[3] <= X[3] / 500)

# Optimize
m.optimize()

# Print answer
print("Objective value is", m.objVal)
print("Buy", X[1].x, "at $2.5, then",
      X[2].x, "at $2, then",
      X[3].x, "at $1.5,\nto produce",
      A[1, 1].x + A[2, 1].x, "litres of Blend 1, and",
      A[1, 2].x + A[2, 2].x, "litres of Blend 2.")
