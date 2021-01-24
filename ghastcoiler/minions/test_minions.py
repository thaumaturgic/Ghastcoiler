import logging

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType

class PunchingBag(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="PunchingBag",
                         rank=1,
                         base_attack=0,
                         base_defense=100,
                         **kwargs)
                         