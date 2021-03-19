import logging
import random

from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from minions.tokens import Robosaur, FieryImp, Hyena
from deathrattles.base import Deathrattle


class MechanoEggDeathrattle(Deathrattle):
    "Summon an 8/8 Robosaur."
    def __init__(self):
        super().__init__(name="MechanoEggDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        own_board.add_minion(Robosaur(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class RingMatronDeathrattle(Deathrattle):
    "Summon two 3/2 Imps."
    def __init__(self):
        super().__init__(name="RingMatronDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for _ in range(2):
            own_board.add_minion(FieryImp(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)


class SavannahHighmaneDeathrattle(Deathrattle):
    "Summon two 2/2 Hyenas."
    def __init__(self):
        super().__init__(name="SavannahHighmaneDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for _ in range(2):
            own_board.add_minion(Hyena(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)
