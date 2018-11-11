from vam_method import calculateBFSusingVAM, calculateMincost
from time import sleep
from collections import Counter
from pprint import pprint


def main():
    print("MODI optimality test method:")

    # Initial data for testing

    # matrix = [[19,30,50,10],[70,30,40,60],[40,8,70,20]]
    # demand = [5,8,7,14]
    # supply = [7,9,18]
    #
    matrix = [[2,7,4],[3,3,1],[5,4,7],[1,6,2]]
    demand = [7,9,18]
    supply = [5,8,7,14]


    # rows = int(input("Enter no. of rows:"))
    #
    # matrix = []
    # for i in range(0, rows):
    #     matrix.append([int(x) for x in str(input("Populate row" + str(i + 1) + ":")).split()])
    #
    # demand = [int(x) for x in str(input("Enter demand list:")).split()]
    # supply = [int(x) for x in str(input("Enter supply list:")).split()]

    allCellsIndexList = []

    allocatedCellsDict = calculateBFSusingVAM(matrix, demand, supply)

    mincost = calculateMincost(matrix, allocatedCellsDict)

    print("Minimum cost by VAM = " + str(mincost))


    # print("Testing optimality using MODI method")
    # for i in range(0,3):
    #     print(".")
    #     sleep(1)

    # these list represent the value of ui and vj, respectively..intially all set to 0
    u = [None for _ in range(0, len(matrix))]
    v = [None for _ in range(0, len(matrix[0]))]


    rowsindex = []
    colsindex = []

#     calculate Cij = ui + vj for occupied cells

    allocCellsIndexList = []
    for entry in allocatedCellsDict:
    # each entry is a dict in itself so iterate through each item
        for cost, cell in entry.items():
            allocCellsIndexList.append(cell)
            rowsindex.append(cell[0])
            colsindex.append(cell[1])

    # at this point, rowsindex contains the indexes at row of all allocated cells
    # at this point, colsindex contains the indexes at col of all allocated cells


    # we have to make one of ui or vj = 0..based on whichever has most allocated cells
    rcnt = Counter(rowsindex)
    ccnt = Counter(colsindex)
    if rcnt.most_common()[0][0] > ccnt.most_common()[0][0]:
        #this particular has max allocation, so make u at this row = 0
        u[rcnt.most_common()[0][0]] = 0
    else:
        v[ccnt.most_common()[0][0]] = 0

    # since we have to calculate the Cij for all allocated cells..
    # we must run the counter till we find Cij for each and every cell

    allocCounter = 0

    # print(u)
    # print(v)

    # print(allocCellsIndexList)
    # print(len(allocCellsIndexList))
    while allocCounter<len(allocCellsIndexList):
        for cell in allocCellsIndexList:
            if u[cell[0]] is not None or v[cell[1]] is not None:
               if u[cell[0]] is None and  v[cell[1]] is not None:
                   u[cell[0]] = matrix[cell[0]][cell[1]] - v[cell[1]]
                   break
               elif v[cell[1]] is None and  u[cell[0]] is not None:
                   v[cell[1]] = matrix[cell[0]][cell[1]] - u[cell[0]]
                   break
        allocCounter+=1
    print("u[i] = ", u)
    print("v[j] = ", v)

    #Now check for the opportunity cost for each un-occupied cell

    # we need to have a list of indexes of unallocated cells..
    # but in order to do that..
    # we first need to have a list of all indexes of given matrix
    i=0
    while i<len(matrix):
        j=0
        while j<len(matrix[0]):
            allCellsIndexList.append([i,j])
            j+=1
        i+=1

    # print(allCellsIndexList)

    # this list will contain indexes of all unoccupied cells
    unOccupiedCells = [cell for cell in allCellsIndexList if cell not in allocCellsIndexList]


    # now we'll calculate the opportunity cost Dij for each unoccupied cell
    dij = []
    for uncell in unOccupiedCells:
        opcost = matrix[uncell[0]][uncell[1]] - (u[uncell[0]] + v[uncell[1]])
        dij.append({opcost:uncell})


    opcostlist = []
    neg = dict()
    print("Opportunity Cost ( Dij ):")
    for entry in dij:
    # each entry is a dict in itself so iterate through each item
        for opcost, cell in entry.items():
            print("D", str(cell), " = " , opcost)
            opcostlist.append(opcost)
            if opcost<0:
                neg[opcost] = cell
    if len(neg)>0:
        for negcost, cell in neg.items():
            print("Opportunity Cost = ", negcost, " < 0 at D",cell)
        print("B.F.S is not optimal..can be further improved")
    else:
        print("B.F.S is optimal")



if __name__ == "__main__":
    main()