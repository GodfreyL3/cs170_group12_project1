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
    def expand(self):
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

        
    
    def print_puzzle(self):
        for i in range(3):
            print("")
            for j in range(3):
                if(self.matrix[i][j] == 0):
                    print("b", end = "")
                else:
                    print(self.matrix[i][j], end="")
    

class NodeQueue:

    def __init__(self):
        self.priority_queue = []

    
    def add_uniform(self, newNode):
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            return True
        

        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_uniform() < i.cost_uniform()):
                self.priority_queue.insert(iter, newNode)
                return
            iter += 1
        #  If it is not less than any of the nodes, it has low priority
        self.priority_queue.append(newNode)

        return
        
    
    def add_misplaced(self, newNode):
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            return True
        

        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_misplaced() < i.cost_misplaced()):
                self.priority_queue.insert(iter, newNode)
                return
            iter += 1
        self.priority_queue.append(newNode)

    def add_euclidian(self, newNode):
        if not self.priority_queue:
            self.priority_queue.append(newNode)
            return True
        

        iter = 0
        for i in self.priority_queue:
            if(newNode.cost_euclidian() < i.cost_euclidian()):
                self.priority_queue.insert(iter, newNode)
                return
            iter += 1
        self.priority_queue.append(newNode)

    def isEmpty(self):
        if not self.priority_queue:
            return True
        else:
            return False
    
    def pop(self):
        popped_node = self.priority_queue.pop(0)
        return popped_node

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
            print("Goal!")
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
                print("Goal!")
                print("Solved with " + str(self.expansions) + " expansions")
                nextNode.print_puzzle()
                return
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()

            print("expanding Node...")
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
            print("Goal!")
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
                print("Goal!")
                print("Solved with " + str(self.expansions) + " expansions")
                nextNode.print_puzzle()
                return
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()
            self.expansions += 1

            print("expanding Node...")

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
            print("Goal!")
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
                print("Goal!")
                print("Solved with " + str(self.expansions) + " expansions")
                nextNode.print_puzzle()
                return
            
            # Add node to explored set
            explored.append(nextNode.matrix)

            # Expand Node, add to frontier ONLY IF NOT IN EXPLORED
            new_nodes = nextNode.expand()

            print("expanding Node...")
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
    b = Node(0, [[1,2,3],
                 [7,0,8],
                 [5,6,4]], 0)
    
    tree = Tree(b)

    tree.solve_euclidian()
    


def compare_matrices(a, b):
    for i in range(3):
        for j in range(3):
            if(a[i][j] != b[i][j]):
                return False

    return True
        
    
    

if __name__ == "__main__":
    main()
