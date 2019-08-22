# Solves the diet problem using linear programming -
# given a list of n different foods, their costs and
# the amounts of m different nutrients in those foods,
# determine the cheapest diet satisfying a list of
# nutrional requirements.

from pulp import *
import numpy as np

# Problem specifics and setup

# Names of each food and nutrient
foods = ['Broccoli','Multigrain Bread','Carrots','Potato','Milk','Beef Mince',
     'Banana','Pasta','Pasta Sauce','Scotch Fillet','Chicken Breast',
     'White Rice','Peas','Cucumber','Cauliflower','Peach','Apple',
     'Dark Chocolate','Sweet Potato','Corn']

nutrients = ['Protein','Thiamin','VitaminB6','Folate','Vitamin C','Calcium',
     'Riboflavin','Iron','Sodium','Energy','Dietary Fibre']

num_foods = len(foods)
num_nutrients = len(nutrients)

# Cost of each food stuff
costs = [0.698,0.76,0.198,0.249,0.10,0.796,0.299,0.48,0.28,2.899,0.99,0.29,0.678,
     0.698,0.30,0.598,0.598,1.75,0.398,0.429]

# Nutritional values for each food (row) and nutrient (column)
nutrient_values = [[2320,0.063,0.2,0.108,64.9,40,0.123,0.67,41,142.12,2600],
                  [13360,0.279,0.263,0.075,0.1,103,0.131,2.5,381,1107.7,7400],
                  [930,0.066,0.138,0.019,5.9,33,0.058,0.30,69,171.38,2800],
                  [2570,0.021,0.239,0.017,11.4,0.1,0.038,3.24,10,321.86,2200],
                  [36600,0.415,0.361,0.05,6.8,1257,1.550,0.32,535,1513.16,0],
                  [20000,0.042,0.369,0.006,0,12,0.156,2.24,66,735.68,0],
                  [1090,0.031,0.367,0.020,8.7,5,0.073,0.26,1,372.02,2600],
                  [7000,0.705,0.093,0.284,0,15,0.439,3.35,26,1203.84,11000],
                  [1410,0.024,0.173,0.013,2,27,0.061,0.78,419,204.82,1800],
                  [22460,0.100,0.449,0.004,0,5,0.26,1.8,55,677.16,0],
                  [20850,0.063,0.530,0.004,0,11,0.085,0.74,63,718.96,0],
                  [2020,0.020,0.026,0.001,0,2,0.013,0.14,5,544,300],
                  [5220,0.259,0.083,0.053,18,22,0.1,1.53,108,339,5000],
                  [650,0.027,0.040,0.007,2.8,16,0.033,0.28,2,62.8,0],
                  [1920,0.050,0.184,0.057,48.2,22,0.060,0.42,30,104.5,2000],
                  [910,0.024,0.025,0.004,6.6,6,0.031,0.25,0,163.02,1500],
                  [260,0.017,0.041,0.003,4.6,6,0.026,0.12,1,217.36,2400],
                  [7790,0.034,0.038,0,0,73,0.078,11.9,20,2499.64,10900],
                  [1570,0.078,0.209,0.011,2.4,30,0.061,0.61,55,359.48,3000],
                  [2460,0.016,0.065,0.035,1.6,4,0.027,0.55,186,330.22,1900]]

# Minimum and maximum values for Recommended Daily Intake of each nutrient
# (infinity when limit not available in report)
DMIN = [64000,1.2,1.3,0.4,45,1000,1.3,8,460,11800,30000]
DMAX = ["infinity","infinity",50,1,1000,2500,"infinity",45,2300,16300,50000]

problem = LpProblem("diet", LpMinimize)

# Decision variables
v_amount = LpVariable.dicts("food amount", list(range(num_foods)), lowBound = 0, cat = 'Continuous')

# Constraints
for nutrient in range(num_nutrients):
    problem += lpSum([nutrient_values[food][nutrient]*v_amount[food] for food in range(num_foods)]) >= DMIN[nutrient]

for nutrient in [2,3,4,5,7,8,9,10]:
    problem += lpSum([nutrient_values[food][nutrient]*v_amount[food] for food in range(num_foods)]) <= DMAX[nutrient]

# Objective function
problem += lpSum([costs[k]*v_amount[k] for k in range(num_foods)])

# Solving and output
problem.solve()
print("The objective function value is", problem.objective.value())
print("The optimal diet is ", [v_amount[k].varValue for k in range(num_foods) if v_amount[k].varValue > 0.01], \
      "of", [foods[k] for k in range(num_foods) if v_amount[k].varValue > 0.01], "respectively.")
print("Not very tasty or colourful, but cheap and satisfies the nutrient requirements. Everything the body needs.")
