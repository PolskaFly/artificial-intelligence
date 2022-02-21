import sys
import os

# node class
class Node:
    def __init__(self, city=None, distance=None, cost=None):
        self.city = city
        self.distance = distance
        self.cost = cost
        self.parent = None

# reads the input file
def read_file(file):
    lines = dict()
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line != "END OF INPUT":
                line = line.split(" ")
                if line[0] not in lines:
                    lines[line[0]] = list()
                if line[1] not in lines:
                    lines[line[1]] = list()
                lines[line[0]].append((line[1], float(line[2])))
                lines[line[1]].append((line[0], float(line[2])))
            else:
                break
    return lines

# reads the heuristic file
def read_heuristic(file):
    lines = dict()
    with open(file, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line != "END OF INPUT":
                line = line.split(" ")
                lines[line[0]] = float(line[1])
            else:
                break
    return lines

# creates a node
def create_node(city=None, distance=None, cost=None):
    node = Node(city=city, distance=distance, cost=cost)
    return node

# function that does binary search for faster insertion time
def binary_search(fringe, city_node):
    l = 0
    r = len(fringe)-1

    while(l <= r):
        mid = int((l+r)/2)

        if fringe[mid].cost == city_node.cost:
            return mid

        if fringe[mid].cost > city_node.cost:
            l = mid + 1
        else:
            r = mid - 1

    return mid

# function that adds a node to the fringe
def add_to_fringe(city_node, fringe):
    if len(fringe) > 0:
        index = binary_search(fringe, city_node)
        if(fringe[index].cost > city_node.cost):
            fringe.insert(index+1, city_node)
        else:
            fringe.insert(index, city_node)
    else:
        fringe.append(city_node)

# function that expands a node
def expand_node(popped, fringe, closed, map, nodes_generated, heuristic):
    if popped.city in map:
        for city in map[popped.city]:
            # modification of UCS to be optimal. Checks if in closed
            # then replaces the last copy of the node where it is less.
            if city[0] in closed:
                index = None
                i = len(fringe) - 1
                while(i > 0):
                    if heuristic:
                        if fringe[i].city == city[0] and fringe[i].cost > city[1]+heuristic[city[0]]:
                            index = i
                    else:
                        if fringe[i].city == city[0] and fringe[i].cost > city[1]:
                            index = i
                    i -= 1

                if index:
                    if heuristic:
                        fringe[index].cost = city[1]+heuristic[city[0]]
                    else:
                        fringe[index].cost = city[1]
            else:
                nodes_generated += 1
                if heuristic:
                    new_node = create_node(city=city[0], distance=city[1], cost=city[1]+heuristic[city[0]])  
                else:
                    new_node = create_node(city=city[0], distance=city[1], cost=city[1])

                closed[city[0]] = city[0]

                new_node.parent = popped
                add_to_fringe(new_node, fringe)
    return nodes_generated

# function that initiates the ucs search
def ucs_search(start, goal, map, heuristic):
    fringe = list()
    closed = dict() # dict as check for Node will be significantly faster.
    nodes_expanded = 0
    nodes_generated = 0

    head = create_node(city=start, distance=0, cost=0)
    # add start to fringe
    fringe.append(head)

    while(True):
        if(len(fringe) == 0):
            return None, nodes_expanded, nodes_generated
        
        popped = fringe.pop()

        nodes_expanded += 1

        if popped.city == goal:
            break
        
        nodes_generated = expand_node(popped, fringe, closed, map, nodes_generated, heuristic)

    return popped, nodes_expanded, nodes_generated

# function to print all required information
def print_info(tail, nodes_expanded, nodes_generated):
    print("nodes expanded: ", nodes_expanded)
    print("nodes generated: ", nodes_generated)

    path_list = list()
    distance = 0

    if tail != None:
        while(tail != None):
            path_list.append((tail.city, tail.distance))
            distance += tail.distance
            tail = tail.parent

        print("distance: {0} km".format(distance))

        print("route:")
        while(len(path_list) > 1):
            popped = path_list.pop()
            popped2 = path_list[-1]
            print("{0} to {1}, {2} km".format(popped[0], popped2[0], str(popped2[1])))
    else:
        print("distance: infinity")
        print("route: ")
        print("none")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(0)
    route = sys.argv[1]
    start = sys.argv[2]
    goal = sys.argv[3]
    heuristic = None
    if len(sys.argv) == 5:
        heuristic = sys.argv[4]
    
    map = read_file(os.path.realpath(os.path.abspath(route)))
    if heuristic:
        heuristic = read_heuristic(os.path.realpath(os.path.abspath(heuristic)))

    output, nodes_expanded, nodes_generated = ucs_search(start, goal, map, heuristic)

    print_info(output, nodes_expanded, nodes_generated)

