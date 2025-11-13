import math

def simple_damage(level, power, attack, defence):
    base = ((2 * level / 5 + 2) * power * attack / defence) / 50 + 2
    return math.floor(base)

def damage_calc(level, power_c, defence_c):
    base = ((2 * level / 10 + 3) * power_c / defence_c) / 20
    return math.floor(base)