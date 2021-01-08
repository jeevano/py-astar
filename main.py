import pygame

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (100, 100, 100)
DARK_GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (200, 0, 255)

WINDOW_WIDTH = 400  # width of window
WIDTH = 20          # num of cells in grid

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
pygame.display.set_caption('A* Visualizer')

# node class data structure for A* algorithm
class Node:
    def __init__(self, parent, pos_x, pos_y):
        self.parent = parent
        self.x = pos_x
        self.y = pos_y
        self.pos = [pos_x, pos_y]
        
        self.f = 0
        self.g = 0
        self.h = 0

# algorithm to solve maze
def astar(maze, start, end):
    # maze is 2d array now
    # start is [x, y] end is [x, y]
    global box_width
    
    # create nodes
    s_node = Node(None, start[0], start[1])
    e_node = Node(None, end[0], end[1])
    
    open = []
    closed = []
        
    # START OF ALGORITHM
    open.append(s_node)
    
    # while open list is nonempty
    while (len(open) > 0):
        # true when something has been drawn
        drew = False
        
        # still listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return []
                pygame.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                return []
    
        c_node = open[0]
        ind = 0
        
        # current is node with lowest f val in open list
        for j in range(len(open)):
            if (open[j].f < open[ind].f):
                c_node = open[j]
                ind = j
        
        # remove current from open and add to closed
        open.pop(ind)
        closed.append(c_node)
        if (c_node.pos != start and c_node.pos != end):
            draw(LIGHT_GREY, c_node.x, c_node.y)
            drew = True
        
        # reached end
        if (c_node.pos == e_node.pos):
            path = []
            # compute path
            temp = c_node
            while (temp != None):
                path.append(temp.pos)
                temp = temp.parent
            
            return path
        
        # compute 8 adjacent nodes of current node (c_node)
        
        #   * * * <--   (c.x - 1, c.y + 1)  (c.x, c.y + 1)  (c.x + 1, c.y + 1)
        #   * c * <--   (c.x - 1, c.y)                      (c.x + 1, c.y)
        #   * * * <--   (c.x - 1, c.y - 1)  (c.x, c.y - 1)  (c.x + 1, c.y - 1)
        adjacent = []
        for i in ([[-1, 1], [0, 1], [1, 1], [-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]]):
            a_pos_x = c_node.x + i[0]
            a_pos_y = c_node.y + i[1]
            
            # VALIDATE position
            skip = False
            # ensure with the bounds of maze, if not, skip this node
            if ((a_pos_x >= WIDTH or a_pos_y >= WIDTH) or (a_pos_x < 0 or a_pos_y < 0)):
                skip = True
            
            # if adjacent is wall on maze, skip this node
            if (not skip and maze[a_pos_y][a_pos_x] == 1):
                skip = True
            
            # if valid adjacent, add to adjacent list with current node as parent
            if not skip:
                adjacent.append(Node(c_node, a_pos_x, a_pos_y))
        
        for a in adjacent:
            # compute f , g , h of node a
            a.g = c_node.g + 1      # g is the parent node g + 1 (c_node is parent)
            a.h = abs(a.x - e_node.x) + abs(a.y - e_node.y)     # manhattan distance
            a.f = a.g + a.h         # f is sum of g and h
        
            # if node a in closed list, skip
            skip = False
            for c in closed:
                if (c.pos == a.pos):
                    skip = True
            
            # if node a already in open list but g higher skip
            for o in open:
                if ((a.pos == o.pos) and (a.g > o.g)):
                    skip = True
            
            # add current adjacent node to open list if valid
            if not skip:
                open.append(a)
                if (a.pos != start and a.pos != end):
                    draw(DARK_GREY, a.x, a.y)
                    drew = True
                    
        if drew:
            pygame.time.delay(50)

def draw(color, x, y):
    global box_width
    pygame.draw.rect(WINDOW, color, [box_width * x, box_width * y, box_width, box_width])
    pygame.display.update()

# main function for screen display
def main():
    global clock
    
    pygame.init()
    clock = pygame.time.Clock()
    WINDOW.fill(WHITE)
    running = True
    
    global box_width
    box_width = WINDOW_WIDTH // WIDTH
    
    start = None
    end = None
    grid = [[0 for i in range(WIDTH)] for j in range(WIDTH)]
    
    mode = 'start'
    solving = False
    
    while running:
        # for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row = pos[0] // box_width
                col = pos[1] // box_width
                
                # 1 denotes maze wall, 2 denotes start, 3 end, 0 path
                if (grid[col][row] == 0):
                    if (mode == 'start'):
                        grid[col][row] = 2
                        start = [row, col]
                        mode = 'end'
                    elif (mode == 'end'):
                        grid[col][row] = 3
                        end = [row, col]
                        mode = ''
                    else:
                        grid[col][row] = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                WINDOW.fill(WHITE)
                grid = [[0 for i in range(WIDTH)] for j in range(WIDTH)]
                start = None
                end = None
                mode = 'start'
                solving = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and mode == '':
                solving = True
                path = astar(grid, start, end)
                if not path == None:
                    for i in path:
                        if not (i == start or i == end):
                            draw(PURPLE, i[0], i[1])
                            pygame.time.delay(20)

        # drawing the grid
        if not solving:
            for i in range(WIDTH):
                for j in range(WIDTH):
                    color = WHITE
                    if (grid[i][j] == 1):
                        color = BLACK
                    elif (grid[i][j] == 2):
                        color = BLUE
                    elif (grid[i][j] == 3):
                        color = RED
                    pygame.draw.rect(WINDOW, color, [box_width * j, box_width * i, box_width, box_width])
    
        clock.tick(20)
        
        pygame.display.flip()
        
main()
pygame.quit()
