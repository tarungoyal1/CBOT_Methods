def main():

    print("Vogel approximation method:")

    # Initial data for testing

    # matrix = [[19,30,50,10],[70,30,40,60],[40,8,70,20]]
    # demand = [5,8,7,14]
    # supply = [7,9,18]


    rows = int(input("Enter no. of rows:"))

    matrix = []
    for i in range(0, rows):
        matrix.append([int(x) for x in str(input("Populate row" + str(i + 1) + ":")).split()])

    demand = [int(x) for x in str(input("Enter demand list:")).split()]
    supply = [int(x) for x in str(input("Enter supply list:")).split()]

    allocatedCells = calculateBFSusingVAM(matrix, demand, supply)

    mintpcost = calculateMincost(matrix, allocatedCells)

    print("Minimum cost  = " + str(mintpcost))



def getCellForAllocation(matrix, cutrows, cutcols):
    """
    This method return the indices of the cell from cost matrix for the allocation is to be done
    by calculating the row and col penalty.
    The cell which corresponds to the highest penalty among the row&col will be returned.
    """

#     first calculate the row penalties by computing the difference of two least cost in the row
    rowpenalty = []
    i,j=0,0
    while i<len(matrix):
        if i in cutrows:
            rowpenalty.append(-1)
            i+=1
            continue
        # note: don't do row = matrix[i].. it will do shallow repetition
        row = [x for x in matrix[i]]
        # cut the entry in row at the index where the col is cut
        j=0
        while j<len(matrix[0]):
            if j in cutcols:
                row[j] = 1000000
            j+=1
        i+=1
        # now row has the all uncut values, where cut is 100000
        if len(row)==1:
            rowpenalty.append(row[0])
        elif len(row)>1:
            m1 = min(row)
            row.remove(m1)
            m2 = min(row)
            rowpenalty.append(abs(m1-m2))

    # at this point row penalties computed and inserted in rowpenalties list

    # now compute col penalties

    colpenalty = []
    j = 0
    while j < len(matrix[0]):
        if j in cutcols:
            colpenalty.append(-1)
            j += 1
            continue

        # here logic is slightly altered we need another loop to iterate through the
        # col entries and we make use of that same loop to insert only those values which
        # don't fall in cutrows
        i = 0
        c = []
        while i < len(matrix):
            if i in cutrows:
                c.append(1000000)
            else:
                c.append(matrix[i][j])
            i += 1
        j += 1

        col = [x for x in c]

        # now col has the all uncut values, where cut is 100000

        if len(col) == 1:
            colpenalty.append(col[0])
        elif len(row) > 1:
            m1 = min(col)
            col.remove(m1)
            m2 = min(col)
            colpenalty.append(abs(m1 - m2))

    #Now row and col panelty is computed for each iteration
    #Now we'll select the row or col wherever the panelty is highest..and the cell where cost is minimum


    cell = [-1,-1]
    maxpanelty = max(max(rowpenalty), max(colpenalty))

    if maxpanelty in rowpenalty:
        # print(maxpanelty)
        cell[0] = rowpenalty.index(maxpanelty)
        # now compute the index for col which has least cost

        k=0
        while k<len(matrix[0]):
            if k in cutcols:
                k+=1
                continue
            else:
                m = matrix[cell[0]][k]
                cell[1] = k
                break
        j = k+1
        while j < len(matrix[0]):
            if j in cutcols:
                j+=1
                continue
            if matrix[cell[0]][j] < m:
                m = matrix[cell[0]][j]
                cell[1] = j
            j += 1

    else:
        # print(maxpanelty)
        cell[1] = colpenalty.index(maxpanelty)
        # now compute the index for row which has least cost
        k = 0
        while k < len(matrix):
            if k in cutrows:
                k += 1
                continue
            else:
                m = matrix[k][cell[1]]
                cell[0] = k
                break
        i = k+1
        while i<len(matrix):
            if i in cutrows:
                i+=1
                continue
            if matrix[i][cell[1]]<m:
                m = matrix[i][cell[1]]
                cell[0]=i
            i+=1
    return cell

def calculateBFSusingVAM(matrix, demand, supply):
    if sum(demand) != sum(supply):
        print("!---Problem is UnBalanced---!")
        return

    cutrows = []
    cutcols = []

    allocatedCells = []
    while sum(demand) != 0 and sum(supply) != 0:
        lowestCostCell = getCellForAllocation(matrix, cutrows, cutcols)
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

    return allocatedCells

def calculateMincost(matrix, allocatedCells):
    mincost = 0
    print("Inital basic feasible solution:")
    for entry in allocatedCells:
        # each entry is a dict in itself so iterate through each item
        for cost, cell in entry.items():
            mincost += cost * matrix[int(cell[0])][int(cell[1])]
            print("x" + str(cell) + " = " + str(cost))

    return mincost


if __name__ == "__main__":
    main()