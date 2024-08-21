import pygame
from game_map import Map
from navigation import ShortestPathFinder
from drawer import Drawer
from simulator import Simulator
from unit import * 

obj = {
    "turnInfo": [1,2,57],
    "p1Stats": [22,12.4,2.3,52933],
    "p2Stats": [25,9.5,0.3,82365],
    "p1Units": [
        [],
        [],
        [
            [24,13,75,"2"],
            [22,11,75,"8"],
            [10,9,28,"10"],
            [17,9,75,"12"],
            [14,6,75,"14"],
            [13,6,75,"44"]
        ],
        [[0, 13, 12, ""], 
         [0, 13, 12, ""],
         [0, 13, 12, ""],
         [0, 13, 12, ""],
         [0, 13, 12, ""],
        ],
        [],
        [],
        [],
        []
    ],
    "p2Units": 
    [
        [[4,14,40,"51"],
         [3, 17, 40, "18"],
         [0, 14, 40, "20"],
         [1, 15, 40, "22"],
         [2, 14, 40, "26"],
         [2, 15, 40, "28"],
         [3, 14, 40, "47"],
         [3, 15, 40, "49"]
         ],
        [[13, 23, 300, ""], 
         [13, 25, 30000, ""]],
        [],
        [],
        [],
        [],
        [],
        [[4,14,0,"52"]]
    ]
}

def main():
    sim = Simulator(obj)
    sim.run()

# def main(): 
#     drawer = Drawer.get_instance()  # Get the Drawer instance
#     game_map = Map()  # Initialize your game map
#     s1 = Scout(0, (2, 11), 12)
#     s2 = Scout(1, (4, 18), 12)
#     w1 = Wall(0, (3, 11), 12)
#     w2 = Wall(1, (5, 18), 12)
#     t1 = Turret(0, (4, 11), 12)
#     t2 = Turret(1, (6, 18), 12)
#     sh1 = Support(0, (5, 11), 12)
#     sh2 = Support(1, (7, 18), 12)
#     sh2.upgrade()

#     game_map.add_unit(s1.loc, s1)
#     game_map.add_unit(s2.loc, s2)
#     game_map.add_unit(w1.loc, w1)
#     game_map.add_unit(w2.loc, w2)
#     game_map.add_unit(t1.loc, t1)
#     game_map.add_unit(t2.loc, t2)
#     game_map.add_unit(sh1.loc, sh1)
#     game_map.add_unit(sh2.loc, sh2)

#     nav = ShortestPathFinder()
#     nav.initialize_map(game_map)

#     a = nav.navigate_multiple_endpoints(s1.start_loc, s1.end_edge_locations, game_map)
#     print(a)
    
#     while True:
#         drawer.update_display(game_map)
#         pygame.time.wait(1000)
    
#     pygame.quit()

if __name__ == "__main__":
    main()
