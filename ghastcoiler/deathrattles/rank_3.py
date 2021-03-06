import logging
import random

from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from minions.tokens import Spider, Rat, Microbot
from deathrattles.base import Deathrattle


class InfestedWolfDeathrattle(Deathrattle):
    "Summon two 1/1 Spiders."
    def __init__(self):
        super().__init__(name="InfestedWolfDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = Spider,
            minions_to_spawn = 2,
            triggered_from_macaw = macaw_trigger)


# class PilotedShredderDeathrattle(Deathrattle):
#     "Summon a random 2-Cost minion."
#     def __init__(self):
#         super().__init__(name="PilotedShredderDeathrattle")

#     def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
#         from utils.minion_utils import MinionUtils
#         minionUtils = MinionUtils()
#         two_mana_minions = [minion for minion in minionUtils.get_minions() if minion.mana_cost == 2]
#         num_minions = 2 if minion.golden else 1
#         for _ in range(num_minions):
#             new_minion = two_mana_minions[random.randint(0, len(two_mana_minions)-1)]
#             new_minion.attacked = minion.attacked
#             own_board.add_minion(new_minion, position=minion.position, to_right=macaw_trigger)


class RatPackDeathrattle(Deathrattle):
    "Summon a number of 1/1 Rats equal to this minion's Attack."
    def __init__(self):
        super().__init__(name="RatPackDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = Rat,
            minions_to_spawn = minion.attack,
            triggered_from_macaw = macaw_trigger)


class ReplicatingMenaceDeathrattle(Deathrattle):
    "Summon three 1/1 Microbots."
    def __init__(self, golden: Optional[bool] = False):
        super().__init__(name="ReplicatingMenaceDeathrattle")
        self.golden = golden

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = Microbot,
            summon_golden_minion = self.golden,
            minions_to_spawn = 3,
            triggered_from_macaw = macaw_trigger)
