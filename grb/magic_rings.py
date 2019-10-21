"""Solves Euler problem 68 using linear programming in Gurobi for a k-gon ring"""
# Note: Currently compute in powers of 11: convert to base 11 to get the true answer
from gurobipy import *

# Problem initiate and setup
m = Model("MagicRings")

# Data
k = 5  # For a k-gon
n = 2 * k  # Number of cells (Two rings of k)
N = 3 * k  # Number of digits
positions = range(k)
digits = range(1, n + 1)

# Add variables
Outer = {}  # Outer ring
Inner = {}  # Inner ring
for pos in positions:
    for dig in digits:
        Outer[pos, dig] = m.addVar(vtype=GRB.BINARY)  # Is the number in the outer ring
        Inner[pos, dig] = m.addVar(vtype=GRB.BINARY)  # Is the number in the inner ring

# Set objective
m.setObjective(quicksum(d * Outer[incr, d] * (n+1) ** (N - 1 - 3 * incr) +
                        d * Inner[incr, d] * (n+1) ** (N - 2 - 3 * incr) +
                        d * Inner[(incr + 1) % k, d] * (n+1) ** (N - 3 - 3 * incr) for d in digits for incr in range(k)), GRB.MAXIMIZE)

# Add the constraints

# Equality constraint a == b, b == c, ..., f = g
for pos in positions:
    m.addConstr(quicksum(d * Outer[pos % k, d] +
                         d * Inner[pos % k, d] +
                         d * Inner[(pos + 1) % k, d] for d in digits) ==
                quicksum(d * Outer[(pos + 1) % k, d] +
                         d * Inner[(pos + 1) % k, d] +
                         d * Inner[(pos + 2) % k, d] for d in digits))

# Use each position at most once
for pos in positions:
    m.addConstr(quicksum(Outer[pos, dig] for dig in digits) <= 1)
    m.addConstr(quicksum(Inner[pos, dig] for dig in digits) <= 1)

# Use each digit once
for dig in digits:
    m.addConstr(quicksum(Outer[pos, dig] for pos in positions) +
                quicksum(Inner[pos, dig] for pos in positions) == 1)

# Start with smallest outer digit
for pos in positions:
    m.addConstr(quicksum(d * Outer[0, d] for d in digits) <= quicksum(d * Outer[pos, d] for d in digits))

# 10 must be in the outer loop
# if 10 in positions:
    #m.addConstr(quicksum(Inner[pos, 10] for pos in positions) == 0)

# Optimise
m.optimize()

# Print answer
print("Objective value is", int(m.objVal))