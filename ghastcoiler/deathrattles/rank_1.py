from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from deathrattles.base import Deathrattle
from minions.tokens import SkyPirate


class FiendishServantDeathrattle(Deathrattle):
    """When Fiendish Servant dies, add it's power to another minion on the board"""
    def __init__(self):
        super().__init__(name="FiendishServantDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for _ in range(2 if minion.golden else 1):
            target_minion = own_board.random_minion()
            if target_minion:
                target_minion.add_stats(minion.attack, 0)


# class MecharooDeathrattle(Deathrattle):
#     """When Mecharoo dies, create a Jo-E Bot token"""
#     def __init__(self):
#         super().__init__(name="MecharooDeathrattle")

#     def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard):
#         logging.debug("Mecharoo deathrattle triggered, creating Jo-E Bot")
#         own_board.add_minion(JoEBot(golden=minion.golden, attacked=minion.attacked), position=minion.position)


class ScallywagDeathrattle(Deathrattle):
    """Summon a 1/1 Pirate. It attacks immediately."""
    def __init__(self):
        super().__init__(name="ScallywagDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = SkyPirate,
            triggered_from_macaw = macaw_trigger,
            should_attack = True)
