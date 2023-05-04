from array import *
import copy
from math import dist
from queue import PriorityQueue


# set goal state, 0 represnts empty state
goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]

# Node class
class Node:
    def __init__(self, parent, matrix, incoming_cost):
        
        # Point to parent
        self.parent = parent

        # Store matrix state
        self.matrix = matrix

        self.incoming_cost = incoming_cost

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
        return count + self.incoming_cost
    
    # Uniform cost is basically the same, without any tracking of how long it toook to get to a certain noide
    def cost_uniform(self):
        cost = 0
        for i in range(3):
            for j in range(3):
                if(self.matrix[i][j] != goal[i][j]):
                    cost += 1
        return cost

    # Calculates euclidian distance
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
        return cost + self.incoming_cost
    
    # Returns an array of matrices that have all possible moves
    def possible_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                # Find position of empty spot
                if(self.matrix[i][j] == 0):
                    pos_x, pos_y = i,j
                    break

        # Swap positions
        next_matrix = copy.deepcopy(self.matrix)
        if(pos_x > 0):
            temp = next_matrix[i - 1][j]
            next_matrix[i - 1][j] = 0
            next_matrix[i][j] = temp
            moves.append(next_matrix)

        next_matrix = copy.deepcopy(self.matrix)
        if(pos_x < 2):
            temp = next_matrix[i + 1][j]
            next_matrix[i + 1][j] = 0
            next_matrix[i][j] = temp
            moves.append(next_matrix)

        next_matrix = copy.deepcopy(self.matrix)
        if(pos_y > 0):
            temp = next_matrix[i][j - 1]
            next_matrix[i][j - 1] = 0
            next_matrix[i][j] = temp
            moves.append(next_matrix)

        next_matrix = copy.deepcopy(self.matrix)
        if(pos_y < 2):
            temp = next_matrix[i][j + 1]
            next_matrix[i][j + 1] = 0
            next_matrix[i][j] = temp
            moves.append(next_matrix)

        return moves
    
    def __repr__(self) -> str:
        pass
    
    def print_puzzle(self):
        for i in range(3):
            print("")
            for j in range(3):
                if(self.matrix[i][j] == 0):
                    print("b", end = "")
                else:
                    print(self.matrix[i][j], end="")
    
class Problem:
    def __init__(self, starting_matrix):

        #   Start node will be from 0
        self.starting_state = Node(0, starting_matrix, 0)

        # Create our priority Queue for our frontier
        self.frontier = PriorityQueue()


    def solve_uniform():
        



    




                    

def main():
    a = Node(0, [[2,1,3],
                 [4,0,6],
                 [7,0,8]], 1)
    
    print(a.possible_moves())
    
    

if __name__ == "__main__":
    main()
