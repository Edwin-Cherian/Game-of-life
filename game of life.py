import pygame
import random
import time



# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

pygame.init()

# Define grid size and margins
rows = 100
cols = 100
width = 8
height = 8
margin = 1

running = False

# Set the width and height of the screen [width, height]
size = (cols * (width + margin), rows * (height + margin))
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")


def readable(arr):
    output = ''
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            output += str(arr[i][j]) + " , "
        output += '\n'
    return output

grid = [[0 for x in range(cols)] for y in range(rows)]

def findneighbour(position):
    row, col = position

    # print(row, col)

    neighbours = ((row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                  (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1))

    actual = []

    for i in neighbours:
        row, col = i

        if 0 <= row <= (rows - 1) and 0 <= col <= (cols - 1):
            actual.append(i)
    return actual


def update_grid(): ## manipulates array (handles the logic)
    newgrid = [[0 for i in range(cols)] for j in range(rows)]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            neighbours = findneighbour((row, col))
            count = 0
            for neighbour in neighbours:
                x, y = neighbour ## x,y are coords of the neighbour row,col is the coords of the node we are checking the neighbours of
                if grid[x][y] == 1:
                    count += 1
            #print(a,b,count)


            if grid[row][col] == 1:
                if count == 2 or count == 3:
                    newgrid[row][col] = 1
            else:
                if count == 3:
                    newgrid[row][col] = 1


    return newgrid

def update_display(): ## manipulates the screen (handles the visuals)
    for row in range(rows):
        for column in range(cols):
            if grid[row][column] == 1:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(screen, color, [margin + (margin + width) * column, margin + (margin + height) * row, width, height])
    pygame.display.flip()

def run_simulation():
    global running
    global grid
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = False
    s=time.perf_counter()
    grid = update_grid() ## updates the array of values
    screen.fill(BLACK)
    update_display() ## update the actual display
    print(1/(time.perf_counter()-s))
    clock.tick(60)

def draw_mousepos():
    pressed = pygame.mouse.get_pressed()
    if pressed[0]:
        pos = pygame.mouse.get_pos()
        x, y = pos
        column = x // (width + margin)
        row = y // (height + margin)
        # Debug prints
        #print("Click ", pos, "Grid coordinates: ", row, column)
        grid[row][column] = 1
    elif pressed[2]:
        pos = pygame.mouse.get_pos()
        x, y = pos
        column = x // (width + margin)
        row = y // (height + margin)
        #print("Click ", pos, "Grid coordinates: ", row, column)
        grid[row][column] = 0

def event_handeler():
    global done
    global running
    global grid
    if event.type == pygame.QUIT: # If user clicked close
        done = True # Flag that we are done so we exit this loop

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            running = True

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            grid = [[0 for i in range(cols)] for j in range(rows)]


    if event.type == pygame.KEYDOWN: ## generates random grid 10%,20% and 30% depending on if 1,2 or 3 is clicked
        if event.key == pygame.K_1:
            grid = [[1 if random.random() < 0.1 else 0 for i in range(cols)] for j in range(rows)]
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_2:
            grid = [[1 if random.random() < 0.2 else 0 for i in range(cols)] for j in range(rows)]
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_3:
            grid = [[1 if random.random() < 0.3 else 0 for i in range(cols)] for j in range(rows)]

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): # User did something
        event_handeler()

        draw_mousepos() # places black square where mouse is being moved


        # --- start simulation
        while running:
            run_simulation()

    screen.fill(BLACK)
    update_display()

    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit()