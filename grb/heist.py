# List of pieces which are stored within a bounding rectangle
# Each piece has two entries, one for each side
# Coded as:
#   - is a blank square
#   . is a lock
#   X is a missing square
#   | is the end of the piece
#     other letters are colours White, Blue, Red, Green

from gurobipy import *
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

# Problem initiate and setup
m = Model("Heist")
ROTATION = True
REVERSAL = True

if ROTATION and REVERSAL:
    ONE_FOUR_OR_EIGHT = 8
elif ROTATION:
    ONE_FOUR_OR_EIGHT = 4
else:
    ONE_FOUR_OR_EIGHT = 1

MAX_PIECE_LENGTH = 5


def rotate_clockwise(current_piece):
    """Rotates a piece clockwise"""
    rows = current_piece.split('|')
    num_rows = len(rows)
    num_cols = len(rows[0])

    rotated_piece = ''
    for col in range(num_cols):
        for row in rows[::-1]:
            rotated_piece += row[col]
        rotated_piece += '|'

    rotated_piece = rotated_piece.rstrip('|')
    return rotated_piece


# Data
PieceData = [
    ["-.-|"  # 1
     ".-X",
     "W-.|"
     "X.-"],
    [".XX|"  # 2
     "-.-|"
     "XX.",
     "XX-|"
     ".-.|"
     "-XX"],
    ["-.-|"  # 3
     ".XX|"
     "-XX",
     "-.-|"
     "XXW|"
     "XX-"],
    ["-X-|"  # 4
     ".-.",
     "-X-|"
     ".-R"],
    ["X.X|"  # 5
     ".-X|"
     "X.-",
     "X-X|"
     "X.-|"
     ".-X"],
    ["X.|"  # 6
     ".-|"
     "X.|"
     "X-",
     "-X|"
     ".-|"
     "-X|"
     ".X"],
    ["X.|"  # 7
     ".-|"
     "X.",
     ".X|"
     "-.|"
     "RX"],
    ["B-X|"  # 8
     "X.-|"
     "XX.",
     "X-.|"
     "-.X|"
     ".XX"],
    ["X-X|"  # 9
     "-.-|"
     "X-X",
     "X.X|"
     ".-.|"
     "X.X"],
    [".-.-.",  # 10
     ".-.-G"],
    ["X-|"  # 11
     "-.|"
     ".X|"
     "-X",
     ".X|"
     "-.|"
     "X-|"
     "X."],
    ["X.|"  # 12
     "X-|"
     "X.|"
     ".-",
     "-X|"
     ".X|"
     "-X|"
     ".-"],
    ["XX-|" # 13
     ".-B|"
     "XX-",
     "-XX|"
     ".-.|"
     "-XX"]
]

# Board Data
BData1 = [
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-.",
    ".-.-.-.-",
    "-.-.-.-R",
    ".-.-.-B-",
    "-.-.-W-."]

BData2 = [
  ".-.-.-.-",
  "-R-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-W-",
  "-.-.-.-."]

BData3 = [
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-W-",
  "-.-.-.-."]

BData4 = [
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-.",
  ".-.-.-.-",
  "-.-.-.-."]

BData = BData4
gridsize = [len(BData), len(BData[0])]
rows = range(gridsize[0])
columns = range(gridsize[1])

# Construct an invisible extended grid outside the real grid to aid in ease of calculation
ext_gridsize = [gridsize[0] + MAX_PIECE_LENGTH - 1, gridsize[1] + MAX_PIECE_LENGTH - 1]
ext_rows = range(ext_gridsize[0])
ext_columns = range(ext_gridsize[1])

# Construct the rotations and form the full piece list
AllPieceSides = []
for piece_id, piece in enumerate(PieceData):

    if ROTATION and REVERSAL:
        front = piece[0]
        front90 = rotate_clockwise(front)
        front180 = rotate_clockwise(front90)
        front270 = rotate_clockwise(front180)

        back = piece[1]
        back90 = rotate_clockwise(back)
        back180 = rotate_clockwise(back90)
        back270 = rotate_clockwise(back180)

        AllPieceSides.extend([front, front90, front180, front270,
                              back, back90, back180, back270])

    elif ROTATION:
        front = piece[0]
        front90 = rotate_clockwise(front)
        front180 = rotate_clockwise(front90)
        front270 = rotate_clockwise(front180)

        AllPieceSides.extend([front, front90, front180, front270])

    else:
        front = piece[0]

        AllPieceSides.extend([front])

num_pieces = len(PieceData)
num_piece_sides = len(AllPieceSides)
piece_sides = range(1, num_piece_sides + 1)

# Add variables

# Is this board space this piece type?
X = {(row, col, piece): m.addVar(vtype=GRB.BINARY)
     for row in ext_rows
     for col in ext_columns
     for piece in piece_sides}

# Is this board space a starting point (top left) for this piece's bounding box?
S = {(row, col, piece): m.addVar(vtype=GRB.BINARY)
     for row in rows
     for col in columns
     for piece in piece_sides}

# Add constraints

# Exactly one piece type per board space
for row in rows:
    for col in columns:
        m.addConstr(quicksum(X[row, col, piece]
                             for piece in piece_sides) == 1)

# No pieces can lie outside the grid
for row in ext_rows:
    for col in ext_columns:
        if row >= gridsize[0] or col >= gridsize[1]:
            for piece in piece_sides:
                m.addConstr(X[row, col, piece] == 0)

# Use each piece exactly once
for p in range(num_pieces):
    m.addConstr(
        quicksum(S[row, col, piece]
                 for row in rows
                 for col in columns
                 for piece in range(1 + ONE_FOUR_OR_EIGHT * p,
                                    1 + ONE_FOUR_OR_EIGHT * (p + 1))) == 1
                )

for piece_id in piece_sides:
    # Split the piece into its rows and calculate the size of the bounding box
    shape = AllPieceSides[piece_id - 1]
    split_piece = shape.split('|')
    width = len(split_piece[0])
    height = len(split_piece)

    # Calculate the indices of the blocks relative to the top left block
    piece_index = []
    for piece_row in range(len(split_piece)):
        for piece_col in range(len(split_piece[0])):
            if split_piece[piece_row][piece_col] != 'X':
                piece_index.append([piece_row, piece_col])

    for row in rows:
        for col in columns:
            for cell in piece_index:
                # This constraint relates the starting piece to the shape of the piece
                m.addConstr(
                    S[row, col, piece_id] <= X[row + cell[0], col + cell[1], piece_id]
                )
                # This constraint limits us to looking at piece positions that have
                # piece gems matching board gems
                if row + cell[0] < gridsize[0] and col + cell[1] < gridsize[1]:
                    if split_piece[cell[0]][cell[1]] == BData[row + cell[0]][col + cell[1]]:
                        continue
                    else:
                        m.addConstr(
                            S[row, col, piece_id] == 0
                        )

# Set objective
m.setObjective(0, GRB.MAXIMIZE)  # Arbitrary objective, constraint problem

# Optimize
m.optimize()

# Print answer
data = np.zeros((gridsize[0], gridsize[1]), dtype=int)
Sdata = []

for row in rows:
    for col in columns:
        for piece in piece_sides:
            if S[row, col, piece].x == 1:
                if piece % 8 <= 4:
                    Sdata.append(str(int(np.ceil(piece / ONE_FOUR_OR_EIGHT))) + 'f')
                else:
                    Sdata.append(str(int(np.ceil(piece / ONE_FOUR_OR_EIGHT))) + 'b')
            if X[row, col, piece].x == 1:
                data[row, col] = np.ceil(piece / ONE_FOUR_OR_EIGHT)

print(data)
print(Sdata)
