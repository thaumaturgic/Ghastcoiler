import logging

from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType
from deathrattles.rank_3 import InfestedWolfDeathrattle, PilotedShredderDeathrattle, RatPackDeathrattle

class ArcaneAssistant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Arcane Assistant",
                         rank=3,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Elemental],
                         **kwargs)

class ArmoftheEmpire(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Arm of the Empire",
                         rank=3,
                         base_attack=4,
                         base_defense=5,
                         **kwargs)

    def on_friendly_attacked(self, friendly_minion: Minion): #TODO: IMPLEMENT AND TEST
        """ Whenever a friendly Taunt minion is attacked, give it +3 Attack.
        """
        buff = 6 if self.golden else 3
        if friendly_minion.taunt:
            friendly_minion.add_stats(buff,0)

class BloodsailCannoneer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bloodsail Cannoneer",
                         rank=3,
                         base_attack=4,
                         base_defense=3,
                         types=[MinionType.Pirate],
                         **kwargs)

class BronzeWarden(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bronze Warden",
                         rank=3,
                         base_attack=2,
                         base_defense=1,
                         types=[MinionType.Dragon],
                         base_divine_shield=True,
                         base_reborn=True,
                         **kwargs)

class ColdlightSeer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Coldlight Seer",
                         rank=3,
                         base_attack=2,
                         base_defense=3,
                         types=[MinionType.Murloc],
                         **kwargs)
                         
class CracklingCyclone(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Crackling Cyclone",
                         rank=3,
                         base_attack=4,
                         base_defense=1,
                         types=[MinionType.Elemental],
                         base_divine_shield=True,
                         **kwargs)
        self.windfury = False if self.golden else True
        self.megawindfury = True if self.golden else False #TODO: TEST

class Crystalweaver(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Crystalweaver",
                         rank=3,
                         base_attack=5,
                         base_defense=4,
                         **kwargs)

class DeflectoBot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Deflect-o-Bot",
                         rank=3,
                         base_attack=3,
                         base_defense=2,
                         base_divine_shield=True,
                         types=[MinionType.Mech],
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion): #TODO: TEST
        if MinionType.Mech in other_minion.types:
            attack = 2 if self.golden else 1
            self.divine_shield = True
            self.add_stats(attack,0)

class FelfinNavigator(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Felfin Navigator",
                         rank=3,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Murloc],
                         **kwargs)

class HangryDragon(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Hangry Dragon",
                         rank=3,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Dragon],
                         **kwargs)

class Houndmaster(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Houndmaster",
                         rank=3,
                         base_attack=4,
                         base_defense=3,
                         **kwargs)

class ImpGangBoss(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Imp Gang Boss",
                         rank=3,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Demon],
                         **kwargs)

    def on_receive_damage(self):
        """Whenever this minion takes damage, summon a 1/1 Imp.""" #TODO: IMPLEMENT
        pass


class InfestedWolf(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Infested Wolf",
                         rank=3,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Beast],
                         base_deathrattle=InfestedWolfDeathrattle(), # TODO: TEST
                         **kwargs)

class IronSensei(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Iron Sensei",
                         rank=3,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Mech],
                         **kwargs)

# TODO: All the busted shit this guy does
class Khadgar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Khadgar",
                         rank=3,
                         base_attack=2,
                         base_defense=2,
                         **kwargs)

class MonstrousMacaw(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Monstrous Macaw",
                         rank=3,
                         base_attack=4,
                         base_defense=3,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_attacked_after(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        """After this attacks, trigger a random friendly minion's Deathrattle.
        """
        #TODO: IMPLEMENT
        pass

class PilotedShredder(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Piloted Shredder",
                         rank=3,
                         base_attack=4,
                         base_defense=3,
                         types=[MinionType.Mech],
                         base_deathrattle=PilotedShredderDeathrattle(), # TODO: TEST
                         **kwargs)

class RatPack(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rat Pack",
                         rank=3,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Beast],
                         base_deathrattle=RatPackDeathrattle(),
                         **kwargs)

class ReplicatingMenace(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Replicating Menace",
                         rank=3,
                         base_attack=3,
                         base_defense=1,
                         types=[MinionType.Mech],
                         base_deathrattle=RatPackDeathrattle(), #TODO: TEST
                         **kwargs)

class SaltyLooter(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Salty Looter",
                         rank=3,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Pirate],
                         **kwargs)

class ScrewjankClunker(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Screwjank Clunker",
                         rank=3,
                         base_attack=2,
                         base_defense=5,
                         types=[MinionType.Mech],
                         **kwargs)
                         
class SoulDevourer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Soul Devourer",
                         rank=3,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Demon],
                         **kwargs)

class SoulJuggler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Soul Juggler",
                         rank=3,
                         base_attack=3,
                         base_defense=3,
                         **kwargs)

    def on_friendly_removal(self, other_minion: Minion):
        """After a friendly Demon dies, deal 3 damage to a random enemy minion.
        """
        #TODO: 
        pass

class SouthseaStrongarm(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Southsea Strongarm",
                         rank=3,
                         base_attack=4,
                         base_defense=3,
                         types=[MinionType.Pirate],
                         **kwargs)

class StasisElemental(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Stasis Elemental",
                         rank=3,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Elemental],
                         **kwargs)

class TwilightEmissary(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Twilight Emissary",
                         rank=3,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Dragon],
                         **kwargs)

class WardenofOld(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Warden of Old",
                         rank=3,
                         base_attack=3,
                         base_defense=3,
                         # Dont care about death rattle
                         **kwargs)     
