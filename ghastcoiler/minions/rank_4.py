import logging

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType
from minions.tokens import GuardBot
from deathrattles.rank_4 import MechanoEggDeathrattle, RingMatronDeathrattle, \
    SavannahHighmaneDeathrattle


class AnnoyoModule(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Annoy-o-Module",
                         rank=4,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Mech],
                         base_taunt=True,
                         base_divine_shield=True,
                         **kwargs)


class Bigfernal(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bigfernal",
                         rank=4,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Demon],
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion):
        if MinionType.Demon in other_minion.types:
            stats = 2 if self.golden else 1
            self.add_stats(stats, stats)


class BolvarFireblood(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bolvar, Fireblood",
                         rank=4,
                         base_attack=1,
                         base_defense=7,
                         base_divine_shield=True,
                         **kwargs)

    def on_any_minion_loses_divine_shield(self):
        self.add_stats(4 if self.golden else 2, 0)


class CaveHydra(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="CaveHydra",
                         rank=4,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Beast],
                         base_cleave=True,
                         **kwargs)


class ChampionofYShaarj(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Champion of Y'Shaarj",
                         rank=4,
                         base_attack=4,
                         base_defense=4,
                         **kwargs)

    def on_friendly_attacked(self, friendly_minion: Minion):
        if friendly_minion.taunt:
            stats = 2 if self.golden else 1
            self.add_stats(stats, stats)


class CobaltScalebane(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Cobalt Scalebane",
                         rank=4,
                         base_attack=5,
                         base_defense=5,
                         types=[MinionType.Dragon],
                         **kwargs)


class DefenderofArgus(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Defender of Argus",
                         rank=4,
                         base_attack=2,
                         base_defense=3,
                         **kwargs)


class DrakonidEnforcer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Drakonid Enforcer",
                         rank=4,
                         base_attack=3,
                         base_defense=6,
                         types=[MinionType.Dragon],
                         **kwargs)

    def on_any_minion_loses_divine_shield(self):
        stats = 4 if self.golden else 2
        self.add_stats(stats, stats)


class Goldgrubber(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Goldgrubber",
                         rank=4,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Pirate],
                         **kwargs)


class HeraldofFlame(Minion):  # TODO: Overkill trigger
    def __init__(self, **kwargs):
        super().__init__(name="Herald of Flame",
                         rank=4,
                         base_attack=5,
                         base_defense=6,
                         types=[MinionType.Dragon],
                         **kwargs)


class MajordomoExecutus(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Majordomo Executus",
                         rank=4,
                         base_attack=6,
                         base_defense=3,
                         **kwargs)


class MechanoEgg(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Mechano-Egg",
                         rank=4,
                         base_attack=0,
                         base_defense=5,
                         types=[MinionType.Mech],
                         base_deathrattle=MechanoEggDeathrattle(),
                         **kwargs)


class MenagerieJug(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Menagerie Jug",
                         rank=4,
                         base_attack=3,
                         base_defense=3,
                         **kwargs)


class PrimalfinLookout(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Primalfin Lookout",
                         rank=4,
                         base_attack=3,
                         base_defense=2,
                         types=[MinionType.Murloc],
                         **kwargs)


class QirajiHarbinger(Minion):
    "After a friendly minion with Taunt dies, give its neighbors +2/+2."
    def __init__(self, **kwargs):
        super().__init__(name="Qiraji Harbinger",
                         rank=4,
                         base_attack=5,
                         base_defense=5,
                         **kwargs)

    def on_friendly_removal(self, other_minion: Minion):
        if other_minion.taunt:
            pass #  TODO
        pass


class RingMatron(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Ring Matron",
                         rank=4,
                         base_attack=6,
                         base_defense=4,
                         types=[MinionType.Demon],
                         base_deathrattle=RingMatronDeathrattle(),
                         **kwargs)


class RipsnarlCaptain(Minion):
    "Whenever another friendly Pirate attacks, give it +2/+2."
    def __init__(self, **kwargs):
        super().__init__(name="Ripsnarl Captain",
                         rank=4,
                         base_attack=4,
                         base_defense=5,
                         types=[MinionType.Pirate],
                         **kwargs)

    def on_friendly_attack_before(self, attacking_minion: Minion, own_board: PlayerBoard):
        stats = 4 if self.golden else 2
        if MinionType.Pirate in attacking_minion.types:
            attacking_minion.add_stats(stats, stats)


class SavannahHighmane(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Savannah Highmane",
                         rank=4,
                         base_attack=6,
                         base_defense=5,
                         types=[MinionType.Beast],
                         base_deathrattle=SavannahHighmaneDeathrattle(),
                         **kwargs)


class SecurityRover(Minion):
    "Whenever this minion takes damage, summon a 2/3 Mech with Taunt."
    def __init__(self, **kwargs):
        super().__init__(name="Security Rover",
                         rank=4,
                         base_attack=2,
                         base_defense=6,
                         types=[MinionType.Mech],
                         **kwargs)

    def on_receive_damage(self, own_board: PlayerBoard):  # TODO: TEST
        own_board.add_minion(GuardBot(golden=self.golden, attacked=self.attacked), position=self.position+1)


class Siegebreaker(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Siegebreaker",
                         rank=4,
                         base_attack=5,
                         base_defense=8,
                         base_taunt=True,
                         types=[MinionType.Demon],
                         **kwargs)

    def adjust_demon_power(self, other_minion: Minion, add_power: bool):
        buffAmount = 2 if self.golden else 1
        if MinionType.Demon in other_minion.types:
            if add_power:
                other_minion.add_stats(buffAmount, 0)
            else:
                other_minion.remove_stats(buffAmount, 0)

    def on_summon(self, other_minion: Minion, own_board: PlayerBoard):
        self.adjust_demon_power(other_minion, True)

    def on_friendly_summon(self, other_minion: Minion):
        self.adjust_demon_power(other_minion, True)

    def on_removal(self, other_minion: Minion, own_board: PlayerBoard):
        self.adjust_demon_power(other_minion, False)


class Toxfin(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Toxfin",
                         rank=4,
                         base_attack=1,
                         base_defense=2,
                         types=[MinionType.Murloc],
                         **kwargs)


class VirmenSensei(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Virmen Sensei",
                         rank=4,
                         base_attack=4,
                         base_defense=5,
                         **kwargs)


class WildfireElemental(Minion):
    # TODO: Overkill triggers
    def __init__(self, **kwargs):
        super().__init__(name="Wildfire Elemental",
                         rank=4,
                         base_attack=7,
                         base_defense=3,
                         types=[MinionType.Elemental],
                         **kwargs)
