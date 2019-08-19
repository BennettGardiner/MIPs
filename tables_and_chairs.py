 # A script to solve the tables and chairs problem using Linear Programming.

# The problem is as follows - there is a grid of (originally) 8 rows and 18 columns,
# each cell can contain a maximum of one object:
#       - a table
#       - a chair
#       - a bin
# There are bins in the two middle cells in the last row. Chairs must be next to
# at least one table, and tables cannot touch, even diagonally. Maximise the number
# of chairs.

from pulp import *

# Problem specifics and setup
num_rows = 17
num_cols = 18
TABLES_TOUCH_DIAG = False

problem = LpProblem("maximise_chairs", LpMaximize)

# Decision variables
v_chairs = LpVariable.dicts("chairs", (range(num_rows), range(num_cols)), lowBound = 0, upBound = 1, cat = LpInteger)
v_tables = LpVariable.dicts("tables", (range(num_rows), range(num_cols)), lowBound = 0, upBound = 1, cat = LpInteger)
v_bins = LpVariable.dicts("bins", (range(num_rows), range(num_cols)), lowBound = 0, upBound = 1, cat = LpInteger)

# Constraints

# Bin preassignments
problem += v_bins[6][int(num_cols/2)] == 1
problem += v_bins[6][int(num_cols/2)-1] == 1

problem += v_bins[16][int(num_cols/2)-1] == 1

# At most one object per cell
for row in range(num_rows):
    for col in range(num_cols):
        problem += v_chairs[row][col] + v_tables[row][col] + v_bins[row][col] <= 1

# Tables cannot touch
if TABLES_TOUCH_DIAG:
    # This stops tables touching vertically
    for row in range(num_rows-1):
        for col in range(num_cols):
            problem += v_tables[row][col] + v_tables[row+1][col] <= 1
    # This stops tables touching horizontally
    for row in range(num_rows):
        for col in range(num_cols-1):
                problem += v_tables[row][col] + v_tables[row][col+1] <= 1
else:
    # Check a 2x2 box (below and to the right) to check no diagonal, horizontal or vertically touching tables
    for row in range(num_rows-1):
        for col in range(num_cols-1):
            problem += v_tables[row][col] + v_tables[row+1][col] + v_tables[row][col+1] + v_tables[row+1][col+1] <= 1

# Every chair needs a table next to it

# General Case
for row in range(1,num_rows-1):
    for col in range(1,num_cols-1):
        problem += v_chairs[row][col] <= v_tables[row+1][col] + v_tables[row-1][col] + v_tables[row][col+1] + v_tables[row][col-1]

# Edge Cases
for col in range(1,num_cols-1):
    problem += v_chairs[0][col] <= v_tables[1][col] + v_tables[0][col+1] + v_tables[0][col-1]
for col in range(1,num_cols-1):
    problem += v_chairs[num_rows-1][col] <= v_tables[num_rows-2][col] + v_tables[num_rows-1][col+1] + v_tables[num_rows-1][col-1]
for row in range(1,num_rows-1):
    problem += v_chairs[row][0] <= v_tables[row+1][0] + v_tables[row-1][0] + v_tables[row][1]
for row in range(1,num_rows-1):
    problem += v_chairs[row][num_cols-1] <= v_tables[row+1][col] + v_tables[row-1][num_cols-1] + v_tables[row][num_cols-2]

# Corner Cases
problem += v_chairs[0][0] <= v_tables[1][0] + v_tables[0][1]
problem += v_chairs[num_rows-1][0] <= v_tables[num_rows-2][0] + v_tables[num_rows-1][1]
problem += v_chairs[0][num_cols-1] <= v_tables[1][num_cols-1] + v_tables[0][num_cols-2]
problem += v_chairs[num_rows-1][num_cols-1] <= v_tables[num_rows-2][num_cols-1] + v_tables[num_rows-1][num_cols-2]

# Objective function
problem += lpSum(v_chairs[row][col] for row in range(num_rows) for col in range(num_cols))

# Solving
problem.solve()
print("There are", problem.objective.value(), "chairs.")
print("There are", sum([v_tables[row][col].varValue for row in range(num_rows) for col in range(num_cols)]), 'tables.')

# Plotting
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

data_mat = np.zeros([num_rows, num_cols], dtype = int)

for row in range(num_rows):
    for col in range(num_cols):
        if v_chairs[row][col].varValue == 1:
            data_mat[row,col] = 1
        elif v_tables[row][col].varValue == 1:
            data_mat[row,col] = 2
        elif v_bins[row][col].varValue == 1:
            data_mat[row,col] = 3

print(data_mat)
# create discrete colormap
cmap = colors.ListedColormap(['white', 'red', 'blue', 'green'])
bounds = [-0.5,0.5,1.5,2.5,3.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
ax.imshow(data_mat, cmap=cmap, norm=norm)

# draw gridlines
ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
ax.set_xticks(np.arange(-.5, num_cols, 1));
ax.set_yticks(np.arange(-.5, num_rows, 1));

# turn off tick labels
ax.set_yticklabels([])
ax.set_xticklabels([])

plt.show()
