"""Solves problem 351 from project Euler using linear programming in Gurobi"""
import csv
from gurobipy import *

# Problem initiate and setup
m = Model("MatSum")

# Data
matrix = []
with open('matrix.txt', 'r+') as file:
    for line in file.readlines():
        matrix.append([int(x) for x in line.split()])

RowSet = range(len(matrix))
ColSet = range(len(matrix))

# Add variables
x_vars = {(row, col): m.addVar(vtype=GRB.BINARY, name="x_{0}_{1}".format(row, col)) for row in RowSet for col in ColSet}

# Set objective
m.setObjective(quicksum([matrix[row][col] * x_vars[row, col] for row in RowSet for col in ColSet]), GRB.MAXIMIZE)

# Add the constraints
for col in ColSet:
    m.addConstr(quicksum([x_vars[row, col] for row in RowSet]) == 1)  # One value in every column
for row in RowSet:
    m.addConstr(quicksum([x_vars[row, col] for col in ColSet]) == 1)  # One value in every row

# Optimize
m.optimize()

# Print answer
print("Objective value is", m.objVal) 