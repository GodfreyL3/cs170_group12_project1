from array import *
from math import dist


# set goal state, 0 represnts empty state
goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

# Node class
class Node:
    def __init__(self, matrix):
        
        # Point to parent
        #self.parent = parent

        # Store matrix state
        self.matrix = matrix

        # define distance from starting
        #self.level = parent.level + 1

        # define cost to final state

    # This function will determine the cost(distance) away from teh goal state given just the 
    # number of misplaced tiles. No matter how far, it will always be 1 if in the wrong spot,
    # and 0 if in the right spot.
    def cost_misplaced(self):
        count = 0
        for i in range(3):
            for j in range(3):
                if(self.matrix[i][j] != goal[i][j]):
                    count += 1
        return count
    
    def cost_euclidian(self):
        cost = 0
        for x in range(9):
            for i in range(3):
                for j in range(3):
                    if(self.matrix[i][j] == x):
                        if(x == 0):
                            cost += dist([i,j], [2,2])
                        elif(x == 1):
                            cost += dist([i,j], [0,0])
                        elif(x == 2):
                            cost += dist([i,j], [0,1])
                        elif(x == 3):
                            cost += dist([i,j], [0,2])
                        elif(x == 4):
                            cost += dist([i,j], [1,0])
                        elif(x == 5):
                            cost += dist([i,j], [1,1])
                        elif(x == 6):
                            cost += dist([i,j], [1,2])
                        elif(x == 7):
                            cost += dist([i,j], [2,0])
                        elif(x == 8):
                            cost += dist([i,j], [2,1])
        return cost
                    

    # This function will determine the cost(distance) away from the goal state given the
    # sum of the distances of each tile from its goal state. This will be used to determine
    # the cost of the path.
    def cost_manhattan(self):
        pass

def main():
    a = Node([[1,0,2],
              [3,4,5],
              [8,7,6]])
    print(a.cost_euclidian())
    print("Welcome to the 8 Puzzle Solver!")
    print("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle.")
    choice = input()
    if(choice == "1"):
        pass
    elif(choice == "2"):
        print("Enter your puzzle, use a zero to represent the blank")
        firstRow = input("Enter the first row, use space or tabs between numbers: \t")
        secondRow = input("Enter the second row, use space or tabs between numbers: \t")
        thirdRow = input("Enter the third row, use space or tabs between numbers: \t")
        print()
        print("Enter your choice of algorithm")
        print("Uniform Cost Search\nA* with the Misplaced Tile heuristic\nA* with the Euclidean distance heuristic\n")
        algo = input()
    else:
        print("Invalid input, please try again.")
        main()

    """
    print(f"To solve this problem the search algorithm expanded a total of {numNodes} nodes.")
    print(f"The maximum number of nodes in the queue at any one time: {maxNodes}.")
    print(f"The depth of the goal node was {depth}.")
    """

if __name__ == "__main__":
    main()
