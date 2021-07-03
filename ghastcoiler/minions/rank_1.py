import logging

from minions.base import Minion
from minions.types import MinionType

from deathrattles.rank_1 import FiendishServantDeathrattle, ScallywagDeathrattle


class AcolyteOfCThun(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Acolyte of C'Thun",
                         id="BGS_106",
                         gold_id="TB_BaconUps_255",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         base_taunt=True,
                         base_reborn=True,
                         **kwargs)


class Alleycat(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Alleycat",
                         id="CFM_315",
                         gold_id="TB_BaconUps_093",
                         rank=1,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Beast],
                         **kwargs)


class DeckSwabbie(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Deck Swabbie",
                         id="BGS_055",
                         gold_id="TB_BaconUps_126",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Pirate],
                         **kwargs)


class DragonspawnLieutenant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Dragonspawn Lieutenant",
                         id="BGS_039",
                         gold_id="TB_BaconUps_146",
                         rank=1,
                         base_attack=2,
                         base_health=3,
                         types=[MinionType.Dragon],
                         base_taunt=True,
                         **kwargs)


class FiendishServant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Fiendish Servant",
                         id="YOD_026",
                         gold_id="TB_BaconUps_112",
                         rank=1,
                         base_attack=2,
                         base_health=1,
                         types=[MinionType.Demon],
                         base_deathrattle=FiendishServantDeathrattle(),
                         **kwargs)


class MicroMachine(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Micro Machine",
                         id="BGS_027",
                         gold_id="TB_BaconUps_094",
                         rank=1,
                         base_attack=1,
                         base_health=2,
                         types=[MinionType.Mech],
                         mana_cost=2,
                         **kwargs)


class MicroMummy(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Micro Mummy",
                         id="ULD_217",
                         gold_id="TB_BaconUps_250",
                         rank=1,
                         base_attack=1,
                         base_health=2,
                         types=[MinionType.Mech],
                         base_reborn=True,
                         mana_cost=2,
                         **kwargs)


class MurlocTidecaller(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Tidecaller",
                         id="EX1_509",
                         gold_id="TB_BaconUps_011",
                         rank=1,
                         base_attack=1,
                         base_health=2,
                         types=[MinionType.Murloc],
                         **kwargs)


class MurlocTidehunter(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Tidehunter",
                         id="EX1_506",
                         gold_id="TB_BaconUps_003",
                         rank=1,
                         base_attack=2,
                         base_health=1,
                         types=[MinionType.Murloc],
                         mana_cost=2,
                         **kwargs)


class RazorfenGeomancer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Razorfen Geomancer",
                         id="BG20_100",
                         gold_id="BG20_100_G",
                         rank=1,
                         base_attack=3,
                         base_health=1,
                         types=[MinionType.Quilboar],
                         **kwargs)


class RedWhelp(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Red Whelp",
                         id="BGS_019",
                         gold_id="TB_BaconUps_102",
                         rank=1,
                         base_attack=1,
                         base_health=2,
                         types=[MinionType.Dragon],
                         **kwargs)

    def at_beginning_game(self, game_instance, player_starts, own_board, opposing_board):
        # TODO: Test this
        number_dragons = own_board.count_minion_type(MinionType.Dragon)
        for _ in range(1 + self.golden):
            minion = opposing_board.random_minion()
            if minion:
                minion.receive_damage(number_dragons, False, opposing_board)
                logging.debug(f"{self.minion_string()} deals {number_dragons} damage to {minion.minion_string()}")
        if player_starts:
            game_instance.check_deaths(own_board, opposing_board)
        else:
            game_instance.check_deaths(opposing_board, own_board)


class RefreshingAnomaly(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Refreshing Anomaly",
                         id="BGS_116",
                         gold_id="TB_BaconUps_167",
                         rank=1,
                         base_attack=1,
                         base_health=4,
                         types=[MinionType.Elemental],
                         **kwargs)


class RockpoolHunter(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rockpool Hunter",
                         id="UNG_073",
                         gold_id="TB_BaconUps_061",
                         rank=1,
                         base_attack=2,
                         base_health=3,
                         types=[MinionType.Murloc],
                         mana_cost=2,
                         **kwargs)


class Scallywag(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Scallywag",
                         id="BGS_061",
                         gold_id="TB_BaconUps_141",
                         rank=1,
                         base_attack=2,
                         base_health=1,
                         types=[MinionType.Pirate],
                         base_deathrattle=ScallywagDeathrattle(),
                         **kwargs)


class ScavengingHyena(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Scavenging Hyena",
                         id="EX1_531",
                         gold_id="TB_BaconUps_043",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Beast],
                         mana_cost=2,
                         **kwargs)

    def on_friendly_removal(self, other_minion):
        if MinionType.Beast in other_minion.types:
            multiplier = 2 if self.golden else 1
            self.attack += (2 * multiplier)
            self.health += multiplier


class Sellemental(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Sellemental",
                         id="BGS_115",
                         gold_id="TB_BaconUps_156",
                         rank=1,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Elemental],
                         **kwargs)


class SunBaconRelaxer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Sun-Bacon Relaxer",
                         id="BG20_301",
                         gold_id="BG20_301_G",
                         rank=1,
                         base_attack=1,
                         base_health=2,
                         types=[MinionType.Quilboar],
                         **kwargs)


class VulgarHomunculus(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Vulgar Homunculus",
                         id="LOOT_013",
                         gold_id="TB_BaconUps_148",
                         rank=1,
                         base_attack=2,
                         base_health=4,
                         types=[MinionType.Demon],
                         base_taunt=True,
                         mana_cost=2,
                         **kwargs)


class WrathWeaver(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Wrath Weaver",
                         id="BGS_004",
                         gold_id="TB_BaconUps_079",
                         rank=1,
                         base_attack=1,
                         base_health=3,
                         **kwargs)
