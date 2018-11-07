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

    cutrows = []
    allocatedCells = []
    j = 0
    while j<len(matrix[0]):
        lowestCostCell = getLowestCostCellInCol(matrix, cutrows, demand, supply, j)
        if supply[lowestCostCell[0]] == demand[lowestCostCell[1]]:
            allocatedCells.append({supply[lowestCostCell[0]]: lowestCostCell})
            demand[lowestCostCell[1]] = 0
            supply[lowestCostCell[0]] = 0
            cutrows.append(lowestCostCell[0])
        elif supply[lowestCostCell[0]] < demand[lowestCostCell[1]]:
            allocatedCells.append({supply[lowestCostCell[0]]: lowestCostCell})
            demand[lowestCostCell[1]] -= supply[lowestCostCell[0]]
            supply[lowestCostCell[0]] = 0
            cutrows.append(lowestCostCell[0])
            # calling continue is crucial, as it makes control stays at same col until full demand is allocated
            continue
        else:
            allocatedCells.append({demand[lowestCostCell[1]]: lowestCostCell})
            supply[lowestCostCell[0]] -= demand[lowestCostCell[1]]
            demand[lowestCostCell[1]] = 0
            #     don't cut row here because only demand is fully assigned not supply

        j += 1

    print(allocatedCells)
    mincost = 0
    print("Inital basic feasible solution:")
    for entry in allocatedCells:
        # each entry is a dict in itself so iterate through each item
        for cost, cell in entry.items():
            mincost += cost * matrix[int(cell[0])][int(cell[1])]
            print("x" + str(cell) + " = " + str(cost))

    print("Minimum cost  = " + str(mincost))


def getLowestCostCellInCol(matrix, cutrows, demand, supply, colIndex):
    i=0
    l = [-1, -1]
    m = 100000

    while i < len(matrix):
            if i in cutrows:
                i += 1
                continue
            if matrix[i][colIndex]<m:
                m=matrix[i][colIndex]
                # print(m)
                l[0] = i
                l[1] = colIndex
            i+=1
    # print(l)

    # means all rows are cut so min cell can not be obtained in this row
    if l[0]==-1 or l[1]==-1:
        return l

    # till now l contains index of only 1 cell having least cost

    least = [list([l[0], l[1]])]

    # now check if two or more cells has same minimum cost
    i=0
    while i < len(matrix):
        if i in cutrows:
            i += 1
            continue
        if i!=l[1] and (matrix[i][colIndex] == matrix[l[0]][l[1]]):
            least.append([i, colIndex])
        i += 1

    # now least contains indexes of all cells as list that has same min. cost,
    # but only return the index of that cell where max allocation of min(supply, demand) can be done in the cell of this row

    mini = []
    for lindex in least:
        if lindex[0]==-1 or lindex[1]==-1:
            continue
        mini.append(min(supply[lindex[0]], demand[lindex[1]]))
    return least[mini.index(max(mini))]




if __name__ == "__main__":
    main()