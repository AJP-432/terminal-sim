from constants import *

class Map: 
    def __init__(self) -> None:
        self.map = [[set() for _ in range(ARENA_SIZE)] for _ in range(ARENA_SIZE)]

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
        if len(self[loc]) == 0 or len(self[loc]) > 1:
            return False
        for unit in self[loc]:
            if unit.unit_type == UnitType.WALL or unit.unit_type == UnitType.SUPPORT or unit.unit_type == UnitType.TURRET:
                return True
        return False

    def add_unit(self, loc: tuple[int, int], unit: UnitType) -> None:
        self[loc].add(unit)
    
    def remove_unit(self, loc: tuple[int, int], unit: UnitType) -> None:
        self[loc].remove(unit)