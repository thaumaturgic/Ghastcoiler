import logging

from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType
from minions.tokens import Plant
from deathrattles.base import Deathrattle

class GentleDjinniDeathrattle(Deathrattle):
    "Summon another random Elemental and add a copy of it to your hand."
    def __init__(self):
        super().__init__(name="GentleDjinniDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        # Filter out un purchaseable elementals like curator token, water droplet, and elementals above current tech level
        not_allowed_elementals = ["Amalgam", "Water Droplet", "Gentle Djinni"]
        isSpawnable = lambda x: (MinionType.Elemental in x.types) and (x.name not in not_allowed_elementals)
        elementals_to_summon = 2 if minion.golden else 1
        Deathrattle.summon_random_minions(minion, own_board, elementals_to_summon, isSpawnable, macaw_trigger)


class GhastcoilerDeathrattle(Deathrattle):
    "Summon 2 random Deathrattle minions."
    def __init__(self):
        super().__init__(name="GhastcoilerDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        # TODO: Filter out death rattle minions with types not in the game
        not_allowed_minions = ["Ghastcoiler"]
        isSpawnable = lambda x: (len(x.deathrattles) > 0) and (x.name not in not_allowed_minions)
        
        minions_to_summon = 4 if minion.golden else 2
        Deathrattle.summon_random_minions(minion, own_board, minions_to_summon, isSpawnable, macaw_trigger)


class GoldrinntheGreatWolfDeathrattle(Deathrattle):
    "Give your Beasts +5/+5."
    def __init__(self):
        super().__init__(name="GoldrinntheGreatWolfDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for other_minion in own_board.minions:
            if MinionType.Beast in other_minion.types:
                if other_minion == minion and not macaw_trigger:
                    continue
                stats = 10 if minion.golden else 5
                other_minion.add_stats(stats,stats)


class KangorsApprenticeDeathrattle(Deathrattle):
    "Summon the first 2 friendly Mechs that died this combat."
    def __init__(self):
        super().__init__(name="KangorsApprenticeDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        #TODO: IMPLEMENT
        pass


class NadinatheRedDeathrattle(Deathrattle):
    "Give your Dragons Divine Shield."
    def __init__(self):
        super().__init__(name="NadinatheRedDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for other_minion in own_board.minions:
            if MinionType.Dragon in other_minion.types:
                other_minion.divine_shield = True


class TheTideRazorDeathrattle(Deathrattle):
    " Summon 3 random Pirates."
    def __init__(self):
        super().__init__(name="TheTideRazorDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        not_allowed_pirates = ["Amalgam", "Sky Pirate"]
        isSpawnable = lambda x: (MinionType.Pirate in x.types) and (x.name not in not_allowed_pirates)
        
        minions_to_summon = 6 if minion.golden else 3
        Deathrattle.summon_random_minions(minion, own_board, minions_to_summon, isSpawnable, macaw_trigger)
        pass

# TODO: Test
class LivingSporesDeathrattle(Deathrattle):
    "Summon two 1/1 Plants."
    def __init__(self):
        super().__init__(name="LivingSporesDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board, minion, Plant, False, 2, macaw_trigger)
