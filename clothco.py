# A company has the ability to make some number of clothing items (with each 
# item costing labour and cloth, as well as a dollar amount to make) which can
# be sold to the public. There is a limited number of hours of labour and square
# meterage of cloth, and it costs some amount to rent the individual machine which 
# produces each item (this is a once off cost). What should the company's manufacturing
# strategy entail?

from pulp import *

item_list = ["Shirts", "Shorts", "Pants"]
num_items = len(item_list)
labour_list = [3, 2, 6] # in hours
cloth_list = [4, 3, 4] # in m^2
price_list = [12, 8, 15] # in $
cost_list = [6, 4, 8] # in $
machine_cost_list = [200, 150, 100] # in $

labour_max = 150 # hours
cloth_max = 160 # m^2

profit_list = [price_list[i] - cost_list[i] for i in range(num_items)]

problem = LpProblem("clothco", LpMaximize)

# Decision Variables

# Variables for the number of items
v_items = LpVariable.dicts("num_items", list(range(num_items)), 0, cat=LpInteger)

# Variables for machine rent use, binary on/off switch
v_supp = LpVariable.dicts("machine_rent", list(range(len(item_list), 2 * len(item_list) + 1)), 0, 1, cat=LpInteger)

# Add the dictionaries together.
v_items.update(v_supp)
v = v_items

# Constraints
c1 = lpSum(labour_list[i] * v[i] for i in range(num_items)) <= labour_max
c2 = lpSum(cloth_list[i] * v[i] for i in range(num_items)) <= cloth_max

c3 = v[0] <= 40 * v[3]
c4 = v[1] <= 160/3 * v[4]
c5 = v[2] <= 25 * v[5]

problem += c1
problem += c2
problem += c3
problem += c4
problem += c5

# Objective function
problem += lpSum(profit_list[i] * v[i] for i in range(num_items)) \
            - lpSum(machine_cost_list[j-num_items] * v[j] for j in range(3,6))

print(problem)

# Solving
problem.solve()

print("ClothCo should make")
for i in range(3):
    print(f"{v[i].varValue} {item_list[i]}")

z = []
for j in range(3,6):
    if v[j].varValue == 1:
        z.append(item_list[j-3])

print("We are only using the machine/s to make", ','.join(z))

obj = sum(profit_list[i] * v[i].varValue for i in range(num_items)) \
            - sum(machine_cost_list[j-num_items] * v[j].varValue for j in range(3,6))

print(f"The profit will be ${problem.objective.value()}")
