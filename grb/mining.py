# Solves a problem of minimising costs of mining and
# delivering two good types to a set of customers,
# from a set of deposits.

from gurobipy import *

# Problem initiate and setup
m = Model("Mining")

Customers = ["C1","C2","C3"]
Deposits = ["D1","D2","D3","D4"]
I = range(len(Customers))
J = range(len(Deposits))

# Data
c = [7.4,19.6,17,13.8,8.2] # Cost per tonne of mining from deposits
u = [205000,206000,229000,173000,181000] # Mining capacity of deposits
r = [55000,45000,59000,43000,60000,46000,48000,52000,57000,58000] # Required tonnes from customers
Al = [53.5,58,57.6,58,55.6] # Al content from deposits
Si = [4.5,6,5.7,4.9,4.2] # Sil content from deposits
MinAl = [55.9,53.5,52.2,55.8,57.2,54.6,54.9,57.2,54.2,54.5] # Min Al requirement of customers
MinSi =[4.2,5.3,4.7,4.8,5.7,5.0,5.6,5.3,5.0,5.5] # Min Sil requirement of customers

# Add variables
X={}
for i in I:
    for j in J:
        X[i,j] = m.addVar() # How many tonnes to mine from deposit j to give to customer i

# Set objective
m.setObjective(quicksum(c[j]*X[i,j] for i in I for j in J), GRB.MINIMIZE)

# Add the constraints
for j in J:
    m.addConstr(quicksum(X[i,j] for i in I) <= u[j]) # Amount mined cannot exceed capacity

for i in I:
    m.addConstr(quicksum(X[i,j] for j in J) >= r[i]) # Each customer must get min required tonnage
    m.addConstr(quicksum((MinAl[i]-Al[j])*X[i,j] for j in J) <= 0) # Min Al constraint
    m.addConstr(quicksum((MinSi[i]-Si[j])*X[i,j] for j in J) <= 0) # Min Sil constraint

# Optimize
m.optimize()

# Print answer
print("Objective is", m.objVal)
for i in I:
    print("Customer %d"%(i), [X[i,j].x for j in J])
