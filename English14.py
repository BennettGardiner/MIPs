eng_file = open('English.txt')
eng_data = eng_file.readlines()

from pulp import *

# Problem specifics
num_letters = 8  # Restrict to 14 letters

problem = LpProblem("English14", LpMaximize)

# Decision variables
v_words = LpVariable.dicts("word_used", [k for k in range(len(eng_data))], 0, 1, LpInteger)
v_letters = LpVariable.dicts("letter_used", [m for m in range(26)], 0, 1, LpInteger)

# Constraints

# Can only use num_letters letters
problem += lpSum(v_letters[m] for m in range(26)) == num_letters

# Set up a list of the words and values
words = []
values = []
count = 0
for line in eng_data:
    word, value = line.split(',')

    if value[-1] == 'n':
        value = int(value[:-1])
    else:
        value = int(value)

    words.append(word)
    values.append(value)

    # Find unique leters in word and convert to their variable numbers
    letters = set()
    letter_sigs = []
    for k in range(len(word)):
        letters.add(word[k])
        letter_sigs.append(ord(word[k]) - 96 - 1)

    # Constraint to link words and letter variables, word will only be indicated
    # or 'switched on' if all letters are 'on'.
    problem += v_words[count] <= lpSum([v_letters[letter_sigs[k]] for k in range(len(letter_sigs))])/len(letter_sigs)

    count += 1

total_words = count - 1

# Objective function
problem += lpSum([values[k]*v_words[k] for k in range(len(eng_data))])

# Solve and print results
problem.solve()
print([words[k] for k in range(len(words)) if v_words[k].varValue == 1])
print("Objective value is", problem.objective.value())
#print([v_letters[k].varValue for k in range(26) if v_letters[k].varValue == 1])
print([v_letters[m].varValue for m in range(26)])

num_words_used = sum([v_words[k].varValue for k in range(len(words))])
print("There are", int(num_words_used), "words available.")
eng_file.close()
