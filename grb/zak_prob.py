# Solving Z. Barker's Planet Sweep puzzle.
from gurobipy import *

# Data
positions = range(1, 16)
num_planets = 5
num_bombs = 3
connect_list = [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 1],  # Outer loop
                [7, 8], [8, 9], [9, 10], [10, 11], [11, 7],  # Middle loop
                [12, 13], [13, 14], [14, 15], [15, 12],  # Inner loop
                [1, 12], [2, 7], [3, 7], [4, 15], [5, 9], [6, 10], [8, 13], [11, 14]]

planet_count = [2, 5, 3, 3, 2]
colour_names = ['Purple', 'Blue', 'Green', 'Pink', 'Red']

# Problem initiate and setup
m = Model("ZakProb")
X = {}
Y = {}

# Add variables
for pos in positions:
    for colour in range(num_planets):
        # Is there a planet type colour in position pos?
        X[pos, colour] = m.addVar(vtype=GRB.BINARY)

for connection in connect_list:
    for colour in range(num_planets):
        # Is there a same colour connection on any of the links?
        Y[connection[0], connection[1], colour] = m.addVar(vtype=GRB.BINARY)

# Add the constraints

# Presets [Pu, B, G, Pi, R], some of the positions are safe to click
m.addConstr(X[3, 1] == 1)
m.addConstr(X[1, 1] == 1)
m.addConstr(X[5, 2] == 1)
m.addConstr(X[8, 3] == 1)
m.addConstr(X[11, 1] == 1)
m.addConstr(X[15, 2] == 1)

# Each position is only one colour
for pos in positions:
    m.addConstr(quicksum(X[pos, colour] for colour in range(num_planets)) == 1)

# Colour number constraint
for colour in range(num_planets):
    m.addConstr(quicksum(X[pos, colour] for pos in positions) == planet_count[colour])

# Bomb constraint
m.addConstr(quicksum(Y[connection[0], connection[1], colour] for colour in range(num_planets) for connection in
                     connect_list) == num_bombs)

# Linking of connections to planets
for colour in range(num_planets):
    for connection in connect_list:
        m.addConstr(
            Y[connection[0], connection[1], colour] <= (X[connection[0], colour] + X[connection[1], colour]) / 2)

# Objective
m.setObjective(0, GRB.MAXIMIZE)

# Solve
m.optimize()

# Print answer
for pos in positions:
    for colour in range(num_planets):
        if X[pos, colour].x == 1:
            print(f"Position {pos} is {colour_names[colour]}")

for colour in range(num_planets):
    for connection in connect_list:
        if Y[connection[0], connection[1], colour].x == 1:
            print(f"There is a bomb on connection {connection[0]} to "
                  f"{connection[1]}")

# Position 1 is Blue
# Position 2 is Red
# Position 3 is Blue
# Position 4 is Purple
# Position 5 is Green
# Position 6 is Green
# Position 7 is Purple
# Position 8 is Pink
# Position 9 is Blue
# Position 10 is Blue
# Position 11 is Blue
# Position 12 is Pink
# Position 13 is Red
# Position 14 is Pink
# Position 15 is Green
# There is a bomb on connection 9 to 10
# There is a bomb on connection 10 to 11
# There is a bomb on connection 5 to 6
