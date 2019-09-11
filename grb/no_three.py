# How many points can fit on an nxn grid if no three points are co-linear?
# import matplotlib
# matplotlib.use('tkagg')
# import matplotlib.pyplot as plt
# plt.plot([1,2,3])
# plt.show()
from gurobipy import *
import sys, time
start = time.time()
#
# Data
n = 1500

# Problem initiate and setup
m = Model("NoThree")
X = {}

# Add variables
for row in range(0, n):
    for col in range(0, n):
        X[row, col] = m.addVar(vtype=GRB.BINARY)  # Is there a point on row, col?

# Add the constraints

# There is a maximum of two points in each row
for row in range(0, n):
    m.addConstr(quicksum(X[row, col] for col in range(0, n)) <= 2)

# There is a maximum of two points in each column
for col in range(0, n):
    m.addConstr(quicksum(X[row, col] for row in range(0, n)) <= 2)

# There is a maximum of two points on each diagonal (/)
for k in range(1, n):
    m.addConstr(quicksum(X[row, k - row] for row in range(k, -1, -1)) <= 2)
for r in range(1, n - 1):
    m.addConstr(quicksum(X[row, r + n - row - 1] for row in range(n - 1, r - 1, -1)) <= 2)

# There is a maximum of two points on each diagonal (\)
for k in range(n - 2, -1, -1):
    m.addConstr(quicksum(X[row, row - k] for row in range(k, n)) <= 2)
for r in range(1, n - 1):
    m.addConstr(quicksum(X[row, row + r] for row in range(n - r)) <= 2)

# Objective
m.setObjective(quicksum(X[row, col] for row in range(n) for col in range(n)), GRB.MAXIMIZE)

# Solve
m.optimize()

# Print answer
p_locs = []
for row in range(n):
    for col in range(n):
        if X[row, col].x == 1.0:
            p_locs.append([row, col])
print(p_locs)
print(str(len(p_locs)) + f' points for n = {n}')
print(f'Solution took {time.time() - start} seconds to compute')
