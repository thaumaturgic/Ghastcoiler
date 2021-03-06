import logging
import random

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType
from deathrattles.rank_6 import GentleDjinniDeathrattle, GhastcoilerDeathrattle, \
    GoldrinntheGreatWolfDeathrattle, \
    NadinatheRedDeathrattle, TheTideRazorDeathrattle


class Amalgadon(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Amalgadon",
                         id="BGS_069",
                         gold_id="TB_BaconUps_121",
                         rank=6,
                         base_attack=6,
                         base_health=6,
                         types=[MinionType.Murloc, MinionType.Dragon, MinionType.Demon, MinionType.Beast, MinionType.Mech, MinionType.Pirate, MinionType.Elemental, MinionType.Quilboar],
                         **kwargs)


class CaptainFlatTusk(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Captain Flat Tusk",
                         id="BG20_206",
                         gold_id="BG20_206_G",
                         rank=6,
                         base_attack=9,
                         base_health=6,
                         legendary=True,
                         types=[MinionType.Quilboar],
                         **kwargs)


class ArchdruidHamuul(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Archdruid Hamuul",
                         id="BG20_304",
                         gold_id="BG20_304_G",
                         rank=6,
                         base_attack=4,
                         base_health=4,
                         legendary=True,
                         **kwargs)


class Charlga(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Charlga",
                         id="BG20_303",
                         gold_id="BG20_303_G",
                         rank=6,
                         base_attack=4,
                         base_health=4,
                         legendary=True,
                         types=[MinionType.Quilboar],
                         **kwargs)


class DreadAdmiralEliza(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Dread Admiral Eliza",
                         id="BGS_047",
                         gold_id="TB_BaconUps_134",
                         rank=6,
                         base_attack=6,
                         base_health=7,
                         legendary=True,
                         types=[MinionType.Pirate],
                         **kwargs)

    def buff_board(self, own_board: PlayerBoard):
        attack = 4 if self.golden else 2
        health = 2 if self.golden else 1
        for minion in own_board.minions:
            minion.add_stats(attack, health)
        
    def on_attack_before(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.buff_board(own_board)

    def on_friendly_attack_before(self, attacking_minion: Minion, own_board: PlayerBoard):
        if MinionType.Pirate in attacking_minion.types:
            self.buff_board(own_board)


class FoeReaper4000(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Foe Reaper 4000",
                         id="GVG_113",
                         gold_id="TB_BaconUps_153",
                         rank=6,
                         base_attack=6,
                         base_health=9,
                         base_cleave=True,
                         legendary=True,
                         types=[MinionType.Mech],
                         **kwargs)


class GentleDjinni(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Gentle Djinni",
                         id="BGS_121",
                         gold_id="TB_BaconUps_165",
                         rank=6,
                         base_attack=4,
                         base_health=5,
                         base_deathrattle=GentleDjinniDeathrattle(),
                         types=[MinionType.Elemental],
                         **kwargs)


class Ghastcoiler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Ghastcoiler",
                         id="BGS_008",
                         gold_id="TB_BaconUps_057",
                         rank=6,
                         base_attack=7,
                         base_health=7,
                         base_deathrattle=GhastcoilerDeathrattle(),
                         types=[MinionType.Beast],
                         **kwargs)


class GoldrinntheGreatWolf(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Goldrinn, the Great Wolf",
                         id="BGS_018",
                         gold_id="TB_BaconUps_085",
                         rank=6,
                         base_attack=4,
                         base_health=4,
                         legendary=True,
                         base_deathrattle=GoldrinntheGreatWolfDeathrattle(),
                         types=[MinionType.Beast],
                         **kwargs)


class ImpMama(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Imp Mama",
                         id="BGS_044",
                         gold_id="TB_BaconUps_116",
                         rank=6,
                         base_attack=6,
                         base_health=10,
                         types=[MinionType.Demon],
                         **kwargs)

    def on_receive_damage(self, own_board: PlayerBoard):
        from utils.minion_utils import get_minions
        disallowed_demons = ["Amalgam", "Fiery Imp", "Imp", "Imp Mama", "Voidwalker"]
        select_demons = lambda x: (MinionType.Demon in x.types) and (x.name not in disallowed_demons)

        demons = get_minions(select_demons)
        demon = demons[random.randint(0,len(demons)-1)](taunt=True)
        own_board.add_minion(demon, self.position, True)


class KalecgosArcaneAspect(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kalecgos, Arcane Aspect",
                         id="BGS_041",
                         gold_id="TB_BaconUps_109",
                         rank=6,
                         base_attack=4,
                         base_health=12,
                         legendary=True,
                         types=[MinionType.Dragon],
                         **kwargs)


class LieutenantGarr(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Lieutenant Garr",
                         id="BGS_124",
                         gold_id="TB_BaconUps_163",
                         rank=6,
                         base_attack=8,
                         base_health=8,
                         legendary=True,
                         types=[MinionType.Elemental],
                         **kwargs)


class LilRag(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Lil' Rag",
                         id="BGS_100",
                         gold_id="TB_BaconUps_200",
                         rank=6,
                         base_attack=6,
                         base_health=6,
                         legendary=True,
                         types=[MinionType.Elemental],
                         **kwargs)


class Maexxna(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Maexxna",
                         id="FP1_010",
                         gold_id="TB_BaconUps_155",
                         rank=6,
                         base_attack=2,
                         base_health=8,
                         base_poisonous=True,
                         legendary=True,
                         types=[MinionType.Beast],
                         **kwargs)


class NadinatheRed(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nadina the Red",
                         id="BGS_040",
                         gold_id="TB_BaconUps_154",
                         rank=6,
                         base_attack=7,
                         base_health=4,
                         legendary=True,
                         base_deathrattle=NadinatheRedDeathrattle(),
                         **kwargs)


class TheTideRazor(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="The Tide Razor",
                         id="BGS_079",
                         gold_id="TB_BaconUps_137",
                         rank=6,
                         base_attack=6,
                         base_health=4,
                         base_deathrattle=TheTideRazorDeathrattle(),
                         **kwargs)


class ZappSlywick(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Zapp Slywick",
                         id="BGS_022",
                         gold_id="TB_BaconUps_091",
                         rank=6,
                         base_attack=7,
                         base_health=10,
                         base_windfury=True,
                         legendary=True,
                         **kwargs)
        self.windfury = False if self.golden else True
        self.mega_windfury = True if self.golden else False
        self.attacks_lowest_power = True
