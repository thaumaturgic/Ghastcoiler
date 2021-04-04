import logging
import random

from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from deathrattles.base import Deathrattle
from minions.tokens import DamagedGolem, Imp, BigBadWolf


class HarvestGolemDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="HarvestGolemDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        logging.debug("Harvest Golem deathrattle triggered, creating Damaged Golem")
        own_board.add_minion(DamagedGolem(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class ImprisonerDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="ImprisonerDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        logging.debug("Imprisoner deathrattle triggered, creating Imp")
        own_board.add_minion(Imp(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class KaboomBotDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="KaboomBotDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        if minion.golden:
            logging.debug("Kaboom Bot (golden) deathrattle triggered, dealing 4 damage twice")
        else:
            logging.debug("Kaboom Bot deathrattle triggered, dealing 4 damage")
        number_bombs = 2 if minion.golden else 1
        for _ in range(number_bombs):
            opposing_minion = opposing_board.random_minion()
            if opposing_minion:
                opposing_minion.receive_damage(amount=4, poisonous=False, own_board=opposing_board)


class KindlyGrandmotherDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="KindlyGrandmotherDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        logging.debug("Kindly Grandmother deathrattle triggered, creating Big Bad Wolf")
        own_board.add_minion(BigBadWolf(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class SpawnofNZothDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="SpawnofNZothDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Spawn of NZoth deathrattle triggered")
        bonus = 2 if minion.golden else 1
        for other_minion in own_board.get_living_minions():
            other_minion.add_stats(bonus, bonus)


class UnstableGhoulDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="UnstableGhoulDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Unstable Ghoul deathrattle triggered")
        triggers = 2 if minion.golden else 1
        for _ in range(triggers):
            for opposing_minion in opposing_board.get_living_minions():
                opposing_minion.receive_damage(1, False, opposing_board)
            for friendly_minion in own_board.get_living_minions():
                friendly_minion.receive_damage(1, False, own_board)


class SelflessHeroDeathrattle(Deathrattle):
    def __init__(self):
        super().__init__(name="SelflessHeroDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Selfless Hero deathrattle triggered")
        iterations = 2 if minion.golden else 1
        for _ in range(iterations):
            unshielded_minions = [minion for minion in own_board.minions if not minion.divine_shield]
            board_index = unshielded_minions[random.randint(0, len(unshielded_minions) - 1)].position
            own_board.minions[board_index].divine_shield = True
