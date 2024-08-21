import pygame
from constants import *
from game_map import Map
from unit import Unit

PLAYER_1_COLOR = (0, 0, 255)  # Blue
PLAYER_2_COLOR = (255, 165, 0)  # Orange
UPGRADE_RING_COLOR = (255, 255, 0)  # Yellow

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

    def draw_unit(self, unit: Unit, cell_x, cell_y, size=20):
        """Draws a unit on the screen centered in its grid cell."""
        color = PLAYER_1_COLOR if unit.player_index == 1 else PLAYER_2_COLOR
        
        # Calculate the center position for the unit in the grid cell
        center_x = cell_x + self.CELL_SIZE // 2
        center_y = cell_y + self.CELL_SIZE // 2

        if unit.get_unit_type() == UnitType.TURRET:
            pygame.draw.rect(self.win, color, pygame.Rect(
                center_x - size // 2, center_y - size // 2, size, size))
        elif unit.get_unit_type() == UnitType.SUPPORT:
            pygame.draw.circle(self.win, color, (center_x, center_y), size // 2)
        elif unit.get_unit_type() == UnitType.WALL:
            pygame.draw.circle(self.win, color, (center_x, center_y), size // 4)
        elif unit.get_unit_type() == UnitType.SCOUT:
            pygame.draw.line(self.win, color, (center_x - size // 2, center_y - size // 2), 
                             (center_x + size // 2, center_y + size // 2), 3)
            pygame.draw.line(self.win, color, (center_x - size // 2, center_y + size // 2), 
                             (center_x + size // 2, center_y - size // 2), 3)
        
        # Draw upgrade ring if the unit is upgraded
        if unit.is_upgraded():
            pygame.draw.circle(self.win, UPGRADE_RING_COLOR, (center_x, center_y), size, 2)
    
    def draw_board(self, game_map: Map):
        """Draw the board with dots representing valid locations and units."""
        self.win.fill((0, 0, 0))  # Clear the screen with black

        for y in range(ARENA_SIZE):
            for x in range(ARENA_SIZE):
                cell_x = x * self.CELL_SIZE
                cell_y = y * self.CELL_SIZE

                # Invert the y-coordinate to flip the board vertically
                screen_y = ARENA_SIZE - 1 - y
                if is_in_bounds((x, y)) and game_map.is_empty((x, y)):
                    pygame.draw.circle(
                        self.win,
                        ((255, 0, 0) if (x, y) in self.edge_locations else self.DOT_COLOR if y <= 13 else (0, 70, 0)),
                        (cell_x + self.CELL_SIZE // 2, screen_y * self.CELL_SIZE + self.CELL_SIZE // 2),
                        self.DOT_RADIUS
                    )
                
                elif is_in_bounds((x, y)) and not game_map.is_empty((x, y)):
                    unit = list(game_map[x, y])[0]
                    self.draw_unit(unit, cell_x, screen_y * self.CELL_SIZE)
 
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
        self.draw_board(game_map)  # Draw the base board with dots
        self.display_coordinates()  # Show coordinates of the hovered spot
        pygame.display.flip()  # Refresh the display

    def quit(self):
        """Properly quit Pygame."""
        pygame.quit()
