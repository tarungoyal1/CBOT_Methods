def main():

    # matrix = [[4,2,7,5,2],[3,5,6,11,12],[7,1,6,7,4],[8,5,9,9,15]]
    # demand = [30,20,15,7,3]
    # supply = [20,10,30,15]


    rows = int(input("Enter no. of rows:"))

    matrix = []
    for i in range(0, rows):
        matrix.append([int(x) for x in str(input("Populate row" + str(i + 1) + ":")).split()])

    demand = [int(x) for x in str(input("Enter demand list:")).split()]
    supply = [int(x) for x in str(input("Enter supply list:")).split()]

    if sum(demand) != sum(supply):
        print("!---Problem is UnBalanced---!")
        return

    cutcols = []
    allocatedCells = []
    i=0
    while sum(demand)!=0 and sum(supply)!=0:
        lowestCostCell = getLowestCostCellInRow(matrix, cutcols, demand, supply, i)
        if supply[lowestCostCell[0]] == demand[lowestCostCell[1]]:
            allocatedCells.append({supply[lowestCostCell[0]]: lowestCostCell})
            demand[lowestCostCell[1]] = 0
            supply[lowestCostCell[0]] = 0
            cutcols.append(lowestCostCell[1])
        elif supply[lowestCostCell[0]] < demand[lowestCostCell[1]]:
            allocatedCells.append({supply[lowestCostCell[0]]: lowestCostCell})
            demand[lowestCostCell[1]] -= supply[lowestCostCell[0]]
            supply[lowestCostCell[0]] = 0
        #     don't cut column here because only supply is fully assigned not demand
        else:
            allocatedCells.append({demand[lowestCostCell[1]]: lowestCostCell})
            supply[lowestCostCell[0]] -= demand[lowestCostCell[1]]
            demand[lowestCostCell[1]] = 0
            cutcols.append(lowestCostCell[1])
            # calling continue is crucial, as it makes control stays at same row until full supply is allocated
            continue
        i += 1

    print(allocatedCells)
    mincost = 0
    print("Inital basic feasible solution:")
    for entry in allocatedCells:
        # each entry is a dict in itself so iterate through each item
        for cost, cell in entry.items():
            mincost += cost * matrix[int(cell[0])][int(cell[1])]
            print("x" + str(cell) + " = " + str(cost))

    print("Minimum cost  = " + str(mincost))



def getLowestCostCellInRow(matrix, cutcols, demand, supply, rowIndex):
    j = 0
    l = [-1, -1]
    m = 100000

    while j < len(matrix[0]):
            if j in cutcols:
                j += 1
                continue
            if matrix[rowIndex][j]<m:
                m=matrix[rowIndex][j]
                # print(m)
                l[0] = rowIndex
                l[1] = j
            j+=1
    # print(l)

    # means all cols are cut so min cell can not be obtained in this row
    if l[0]==-1 or l[1]==-1:
        return l

    # till now l contains index of only 1 cell having least cost

    least = [list([l[0], l[1]])]

    # now check if two or more cells has same minimum cost
    j=0
    while j < len(matrix[0]):
        if j in cutcols:
            j += 1
            continue
        if j!=l[1] and (matrix[rowIndex][j] == matrix[l[0]][l[1]]):
            least.append([rowIndex, j])
        j += 1

    # now least contains indexes of all cells as list that has same min. cost,
    # but only return the index of that cell where max allocation of min(supply, demand) can be done in the cell of this row

    mini = []
    for lindex in least:
        mini.append(min(supply[lindex[0]], demand[lindex[1]]))
    return least[mini.index(max(mini))]

if __name__ == "__main__":
    main()