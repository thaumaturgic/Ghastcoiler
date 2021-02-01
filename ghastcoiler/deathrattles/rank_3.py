import logging

from game.player_board import PlayerBoard
from minions.base import Minion
from minions.tokens import Spider, Rat, Microbot
from deathrattles.base import Deathrattle


class InfestedWolfDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="InfestedWolfDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Infested Wolf deathrattle triggered, creating spider tokens")
        own_board.add_minion(Spider(golden=minion.golden, attacked=minion.attacked), position=minion.position)


class PilotedShredderDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="PilotedShredderDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Piloted Shredder deathrattle triggered, creating random 2 drop")
        # TODO: IMPLEMENT
        # own_board.add_minion(Spider(golden=minion.golden, attacked=minion.attacked), position=minion.position)


class RatPackDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="RatPackDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        number_rats = minion.attack
        logging.debug(f"Rat pack deathrattle triggered, creating {number_rats} rats")
        for _ in range(number_rats):
            own_board.add_minion(Rat(golden=minion.golden, attacked=minion.attacked), position=minion.position)


class ReplicatingMenaceDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="ReplicatingMenaceDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Replicating menace deathrattle triggered, creating 3 microbots")
        for _ in range(3):
            own_board.add_minion(Microbot(golden=minion.golden, attacked=minion.attacked), position=minion.position)
