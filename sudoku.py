# Solving Sudoku puzzles using linear programming

from pulp import *
import math

# Problem specifics
n = 4 # This is an nxn sudoku, n must be a square number
problem = LpProblem("sudoku",LpMaximize)

# Decision variables
v = LpVariable.dicts("value", \
    [(row,col,val) for row in range(1, n+1) for col in range(1,n+1) \
    for val in range(1, n+1)], 0, 1, LpInteger)

# Constraints
# Each cell has only one value
for row in range(1, n+1):
    for col in range(1, n+1):
        problem += lpSum([v[row,col,val] for val in range(1,n+1)]) == 1

# Each row has one of each symbol
for row in range(1, n+1):
    for val in range(1, n+1):
        problem += lpSum([v[row,col,val] for col in range(1, n+1)]) == 1

# Each column has one of each symbol
for col in range(1, n+1):
    for val in range(1, n+1):
        problem += lpSum([v[row,col,val] for row in range(1, n+1)]) == 1

# Each box has one of each symbol
for j in range(int(math.sqrt(n))):
    for k in range(int(math.sqrt(n))):
        for val in range(1,n+1):
            problem += lpSum([v[row,col,val] for row in range(int(math.sqrt(n)*j) + 1, int(math.sqrt(n)*j) + int(math.sqrt(n))+1) \
                        for col in range(int(math.sqrt(n)*k)+1, int(math.sqrt(n)*k) + int(math.sqrt(n))+1)]) == 1

# Pre-assignments
problem += v[1,1,1] == 1
problem += v[2,4,4] == 1
problem += v[3,3,2] == 1
problem += v[4,2,3] == 1

# Objective

# Not required, arbitrary
problem += 1

# Solve and report
problem.solve()

for row in range(1,n+1):
    print([sum([k*int(v[row,col,k].varValue) for k in range(1,n+1)]) for col in range(1,n+1)])
