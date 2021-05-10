import logging
import random

from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType
from deathrattles.base import Deathrattle

class GentleDjinniDeathrattle(Deathrattle):
    "Summon another random Elemental and add a copy of it to your hand."
    def __init__(self):
        super().__init__(name="GentleDjinniDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        #TODO: IMPLEMENT
        pass


class GhastcoilerDeathrattle(Deathrattle):
    "Summon 2 random Deathrattle minions."
    def __init__(self):
        super().__init__(name="GhastcoilerDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        #TODO: IMPLEMENT
        pass


class GoldrinntheGreatWolfDeathrattle(Deathrattle):
    "Give your Beasts +5/+5."
    def __init__(self):
        super().__init__(name="GoldrinntheGreatWolfDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for other_minion in own_board:
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
        for other_minion in own_board:
            if MinionType.Dragon in other_minion.types:
                other_minion.divine_shield = True


class TheTideRazorDeathrattle(Deathrattle):
    " Summon 3 random Pirates."
    def __init__(self):
        super().__init__(name="TheTideRazorDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        #TODO: IMPLEMENT
        pass