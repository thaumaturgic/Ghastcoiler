import logging

from game.player_board import PlayerBoard
from minions.base import Minion
from deathrattles.base import Deathrattle
from minions.tokens import JoEBot


class FiendishServantDeathrattle(Deathrattle):
    """When Fiendish Servant dies, add it's power to another minion on the board"""
    def __init__(self):
        super().__init__(name="FiendishServantDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        target_minion = own_board.random_minion()
        if target_minion:
            target_minion.add_attack(minion.last_attack)
            logging.debug(f"Fiendish Servant deathrattle triggers onto {target_minion.minion_string()}")
        else:
            logging.debug("Fiendish Servant deathrattle triggers but there are no targets left")


class MecharooDeathrattle(Deathrattle):
    """When Mecharoo dies, create a Jo-E Bot token"""
    def __init__(self):
        super().__init__(name="MecharooDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
        logging.debug("Mecharoo deathrattle triggered, creating Jo-E Bot")
        own_board.add_minion(JoEBot(golden=minion.golden, attacked=minion.attacked), position=minion.position)
