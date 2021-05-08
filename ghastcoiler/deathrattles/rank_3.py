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
        logging.debug("Infested Wolf deathrattle triggered, creating spider tokens")
        for _ in range(2):
            own_board.add_minion(Spider(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class PilotedShredderDeathrattle(Deathrattle):
    "Summon a random 2-Cost minion."
    def __init__(self):
        super().__init__(name="PilotedShredderDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        from utils.minion_utils import MinionUtils
        minionUtils = MinionUtils()
        two_mana_minions = [minion for minion in minionUtils.get_all_minions() if minion.mana_cost == 2]
        num_minions = 2 if minion.golden else 1
        for _ in range(num_minions):
            new_minion = two_mana_minions[random.randint(0, len(two_mana_minions)-1)]
            new_minion.attacked = minion.attacked
            own_board.add_minion(new_minion, position=minion.position, to_right=macaw_trigger)


class RatPackDeathrattle(Deathrattle):
    "Summon a number of 1/1 Rats equal to this minion's Attack."
    def __init__(self):
        super().__init__(name="RatPackDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        number_rats = minion.attack
        logging.debug(f"Rat pack deathrattle triggered, creating {number_rats} rats")
        for _ in range(number_rats):
            own_board.add_minion(Rat(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class ReplicatingMenaceDeathrattle(Deathrattle):
    "Summon three 1/1 Microbots."
    def __init__(self):
        super().__init__(name="ReplicatingMenaceDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        logging.debug("Replicating menace deathrattle triggered, creating 3 microbots")
        # TODO: Handle the golden version of this deathrattle.
        # The deathrattle being gold determines 2/2 bots, NOT the host minion
        for _ in range(3):
            own_board.add_minion(Microbot(attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)
