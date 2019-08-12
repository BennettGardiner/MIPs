# Imagine that you work for a company that builds computers.
# A computer is a fairly complex product, and there are several factories that assemble them which the company pays a certain amount per unit.
# The cost of this computer model on the market is fixed at 500$, different factories assemble the computers at different speeds and costs. Factory f0 produces 2000 per day at 450$ per unit, factory f1 1500 per day at 420$ per unit and f2 1000 per day at 400$ per unit. We have 1 month to assemble 80 000 units under the constraint that no factory is to produce more than double the units than any other factory. The question is, what is the optimal production allocation between the factories such # that we maximize the profit obtained from selling the computers under those constraints?

from pulp import *

problem = LpProblem("computer_factories", LpMaximize)

# factory cost per day
cf0 = 450
cf1 = 420
cf2 = 400

# factory throughput per day
f0 = 2000
f1 = 1500
f2 = 1000

# production goal
goal = 80000

# time limit
max_num_days = 30

num_factories = 3

# Decision Variables
factory_days = LpVariable.dicts("factoryDays", list(range(num_factories)), 0, 30, cat='Continuous')

# Constraints
c1 = factory_days[0] * f0 + factory_days[1] * f1 + factory_days[2] * f2 >= goal

c2 = factory_days[0] * f0 <= 2 * factory_days[1] * f1
c3 = factory_days[0] * f0 <= 2 * factory_days[2] * f2
c4 = factory_days[1] * f1 <= 2 * factory_days[0] * f0
c5 = factory_days[1] * f1 <= 2 * factory_days[2] * f2
c6 = factory_days[2] * f2 <= 2 * factory_days[0] * f0
c7 = factory_days[2] * f2 <= 2 * factory_days[1] * f1

problem += c1
problem += c2
problem += c3
problem += c4
problem += c5
problem += c6
problem += c7

# objective function
problem += - factory_days[0] * cf0 * f0 - factory_days[1] * cf1 * f1 - factory_days[2] * cf2 * f2

print(problem)

# solving
problem.solve()

for i in range(3):
    print(f"Factory {i}: {factory_days[i].varValue}")

z = factory_days[0].varValue * cf0 * f0 + factory_days[1].varValue * cf1 * f1 + factory_days[2].varValue * cf2 * f2
print(round(z))
