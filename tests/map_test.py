import pytest
import sys # added!
sys.path.append("..") # added!
from map import Map
from constants import *

def test_map_initialization():
    game_map = Map()
    # Check if all locations are initialized as empty sets
    for row in range(ARENA_SIZE):
        for col in range(ARENA_SIZE):
            if is_in_bounds((row, col)):
                assert game_map.is_empty((row, col))

def test_getitem_setitem():
    game_map = Map()
    loc = (10, 10)
    units = {UnitType.SCOUT, UnitType.SCOUT}
    game_map[loc] = units
    assert game_map[loc] == units

def test_is_empty():
    game_map = Map()
    loc = (12, 12)
    assert game_map.is_empty(loc)
    game_map.add_unit(loc, UnitType.WALL)
    assert not game_map.is_empty(loc)

def test_add_unit():
    game_map = Map()
    loc = (15, 17)
    game_map.add_unit(loc, UnitType.SUPPORT)
    assert UnitType.SUPPORT in game_map[loc]
    game_map.add_unit(loc, UnitType.TURRET)
    assert UnitType.TURRET in game_map[loc]
    assert len(game_map[loc]) == 2  # Ensure both units are in the set

def test_remove_unit():
    game_map = Map()
    loc = (15, 4)
    game_map.add_unit(loc, UnitType.SCOUT)
    game_map.add_unit(loc, UnitType.TURRET)
    game_map.remove_unit(loc, UnitType.SCOUT)
    assert UnitType.SCOUT not in game_map[loc]
    assert UnitType.TURRET in game_map[loc]
    assert len(game_map[loc]) == 1

def test_remove_nonexistent_unit():
    game_map = Map()
    loc = (14, 15)
    game_map.add_unit(loc, UnitType.WALL)
    with pytest.raises(KeyError):
        game_map.remove_unit(loc, UnitType.TURRET)

def test_access_out_of_bounds():
    game_map = Map()
    out_of_bounds_loc = (ARENA_SIZE, ARENA_SIZE)  # Invalid location
    with pytest.raises(IndexError):
        _ = game_map[out_of_bounds_loc]
    with pytest.raises(IndexError):
        game_map[out_of_bounds_loc] = {UnitType.WALL}
