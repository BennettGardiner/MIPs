eng_file = open('English.txt')
eng_data = eng_file.readlines()

from gurobipy import *

# Problem initiate and setup
m = Model("English14")

# Problem specifics
NUM_LETTERS = 14  # Restrict to 14 letters

LetterIn = {}
for i in range(26):
    LetterIn[i] = m.addVar(vtype = GRB.BINARY) # Letter variable

# Letter constraint
m.addConstr(quicksum(LetterIn[i] for i in range(26)) <= NUM_LETTERS)

count = 0
WordIn = {}
words = []
values = []
for line in eng_data:
    word, value = line.split(',')
    value.rstrip()
    words.append(word)
    values.append(value)
    WordIn[count] = m.addVar(vtype = GRB.BINARY) # Word variables
    
    # Find unique leters in word and convert to their variable numbers
    letters = set()
    letter_sigs = []
    for k in range(len(word)):
        letters.add(word[k])
        letter_sigs.append(ord(word[k]) - 96 - 1)
        
    # Constraint to link word and its unique letters (tight constraint)
    for n in range(len(letter_sigs)):
        m.addConstr(WordIn[count] <= LetterIn[letter_sigs[n]])
        
    # Constraint to link word and its unique letters (looser constraint)
    # m.addConstr(WordIn[count] * len(letter_sigs) <= quicksum([LetterIn[letter_sigs[k]] for k in range(len(letter_sigs))]))
    
    count += 1

# Objective function
m.setObjective(quicksum(values[k]*WordIn[k] for k in range(len(words))), GRB.MAXIMIZE)

# Optimize
m.optimize()

# Print answer
print("Objective value is", m.objVal)
print("".join([chr(k + 97 -32*int(LetterIn[k].x)) for k in range(26)]))
num_words_used = sum([WordIn[k].x for k in range(len(words))])
print("There are", int(num_words_used), "words available.")


eng_file.close()
