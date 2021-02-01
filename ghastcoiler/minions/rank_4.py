import logging

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType


class CaveHydra(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="CaveHydra",
                         rank=4,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Beast],
                         base_cleave=True,
                         **kwargs)
