# This problem is the classic set covering problem - given a set of
# towns, minimize the number of fire stations if each town must be
# covered by at least one station.
from gurobipy import *

# Problem setup
covers = [[1,2], [1,2,6], [3,4], [3,4,5], [4,5,6], [2,5,6]]
num_towns = len(covers)
m = Model("Towns")

# Decision variables
StationIn = {}
for i in range(1, num_towns + 1):
    StationIn[i] = m.addVar(vtype = GRB.BINARY) # Station in town variable

# Constraints
for j in range(num_towns):
    town_list = []
    for i in range(len(covers[j])):
        town_list.append(covers[j][i])
    # Each town must be covered at least once
    m.addConstr(quicksum([StationIn[town_list[k]] for k in range(len(town_list))]) >= 1)

# Objective function
m.setObjective(quicksum([StationIn[j] for j in range(1, num_towns + 1)]), GRB.MINIMIZE)

# Solve
m.optimize()

# Print results
print("We need to build stations in", int(m.objVal), "towns", [k for k in range(1, num_towns + 1) if StationIn[k].x == 1])
