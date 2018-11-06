def main():
    rows = int(input("Enter no. of rows:"))

    matrix = []
    for i in range(0, rows):
        matrix.append([int(x) for x in str(input("Populate row"+str(i+1)+":")).split()])

    demand = [int(x) for x in str(input("Enter demand list:")).split()]
    supply = [int(x) for x in str(input("Enter supply list:")).split()]

    if sum(demand) != sum(supply):
        print("!---Problem is UnBalanced---!")
        return


    i,j=0,0

    allocatedCells = []
    while i<rows:
        if supply[i]==demand[j]:
            allocatedCells.append({supply[i]: [i, j]})
            demand[j] = 0
            supply[i] = 0
            i += 1
            j += 1
        elif supply[i]<demand[j]:
            #     means allocate supply value, make it 0 and reduce it from demand
            allocatedCells.append({supply[i]: [i, j]})
            demand[j] -= supply[i]
            supply[i] = 0
            i += 1
        else:
            allocatedCells.append({demand[j]: [i, j]})
            supply[i] -= demand[j]
            demand[j] = 0
            j += 1

    mincost = 0
    print("Inital basic feasible solution:")
    for entry in allocatedCells:
        # each entry is a dict in itself so iterate through each item
        for cost, cell in entry.items():
            mincost+=cost*matrix[int(cell[0])][int(cell[1])]
            print("x"+str(cell)+" = "+str(cost))

    print("Minimum cost  = "+str(mincost))



    # print(matrix)
    # print(demand)
    # print(supply)

if __name__ == "__main__":
    main()