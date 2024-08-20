import pytest
from unit import Unit, Wall, Support, Turret, Scout
from constants import UnitType, ARENA_SIZE

def test_wall_initialization():
    wall = Wall(player_index=0, loc=(0, 13), hp=100)
    assert wall.unit_type == UnitType.WALL
    assert wall.player_index == 0
    assert wall.loc == (0, 13)
    assert wall.hp == 100

def test_support_initialization():
    support = Support(player_index=1, loc=(6, 19), hp=80)
    assert support.unit_type == UnitType.SUPPORT
    assert support.player_index == 1
    assert support.loc == (6, 19)
    assert support.hp == 80
    assert support.shield == 3
    assert support.range == 2.5
    assert support.bonus_shield == 0

def test_turret_initialization():
    turret = Turret(player_index=0, loc=(9, 12), hp=75)
    assert turret.unit_type == UnitType.TURRET
    assert turret.player_index == 0
    assert turret.loc == (9, 12)
    assert turret.hp == 75
    assert turret.damage == 6
    assert turret.range == 2.5

def test_scout_initialization():
    scout = Scout(player_index=0, loc=(5, 8), hp=12)
    assert scout.unit_type == UnitType.SCOUT
    assert scout.player_index == 0
    assert scout.loc == (5, 8)
    assert scout.hp == 12
    assert scout.start_loc == (5, 8)
    assert scout.damage == 2
    assert scout.range == 4.5

def test_my_team():
    wall = Wall(player_index=0, loc=(4, 12), hp=100)
    assert wall.my_team(0) == True
    assert wall.my_team(1) == False

def test_is_it():
    turret = Turret(player_index=0, loc=(18, 12), hp=50)
    assert turret.is_it(UnitType.TURRET) == True
    assert turret.is_it(UnitType.WALL) == False

def test_support_upgrade():
    support = Support(player_index=0, loc=(10, 10), hp=80)
    support.upgrade()
    assert support.shield == 5
    assert support.range == 6
    assert support.bonus_shield == 0.3
    assert support.give_shield() == 8

def test_support_give_shield():
    support = Support(player_index=1, loc=(4, 14), hp=80)
    assert support.give_shield() == 3
    support.upgrade()
    assert support.give_shield() == 8.9

def test_turret_upgrade():
    turret = Turret(player_index=1, loc=(10, 15), hp=50)
    turret.upgrade()
    assert turret.damage == 14
    assert turret.range == 4.5

def test_turret_give_damage():
    turret = Turret(player_index=1, loc=(10, 15), hp=50)
    assert turret.give_damage() == 6
    turret.upgrade()
    assert turret.give_damage() == 14
