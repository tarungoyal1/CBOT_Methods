def main():

    # matrix = [[2,7,4],[3,3,1],[5,4,7],[1,6,2]]
    # demand = [7, 9, 18]
    # supply = [5,8,7,14]


    rows = int(input("Enter no. of rows:"))

    matrix = []
    for i in range(0, rows):
        matrix.append([int(x) for x in str(input("Populate row" + str(i + 1) + ":")).split()])

    demand = [int(x) for x in str(input("Enter demand list:")).split()]
    supply = [int(x) for x in str(input("Enter supply list:")).split()]

    if sum(demand) != sum(supply):
        print("!---Problem is UnBalanced---!")
        return

    cutrows = []
    cutcols = []

    allocatedCells = []
    while sum(demand)!=0 and sum(supply)!=0:
        lowestCostCell = getLowestCostCellIndex(matrix, cutrows, cutcols, demand, supply)
        if supply[lowestCostCell[0]] == demand[lowestCostCell[1]]:
            allocatedCells.append({supply[lowestCostCell[0]]: lowestCostCell})
            demand[lowestCostCell[1]] = 0
            supply[lowestCostCell[0]] = 0
            cutrows.append(lowestCostCell[0])
            cutcols.append(lowestCostCell[1])
        elif supply[lowestCostCell[0]] < demand[lowestCostCell[1]]:
            #     means allocate supply value, make it 0 and reduce it from demand
            allocatedCells.append({supply[lowestCostCell[0]]: lowestCostCell})
            demand[lowestCostCell[1]] -= supply[lowestCostCell[0]]
            supply[lowestCostCell[0]] = 0
            cutrows.append(lowestCostCell[0])
        else:
            allocatedCells.append({demand[lowestCostCell[1]]: lowestCostCell})
            supply[lowestCostCell[0]] -= demand[lowestCostCell[1]]
            demand[lowestCostCell[1]] = 0
            cutcols.append(lowestCostCell[1])

    mincost = 0
    print("Inital basic feasible solution:")
    for entry in allocatedCells:
        # each entry is a dict in itself so iterate through each item
        for cost, cell in entry.items():
            mincost += cost * matrix[int(cell[0])][int(cell[1])]
            print("x" + str(cell) + " = " + str(cost))

    print("Minimum cost  = " + str(mincost))

def getLowestCostCellIndex(matrix, cutrows, cutcols, demand, supply):
    i,j=0,0
    temp = [[-1 for _ in range(0, len(matrix[0]))] for _ in range(0, len(matrix))]
    while i< len(matrix):
        j=0
        while j<len(matrix[0]):
            if i in cutrows or j in cutcols:
                temp[i][j] = -1
            else:
                temp[i][j] = matrix[i][j]
            j+=1
        i+=1

    # print(temp)
    l=[-1,-1]
    m=100000
    i=0
    while i<len(matrix):
        j=0
        while j<len(matrix[0]):
            if temp[i][j]==-1:
                j+=1
                continue
            if temp[i][j]<m:
                l[0] = i
                l[1] = j
                m = temp[i][j]
            j+=1
        i+=1

    least = [list([l[0],l[1]])]

    i,j = 0,0
    while i< len(matrix):
        j=0
        while j<len(matrix[0]):
            if (i!=l[0] and j!=l[1]) and temp[i][j]!=-1:
                if temp[l[0]][l[1]]==temp[i][j]:

                    least.append([i,j])
            j+=1
        i+=1

    mini = []
    for lindex in least:
        mini.append(min(supply[lindex[0]], demand[lindex[1]]))

    return least[mini.index(max(mini))]

if __name__ == "__main__":
    main()