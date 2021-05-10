import logging

from game.player_board import PlayerBoard

from minions.base import Minion
from minions.types import MinionType

from deathrattles.rank_5 import KingBagurgleDeathrattle, SneedsOldShredderDeathrattle, VoidlordDeathrattle

class AgamaggantheGreatBoar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Agamaggan, the Great Boar",
                         id="BG20_205",
                         gold_id="BG20_205_G",
                         rank=5,
                         base_attack=6,
                         base_defense=6,
                         types=[MinionType.Quilboar],
                         **kwargs)


class AggemThorncurse(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Aggem Thorncurse",
                         id="BG20_302",
                         gold_id="BG20_302_G",
                         rank=5,
                         base_attack=3,
                         base_defense=6,
                         types=[MinionType.Quilboar],
                         **kwargs)


class AnnihilanBattlemaster(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Annihilan Battlemaster",
                         id="BGS_010",
                         gold_id="TB_BaconUps_083",
                         rank=5,
                         base_attack=3,
                         base_defense=1,
                         types=[MinionType.Demon],
                         **kwargs)


class BaronRivendare(Minion):
    #TODO: Implement
    def __init__(self, **kwargs):
        super().__init__(name="Baron Rivendare",
                         id="FP1_031",
                         gold_id="TB_BaconUps_055",
                         rank=5,
                         base_attack=1,
                         base_defense=7,
                         **kwargs)


class BrannBronzebeard(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Brann Bronzebeard",
                         id="LOE_077",
                         gold_id="TB_BaconUps_045",
                         rank=5,
                         base_attack=2,
                         base_defense=4,
                         **kwargs)


class BristlebackKnight(Minion):
    #TODO: Implement frenzy trigger
    def __init__(self, **kwargs):
        super().__init__(name="Bristleback Knight",
                         id="BG20_204",
                         gold_id="BG20_204_G",
                         rank=5,
                         base_attack=4,
                         base_defense=8,
                         base_divine_shield=True,
                         base_windfury=True,
                         types=[MinionType.Quilboar],
                         **kwargs)
        self.windfury = False if self.golden else True
        self.mega_windfury = True if self.golden else False


class CapnHoggarr(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Cap'n Hoggarr",
                         id="BGS_072",
                         gold_id="TB_BaconUps_133",
                         rank=5,
                         base_attack=6,
                         base_defense=6,
                         types=[MinionType.Pirate],
                         **kwargs)


class DeadlySpore(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Deadly Spore",
                         id="BGS_131",
                         gold_id="TB_BaconUps_251",
                         rank=5,
                         base_attack=1,
                         base_defense=1,
                         base_poisonous=True,
                         **kwargs)


class FacelessTaverngoer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Faceless Taverngoer",
                         id="BGS_113",
                         gold_id="TB_BaconUps_305",
                         rank=5,
                         base_attack=4,
                         base_defense=4,
                         **kwargs)


class IronhideDirehorn(Minion):
    #TODO: Overkill triggers
    def __init__(self, **kwargs):
        super().__init__(name="Ironhide Direhorn",
                         id="TRL_232",
                         gold_id="TB_BaconUps_051",
                         rank=5,
                         base_attack=7,
                         base_defense=7,
                         types=[MinionType.Beast],
                         **kwargs)


class KingBagurgle(Minion):
    #TODO: Test Deathrattle
    def __init__(self, **kwargs):
        super().__init__(name="King Bagurgle",
                         id="BGS_030",
                         gold_id="TB_BaconUps_100",
                         rank=5,
                         base_attack=6,
                         base_defense=3,
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
                         base_defense=2,
                         **kwargs)


class MalGanis(Minion):
    #TODO: Aura
    def __init__(self, **kwargs):
        super().__init__(name="Mal'Ganis",
                         id="BGS_010",
                         gold_id="TB_BaconUps_083",
                         rank=5,
                         base_attack=9,
                         base_defense=7,
                         types=[MinionType.Demon],
                         **kwargs)


class MamaBear(Minion):
    #TODO: Summon triggers
    def __init__(self, **kwargs):
        super().__init__(name="Mama Bear",
                         id="BGS_021",
                         gold_id="TB_BaconUps_090",
                         rank=5,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Beast],
                         **kwargs)


class Murozond(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murozond",
                         id="BGS_043",
                         gold_id="TB_BaconUps_110",
                         rank=5,
                         base_attack=5,
                         base_defense=5,
                         types=[MinionType.Dragon],
                         **kwargs)


class MythraxtheUnraveler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Mythrax the Unraveler",
                         id="BGS_202",
                         gold_id="TB_BaconUps_258",
                         rank=5,
                         base_attack=4,
                         base_defense=4,
                         **kwargs)


class NatPagleExtremeAngler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nat Pagle, Extreme Angler",
                         id="BGS_046",
                         gold_id="TB_BaconUps_132",
                         rank=5,
                         base_attack=8,
                         base_defense=5,
                         types=[MinionType.Pirate],
                         **kwargs)


class NomiKitchenNightmare(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nomi, Kitchen Nightmare",
                         id="BGS_104",
                         gold_id="TB_BaconUps_201",
                         rank=5,
                         base_attack=4,
                         base_defense=4,
                         **kwargs)


class RazorgoretheUntamed(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Razorgore, the Untamed",
                         id="BGS_036",
                         gold_id="TB_BaconUps_106",
                         rank=5,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Dragon],
                         **kwargs)


class SeabreakerGoliath(Minion):
    #TODO: Overkill trigger
    def __init__(self, **kwargs):
        super().__init__(name="Seabreaker Goliath",
                         id="BGS_080",
                         gold_id="TB_BaconUps_142",
                         rank=5,
                         base_attack=6,
                         base_defense=7,
                         base_windfury=True,
                         types=[MinionType.Pirate],
                         **kwargs)


class SneedsOldShredder(Minion):
    #TODO: Test Deathrattle
    def __init__(self, **kwargs):
        super().__init__(name="Sneed's Old Shredder",
                         id="BGS_006",
                         gold_id="TB_BaconUps_080",
                         rank=5,
                         base_attack=5,
                         base_defense=7,
                         types=[MinionType.Mech],
                         base_deathrattle=[SneedsOldShredderDeathrattle()],
                         **kwargs)


class StrongshellScavenger(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Strongshell Scavenger",
                         id="ICC_807",
                         gold_id="TB_BaconUps_072",
                         rank=5,
                         base_attack=2,
                         base_defense=3,
                         **kwargs)


class TavernTempest(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Tavern Tempest",
                         id="BGS_123",
                         gold_id="TB_BaconUps_162",
                         rank=5,
                         base_attack=4,
                         base_defense=4,
                         types=[MinionType.Elemental],
                         **kwargs)


class Voidlord(Minion):
    #TODO: Test Deathrattle
    def __init__(self, **kwargs):
        super().__init__(name="Voidlord",
                         id="LOOT_368",
                         gold_id="TB_BaconUps_059",
                         rank=5,
                         base_attack=3,
                         base_defense=1,
                         base_deathrattle=[VoidlordDeathrattle()],
                         types=[MinionType.Demon],
                         **kwargs)
                                                      