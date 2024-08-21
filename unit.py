from abc import ABC
from typing import Literal
from constants import * 
import queue

class Unit(ABC):
    def __init__(self, unit_type: UnitType, player_index: Literal[0, 1], loc: tuple[int, int], hp: float) -> None:
        if not is_in_bounds(loc):
            raise ValueError("Unit is out of bounds")
        
        self.unit_type = unit_type
        self.player_index = player_index
        self.loc = loc
        self.hp = hp
        self.upgraded = False
        self.range = 0

        assert self.loc[1] < 14 if self.player_index == 0 else self.loc[1] >= 14
    
    def my_team(self, player_index: Literal[0, 1]) -> bool:
        return self.player_index == player_index

    def is_it(self, unit_type: UnitType) -> bool:
        return self.unit_type == unit_type

    def is_dead(self) -> bool:
        return self.hp <= 0

    def is_upgraded(self) -> bool:
        return self.upgraded

    def get_unit_type(self) -> UnitType:
        return self.unit_type

    def get_loc(self) -> tuple[int, int]:
        return self.loc

    def get_range(self) -> float:
        return self.range

    def get_health(self) -> float:
        return self.hp

    def give_damage(self):
        return 0
        
class Wall(Unit):
    def __init__(self, player_index: Literal[0, 1], loc: tuple[int, int], hp: float) -> None:
        super().__init__(UnitType.WALL, player_index, loc, hp)
        self.range = 0
    
    def upgrade(self):
        self.upgraded = True
    
class Support(Unit):
    def __init__(self, player_index: Literal[0, 1], loc: tuple[int, int], hp: float) -> None:
        super().__init__(UnitType.SUPPORT, player_index, loc, hp)
        self.shield = 3
        self.range = 2.5
        self.bonus_shield = 0
        self.have_shielded = set()

    def upgrade(self) -> None:
        self.shield = 5
        self.range = 6
        self.bonus_shield = 0.3
        self.upgraded = True
    
    def give_shield(self):
        y = self.loc[1]
        return self.shield + (self.bonus_shield * abs((y - (0 if self.player_index == 0 else ARENA_SIZE - 1))))

    def have_given_shield(self, unit: Unit):
        return unit in self.have_shielded

class Turret(Unit):
    def __init__(self, player_index: Literal[0, 1], loc: tuple[int, int], hp: float) -> None:
        super().__init__(UnitType.TURRET, player_index, loc, hp)
        self.damage = 6
        self.range = 2.5

    def upgrade(self) -> None:
        self.damage = 14
        self.range = 4.5
        self.upgraded = True
    
    def give_damage(self):
        return self.damage

class Scout(Unit):
    def __init__(self, player_index: Literal[0, 1], loc: tuple[int, int], hp: float) -> None:
        super().__init__(UnitType.SCOUT, player_index, loc, hp)
        self.start_loc = loc
        self.damage = 2
        self.range = 4.5
        self.end_edge_locations = end_edge_locations(get_quadrant(loc))
        self.path: queue = []
    
    def give_damage(self):
        return self.damage

    def set_path(self, path: list):
        self.path = queue.Queue()
        for loc in path:
            self.path.put(loc)
    
    def next_step(self):
        loc = self.path.get()
        self.loc = loc
        return loc

    def path_empty(self):
        return self.path.empty()