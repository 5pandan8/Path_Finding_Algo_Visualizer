import pygame
from queue import PriorityQueue
import pygame_menu

pygame.init()

# Defining the Width of our window
SIZE = 800
WIN = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Path Finding Algorithm Visualizer")

# Defining the RGB value of the colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208) 

# Defining the class whose object represent each square on our grid
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width #This represents the x cord of the top left point of the square
        self.y = col * width #This represents the y cord of the top left point of the square
        self.color = WHITE
        self.neighbors = []
        self.width = width #This represents the length of size of the square
        self.total_rows = total_rows #This is required while creating the list of neighbors for that square

    def get_pos(self): 
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win): #This function draws that particular square on the Window
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width)) #(Window, color, Cord of the square like the x and y cord of the top left point of the square and its length on each side x axis and y axis)

    def update_neighbors(self, grid):
        self.neighbors = []

        #If the mentions square is a valid square - not out of boundary and not barrier add to the neighbor list
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN 
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])

    # Comparator function for two square
    def __lt__(self, other):
        return False
    
# the function to get value of heuristic for the A star Algo, we are using Manhattan Distance (L Distance)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#draw in this function is a lambda function which draws the present state of whole grid
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# Function to implement A Star Algorithm
def aStar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False

# Function to implement BFS Algo
def bfs(draw, start, end):
    open_set = []
    came_from = {}
    open_set.append(start)
    open_set_hash = {start}
    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.pop(0)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in open_set_hash:
                came_from[neighbor] = current
                open_set.append(neighbor)
                open_set_hash.add(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False



# This function makes 2-d List of Squares forming the whole grid
def make_grid(rows, width):
    grid = []
    gap = width // rows #defining the length of each side of the square
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# This function is used to draw the grid line
def draw_grid(win, rows, width):
    gap = width // rows #defining the length of each side of the square
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i* gap)) #This Draws a line with the start and end cord (ROWS)
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j* gap, width)) #This Draws a line with the start and end cord (COLS)

# This function draws the whole grid in the present state of all the square
def draw(win, grid, rows, width):
    win.fill(WHITE)
 
    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# This function helps to get the row and col number of the square which is being clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    
    return row, col

# This is the main function of the visualization application
def visualizer(win, width):
    ROWS = 50 #Defining the number of rows required on the grid
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True

    # While loop to continues refresh the window and montior any user actions
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                # This is to ensure that the code doesn't crashed due to user clicking on a position out of the window
                if row < 0 or row > ROWS-1 or col < 0 or col > ROWS-1:
                    continue
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()
                    
            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                 # This is to ensure that the code doesn't crashed due to user clicking on a position out of the window
                if row < 0 or row > ROWS-1 or col < 0 or col > ROWS-1:
                    continue
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Here we are updating the neighbor list for each square depending on the present state of the grid
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if AlgoNum == 1:
                        aStar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    elif AlgoNum == 2:
                        bfs(lambda: draw(win, grid, ROWS, width), start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_m:
                    menu.mainloop(WIN)

    pygame.quit()

AlgoNum = 1

def set_algo(selected, value):
    global AlgoNum 
    AlgoNum = value

def start_the_game():
    visualizer(WIN, SIZE) 

mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
mytheme.background_color=(255, 255, 255, 255)
mytheme.selection_color  =(0,0,0,255)

menu = pygame_menu.Menu('Welcome', SIZE, SIZE,
                       theme=mytheme)

menu.add.selector('Algorithm :', [('A Start', 1), ('BFS', 2)], onchange=set_algo)
menu.add.button('Visualize', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

HELP1 = 'Press SPACE to Start visualization'
HELP2 = 'Press Left Mouse click to place the start, end and barrier square'
HELP3 = 'Press Right Mouse Click to reset the selected square'
HELP4 = 'Press C to clear the grid'
HELP5 = 'Press M to return to the Main Menu'

menu.add.label(" ", max_char=-1, font_size=20)
menu.add.label(" ", max_char=-1, font_size=20)
menu.add.label(HELP1, max_char=-1, font_size=20)
menu.add.label(HELP2, max_char=-1, font_size=20)
menu.add.label(HELP3, max_char=-1, font_size=20)
menu.add.label(HELP4, max_char=-1, font_size=20)
menu.add.label(HELP5, max_char=-1, font_size=20)



menu.mainloop(WIN)
