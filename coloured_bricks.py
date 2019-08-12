bricks = ['a1', 'a2', 'a3', 'b1', 'b2',
          'c1', 'c2', 'c3', 'c4',
          'd1', 'd2', 'e1']

XSIZE = 4
YSIZE = 3
positions = [(x,y) for x in range(XSIZE) for y in range(YSIZE)]

from pulp import *

v = LpVariable.dicts("bricks", (range(XSIZE), range(YSIZE), bricks,
    range(XSIZE)), lowBound = 0, upBound = 1, cat = LpInteger)

# We want to tell PuLP to minimize the distance bricks have from their colleagues to the right.
# For that, we need to construct a penalty matrix first.
# We say that any block in column x that ought to be in colum rb has a penalty of 10 for each column in between:

m = LpProblem("Bricks", LpMinimize)

penalties = {}
for x in range(XSIZE):
    for rb in range(XSIZE):
        penalties[(x, rb)] = 10 * abs(rb - x)

# Function to minimise
m += lpSum([penalties[(x,rb)] * v[x][y][b][rb] \
    for x,y in positions for b in bricks for rb in range(XSIZE)])

# Constraint 1: one block per position
for x, y in positions:
    m += lpSum([v[x][y][b][rb] for b in bricks \
        for rb in range(XSIZE)]) <= 1

# Constraint 2: one position per brick
for b in bricks:
    m += lpSum([v[x][y][b][rb] for x, y in positions \
        for rb in range(XSIZE)]) == 1

# Condition 3: no bricks right of the rb column
for x in range(XSIZE):
    for rb in range(XSIZE):
        if x > rb:
            m += lpSum([v[x][y][b][rb] for y in range(YSIZE) \
                for b in bricks]) == 0

# Condition 4: bricks of same colour stick together
pairs = [('a1', 'a2'), ('a1', 'a3'), ('a2', 'a3'),
     ('b1', 'b2'),
     ('c1', 'c2'), ('c1', 'c3'), ('c2', 'c3'),
     ('c1', 'c4'), ('c2', 'c4'), ('c3', 'c4'),
     ('d1', 'd2')
    ]

for b1, b2 in pairs:
    for rb in range(XSIZE):
        m += lpSum([v[x][y][b1][rb] for x,y in positions] \
             + [-v[x][y][b2][rb] for x,y in positions]) == 0

# Solving
m.solve()
print("Status:", LpStatus[m.status])

for y in range(YSIZE):
    row = ""
    for x in range(XSIZE):
        for b in bricks:
            for rb in range(XSIZE):
                val = value(v[x][y][b][rb])
                if val == 1:
                    row += '{}[{}]'.format(b, rb)
        row += '\t'
    print(row)
