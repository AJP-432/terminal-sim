import pygame
from map import Map
from drawer import Drawer

def main():
    drawer = Drawer.get_instance()  # Get the Drawer instance
    game_map = Map()  # Initialize your game map

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update the display with the current map state
        drawer.update_display(game_map)
    
    drawer.quit()  # Quit Pygame properly

if __name__ == "__main__":
    main()
