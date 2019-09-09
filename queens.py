# Solves the classic queens problem of find a configuration of n mutually non-
# attacking chess queens on a nxn board

from gurobipy import *

# Problem initiate and setup
m = Model("Queens")

# Data
n = 4 # n >= 4

# Add variables
X={}
for i in range(0,n):
    for j in range(0,n):
        X[i,j] = m.addVar(vtype = GRB.BINARY) # Is there a queen on row i, col j?

# Add the constraints

# There are n queens
m.addConstr(quicksum(X[row, col] for row in range(0, n) for col in range(0, n)) == n)

# There is only one queen in each row
for row in range(0,n):
    m.addConstr(quicksum(X[row, col] for col in range(0,n)) == 1)

# There is only one queen in each column
for col in range(0,n):
    m.addConstr(quicksum(X[row, col] for row in range(0,n)) == 1)

# There is only one queen on each diagonal (/)
for k in range(1, n):
    m.addConstr(quicksum(X[row, k - row] for row in range(k, -1, -1)) == 1)

for m in range(1, n - 1):
    m.addConstr(quicksum(X[row, m + n - row - 1] for row in range(n - 1, m - 1, -1)) == 1)

# There is only one queen on each diagonal (\)
for k in range(n - 2, -1, -1):
    m.addConstr(quicksum(X[row, row - k] for row in range(k, n)) == 1)

for m in range(1, n -1):
    m.addConstr(quicksum(X[row, row + m] for row in range(n - m)) == 1)

# No objective necessary

# Optimize
m.optimize()

# Print answer
for i in range(n):
    print([X[i,j].x for j in range(n)])
