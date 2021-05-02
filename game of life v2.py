import numpy as np
import pygame
import time


## <-------GRID SETUP------->
ROWS = 200
COLS = 200
tilewidth = 4
tileheight = 4
margin = 0
mygrid = np.zeros((ROWS,COLS))
mygrid = np.pad(mygrid,1,constant_values=0) ##pads the array so that it can be shifted later


#----WINDOW SETTINGS---->
WIDTH = (COLS+2)*(tilewidth+margin)
HEIGHT = (ROWS+2)*(tileheight+margin)


#<----COLOURS---->
WHITE = (255,255,255)
BLACK = (0,0,0)


#<----SETUP PYGAME WINDOW---->
pygame.init()
pygame.display.set_caption("Game of Life V3")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60
running = False


##<-------FUNCTIONS------->
def event_handler():
    global run
    global running
    global mygrid
    global changes
    global index

    if event.type == pygame.QUIT:
        run = False
        running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r: ## reset grid and display
            screen.fill(BLACK)
            mygrid = np.zeros((ROWS,COLS))
            mygrid = np.pad(mygrid,1,constant_values=0)

        elif event.key == pygame.K_q: ## create random grid and update display
            screen.fill(BLACK)
            mygrid = np.random.randint(2,size=(ROWS,COLS))
            mygrid = np.pad(mygrid,1,constant_values=0)
            changes=[]
            index=0
            full_update_display(mygrid)

        elif event.key == pygame.K_KP_PLUS: ## runs a single step in the simulation
            changes=[]
            index=0
            mygrid = update_mygrid(mygrid)

        else:
            running = not running ## starts/stops running program

    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        pos = pygame.mouse.get_pos()
        x, y = pos
        column = x // (tilewidth + margin)
        row = y // (tileheight + margin)
        mygrid[row,column] = 1
        cell = pygame.Rect([margin + (margin + tilewidth) * column, margin + (margin + tileheight) * row, tilewidth, tileheight])
        pygame.draw.rect(screen, WHITE, cell)
        pygame.display.update(cell)

    elif pressed[2]:
        pos = pygame.mouse.get_pos()
        x, y = pos
        column = x // (tilewidth + margin)
        row = y // (tileheight + margin)
        mygrid[row,column] = 0
        cell = pygame.Rect([margin + (margin + tilewidth) * column, margin + (margin + tileheight) * row, tilewidth, tileheight])
        pygame.draw.rect(screen, BLACK, cell)
        pygame.display.update(cell)


def get_shifted(grid):
    ulshift = np.roll(grid,(-1,-1),axis=(0,1))
    ushift = np.roll(grid,(-1,0),axis=(0,1))
    urshift = np.roll(grid,(-1,1),axis=(0,1))
    rshift = np.roll(grid,(0,1),axis=(0,1))
    drshift = np.roll(grid,(1,1),axis=(0,1))
    dshift = np.roll(grid,(1,0),axis=(0,1))
    dlshift = np.roll(grid,(1,-1),axis=(0,1))
    lshift = np.roll(grid,(0,-1),axis=(0,1))
    shifted_grids = np.array([ulshift,ushift,urshift,rshift,drshift,dshift,dlshift,lshift])
    return shifted_grids


def update_cell(state, neighbours):
    if state == 1: ## if cell is alive
        if neighbours == 2 or neighbours == 3:
            return 1
    else: ## if cell is dead
        if neighbours == 3:
            return 1
    return 0
update_cell = np.frompyfunc(update_cell, 2, 1) ##converts function into a ufunc


def update_mygrid(grid):
    shifted_grids = get_shifted(grid)
    neighbour_grid = shifted_grids[:,1:-1,1:-1].sum(0).flatten() ##for each cell it gets the number of living neighbours this array is then flattened into a 1d array
    newgrid = grid[1:-1,1:-1].flatten() ##unpads array and flattens into a 1d array
    newgrid = update_cell(newgrid, neighbour_grid).reshape(ROWS, COLS)
    newgrid = np.pad(newgrid, 1, constant_values=0)
    update_display(grid.flatten(), newgrid.flatten())
    pygame.display.update()
    return newgrid


index = 0
changes = []
def update_display(grid, newgrid):
    global index
    global changes

    if newgrid != grid:
        if newgrid == 1:
            color = WHITE
        else:
            color = BLACK
        row = index//(COLS+2) ## this is the number of WHOLE columns that would fit aka row index
        column = index%(COLS+2) ## this is the remainder when you try to divide by column length aka column index
        cell = pygame.Rect([margin + (margin+tilewidth)*column, margin + (margin+tileheight)*row, tilewidth, tileheight])
        pygame.draw.rect(screen, color, cell)
        changes.append(cell)
    index +=1
update_display = np.frompyfunc(update_display, 2, 0) ##converts function into a ufunc

def full_update_display(newgrid):
    for row in range(ROWS):
        for column in range(COLS):
            if newgrid[row][column] == 1:
                color = WHITE
            else:
                color = BLACK
            pygame.draw.rect(screen, color, [margin + (margin + tilewidth) * column, margin + (margin + tileheight) * row, tilewidth, tileheight])
    pygame.display.flip()

#<----RUN PROGRAM IN PYGAME---->
run = True
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        event_handler()

    while running: ## running the actual simulation
        for event in pygame.event.get():
            event_handler()

        s=time.perf_counter()
        mygrid = update_mygrid(mygrid) ##updates grid and display once
        index=0 ##resets variables used to update grid
        changes=[]
        print(1/(time.perf_counter()-s))

    pygame.display.update()