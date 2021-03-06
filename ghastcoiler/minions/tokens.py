import logging

from minions.base import Minion
from minions.types import MinionType

class Amalgam(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Amalgam",
                         id="TB_BaconShop_HP_033t",
                         gold_id="",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Murloc, 
                         MinionType.Dragon, 
                         MinionType.Demon, 
                         MinionType.Beast, 
                         MinionType.Mech, 
                         MinionType.Pirate, 
                         MinionType.Elemental,
                         MinionType.Quilboar],
                         **kwargs)


class BigBadWolf(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Big Bad Wolf",
                         id="KAR_005a",
                         gold_id="TB_BaconUps_004t",
                         rank=1,
                         base_attack=3,
                         base_health=2,
                         types=[MinionType.Beast],
                         **kwargs)


class DamagedGolem(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Damaged Golem",
                         id="VAN_skele21",  # TODO: Double check this
                         gold_id="TB_BaconUps_006t",
                         rank=1,
                         base_attack=2,
                         base_health=1,
                         types=[MinionType.Mech],
                         **kwargs)


class FieryImp(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Fiery Imp",
                         id="DMF_533t",
                         gold_id="TB_BaconUps_309t",
                         rank=1,
                         base_attack=3,
                         base_health=2,
                         types=[MinionType.Demon],
                         **kwargs)


class FishofNZoth(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Fish of N'Zoth",
                         id="TB_BaconShop_HP_105t",
                         gold_id="TB_BaconUps_307",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_friendly_removal(self, other_minion: Minion):
        if len(other_minion.deathrattles) > 0:
            logging.debug(f"Fish of N'zoth gets deathrattles {other_minion.deathrattles} from {other_minion.minion_string()}")
            self.deathrattles += other_minion.deathrattles


class GuardBot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Guard Bot",
                         id="BOT_218t",
                         gold_id="TB_BaconUps_041t",
                         rank=1,
                         base_attack=2,
                         base_health=3,
                         base_taunt=True,
                         types=[MinionType.Mech],
                         **kwargs)


class Hyena(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Hyena",
                         id="ULD_154t",
                         gold_id="TB_BaconUps_049t",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Beast],
                         **kwargs)


class Imp(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Imp",
                         id="BRM_006t", # TODO: Double check
                         gold_id="TB_BaconUps_030t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Demon],
                         **kwargs)


class IronhideRunt(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Ironhide Runt",
                         id="BRM_006t",
                         gold_id="TB_BaconUps_030t",
                         rank=1,
                         base_attack=5,
                         base_health=5,
                         types=[MinionType.Beast],
                         **kwargs)


class Microbot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Microbot",
                         id="BOT_312t",
                         gold_id="TB_BaconUps_032t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Mech],
                         **kwargs)

class MurlocScout(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Scout",
                         id="EX1_506a",
                         gold_id="TB_BaconUps_003t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Murloc],
                         **kwargs)

class Plant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Plant",
                         id="UNG_999t2t1",
                         gold_id="", # No gold version
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         **kwargs)

class Rat(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rat",
                         id="CFM_316t",
                         gold_id="TB_BaconUps_027t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Beast],
                         **kwargs)


class Robosaur(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Robosaur",
                         id="BOT_537t",
                         gold_id="TB_BaconUps_039t",
                         rank=1,
                         base_attack=8,
                         base_health=8,
                         types=[MinionType.Mech],
                         **kwargs)


class SkyPirate(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Sky Pirate",
                         id="BGS_061t",
                         gold_id="TB_BaconUps_141t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Pirate],
                         **kwargs)


class Spider(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Spider",
                         id="OG_216a",
                         gold_id="TB_BaconUps_026t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Beast],
                         **kwargs)

class Tabbycat(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Tabbycat",
                         id="CFM_315t",
                         gold_id="TB_BaconUps_093t",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Beast],
                         **kwargs)


class Voidwalker(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Voidwalker",
                         id="CS2_065",
                         gold_id="TB_BaconUps_059t",
                         rank=1,
                         base_attack=1,
                         base_health=3,
                         base_taunt=True,
                         types=[MinionType.Demon],
                         **kwargs)


class WaterDroplet(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Water Droplet",
                         id="BGS_115t",
                         gold_id="",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Elemental],
                         **kwargs)
