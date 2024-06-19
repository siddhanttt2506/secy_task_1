import pygame
import random

# Initialize pygame
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Prompt the user to specify the grid size and tile size
# Example input:
# Enter grid width (number of tiles): 40
# Enter grid height (number of tiles): 40
# Enter tile size (pixels): 20
GRID_WIDTH = int(input("Enter grid width (number of tiles): "))
GRID_HEIGHT = int(input("Enter grid height (number of tiles): "))
tile_pix = int(input("Enter tile size (pixels): "))

# Set the initial window dimensions
WIDTH = GRID_WIDTH * tile_pix
HEIGHT = GRID_HEIGHT * tile_pix

# Frames per second
fps_game = 60
clock = pygame.time.Clock()

# Create the game window
scr_game = pygame.display.set_mode((WIDTH, HEIGHT))

# Function to update grid dimensions based on new tile size
def update_grid_dimensions():
    global WIDTH, HEIGHT, scr_game, GRID_WIDTH, GRID_HEIGHT
    WIDTH = GRID_WIDTH * tile_pix
    HEIGHT = GRID_HEIGHT * tile_pix
    scr_game = pygame.display.set_mode((WIDTH, HEIGHT))
    print(f"Updated window size: {WIDTH}x{HEIGHT}")

# Function to generate a set of random positions on the grid
def generate(num):
    return set([(random.randrange(0, GRID_WIDTH), random.randrange(0, GRID_HEIGHT)) for _ in range(num)])

# Function to draw the grid and fill in the active positions
def make_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * tile_pix, row * tile_pix)
        pygame.draw.rect(scr_game, YELLOW, (*top_left, tile_pix, tile_pix))

    # Draw horizontal lines
    for row in range(GRID_HEIGHT):
        pygame.draw.line(scr_game, BLACK, (0, row * tile_pix), (WIDTH, row * tile_pix))
    # Draw vertical lines
    for col in range(GRID_WIDTH):
        pygame.draw.line(scr_game, BLACK, (col * tile_pix, 0), (col * tile_pix, HEIGHT))

# Function to adjust the grid based on the game rules
def adjusting_grid(positions):
    all_neighbors = set()
    new_positions = set()
    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)
        # Filter neighbors that are alive
        neighbors = list(filter(lambda x: x in positions, neighbors))
        # Keep the cell alive if it has 2 or 3 live neighbors
        if len(neighbors) in [2, 3]:
            new_positions.add(position)
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))
        # Revive the cell if it has exactly 3 live neighbors
        if len(neighbors) == 3:
            new_positions.add(position)
    return new_positions

# Function to get the neighbors of a cell
def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx >= GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy >= GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors

# Function to add a glider pattern
def add_glider(positions):
    glider = [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    for pos in glider:
        positions.add(pos)

# Function to add a block pattern
def add_block(positions):
    block = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for pos in block:
        positions.add(pos)

def main():
    global tile_pix, WIDTH, HEIGHT  # Make tile_pix, WIDTH, and HEIGHT global variables to access them inside main()
    running = True  # Game loop flag
    playing = False  # Game playing flag
    count = 0
    count_freq = 10
    generations = 0  # Generation counter

    positions = set()  # Set to store active positions
    while running:
        clock.tick(fps_game)  # Control the frame rate

        if playing:
            count += 1

        if count >= count_freq:
            count = 0
            positions = adjusting_grid(positions)
            generations += 1

        pygame.display.set_caption(f"Playing - Generations: {generations}" if playing else f"Paused - Generations: {generations}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the window is closed
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the mouse is clicked
                x, y = pygame.mouse.get_pos()
                col = x // tile_pix
                row = y // tile_pix
                pos = (col, row)
                if pos in positions:
                    positions.remove(pos)  # Remove position if it exists
                else:
                    positions.add(pos)  # Add position if it doesn't exist

            if event.type == pygame.KEYDOWN:  # Check if a key is pressed
                if event.key == pygame.K_SPACE:
                    playing = not playing  # Toggle playing state

                if event.key == pygame.K_c:
                    positions = set()  # Clear all positions and Stop playing
                    playing = False
                    count = 0
                    generations = 0

                if event.key == pygame.K_g:
                    positions = generate(random.randrange(2, 5) * GRID_WIDTH)  # Generate random positions

                if event.key == pygame.K_s and not playing:
                    positions = adjusting_grid(positions)  # Step simulation one generation forward
                    generations += 1

                if event.key == pygame.K_1:
                    add_glider(positions)  # Add predefined glider pattern

                if event.key == pygame.K_2:
                    add_block(positions)  # Add predefined block pattern

                if event.key == pygame.K_5 :
                    if tile_pix < 40:
                        tile_pix += 2  # Increase tile size (zoom in)
                        update_grid_dimensions()  # Update grid dimensions accordingly

                if event.key == pygame.K_6:
                    if tile_pix > 4:
                        tile_pix -= 2  # Decrease tile size (zoom out)
                        update_grid_dimensions()  # Update grid dimensions accordingly

        scr_game.fill(GREY)  # Fill the screen with grey background
        make_grid(positions)  # Draw the grid and cells
        pygame.display.update()  # Update the display to show changes

    pygame.quit()  # Quit pygame when exiting the main loop

if __name__ == "__main__":
    main()
