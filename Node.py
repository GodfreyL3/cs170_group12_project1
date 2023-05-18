from array import *
import copy
from math import dist


# set goal state, 0 represents a empty state
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

        # Store cost to get to this state
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
                if(self.matrix[i][j] == 0):
                    continue
                if(self.matrix[i][j] != goal[i][j]):
                    count += 1
        return count
    
    # Uniform cost is basically the same, without any tracking of how close we are to the goal
    def cost_uniform(self):
        return self.incoming_cost

    # Calculates euclidian distance
    def cost_euclidian(self):
        cost = 0
        for x in range(9):
            for i in range(3):
                for j in range(3):
                    if(self.matrix[i][j] == x):
                        if(x == 0):
                            cost += 0
                        elif(x == 1):
                            cost += dist([i,j], [0,0]) #calcs distance between two tiles
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
    
    # Returns an array of matrices that have all possible moves
    def expand(self):
        moves = []
        for i in range(3):
            for j in range(3):
                # Find position of empty spot
                if(self.matrix[i][j] == 0):
                    pos_x, pos_y = i,j
                    break

        # Swap positions part
        # Copy the matrix
        next_matrix = copy.deepcopy(self.matrix) 

        #check all possible moves
        #if possible, then move the performed swap to the moves array
        if(pos_x > 0):
            temp = next_matrix[pos_x - 1][pos_y] 
            next_matrix[pos_x - 1][pos_y] = 0
            next_matrix[pos_x][pos_y] = temp
            moves.append(Node(self, next_matrix, self.incoming_cost + 1))

        #repeat for all possible moves
        next_matrix = copy.deepcopy(self.matrix)
        if(pos_x < 2):
            temp = next_matrix[pos_x + 1][pos_y]
            next_matrix[pos_x + 1][pos_y] = 0
            next_matrix[pos_x][pos_y] = temp
            moves.append(Node(self, next_matrix, self.incoming_cost + 1))

        next_matrix = copy.deepcopy(self.matrix)
        if(pos_y > 0):
            temp = next_matrix[pos_x][pos_y - 1]
            next_matrix[pos_x][pos_y - 1] = 0
            next_matrix[pos_x][pos_y] = temp
            moves.append(Node(self, next_matrix, self.incoming_cost + 1))

        next_matrix = copy.deepcopy(self.matrix)
        if(pos_y < 2):
            temp = next_matrix[pos_x][pos_y + 1]
            next_matrix[pos_x][pos_y + 1] = 0
            next_matrix[pos_x][pos_y] = temp
            moves.append(Node(self, next_matrix, self.incoming_cost + 1))

        return moves

        
    #prints the puzzle in a 3x3 grid
    def print_puzzle(self):
        for i in range(3):
            print("")
            for j in range(3):
                if(self.matrix[i][j] == 0):
                    print("b", end="")
                else:
                    print(self.matrix[i][j], end="")

    #prints the puzzle in a 3x3 grid and its parents
    def print_ancestors(self):

        currNode = self
        while(currNode.parent):
            currNode.print_puzzle()
            print("\n^^^", end="")
            currNode = currNode.parent

        # FOr the top node :)
        currNode.print_puzzle()
    

class NodeQueue:
    #modified priority queue to handle nodes

    def __init__(self):
        self.priority_queue = []

        self.maxNodes = 0 #number of node in the queue at any given time

    
    def add_uniform(self, newNode):
        #if the queue is empty, just add the node
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            self.maxNodes += 1
            return True
        

        #holds the ammount of itterations we have done
        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_uniform() < i.cost_uniform()):
                self.priority_queue.insert(iter, newNode)
                #tracks how large the queue gets
                if(len(self.priority_queue) > self.maxNodes):
                    self.maxNodes += 1
                return
            iter += 1
        #  If it is not less than any of the nodes, it has low priority
        self.priority_queue.append(newNode)

        return
        
    # Adds a node to the queue based on the number of misplaced tiles

    def add_misplaced(self, newNode):
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            self.maxNodes += 1
            return True
        

        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_misplaced() + newNode.incoming_cost < i.cost_misplaced() + i.incoming_cost):
                self.priority_queue.insert(iter, newNode)
                if(len(self.priority_queue) > self.maxNodes):
                    self.maxNodes += 1
                return
            iter += 1
        self.priority_queue.append(newNode)

    def add_euclidian(self, newNode):
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            self.maxNodes += 1
            return True
        

        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_euclidian() + newNode.incoming_cost < i.cost_euclidian() + i.incoming_cost):
                self.priority_queue.insert(iter, newNode)
                if(len(self.priority_queue) > self.maxNodes):
                    self.maxNodes += 1
                return
            iter += 1
        self.priority_queue.append(newNode)

    #checks if the queue is empty
    def isEmpty(self):
        if not self.priority_queue:
            return True
        else:
            return False
    
    #returns the first node in the queue
    def pop(self):
        popped_node = self.priority_queue.pop(0)
        return popped_node

    #prints the queue
    def print_frontier(self):
        for i in self.priority_queue:
            i.print_puzzle()

# implementation of the Node class and the NodeQueue class into one tree class            
class Tree:
    def __init__(self, start):

        #how many expansions we have done
        self.expansions = 0

        # Init starts Node
        self.start_state = start
        # Our own Node Queue for the frontier :)
        self.frontier = NodeQueue()

    def solve_uniform(self):

        # inital check if the start state is the goal state
        if(compare_matrices(self.start_state.matrix, goal)):
            print("\n\nGoal!")
            return

        # Init searched matrices list of matrices
        #we cant use nodes since it can be unique
        explored = []
        explored.append(self.start_state.matrix)

        # Add first Nodes
        init_frontier = self.start_state.expand()
        for node in init_frontier:
            self.frontier.add_uniform(node)

        # search loop
        while(not self.frontier.isEmpty()):
            nextNode = self.frontier.pop()

            # Check if this is the node we are looking for 
            if(compare_matrices(nextNode.matrix, goal)):
                print("\n\nGoal!")
                print("Solved with " + str(self.expansions) + " expansions")
                nextNode.print_puzzle()
                return nextNode
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()

            # Print the node we are expanding
            print("The best state to expand with g(n) = "+ str(nextNode.incoming_cost) +" and h(n) = 0 is...")
            nextNode.print_puzzle()
            print("    expanding Node...")
            self.expansions += 1

            # Add new nodes to frontier
            for node in new_nodes:
                for explored_node in explored:
                    if(compare_matrices(node.matrix,explored_node)):
                        break
                else:
                    self.frontier.add_uniform(node)
                    continue
                
                        
                    

        print("Failed")

    #code is the same as uniform cost search, but we use the misplaced tiles cost function
    def solve_misplaced(self):

        if(compare_matrices(self.start_state.matrix, goal)):
            print("\n\nGoal!")
            return

        # Init searched matrices
        explored = []
        explored.append(self.start_state.matrix)

        # Add first Nodes
        init_frontier = self.start_state.expand()
        for node in init_frontier:
            self.frontier.add_misplaced(node)

        # search loop
        while(not self.frontier.isEmpty()):
            nextNode = self.frontier.pop()

            # Check if this is the node we are looking for 
            if(compare_matrices(nextNode.matrix, goal)):
                print("\n\nGoal!")
                print("Solved with " + str(self.expansions) + " expansions")
                print("Max number of nodes in the queue was " + str(self.frontier.maxNodes))
                print("The depth of the goal node was " + str(nextNode.incoming_cost))
                nextNode.print_puzzle()
                return nextNode
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()

            print("The best state to expand with g(n) = "+ str(nextNode.incoming_cost) +" and h(n) = " + str(nextNode.cost_misplaced()) + " is...")
            nextNode.print_puzzle()
            print("     expanding Node...")
            self.expansions += 1

            for node in new_nodes:
                for explored_node in explored:
                    if(compare_matrices(node.matrix,explored_node)):
                        break
                else:
                    self.frontier.add_misplaced(node)
                    continue
                
                        

        print("Failed")

    #code is the same as uniform cost search, but we use the euclidian distance cost function
    def solve_euclidian(self):

        if(compare_matrices(self.start_state.matrix, goal)):
            print("\n\nGoal!")
            return

        # Init searched matrices
        explored = []
        explored.append(self.start_state.matrix)

        # Add first Nodes
        init_frontier = self.start_state.expand()
        for node in init_frontier:
            self.frontier.add_euclidian(node)

        # search loop
        while(not self.frontier.isEmpty()):
            nextNode = self.frontier.pop()

            # Check if this is the node we are looking for 
            if(compare_matrices(nextNode.matrix, goal)):
                print("\n\nGoal!")
                print("Solved with " + str(self.expansions) + " expansions")
                nextNode.print_puzzle()
                return nextNode
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()

            print("The best state to expand with g(n) = "+ str(nextNode.incoming_cost) +" and h(n) = " + str(nextNode.cost_euclidian()) + " is...")
            nextNode.print_puzzle()
            print("     expanding Node...")
            self.expansions += 1

            for node in new_nodes:
                for explored_node in explored:
                    if(compare_matrices(node.matrix,explored_node)):
                        break
                else:
                    self.frontier.add_euclidian(node)
                    continue
                
                        
                    

        print("Failed")
            


# driver code
def main():

    print("Welcome to Group 12's 8 puzzle solver")
    print("Type 1 to use a default puzzle, or 2 to enter your own puzzle")
    
    choice = int(input())
    
    if choice == 1:

        b = Node(0, [[1,2,3],
                 [8,0,7],
                 [4,6,5]], 0)
        
    elif choice == 2:
        # User-defined puzzle
        print("Enter your puzzle, enter 3 at a time")
        row1 = input().split()
        row2 = input().split()
        row3 = input().split()
        puzzle = [list(map(int, row1)), list(map(int, row2)), list(map(int, row3))]
        b = Node(0, puzzle, 0)
    else:
        print("Invalid choice. Exiting program.")
        return

    
    print("Enter your choice of algorithm:")
    print("1. Uniform Cost Search")
    print("2. A* with the misplaced Tile heuristic")
    print("3. A* with the euclidean distance heuristic")

    algorithm_choice = input("Enter your algorithm choice: ")

    if algorithm_choice == "1":
        tree = Tree(b)
        answer = tree.solve_uniform()
        answer.print_ancestors()
    elif algorithm_choice == "2":
        tree = Tree(b)
        answer = tree.solve_misplaced()
        answer.print_ancestors()
    elif algorithm_choice == "3":
        tree = Tree(b)
        answer = tree.solve_euclidian()
        answer.print_ancestors()
    else:
        print("Invalid choices")
        return


def compare_matrices(a, b):
    for i in range(3):
        for j in range(3):
            if(a[i][j] != b[i][j]):
                return False

    return True
        
    
    

if __name__ == "__main__":
    main()
