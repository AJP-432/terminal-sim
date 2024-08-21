import pygame
from game_map import Map
from navigation import ShortestPathFinder
from drawer import Drawer
import time
from unit import *

class Simulator:
    def __init__(self, action_frame: dict):
        self.action_frame = action_frame
        self.drawer = Drawer.get_instance()
        self.game_map = Map()
        self.nav = ShortestPathFinder()
        self.game_map.initialize_map(self.action_frame)
        self.frame = 0
        self.scout_count = 0

        self.set_paths()
        self.enemy_damage = 0

    def set_paths(self):
        self.scout_count = 0
        start_loc_to_path = {}
        self.nav.initialize_map(self.game_map)
        for unit in self.game_map.all_units:
            if unit.unit_type == UnitType.SCOUT:
                self.scout_count += 1

                if unit.start_loc in start_loc_to_path:
                    unit.set_path(start_loc_to_path[unit.start_loc])
                
                path = self.nav.navigate_multiple_endpoints(unit.loc, unit.end_edge_locations, self.game_map)
                unit.set_path(path)
                start_loc_to_path[unit.start_loc] = path
    
    def run_frame(self):
        self.frame += 1
        self.drawer.update_display(self.game_map)

        # Shielding
        for unit in self.game_map.all_units:
            if unit.unit_type == UnitType.SUPPORT:
                shield_amount = unit.give_shield()

                locs_in_range = get_locations_in_range(unit.get_loc(), unit.get_range())
                for loc in locs_in_range:
                    for target in self.game_map[loc]:
                        if target.player_index == unit.player_index and target.unit_type == UnitType.SCOUT and not unit.have_given_shield(target):
                            target.hp += shield_amount
                            unit.have_shielded.add(target)

        # Movement   
        to_remove = set()
        for unit in self.game_map.all_units:
            if unit.unit_type == UnitType.SCOUT:
                if unit.path_empty(): 
                    self.game_map.remove_unit(unit.get_loc(), unit)
                    to_remove.add(unit)
                    if unit.unit_type == UnitType.SCOUT:
                        self.scout_count -= 1
                        self.enemy_damage += 1
                else:
                    curr_loc = unit.get_loc()
                    next_loc = unit.next_step()
                    self.game_map.remove_unit(curr_loc, unit)
                    self.game_map.add_unit(next_loc, unit)
                    unit.loc = next_loc
        
        for unit in to_remove:
            self.game_map.all_units.remove(unit)
        
        # Attacking
        pending_removal = set()
        structure_destroyed = False
        for unit in self.game_map.all_units:
            if unit.unit_type in [UnitType.TURRET, UnitType.SCOUT]:
                target = self.game_map.find_target(unit)
                if target: 
                    target.hp -= unit.give_damage()
                    if target.hp <= 0:
                        pending_removal.add(target)
                    
                        if target.unit_type in [UnitType.WALL, UnitType.SUPPORT, UnitType.TURRET]:
                                structure_destroyed = True
        
        
        
        # If structure destroyed, recompute paths
        if structure_destroyed:
            self.set_paths()
        
        # Remove destroyed units
        for unit in pending_removal:
            self.game_map.remove_unit(unit.get_loc(), unit)
            self.game_map.all_units.remove(unit)
            if unit.unit_type == UnitType.SCOUT:
                self.scout_count -= 1
    
    def run(self):
        while self.scout_count > 0:
            time.sleep(0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.run_frame()
        
        self.drawer.quit()