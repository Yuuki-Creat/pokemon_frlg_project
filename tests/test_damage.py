# test/test_damage.py
from battle.battle_manager import simple_damage, damage_calc

def test_damage():
    assert simple_damage(50, 50, 100, 100) == 24
    assert damage_calc(36, 120, 50) == 1