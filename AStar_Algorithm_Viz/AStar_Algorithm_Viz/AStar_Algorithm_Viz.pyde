## Attempt to create A* Algorithm

## Globals
cols, rows = 25, 25
grid = [[0 for x in range(cols)] for y in range(rows)]

## Open set contains the nodes that may still require revisiting
## Closed set contains the nodes we do not want to revisit
open_list, closed_list = [], []

class point:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.previous = None
        self.neighbours = [] ## Each point keep track of their neighbours

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.__dict__ == other.__dict__

    def show(self, colour):
        fill(colour)
        noStroke()
        rect(self.i*w, self.j*h, w-1, h-1)

    def addNeighbours(self, grid):
        i, j = self.i, self.j
        if i < cols-1:
            self.neighbours.append(grid[i+1][j])
        if i > 0:
            self.neighbours.append(grid[i-1][j])
        if j < rows-1:
            self.neighbours.append(grid[i][j+1])
        if j > 0:
            self.neighbours.append(grid[i][j-1])

def heuristic(a, b):
    distance = dist(a.i, a.j, b.i, b.j)
    return distance

def heuristic2(a, b):
    distance = abs(a.i - b.i) + (a.j - b.j)
    return distance

def setup():
    global w
    global h
    global starting
    global ending
    global path
    ## Create Canvas
    size(400, 400)
    ## Width and height values already in processing
    w = width / cols
    h = height / rows
    path = []

    ## Create a 5x5 array, assign each point to have a function associated to it
    for i in range(cols):
        for j in range(rows):
            grid[i][j] = point(i, j)

    ## Add all the neighbours for each point
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbours(grid)

    ## Starting node and target node
    starting = grid[0][0]
    ending = grid[1][8]
    open_list.append(starting)

def draw():
    ## Since draw is already looping we can do our A* loop in here
    if open:
        winning_index = 0 ## Start from the start node
        for i in range(len(open_list)):
            if open_list[i].f < open_list[winning_index].f:
                winning_index = i

        ## Current is the node with the lowest 'f' value
        current = open_list[winning_index]

        ## Debugging - usefull to view objects
        #print(current.__dict__)
        # for att in dir(current):
        #     print (att, getattr(current,att))

        ## We have found the goal
        if current == ending:
            # Find the path
            temp = current
            path.append(temp)
            while(temp.previous):
                path.append(temp.previous)
                temp = temp.previous
            noLoop()
            print('Found the target node!')

        open_list.remove(current)
        closed_list.append(current)

        ## Track every neighbour
        neighbours = current.neighbours
        for neighbour in neighbours:
            if neighbour in closed_list:
                continue ## Ignore the neighbour which is in the closed list
            temp_g= current.g + 1

            ## Have we evaluated this node before, if so compare the new g score to the old one
            if neighbour in open_list:
                if temp_g < neighbour.g:
                    neighbour.g = temp_g
            else:
                neighbour.g = temp_g
                open_list.append(neighbour)

            neighbour.h = heuristic2(neighbour, ending)
            neighbour.f = neighbour.g + neighbour.h
            neighbour.previous = current
    else:
        ## No solution
        pass

    ## For Viz ##
    for i in range(cols):
        for j in range(rows):
            grid[i][j].show(color(255))

    for p in open_list:
        p.show(color(0, 255, 0))

    for p in closed_list:
        p.show(color(255, 0, 0))

    for p in path:
        p.show(color(255, 165, 0))
