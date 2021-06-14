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
                         id="BOT_911",
                         gold_id="TB_BaconUps_099",
                         rank=4,
                         base_attack=2,
                         base_health=4,
                         types=[MinionType.Mech],
                         base_taunt=True,
                         base_divine_shield=True,
                         **kwargs)


class Bigfernal(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bigfernal",
                         id="BGS_204",
                         gold_id="TB_BaconUps_304",
                         rank=4,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Demon],
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion):
        if MinionType.Demon in other_minion.types:
            stats = 2 if self.golden else 1
            self.add_stats(stats, stats)


class BolvarFireblood(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bolvar, Fireblood",
                         id="ICC_858",
                         gold_id="TB_BaconUps_047",
                         rank=4,
                         base_attack=1,
                         base_health=7,
                         base_divine_shield=True,
                         legendary=True,
                         **kwargs)

    def on_friendly_minion_loses_divine_shield(self):
        self.add_stats(4 if self.golden else 2, 0)


class Bonker(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bonker",
                         id="BG20_104",
                         gold_id="BG20_104_G",
                         rank=4,
                         base_attack=3,
                         base_health=7,
                         types=[MinionType.Quilboar],
                         base_windfury=True,
                         **kwargs)


class CaveHydra(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Cave Hydra",
                         id="LOOT_078",
                         gold_id="TB_BaconUps_151",
                         rank=4,
                         base_attack=2,
                         base_health=4,
                         types=[MinionType.Beast],
                         base_cleave=True,
                         **kwargs)


class ChampionofYShaarj(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Champion of Y'Shaarj",
                         id="BGS_111",
                         gold_id="TB_BaconUps_301",
                         rank=4,
                         base_attack=4,
                         base_health=4,
                         **kwargs)

    def on_friendly_attacked(self, friendly_minion: Minion):
        if friendly_minion.taunt:
            stats = 2 if self.golden else 1
            self.add_stats(stats, stats)


class CobaltScalebane(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Cobalt Scalebane",
                         id="ICC_029",
                         gold_id="TB_BaconUps_120",
                         rank=4,
                         base_attack=5,
                         base_health=5,
                         types=[MinionType.Dragon],
                         **kwargs)


class DefenderofArgus(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Defender of Argus",
                         id="EX1_093",
                         gold_id="TB_BaconUps_009",
                         rank=4,
                         base_attack=2,
                         base_health=3,
                         **kwargs)


class DrakonidEnforcer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Drakonid Enforcer",
                         id="BGS_067",
                         gold_id="TB_BaconUps_117",
                         rank=4,
                         base_attack=3,
                         base_health=6,
                         types=[MinionType.Dragon],
                         **kwargs)

    def on_friendly_minion_loses_divine_shield(self):
        stats = 4 if self.golden else 2
        self.add_stats(stats, stats)


class DynamicDuo(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Dynamic Duo",
                         id="BG20_207",
                         gold_id="BG20_207_G",
                         rank=4,
                         base_attack=3,
                         base_health=4,
                         base_taunt=True,
                         types=[MinionType.Quilboar],
                         **kwargs)


class HexruinMarauder(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Hexruin Marauder",
                         id="BG20_210",
                         gold_id="BG20_210_G",
                         rank=4,
                         base_attack=3,
                         base_health=5,
                         types=[MinionType.Demon],
                         **kwargs)


class Goldgrubber(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Goldgrubber",
                         id="BGS_066",
                         gold_id="TB_BaconUps_130",
                         rank=4,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Pirate],
                         **kwargs)


class Groundshaker(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Groundshaker",
                         id="BG20_106",
                         gold_id="BG20_106_G",
                         rank=4,
                         base_attack=2,
                         base_health=6,
                         types=[MinionType.Quilboar],
                         **kwargs)


class HeraldofFlame(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Herald of Flame",
                         id="BGS_032",
                         gold_id="TB_BaconUps_103",
                         rank=4,
                         base_attack=6,
                         base_health=6,
                         types=[MinionType.Dragon],
                         **kwargs)

    def on_overkill(self, overkill_amount: int, enemy_board: PlayerBoard):
        damage = 6 if self.golden else 3
        minion_index = 0
        while minion_index < len(enemy_board.minions):
            _, enemy_health = enemy_board.minions[minion_index].receive_damage(amount=damage, poisonous=False, own_board = enemy_board, defer_damage_trigger=True)
            if enemy_health >= 0:
                return
            minion_index += 1

class Junkbot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Junkbot",
                         id="GVG_106",
                         gold_id="TB_BaconUps_046",
                         rank=4,
                         base_attack=1,
                         base_health=5,
                         types=[MinionType.Mech],
                         **kwargs)
    
    #TODO: TEST
    def on_friendly_removal(self, other_minion: Minion):
        if MinionType.Mech in other_minion.types:
            stats = 4 if self.golden else 2
            self.add_stats(stats, stats)


class MajordomoExecutus(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Majordomo Executus",
                         id="BGS_105",
                         gold_id="TB_BaconUps_207",
                         rank=4,
                         base_attack=6,
                         base_health=3,
                         legendary=True,
                         **kwargs)


class MechanoEgg(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Mechano-Egg",
                         id="BOT_537",
                         gold_id="TB_BaconUps_039",
                         rank=4,
                         base_attack=0,
                         base_health=5,
                         types=[MinionType.Mech],
                         base_deathrattle=MechanoEggDeathrattle(),
                         **kwargs)


class MenagerieJug(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Menagerie Jug",
                         id="BGS_083",
                         gold_id="TB_BaconUps_145",
                         rank=4,
                         base_attack=3,
                         base_health=3,
                         **kwargs)


class PrimalfinLookout(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Primalfin Lookout",
                         id="BGS_020",
                         gold_id="TB_BaconUps_089",
                         rank=4,
                         base_attack=3,
                         base_health=2,
                         types=[MinionType.Murloc],
                         **kwargs)


class QirajiHarbinger(Minion):
    "After a friendly minion with Taunt dies, give its neighbors +2/+2."
    def __init__(self, **kwargs):
        super().__init__(name="Qiraji Harbinger",
                         id="BGS_112",
                         gold_id="TB_BaconUps_303",
                         rank=4,
                         base_attack=5,
                         base_health=5,
                         **kwargs)

    def on_friendly_removal_after(self, other_minion: Minion, enemy_board: PlayerBoard):
        if other_minion.taunt:
            pass  # TODO
        pass


class RingMatron(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Ring Matron",
                         id="DMF_533",
                         gold_id="TB_BaconUps_309",
                         rank=4,
                         base_attack=6,
                         base_health=4,
                         types=[MinionType.Demon],
                         base_deathrattle=RingMatronDeathrattle(),
                         **kwargs)


class RipsnarlCaptain(Minion):
    "Whenever another friendly Pirate attacks, give it +2/+2."
    def __init__(self, **kwargs):
        super().__init__(name="Ripsnarl Captain",
                         id="BGS_056",
                         gold_id="TB_BaconUps_139",
                         rank=4,
                         base_attack=4,
                         base_health=5,
                         types=[MinionType.Pirate],
                         **kwargs)

    def on_friendly_attack_before(self, attacking_minion: Minion, own_board: PlayerBoard):
        stats = 4 if self.golden else 2
        if MinionType.Pirate in attacking_minion.types:
            attacking_minion.add_stats(stats, stats)


class SavannahHighmane(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Savannah Highmane",
                         id="EX1_534",
                         gold_id="TB_BaconUps_049",
                         rank=4,
                         base_attack=6,
                         base_health=5,
                         types=[MinionType.Beast],
                         base_deathrattle=SavannahHighmaneDeathrattle(),
                         **kwargs)


class SecurityRover(Minion):
    "Whenever this minion takes damage, summon a 2/3 Mech with Taunt."
    def __init__(self, **kwargs):
        super().__init__(name="Security Rover",
                         id="BOT_218",
                         gold_id="TB_BaconUps_041",
                         rank=4,
                         base_attack=2,
                         base_health=6,
                         types=[MinionType.Mech],
                         **kwargs)

    def on_receive_damage(self, own_board: PlayerBoard):  # TODO: TEST
        own_board.add_minion(GuardBot(golden=self.golden, attacked=self.attacked), position=self.position+1)


# class Siegebreaker(Minion):
#     def __init__(self, **kwargs):
#         super().__init__(name="Siegebreaker",
#                          id="EX1_185",
#                          gold_id="TB_BaconUps_053",
#                          rank=4,
#                          base_attack=5,
#                          base_health=8,
#                          base_taunt=True,
#                          types=[MinionType.Demon],
#                          **kwargs)

#     def adjust_demon_power(self, other_minion: Minion, add_power: bool):
#         buffAmount = 2 if self.golden else 1
#         if MinionType.Demon in other_minion.types:
#             if add_power:
#                 other_minion.add_stats(buffAmount, 0)
#             else:
#                 other_minion.remove_stats(buffAmount, 0)

#     def on_summon(self, other_minion: Minion, own_board: PlayerBoard):
#         self.adjust_demon_power(other_minion, True)

#     def on_friendly_summon(self, other_minion: Minion):
#         self.adjust_demon_power(other_minion, True)

#     def on_removal(self, other_minion: Minion, own_board: PlayerBoard):
#         self.adjust_demon_power(other_minion, False)


class Toxfin(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Toxfin",
                         id="DAL_077",
                         gold_id="TB_BaconUps_152",
                         rank=4,
                         base_attack=1,
                         base_health=2,
                         types=[MinionType.Murloc],
                         **kwargs)


class VirmenSensei(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Virmen Sensei",
                         id="CFM_816",
                         gold_id="TB_BaconUps_074",
                         rank=4,
                         base_attack=4,
                         base_health=5,
                         **kwargs)


class WildfireElemental(Minion):
    # TODO: Overkill triggers
    def __init__(self, **kwargs):
        super().__init__(name="Wildfire Elemental",
                         id="BGS_126",
                         gold_id="TB_BaconUps_166",
                         rank=4,
                         base_attack=7,
                         base_health=3,
                         types=[MinionType.Elemental],
                         **kwargs)
