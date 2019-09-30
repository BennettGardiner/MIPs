"""Solves Project Euler Problem 43 using linear programming in Gurobi"""

from gurobipy import *

# Problem initiate and setup
m = Model("Sub String Divisibility")

# Data
PRIME_LIST = [2, 3, 5, 7, 11, 13, 17]

# Add variables

# Let x_j be the value of the digit in position j,
# x_j \in [0,9] for j \in [1,9], x_0 \in [1,9]
x_vars = {pos: m.addVar(vtype=GRB.INTEGER, lb=0, ub=9, name="x_{0}".format(pos)) for pos in range(1, 10)}
x_vars[0] = m.addVar(vtype=GRB.INTEGER, lb=1, ub=9, name="x_0")

# Let y_{pos, val} = 1 if value val is used in position pos, and 0 otherwise
y_vars = {(pos, val): m.addVar(vtype=GRB.BINARY, name="y_{0}_{1}".format(pos, val)) for pos in range(10) for val in range(10)}

# Let k_p be the multiplier for the prime number p
k_vars = {p: m.addVar(vtype=GRB.INTEGER, lb=1, name='k_{0}'.format(p)) for p in PRIME_LIST}

# Set objective
m.setObjective(0, GRB.MINIMIZE)  # No objective for this problem, merely looking for solutions

# Add the constraints
for val in range(10):
    m.addConstr(quicksum(y_vars[pos, val] for pos in range(10)) == 1)  # Each value is used at least once
for pos in range(10):
    m.addConstr(quicksum(y_vars[pos, val] for val in range(10)) == 1)  # Each value is used only once

for pos in range(10):
   m.addConstr(quicksum(val * y_vars[pos, val] for val in range(10)) == x_vars[pos])  # Links value (x) and indicator vars (y)

# The constraints on divisibility
m.addConstr(100 * x_vars[1] + 10 * x_vars[2] + x_vars[3] == 2 * k_vars[2])
m.addConstr(100 * x_vars[2] + 10 * x_vars[3] + x_vars[4] == 3 * k_vars[3])
m.addConstr(100 * x_vars[3] + 10 * x_vars[4] + x_vars[5] == 5 * k_vars[5])
m.addConstr(100 * x_vars[4] + 10 * x_vars[5] + x_vars[6] == 7 * k_vars[7])
m.addConstr(100 * x_vars[5] + 10 * x_vars[6] + x_vars[7] == 11 * k_vars[11])
m.addConstr(100 * x_vars[6] + 10 * x_vars[7] + x_vars[8] == 13 * k_vars[13])
m.addConstr(100 * x_vars[7] + 10 * x_vars[8] + x_vars[9] == 17 * k_vars[17])

# Add in the answers
AnsList = [1406357289, 1430952867, 4130952867, 1460357289, 4160357289, 4106357289]
for ans in range(len(AnsList)):
    ans_list = [int(i) for i in str(AnsList[ans])]
    m.addConstr(quicksum(y_vars[pos, ans_list[pos]] for pos in range(10)) <= 9)

# Optimize
m.optimize()

# Print answer
print("Objective value is", m.objVal)
print("Our number is", "".join(map(str,[int(x_vars[j].x) for j in range(10)])))
# print("y values are",  [[y_vars[pos, val].x for pos in range(10)] for val in range(10)])
for p in PRIME_LIST:
    print(f'k_{p} is', k_vars[p].x)
print("Total sum of all solutions is", sum(AnsList))
