import pygame
from game_map import Map
from drawer import Drawer
from unit import * 

def main():
    drawer = Drawer.get_instance()  # Get the Drawer instance
    game_map = Map()  # Initialize your game map
    s1 = Scout(0, (2, 11), 12)
    s2 = Scout(1, (4, 18), 12)
    w1 = Wall(0, (3, 11), 12)
    w2 = Wall(1, (5, 18), 12)
    t1 = Turret(0, (4, 11), 12)
    t2 = Turret(1, (6, 18), 12)
    sh1 = Support(0, (5, 11), 12)
    sh2 = Support(1, (7, 18), 12)
    sh2.upgrade()

    game_map.add_unit(s1.loc, s1)
    game_map.add_unit(s2.loc, s2)
    game_map.add_unit(w1.loc, w1)
    game_map.add_unit(w2.loc, w2)
    game_map.add_unit(t1.loc, t1)
    game_map.add_unit(t2.loc, t2)
    game_map.add_unit(sh1.loc, sh1)
    game_map.add_unit(sh2.loc, sh2)

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
