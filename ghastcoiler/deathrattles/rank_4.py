import logging

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
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = Robosaur,
            triggered_from_macaw = macaw_trigger)


class RingMatronDeathrattle(Deathrattle):
    "Summon two 3/2 Imps."
    def __init__(self):
        super().__init__(name="RingMatronDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = FieryImp,
            minions_to_spawn = 2,
            triggered_from_macaw = macaw_trigger)


class SavannahHighmaneDeathrattle(Deathrattle):
    "Summon two 2/2 Hyenas."
    def __init__(self):
        super().__init__(name="SavannahHighmaneDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        Deathrattle.summon_deathrattle_minions(own_board = own_board,
            summoning_minion = minion, 
            summoned_minion_class = Hyena,
            minions_to_spawn = 2,
            triggered_from_macaw = macaw_trigger)
