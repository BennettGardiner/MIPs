# Plots the solutions in the queensNsoln.txt files
import ast

n = 4

f = open(f"QueenSolns/queens{n}plots.txt", "w+")
f.close()

with open(f"QueenSolns/queens{n}solns.txt", "r+") as f:
    lines = f.read().splitlines()
    count = 1
    for line in lines:
        line = ast.literal_eval(line)

        board_top = 'Solution %i \n' % count + '+' + '-' * (2 * n + 1) + '+\n'
        board_bot = '+' + '-' * (2 * n + 1) + '+\n'

        line_str = ''
        for k in range(n):
            col = line[k][1]
            line_str += '|' + ' .' * col + ' Q' + ' .' * (n - col - 1) + ' |\n'

        with open(f"QueenSolns/queens{n}plots.txt", "a+") as f:
            f.write(board_top + line_str + board_bot + '\n')

        count += 1