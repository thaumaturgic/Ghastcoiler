import logging
import random

from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType
from minions.tokens import Imp
from deathrattles.rank_3 import InfestedWolfDeathrattle, \
    RatPackDeathrattle, \
    ReplicatingMenaceDeathrattle


class ArcaneAssistant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Arcane Assistant",
                         id="BGS_128",
                         gold_id="TB_Baconups_203",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Elemental],
                         **kwargs)


class ArmoftheEmpire(Minion):
    """ Whenever a friendly Taunt minion is attacked, give it +2 Attack permanently."""
    def __init__(self, **kwargs):
        super().__init__(name="Arm of the Empire",
                         id="BGS_110",
                         gold_id="TB_BaconUps_302",
                         rank=3,
                         base_attack=4,
                         base_health=5,
                         **kwargs)

    def buff_taunted_minion(self, friendly_minion: Minion):
        buff = 4 if self.golden else 2
        if friendly_minion.taunt:
            friendly_minion.add_stats(buff, 0)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.buff_taunted_minion(self)

    def on_friendly_attacked(self, friendly_minion: Minion):
        self.buff_taunted_minion(friendly_minion)


class Bannerboar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bannerboar",
                         id="BG20_201",
                         gold_id="BG20_201_G",
                         rank=3,
                         base_attack=1,
                         base_health=4,
                         types=[MinionType.Quilboar],
                         **kwargs)


# TODO: Implement frenzy, or not since its going to get removed lol
class BarrensBlacksmith(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Barrens Blacksmith",
                         id="BAR_073",
                         gold_id="TB_BaconUps_320",
                         rank=3,
                         base_attack=3,
                         base_health=5,
                         **kwargs)


class BloodsailCannoneer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bloodsail Cannoneer",
                         id="BGS_053",
                         gold_id="TB_BaconUps_138",
                         rank=3,
                         base_attack=4,
                         base_health=3,
                         types=[MinionType.Pirate],
                         **kwargs)


class BristlebackBrute(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bristleback Brute",
                         id="BG20_103",
                         gold_id="BG20_103_G",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Quilboar],
                         **kwargs)


class BronzeWarden(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bronze Warden",
                         id="BGS_034",
                         gold_id="TB_BaconUps_149",
                         rank=3,
                         base_attack=2,
                         base_health=1,
                         types=[MinionType.Dragon],
                         base_divine_shield=True,
                         base_reborn=True,
                         **kwargs)


class ColdlightSeer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Coldlight Seer",
                         id="EX1_103",
                         gold_id="TB_BaconUps_064",
                         rank=3,
                         base_attack=2,
                         base_health=3,
                         types=[MinionType.Murloc],
                         **kwargs)


class CracklingCyclone(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Crackling Cyclone",
                         id="BGS_119",
                         gold_id="TB_BaconUps_159",
                         rank=3,
                         base_attack=4,
                         base_health=1,
                         types=[MinionType.Elemental],
                         base_divine_shield=True,
                         **kwargs)
        self.windfury = False if self.golden else True
        self.mega_windfury = True if self.golden else False


class Crystalweaver(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Crystalweaver",
                         id="CFM_610",
                         gold_id="TB_BaconUps_070",
                         rank=3,
                         base_attack=5,
                         base_health=4,
                         **kwargs)


class DeflectoBot(Minion):
    """Whenever you summon a Mech during combat, gain +1 Attack and Divine Shield."""
    def __init__(self, **kwargs):
        super().__init__(name="Deflect-o-Bot",
                         id="BGS_071",
                         gold_id="TB_BaconUps_123",
                         rank=3,
                         base_attack=3,
                         base_health=2,
                         base_divine_shield=True,
                         types=[MinionType.Mech],
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion):
        if MinionType.Mech in other_minion.types:
            attack = 2 if self.golden else 1
            self.divine_shield = True
            self.add_stats(attack, 0)


class FelfinNavigator(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Felfin Navigator",
                         id="BT_010",
                         gold_id="TB_BaconUps_124",
                         rank=3,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Murloc],
                         **kwargs)


class HangryDragon(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Hangry Dragon",
                         id="BGS_033",
                         gold_id="TB_BaconUps_104",
                         rank=3,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Dragon],
                         **kwargs)


class Houndmaster(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Houndmaster",
                         id="DS1_070",
                         gold_id="TB_BaconUps_068",
                         rank=3,
                         base_attack=4,
                         base_health=3,
                         **kwargs)


class ImpGangBoss(Minion):
    """Whenever this minion takes damage, summon a 1/1 Imp."""
    def __init__(self, **kwargs):
        super().__init__(name="Imp Gang Boss",
                         id="BRM_006",
                         gold_id="TB_BaconUps_030",
                         rank=3,
                         base_attack=2,
                         base_health=4,
                         types=[MinionType.Demon],
                         **kwargs)

    def on_receive_damage(self, own_board: PlayerBoard):
        own_board.add_minion(Imp(golden=self.golden, attacked=self.attacked), position=self.position+1)


class InfestedWolf(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Infested Wolf",
                         id="OG_216",
                         gold_id="TB_BaconUps_026",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Beast],
                         base_deathrattle=InfestedWolfDeathrattle(),
                         **kwargs)


class IronSensei(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Iron Sensei",
                         id="GVG_027",
                         gold_id="TB_BaconUps_044",
                         rank=3,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Mech],
                         **kwargs)


class Khadgar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Khadgar",
                         id="DAL_575",
                         gold_id="TB_BaconUps_034",
                         rank=3,
                         base_attack=2,
                         base_health=2,
                         mana_cost=2,
                         legendary=True,
                         **kwargs)

    def on_self_summon(self, own_board: PlayerBoard):
        own_board.token_creation_multiplier += 2 if self.golden else 1

    def on_self_removal(self, own_board: PlayerBoard):
        own_board.token_creation_multiplier -= 2 if self.golden else 1


class MonstrousMacaw(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Monstrous Macaw",
                         id="BGS_078",
                         gold_id="TB_BaconUps_135",
                         rank=3,
                         base_attack=4,
                         base_health=3,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_attack_after(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        """After this attacks, trigger a random friendly minion's Deathrattle."""
        deathrattles = []
        for minion in own_board.minions:
            for deathrattle in minion.deathrattles:
                deathrattles += [[minion, deathrattle]]

        if len(deathrattles) == 0:
            return

        triggers = 2 if self.golden else 1
        for _ in range(triggers):
            for _ in range(own_board.deathrattle_multiplier):
                index = random.randint(0, len(deathrattles) - 1)
                minion_pair = deathrattles[index]
                # TODO: Multiply this with baron?
                minion_pair[1].trigger(minion_pair[0], own_board, opposing_board, macaw_trigger=True)


class Necrolyte(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Necrolyte",
                         id="BG20_202",
                         gold_id="BG20_202_G",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Quilboar],
                         **kwargs)


# class PilotedShredder(Minion):
#     def __init__(self, **kwargs):
#         super().__init__(name="Piloted Shredder",
#                          id="BGS_023",
#                          gold_id="TB_BaconUps_035",
#                          rank=3,
#                          base_attack=4,
#                          base_health=3,
#                          types=[MinionType.Mech],
#                          base_deathrattle=PilotedShredderDeathrattle(),
#                          **kwargs)


class RatPack(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rat Pack",
                         id="CFM_316",
                         gold_id="TB_BaconUps_027",
                         rank=3,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Beast],
                         base_deathrattle=RatPackDeathrattle(),
                         **kwargs)


class ReplicatingMenace(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Replicating Menace",
                         id="BOT_312",
                         gold_id="TB_BaconUps_032",
                         rank=3,
                         base_attack=3,
                         base_health=1,
                         types=[MinionType.Mech],
                         base_deathrattle=ReplicatingMenaceDeathrattle(),
                         **kwargs)


class SaltyLooter(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Salty Looter",
                         id="BGS_081",
                         gold_id="TB_BaconUps_143",
                         rank=3,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Pirate],
                         **kwargs)


class ScrewjankClunker(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Screwjank Clunker",
                         id="GVG_055",
                         gold_id="TB_BaconUps_069",
                         rank=3,
                         base_attack=2,
                         base_health=5,
                         types=[MinionType.Mech],
                         **kwargs)


class SoulDevourer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Soul Devourer",
                         id="BGS_059",
                         gold_id="TB_BaconUps_119",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Demon],
                         **kwargs)


class SoulJuggler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Soul Juggler",
                         id="BGS_002",
                         gold_id="TB_BaconUps_075",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         **kwargs)

    # TODO: TEST
    def on_friendly_removal_after(self, other_minion: Minion, friendly_board: PlayerBoard, enemy_board: PlayerBoard):
        """After a friendly Demon dies, deal 3 damage to a random enemy minion.
        """
        triggers = 2 if self.golden else 1
        if MinionType.Demon in other_minion.types:
            for _ in range(triggers):
                target = enemy_board.random_minion()
                if target:
                    target.receive_damage(3, False, enemy_board)


class SouthseaStrongarm(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Southsea Strongarm",
                         id="BGS_048",
                         gold_id="TB_BaconUps_140",
                         rank=3,
                         base_attack=4,
                         base_health=3,
                         types=[MinionType.Pirate],
                         **kwargs)


class StasisElemental(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Stasis Elemental",
                         id="BGS_122",
                         gold_id="TB_BaconUps_161",
                         rank=3,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Elemental],
                         **kwargs)


class Thorncaller(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Thorncaller",
                         id="BG20_105",
                         gold_id="BG20_105_G",
                         rank=3,
                         base_attack=4,
                         base_health=3,
                         types=[MinionType.Quilboar],
                         **kwargs)


class TwilightEmissary(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Twilight Emissary",
                         id="BGS_038",
                         gold_id="TB_BaconUps_108",
                         rank=3,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Dragon],
                         **kwargs)


class WardenofOld(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Warden of Old",
                         id="BGS_200",
                         gold_id="TB_BaconUps_256",
                         rank=3,
                         base_attack=3,
                         base_health=3,
                         **kwargs)
