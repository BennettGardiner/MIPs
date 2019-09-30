"""Attempts solving project Euler problem 164 using linear programming in Gurobi"""

from gurobipy import *
from time import time

# data
t1 = time()
digits = range(10)
p_len = 20
positions = range(p_len)
m = Model("PoolSearch")

# Variables
X = {(p, d): m.addVar(vtype=GRB.BINARY) for p in positions for d in digits}

# Constraints

# Each position used once
for p in positions:
    m.addConstr(quicksum(X[p, d] for d in digits) == 1)

# First digit cannot be zero
m.addConstr(X[0, 0] == 0)

# Three consecutive digits cannot sum to more than 9
for p in range(p_len - 2):
    m.addConstr(quicksum(d * X[p, d] + d * X[p + 1, d] + d * X[p + 2, d] for d in digits) <= 1)


# Objective function
m.setObjective(0, GRB.MINIMIZE)

# Set pooling values
m.setParam(GRB.Param.PoolSolutions, 1e9)
m.setParam(GRB.Param.PoolSearchMode, 2)

# Remove printing
m.setParam(GRB.Param.OutputFlag, 0)

# Run
m.optimize()


# Go through all solutions and get the solution
# solutions = []
# for n in range(num_solutions):
#     m.setParam(GRB.Param.SolutionNumber, n)
#     solutions.append(sum(d*10**(p_len-1-p) for (p,d), x in X.items() if x.Xn >= 0.5))
print(f"Solutions: {m.SolCount}")
t2 = time()
print(f"Time Taken: {t2-t1}s")