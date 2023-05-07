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
        for x in range(9):  # Can be changed to accomidate larger/smaller puzzles
            for i in range(3):
                for j in range(3):
                    if(self.matrix[i][j] == x):
                        if(x == 0):     # We wont take into account where "0" is into the cost
                            cost += 0
                        elif(x == 1):
                            cost += dist([i,j], [0,0])  # dist find the euclidian disnace between two points
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
    
    # Returns an list of matrices called "moves" that have all possible moves from the current nodes
    def expand(self):
        moves = []
        for i in range(3):
            for j in range(3):
                # Find position of empty spot
                if(self.matrix[i][j] == 0):
                    pos_x, pos_y = i,j
                    break

        # These if statements find if a certain move is possible, and if it is adds a new node 
        # to the moves list that represents possible movements
        next_matrix = copy.deepcopy(self.matrix)
        if(pos_x > 0):
            temp = next_matrix[pos_x - 1][pos_y]
            next_matrix[pos_x - 1][pos_y] = 0
            next_matrix[pos_x][pos_y] = temp
            moves.append(Node(self, next_matrix, self.incoming_cost + 1))

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

    # Simple print :)
    def print_puzzle(self):
        for i in range(3):
            print("")
            for j in range(3):
                if(self.matrix[i][j] == 0):
                    print("b", end = "")
                else:
                    print(self.matrix[i][j], end="")

    def print_ancestors(self):

        currNode = self
        while(currNode.parent):
            currNode.print_puzzle()
            print("\n^^^", end="")
            currNode = currNode.parent

        # FOr the top node :)
        currNode.print_puzzle()
    

# NodeQueue class Acts as a PriorityQueue specifically for our Nodes class. PriorityQueue was initially the plan,
# but there was no way to quantify the cost of a node without statically assigning the "__lt__" function to one 
# single comparator for each search method.
class NodeQueue:

    # init "queue" and the number of max nodes for the puzzle
    def __init__(self):
        self.priority_queue = []

        self.maxNodes = 0

    
    # This is why we needed our custom NodeQueue class, so we have 3 different ways to order our Nodes in the Queue
    def add_uniform(self, newNode):

        # If empty, add to front
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            self.maxNodes += 1
            return True
        


        # iter will keep track of where the iterator is pointing, and where it should insert the new Node
        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_uniform() < i.cost_uniform()):
                self.priority_queue.insert(iter, newNode)
                if(len(self.priority_queue) > self.maxNodes):
                    self.maxNodes += 1
                return
            iter += 1
        #  If it is not less than any of the nodes, it has low priority, and will appended to the end
        self.priority_queue.append(newNode)

        return
        
    
    # Other two are the same, except they use different cost functions
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

    # Checks if empty
    def isEmpty(self):
        if not self.priority_queue:
            return True
        else:
            return False
    
    # "pops" node from "queue"
    def pop(self):
        popped_node = self.priority_queue.pop(0)
        return popped_node

    # For debugging, prints all puzzles in the frontier
    def print_frontier(self):
        for i in self.priority_queue:
            i.print_puzzle()
                    
class Tree:
    def __init__(self, start):

        self.expansions = 0

        # Init starts Node
        self.start_state = start
        # Our own Node Queue for the frontier :)
        self.frontier = NodeQueue()

    def solve_uniform(self):

        if(compare_matrices(self.start_state.matrix, goal)):
            print("\n\nGoal!")
            return

        # Init searched matrices
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
                print("Max number of nodes in the queue was " + str(self.frontier.maxNodes))
                print("The depth of the goal node was " + str(nextNode.incoming_cost))
                return nextNode
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()

            print("The best state to expand with g(n) = "+ str(nextNode.incoming_cost) +" and h(n) = 0 is...")
            nextNode.print_puzzle()
            print("    expanding Node...")
            self.expansions += 1

            for node in new_nodes:
                for explored_node in explored:
                    if(compare_matrices(node.matrix,explored_node)):
                        break
                else:
                    self.frontier.add_uniform(node)
                    continue
                
                        
                    

        print("Failed")

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
                print("Max number of nodes in the queue was " + str(self.frontier.maxNodes))
                print("The depth of the goal node was " + str(nextNode.incoming_cost))
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
    elif algorithm_choice == "2":
        tree = Tree(b)
        answer = tree.solve_misplaced()
    elif algorithm_choice == "3":
        tree = Tree(b)
        answer = tree.solve_euclidian()
    else:
        print("Invalid choices")
        return

    answer.print_ancestors()


def compare_matrices(a, b):
    for i in range(3):
        for j in range(3):
            if(a[i][j] != b[i][j]):
                return False

    return True
        
    
    

if __name__ == "__main__":
    main()
