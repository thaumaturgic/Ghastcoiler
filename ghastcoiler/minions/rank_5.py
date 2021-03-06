import logging

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType

from deathrattles.rank_5 import KingBagurgleDeathrattle, SneedsOldShredderDeathrattle, VoidlordDeathrattle, \
    KangorsApprenticeDeathrattle
from minions.tokens import IronhideRunt

class AgamaggantheGreatBoar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Agamaggan, the Great Boar",
                         id="BG20_205",
                         gold_id="BG20_205_G",
                         rank=5,
                         base_attack=6,
                         base_health=6,
                         legendary=True,
                         types=[MinionType.Quilboar],
                         **kwargs)


class AggemThorncurse(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Aggem Thorncurse",
                         id="BG20_302",
                         gold_id="BG20_302_G",
                         rank=5,
                         base_attack=3,
                         base_health=6,
                         legendary=True,
                         types=[MinionType.Quilboar],
                         **kwargs)


class AnnihilanBattlemaster(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Annihilan Battlemaster",
                         id="BGS_010",
                         gold_id="TB_BaconUps_083",
                         rank=5,
                         base_attack=3,
                         base_health=1,
                         types=[MinionType.Demon],
                         **kwargs)


class BaronRivendare(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Baron Rivendare",
                         id="FP1_031",
                         gold_id="TB_BaconUps_055",
                         rank=5,
                         base_attack=1,
                         base_health=7,
                         legendary=True,
                         **kwargs)

    def determine_board_deathrattle_multiplier(self, own_board: PlayerBoard, count_self: bool):
        barons = [minion for minion in own_board.minions if minion.name == "Baron Rivendare"]
        
        if count_self:
            barons += [self]

        if any(baron.golden for baron in barons):
            multiplier = 3
        elif len(barons) > 0:
            multiplier = 2
        else:
            multiplier = 1

        own_board.deathrattle_multiplier = multiplier

    def on_self_summon(self, own_board: PlayerBoard):
        self.determine_board_deathrattle_multiplier(own_board, True)

    def on_self_removal(self, own_board: PlayerBoard):
        self.determine_board_deathrattle_multiplier(own_board, False)


class BrannBronzebeard(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Brann Bronzebeard",
                         id="LOE_077",
                         gold_id="TB_BaconUps_045",
                         rank=5,
                         base_attack=2,
                         base_health=4,
                         legendary=True,
                         **kwargs)


class BristlebackKnight(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Bristleback Knight",
                         id="BG20_204",
                         gold_id="BG20_204_G",
                         rank=5,
                         base_attack=4,
                         base_health=8,
                         base_divine_shield=True,
                         base_windfury=True,
                         types=[MinionType.Quilboar],
                         **kwargs)
        self.windfury = False if self.golden else True
        self.mega_windfury = True if self.golden else False
        self.frenzy_triggered = False

    def on_receive_damage(self, own_board: PlayerBoard):
        if not self.frenzy_triggered:
            self.divine_shield = True
            self.frenzy_triggered = True


class CapnHoggarr(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Cap'n Hoggarr",
                         id="BGS_072",
                         gold_id="TB_BaconUps_133",
                         rank=5,
                         base_attack=6,
                         base_health=6,
                         legendary=True,
                         types=[MinionType.Pirate],
                         **kwargs)


class DeadlySpore(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Deadly Spore",
                         id="BGS_131",
                         gold_id="TB_BaconUps_251",
                         rank=5,
                         base_attack=1,
                         base_health=1,
                         base_poisonous=True,
                         **kwargs)


class FacelessTaverngoer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Faceless Taverngoer",
                         id="BGS_113",
                         gold_id="TB_BaconUps_305",
                         rank=5,
                         base_attack=4,
                         base_health=4,
                         **kwargs)


class IronhideDirehorn(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Ironhide Direhorn",
                         id="TRL_232",
                         gold_id="TB_BaconUps_051",
                         rank=5,
                         base_attack=7,
                         base_health=7,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_overkill(self, friendly_board: PlayerBoard, defending_minion: Minion, enemy_board: PlayerBoard):
        friendly_board.add_minion(IronhideRunt(attacked = self.attacked, golden = self.golden), self.position+1)


class KangorsApprentice(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kangor's Apprentice",
                         id="BGS_012",
                         gold_id="TB_BaconUps_087",
                         rank=5,
                         base_attack=3,
                         base_health=6,
                         base_deathrattle=KangorsApprenticeDeathrattle(),
                         **kwargs)


class KingBagurgle(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="King Bagurgle",
                         id="BGS_030",
                         gold_id="TB_BaconUps_100",
                         rank=5,
                         base_attack=6,
                         base_health=3,
                         legendary=True,
                         base_deathrattle=KingBagurgleDeathrattle(),
                         types=[MinionType.Murloc],
                         **kwargs)


class LightfangEnforcer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Lightfang Enforcer",
                         id="BGS_009",
                         gold_id="TB_BaconUps_082",
                         rank=5,
                         base_attack=2,
                         base_health=2,
                         **kwargs)


class MalGanis(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Mal'Ganis",
                         id="GVG_021",
                         gold_id="TB_BaconUps_060",
                         rank=5,
                         base_attack=9,
                         base_health=7,
                         legendary=True,
                         types=[MinionType.Demon],
                         **kwargs)

    def adjust_demon_power(self, other_minion: Minion, add_power: bool):
        stats = 4 if self.golden else 2
        if MinionType.Demon in other_minion.types:
            if add_power:
                other_minion.add_stats(stats, stats)
            else:
                other_minion.remove_stats(stats, stats)

    def on_summon(self, other_minion: Minion):
        self.adjust_demon_power(other_minion, True)

    def on_friendly_summon(self, other_minion: Minion):
        self.adjust_demon_power(other_minion, True)

    def on_removal(self, other_minion: Minion):
        self.adjust_demon_power(other_minion, False)


class MamaBear(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Mama Bear",
                         id="BGS_021",
                         gold_id="TB_BaconUps_090",
                         rank=5,
                         base_attack=5,
                         base_health=5,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion):
        if MinionType.Beast in other_minion.types:
            stats = 10 if self.golden else 5
            other_minion.add_stats(stats, stats)


class Murozond(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murozond",
                         id="BGS_043",
                         gold_id="TB_BaconUps_110",
                         rank=5,
                         base_attack=5,
                         base_health=5,
                         legendary=True,
                         types=[MinionType.Dragon],
                         **kwargs)


class MythraxtheUnraveler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Mythrax the Unraveler",
                         id="BGS_202",
                         gold_id="TB_BaconUps_258",
                         rank=5,
                         base_attack=4,
                         base_health=4,
                         legendary=True,
                         **kwargs)


class NatPagleExtremeAngler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nat Pagle, Extreme Angler",
                         id="BGS_046",
                         gold_id="TB_BaconUps_132",
                         rank=5,
                         base_attack=8,
                         base_health=5,
                         legendary=True,
                         types=[MinionType.Pirate],
                         **kwargs)


class NomiKitchenNightmare(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nomi, Kitchen Nightmare",
                         id="BGS_104",
                         gold_id="TB_BaconUps_201",
                         rank=5,
                         base_attack=4,
                         base_health=4,
                         legendary=True,
                         **kwargs)


class RazorgoretheUntamed(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Razorgore, the Untamed",
                         id="BGS_036",
                         gold_id="TB_BaconUps_106",
                         rank=5,
                         base_attack=4,
                         base_health=6,
                         legendary=True,
                         types=[MinionType.Dragon],
                         **kwargs)


class SeabreakerGoliath(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Seabreaker Goliath",
                         id="BGS_080",
                         gold_id="TB_BaconUps_142",
                         rank=5,
                         base_attack=6,
                         base_health=7,
                         base_windfury=True,
                         types=[MinionType.Pirate],
                         **kwargs)

    def on_overkill(self, friendly_board: PlayerBoard, defending_minion: Minion, enemy_board: PlayerBoard):
        stats = 4 if self.golden else 2
        for minion in friendly_board.minions:
            if MinionType.Pirate in minion.types and minion is not self:
                minion.add_stats(stats, stats)


class SneedsOldShredder(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Sneed's Old Shredder",
                         id="BGS_006",
                         gold_id="TB_BaconUps_080",
                         rank=5,
                         base_attack=5,
                         base_health=7,
                         types=[MinionType.Mech],
                         base_deathrattle=SneedsOldShredderDeathrattle(),
                         legendary=True,
                         **kwargs)


class StrongshellScavenger(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Strongshell Scavenger",
                         id="ICC_807",
                         gold_id="TB_BaconUps_072",
                         rank=5,
                         base_attack=2,
                         base_health=3,
                         **kwargs)


class TavernTempest(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Tavern Tempest",
                         id="BGS_123",
                         gold_id="TB_BaconUps_162",
                         rank=5,
                         base_attack=4,
                         base_health=4,
                         types=[MinionType.Elemental],
                         **kwargs)


class Voidlord(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Voidlord",
                         id="LOOT_368",
                         gold_id="TB_BaconUps_059",
                         rank=5,
                         base_attack=3,
                         base_health=1,
                         base_deathrattle=VoidlordDeathrattle(),
                         types=[MinionType.Demon],
                         **kwargs)
