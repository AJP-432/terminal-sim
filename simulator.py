from game_map import Map
from navigation import ShortestPathFinder
from unit import *

class Simulator:
    def __init__(self, action_frame: dict):
        self.action_frame = action_frame
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
    
    def self_destruct_scouts(self, loc):
        to_remove = set()
        for unit in self.game_map[loc]:
            if unit.unit_type == UnitType.SCOUT:
                self.scout_count -= 1
                unit.pending_removal = True
        
                to_remove.add(unit)
        
        return to_remove
    
    def breach(self, loc):
        to_remove = set()
        for unit in self.game_map[loc]:
            if unit.unit_type == UnitType.SCOUT:
                self.scout_count -= 1
                self.enemy_damage += 1
                unit.pending_removal = True

                to_remove.add(unit)
            
        return to_remove

    def run_frame(self):
        self.frame += 1

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
                if unit.pending_removal: 
                    continue

                if unit.path_empty(): 
                    # We are completely blocked in, self-destruct
                    if unit.get_loc() not in unit.end_edge_locations:
                        to_remove = to_remove.union(self.self_destruct_scouts(unit.get_loc()))
                        continue
                    
                    # Breached!
                    else: 
                        to_remove = to_remove.union(self.breach(unit.get_loc()))
                else:
                    curr_loc = unit.get_loc()
                    next_loc = unit.next_step()
                    self.game_map.remove_unit(curr_loc, unit)
                    self.game_map.add_unit(next_loc, unit)
                    unit.loc = next_loc
        
        for unit in to_remove:
            self.game_map.all_units.remove(unit)
            self.game_map.remove_unit(unit.get_loc(), unit)
        
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
            self.run_frame()
    
    def summarize(self):
        return self.enemy_damage 