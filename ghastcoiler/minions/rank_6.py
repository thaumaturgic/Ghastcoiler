import logging

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType
from deathrattles.rank_6 import GentleDjinniDeathrattle, GhastcoilerDeathrattle, \
    GoldrinntheGreatWolfDeathrattle, KangorsApprenticeDeathrattle, \
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
                         types=[MinionType.Quilboar],
                         **kwargs)


class Charlga(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Charlga",
                         id="BG20_303",
                         gold_id="BG20_303_G",
                         rank=6,
                         base_attack=7,
                         base_health=7,
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
                         types=[MinionType.Mech],
                         **kwargs)


class GentleDjinni(Minion):
    #TODO: Test Deathrattle
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
    #TODO: Test Deathrattle
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
                         base_deathrattle=GoldrinntheGreatWolfDeathrattle(),
                         types=[MinionType.Beast],
                         **kwargs)


class ImpMama(Minion):
    #TODO: On damage trigger
    def __init__(self, **kwargs):
        super().__init__(name="Imp Mama",
                         id="BGS_044",
                         gold_id="TB_BaconUps_116",
                         rank=6,
                         base_attack=6,
                         base_health=10,
                         types=[MinionType.Demon],
                         **kwargs)


class KalecgosArcaneAspect(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kalecgos, Arcane Aspect",
                         id="BGS_041",
                         gold_id="TB_BaconUps_109",
                         rank=6,
                         base_attack=4,
                         base_health=12,
                         types=[MinionType.Dragon],
                         **kwargs)


class KangorsApprentice(Minion):
    #TODO: Deathrattle
    def __init__(self, **kwargs):
        super().__init__(name="Kangor's Apprentice",
                         id="BGS_012",
                         gold_id="TB_BaconUps_087",
                         rank=6,
                         base_attack=4,
                         base_health=8,
                         base_deathrattle=KangorsApprenticeDeathrattle(),
                         **kwargs)


class LieutenantGarr(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Lieutenant Garr",
                         id="BGS_124",
                         gold_id="TB_BaconUps_163",
                         rank=6,
                         base_attack=8,
                         base_health=1,
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
                         base_deathrattle=NadinatheRedDeathrattle(),
                         **kwargs)


class TheTideRazor(Minion):
    #TODO:Test Deathrattle
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
                         **kwargs)
        self.windfury = False if self.golden else True
        self.mega_windfury = True if self.golden else False
        self.attacks_lowest_power = True
