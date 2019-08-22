from gurobipy import *

Ship=[
    [],
    [[1]],
    [[2,3],[4,5]],
    [[2,6,3],[4,6,5]],
    [[2,6,6,3],[4,6,6,5]],
    [[2,6,6,6,3],[4,6,6,6,5]]
]

ShipChar='0123456'
 
ColSum = [18, 2, 16, 4, 15, 4, 10, 8, 6, 15, 6, 12, 10, 8, 6, 12, 9, 13, 8, 6]
RowSum = [6, 10, 0, 12, 3, 11, 4, 5, 6, 7, 3, 10, 4, 12, 3,
          9, 6, 6, 9, 4, 8, 3, 11, 0, 11, 5, 7, 3, 7, 3]

ShipCount = [0, 23, 29, 12, 9, 7]  
D = [
 [0, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9],
 [9, 0, 9, 9, 9, 0, 9, 9, 2, 9, 9, 9, 9, 0, 9, 9, 9, 0, 9, 0],
 [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 0, 9, 9, 0, 9, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 2, 9, 9],
 [9, 0, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 6, 9, 9, 0, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 0, 9, 9, 9, 9, 9, 9, 9, 0, 0, 9, 0, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 0, 9, 9, 9, 0, 9, 9, 0, 0, 0, 0, 9, 9, 0, 9],
 [9, 9, 9, 0, 9, 0, 9, 0, 0, 9, 9, 0, 9, 9, 9, 0, 9, 9, 9, 9],
 [9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 9, 0, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 9, 3, 9, 0, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 9, 5],
 [9, 9, 0, 9, 9, 9, 9, 0, 9, 0, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 4, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 4, 9, 9, 9, 9, 9, 0, 9, 0, 9, 9, 9, 6, 9, 9, 9],
 [5, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 0, 9, 9, 9, 0, 9, 0, 9, 9],
 [9, 0, 9, 9, 9, 9, 0, 0, 9, 9, 9, 0, 9, 5, 9, 9, 0, 9, 9, 9],
 [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 0, 0, 9, 0, 9, 0, 9, 9, 9, 9, 0, 9, 0, 9, 9, 9, 9, 0, 9],
 [9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 9, 9, 9, 0, 9, 9, 9, 9, 9],
 [9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 9, 9, 9, 2, 9],
 [9, 9, 0, 9, 9, 9, 9, 5, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9],
 [9, 0, 9, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 0, 0, 0, 0, 9, 0, 0],
 [9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 0, 0, 9, 9, 9, 9]]
nRow = len(D)
Row = range(nRow)
nCol = len(D[0])
Col = range(nCol)
Len = range(1,len(ShipCount))

def PieceOK(d,i,j,l):
    # Is it OK to place a ship of length l at location i,j in orientation d
    if l == 1 and d==1:
        # Only have horizontal submarines
        return False
    # Check for running off the end, all compatible squares and surrounded by water
    if d == 0:
        if j+l > nCol:
            return False
        for ll in range(l):
            if D[i][j+ll] < 9 and D[i][j+ll] != Ship[l][d][ll]:
                return False
        for ii in range(max(0,i-1),min(i+2,nRow)):
            for jj in range(max(0,j-1),min(j+l+1,nCol)):
                ## Fail if it is not in the ship itself and it is anything except water
                if ii < i or ii > i or jj < j or jj >= j+l:
                    if D[ii][jj] < 9 and D[ii][jj] > 0:
                        return False
    else:
        if i+l > nRow:
            return False
        for ll in range(l):
            if D[i+ll][j] < 9 and D[i+ll][j] != Ship[l][d][ll]:
                return False
        for ii in range(max(0,i-1),min(i+l+1,nRow)):
            for jj in range(max(0,j-1),min(j+2,nCol)):
                ## Fail if it is not in the ship itself and it is anything except water
                if ii < i or ii >= i+l or jj < j or jj > j:
                    if D[ii][jj] < 9 and D[ii][jj] > 0:
                        return False
    return True    
    
def OverLaps(d,ii,jj,l,i,j):
    # Include a water buffer to right and below
    if d==0:
        return (ii==i or ii+1==i) and jj<=j and jj+l+1 > j
    else:
        return (jj==j or jj+1==j) and ii<=i and ii+l+1 > i

m = Model('BattleShip')

X = {(d,i,j,l): m.addVar(vtype=GRB.BINARY)
    for i in Row for j in Col for d in [0,1] for l in Len
    if PieceOK(d,i,j,l)}

Xtl = tuplelist(X)

ShipTypeCounts = {l:
    m.addConstr(quicksum(X[k] for k in Xtl.select('*','*','*',l))==ShipCount[l])
    for l in Len}
    
RowCounts = {i:
    m.addConstr(quicksum(l*X[0,i,j,l] for j in Col for l in Len 
                         if (0,i,j,l) in X)+
                quicksum(X[1,ii,j,l] for ii in Row for j in Col for l in Len
                         if ii<=i and ii+l>i and (1,ii,j,l) in X)==RowSum[i])
    for i in Row}
    
ColCounts = {j:
    m.addConstr(quicksum(l*X[1,i,j,l] for i in Row for l in Len 
                         if (1,i,j,l) in X)+
                quicksum(X[0,i,jj,l] for i in Row for jj in Col for l in Len
                         if jj<=j and jj+l>j and (0,i,jj,l) in X)==ColSum[j])
    for j in Col}
    
OneShipPerSquare = {(i,j):
    m.addConstr(quicksum(X[d,ii,jj,l] for (d,ii,jj,l) in X 
                         if OverLaps(d,ii,jj,l,i,j))<=1)
    for i in Row for j in Col}
    
for i in Row:
    for j in Col:
        if D[i][j] > 0 and D[i][j] < 9:
            OneShipPerSquare[i,j].Sense = GRB.EQUAL

m.optimize()

Answer = [[' ' for j in Col] for i in Row]
for (d,i,j,l) in X:
    if X[d,i,j,l].x > 0.9:
        if d==0:
            for ll in range(l):
                Answer[i][j+ll]=ShipChar[Ship[l][d][ll]]
        else:
            for ll in range(l):
                Answer[i+ll][j]=ShipChar[Ship[l][d][ll]]

for i in Row:
    print(''.join(Answer[i]))
    
for i in Row:
    for j in Col:
        if D[i][j] > 0 and D[i][j] < 9 and Answer[i][j]!=ShipChar[D[i][j]]:
            print(i,j,D[i][j])




