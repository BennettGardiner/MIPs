"""Solves a problem using linear programming in Gurobi"""

from gurobipy import *
import numpy as np

# Problem initiate and setup
m = Model("Insert model name here")

# Data
# Insert problem specific data here
M = 8
N = 58  # Number of crosses
rows = range(M)
cols = range(M)
symbols = range(2)
lines = range(2 * M + 2)

# Add variables

# Indicator variables
X = {(row, col, symbol): m.addVar(vtype=GRB.BINARY)
     for row in rows
     for col in cols
     for symbol in symbols}

# Line indicator variables, the first three are rows, second three columns,
# last two diagonals
L = {(line, symbol): m.addVar(vtype=GRB.BINARY)
     for line in lines
     for symbol in symbols}

# Add the constraints
# Exactly one symbol per cell
for row in rows:
    for col in cols:
        m.addConstr(quicksum(X[row, col, symbol]
                             for symbol in symbols) == 1)

# Number of crosses
m.addConstr(quicksum(X[row, col, 1]
                     for row in rows
                     for col in cols) == N)

for line in range(M):
    row = line
    m.addConstr(L[line, 0] <= quicksum(X[row, col, 0] for col in range(M)) / M)
    m.addConstr(L[line, 0] >= 1 - quicksum(X[row, col, 1] for col in range(M)))
    m.addConstr(L[line, 1] <= quicksum(X[row, col, 1] for col in range(M)) / M)
    m.addConstr(L[line, 1] >= 1 - quicksum(X[row, col, 0] for col in range(M)))
for line in range(M, 2 * M):
    col = line - M
    m.addConstr(L[line, 0] <= quicksum(X[row, col, 0] for row in range(M)) / M)
    m.addConstr(L[line, 0] >= 1 - quicksum(X[row, col, 1] for row in range(M)))
    m.addConstr(L[line, 1] <= quicksum(X[row, col, 1] for row in range(M)) / M)
    m.addConstr(L[line, 1] >= 1 - quicksum(X[row, col, 0] for row in range(M)))

# diagonals
m.addConstr(L[2 * M, 0] <= quicksum(X[row, row, 0] for row in range(M)) / M)
m.addConstr(L[2 * M, 0] >= 1 - quicksum(X[row, row, 1] for row in range(M)))
m.addConstr(L[2 * M, 1] <= quicksum(X[row, row, 1] for row in range(M)) / M)
m.addConstr(L[2 * M, 1] >= 1 - quicksum(X[row, row, 0] for row in range(M)))

m.addConstr(L[2 * M + 1, 0] <= quicksum(X[M-row-1, row, 0] for row in range(M)) / M)
m.addConstr(L[2 * M + 1, 0] >= 1 - quicksum(X[M-row-1, row, 1] for row in range(M)))
m.addConstr(L[2 * M + 1, 1] <= quicksum(X[M-row-1, row, 1] for row in range(M)) / M)
m.addConstr(L[2 * M + 1, 1] >= 1 - quicksum(X[M-row-1, row, 0] for row in range(M)))

# Set objective
m.setObjective(quicksum(L[line, symbol]
               for line in lines
               for symbol in symbols), GRB.MINIMIZE)

# Optimize
m.optimize()

# Print answer
print(f"With a square board of length {M} and {N} crosses,",
"there are", int(m.objVal), "lines")

board = np.zeros((M, M), dtype=str)
for row in rows:
    for col in cols:
        if X[row, col, 1].x == 1:
            board[row, col] = 'X'
        elif X[row, col, 0].x == 1:
            board[row, col] = '0'

print(board)

