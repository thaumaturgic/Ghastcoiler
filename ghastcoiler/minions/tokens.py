from minions.base import Minion
from minions.types import MinionType

class BigBadWolf(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Big Bad Wolf",
                         rank=1,
                         base_attack=3,
                         base_defense=2,
                         types=[MinionType.Beast],
                         **kwargs)

class DamagedGolem(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Damaged Golem",
                         rank=1,
                         base_attack=2,
                         base_defense=1,
                         types=[MinionType.Mech],
                         **kwargs)


class FieryImp(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Fiery Imp",
                         rank=1,
                         base_attack=3,
                         base_defense=2,
                         types=[MinionType.Demon],
                         **kwargs)

class GuardBot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Guard Bot",
                         rank=1,
                         base_attack=2,
                         base_defense=3,
                         base_taunt=True,
                         types=[MinionType.Mech],
                         **kwargs)


class Hyena(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Hyena",
                         rank=1,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Beast],
                         **kwargs)


class Imp(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Imp",
                         rank=1,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Demon],
                         **kwargs)


class Microbot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Microbot",
                         rank=1,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Mech],
                         **kwargs)


class Rat(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rat",
                         rank=1,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Beast],
                         **kwargs)


class Robosaur(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Robosaur",
                         rank=1,
                         base_attack=8,
                         base_defense=8,
                         types=[MinionType.Mech],
                         **kwargs)


class SkyPirate(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Sky Pirate",
                         rank=1,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Pirate],
                         **kwargs)


class Spider(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Spider",
                         rank=1,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Beast],
                         **kwargs)
