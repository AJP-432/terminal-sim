import pygame
from constants import *

class Drawer:
    _instance = None

    @staticmethod
    def get_instance():
        if Drawer._instance is None:
            Drawer()
        return Drawer._instance

    def __init__(self):
        if Drawer._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Drawer._instance = self

        # Initialize Pygame
        pygame.init()

        # Set up the display
        self.WIDTH, self.HEIGHT = 800, 800  # You can adjust the size as needed
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tower Defense Game Board")

        # Define the dot size and color
        self.DOT_RADIUS = 3
        self.DOT_COLOR = (255, 255, 255)  # White

        # Calculate the grid cell size
        self.CELL_SIZE = self.WIDTH // ARENA_SIZE

        # Assuming get_edges() returns a list of lists of [x, y] pairs
        edges = get_edges()

        # Flatten the list while keeping the pairs as tuples
        flattened_list = [item for sublist in edges for item in sublist]
        paired_list = [tuple(item) for item in flattened_list]

        # Store the pairs as tuples in a set
        self.edge_locations = set(paired_list)

    def draw_board(self):
        """Draw the board with dots representing valid locations."""
        self.win.fill((0, 0, 0))  # Clear the screen with black

        for y in range(ARENA_SIZE):
            for x in range(ARENA_SIZE):
                if is_in_bounds((x, y)):
                    # Invert the y-coordinate to flip the board vertically
                    screen_y = ARENA_SIZE - 1 - y
                    pygame.draw.circle(
                        self.win,
                        (self.DOT_COLOR if (x, y) not in self.edge_locations else (255, 0, 0)),
                        (x * self.CELL_SIZE + self.CELL_SIZE // 2, screen_y * self.CELL_SIZE + self.CELL_SIZE // 2),
                        self.DOT_RADIUS
                    )

    def display_coordinates(self):
        """Display the coordinates of the hovered spot at the bottom of the GUI."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        grid_x = mouse_x // self.CELL_SIZE
        grid_y = mouse_y // self.CELL_SIZE

        # Invert the y-coordinate to match the flipped board
        grid_y = ARENA_SIZE - 1 - grid_y

        if is_in_bounds((grid_x, grid_y)):
            font = pygame.font.SysFont(None, 24)
            coord_text = font.render(f"X: {grid_x}, Y: {grid_y}", True, (255, 255, 255))
            self.win.blit(coord_text, (10, self.HEIGHT - 30))

    def update_display(self, game_map):
        """Update the display with the current state of the game map."""
        self.draw_board()  # Draw the base board with dots

        # Here you would add code to draw the units based on the game_map
        # For example, iterating through the map and drawing units at their locations

        self.display_coordinates()  # Show coordinates of the hovered spot
        pygame.display.flip()  # Refresh the display

    def quit(self):
        """Properly quit Pygame."""
        pygame.quit()
