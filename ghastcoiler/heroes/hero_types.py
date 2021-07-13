from enum import Enum

class HeroType(Enum):
    DEATHWING = 1 # TODO: Test board state import, do we need to apply attack from starting minions or just summoned ones?
    GREYBOUGH = 2
    ILLIDAN_STORMRAGE = 3
    YSHAARJ = 4

def deathwing_summon_effect(minion):
    minion.add_stats(2,0)

def greybough_summon_effect(minion):
    minion.taunt = True
    minion.add_stats(1,2)