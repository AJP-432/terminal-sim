from constants import *
from unit import * 

class Map: 
    def __init__(self) -> None:
        self.map = [[set() for _ in range(ARENA_SIZE)] for _ in range(ARENA_SIZE)]
        self.all_units = set()

    def __getitem__(self, loc: tuple[int, int]) -> set:
        if not is_in_bounds(loc):
            raise IndexError("Location out of bounds")
        return self.map[loc[0]][loc[1]]

    def __setitem__(self, loc: tuple[int, int], value: set) -> None:
        if not is_in_bounds(loc):
            raise IndexError("Location out of bounds")
        self.map[loc[0]][loc[1]] = value
    
    def is_empty(self, loc: tuple[int, int]) -> bool:
        return len(self[loc]) == 0

    def contains_structure(self, loc: tuple[int, int]) -> bool:
        for unit in self[loc]:
            if unit.unit_type == UnitType.WALL or unit.unit_type == UnitType.SUPPORT or unit.unit_type == UnitType.TURRET:
                return True
        return False

    def add_unit(self, loc: tuple[int, int], unit: UnitType) -> None:
        self[loc].add(unit)
    
    def remove_unit(self, loc: tuple[int, int], unit: UnitType) -> None:
        self[loc].remove(unit)
    
    def initialize_map(self, action_frame: dict):
        # Walls
        print("HERE")
        for x, y, hp, _ in action_frame["p1Units"][0]:
            u = Wall(0, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)
            print(f"{x}, {y}, {hp}")
        
        for x, y, hp, _ in action_frame["p2Units"][0]:
            u = Wall(1, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)

        # Supports
        for x, y, hp, _ in action_frame["p1Units"][1]:
            u = Support(0, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)
        
        for x, y, hp, _ in action_frame["p2Units"][1]:
            u = Support(1, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)

        # Turrets
        for x, y, hp, _ in action_frame["p1Units"][2]:
            u = Turret(0, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)
        
        for x, y, hp, _ in action_frame["p2Units"][2]:
            u = Turret(1, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)

        # Scouts
        for x, y, hp, _ in action_frame["p1Units"][3]:
            u = Scout(0, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)
        
        for x, y, hp, _ in action_frame["p2Units"][3]:
            u = Scout(1, (x, y), hp)
            self.add_unit((x, y), u)
            self.all_units.add(u)

        # Upgrades
        for x, y, _, _ in action_frame["p1Units"][7]:
            for u in self[(x, y)]:
                if u.unit_type != UnitType.SCOUT: 
                    u.upgrade()
        
        for x, y, _, _ in action_frame["p2Units"][7]:
            for u in self[(x, y)]:
                if u.unit_type != UnitType.SCOUT:
                    u.upgrade()

    def find_target(self, unit: Unit) -> Unit:
        locs_in_range = get_locations_in_range(unit.get_loc(), unit.get_range())
        best_target = None
        for loc in locs_in_range:
            for target in self[loc]:
                if target.get_health() <= 0 or target.player_index == unit.player_index or unit.unit_type == UnitType.TURRET and target.unit_type in [UnitType.WALL, UnitType.SUPPORT, UnitType.TURRET]:
                    continue
            
                if not best_target:
                    best_target = target
                    continue
                
                # Distance
                if distance_between_locations(unit.get_loc(), loc) < distance_between_locations(unit.get_loc(), best_target.get_loc()):
                    best_target = target
                    continue

                if distance_between_locations(unit.get_loc(), loc) == distance_between_locations(unit.get_loc(), best_target.get_loc()):
                    if target.get_health() < best_target.get_health() and target.get_health() > 0:
                        best_target = target
                        continue
                    
                    if target.get_health() == best_target.get_health():
                        if (unit.player_index == 0 and target.get_loc()[1] < best_target.get_loc()[1]) or (unit.player_index == 1 and target.get_loc()[1] > best_target.get_loc()[1]):
                            best_target = target
                            continue

                        elif target.get_loc()[1] == best_target.get_loc()[1]:
                            # 5. Closest to an Edge
                            if distance_to_closest_edge(target.get_loc()) < distance_to_closest_edge(best_target.get_loc()):
                                best_target = target

        return best_target