"""Solves Euler problem 68 using linear programming in Gurobi for a k-gon ring"""

from gurobipy import *

# Problem initiate and setup
m = Model("MagicRings")

# Data
k = 3
n = 2 * k
positions = range(3)
digits = range(1, n + 1)

# Add variables
Outer = {}  # Outer ring
Inner = {}  # Inner ring
for pos in positions:
    for dig in digits:
        Outer[pos, dig] = m.addVar(vtype=GRB.BINARY)
        Inner[pos, dig] = m.addVar(vtype=GRB.BINARY)

# Set objective
m.setObjective(quicksum(d * Outer[0, d] * 10**8 +
                        d * Inner[0, d] * 10**7 +
                        d * Inner[1, d] * 10**6 +
                        d * Outer[1, d] * 10**5 +
                        d * Inner[1, d] * 10**4 +
                        d * Inner[2, d] * 10**3 +
                        d * Outer[2, d] * 10**2 +
                        d * Inner[2, d] * 10**1 +
                        d * Inner[0, d] * 10**0
                        for d in digits), GRB.MAXIMIZE)

# Add the constraints

# Equality constraint a == b == c == a
m.addConstr(quicksum(d * Outer[0, d] +
                     d * Inner[0, d] +
                     d * Inner[1, d] for d in digits) ==
            quicksum(d * Outer[1, d] +
                     d * Inner[1, d] +
                     d * Inner[2, d] for d in digits) ==
            quicksum(d * Outer[2, d] +
                     d * Inner[2, d] +
                     d * Inner[0, d] for d in digits) ==
            quicksum(d * Outer[0, d] +
                     d * Inner[0, d] +
                     d * Inner[1, d] for d in digits))

# Use each position once
for pos in positions:
    m.addConstr(quicksum(Outer[pos, dig] for dig in digits) <= 1)
    m.addConstr(quicksum(Inner[pos, dig] for dig in digits) <= 1)

# Use each digit once
for dig in digits:
    m.addConstr(quicksum(Outer[pos, dig] for pos in positions) +
                quicksum(Inner[pos, dig] for pos in positions) == 1)

# Start with smallest outer digit
m.addConstr(quicksum(d * Outer[0, d] for d in digits) <= quicksum(d * Outer[1, d] for d in digits))
m.addConstr(quicksum(d * Outer[0, d] for d in digits) <= quicksum(d * Outer[2, d] for d in digits))

# Optimise
m.optimize()

# Print answer
print("Objective value is", int(m.objVal))