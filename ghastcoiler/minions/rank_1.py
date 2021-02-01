import logging

from minions.base import Minion
from minions.types import MinionType

from deathrattles.rank_1 import FiendishServantDeathrattle, ScallywagDeathrattle


class Alleycat(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Alleycat",
                         rank=1,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Beast],
                         **kwargs)


class RabidSaurolisk(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rabid Saurolisk",
                         rank=1,
                         base_attack=3,
                         base_defense=1,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_friendly_summon(self, other_minion):
        if other_minion.deathrattles:
            increase_amount = 2 if self.golden else 1
            self.attack += increase_amount
            self.defense += increase_amount


class DragonspawnLieutenant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Dragonspawn Lieutenant",
                         rank=1,
                         base_attack=2,
                         base_defense=3,
                         types=[MinionType.Dragon],
                         base_taunt=True,
                         **kwargs)


class FiendishServant(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Fiendish Servant",
                         rank=1,
                         base_attack=2,
                         base_defense=1,
                         types=[MinionType.Demon],
                         base_deathrattle=FiendishServantDeathrattle(),
                         **kwargs)


# class Mecharoo(Minion):
#     def __init__(self, **kwargs):
#         super().__init__(name="Mecharoo",
#                          rank=1,
#                          base_attack=1,
#                          base_defense=1,
#                          types=[MinionType.Mech],
#                          base_deathrattle=MecharooDeathrattle())


class MicroMachine(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Micro Machine",
                         rank=1,
                         base_attack=1,
                         base_defense=2,
                         types=[MinionType.Mech],
                         **kwargs)


class MurlocTidecaller(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Tidecaller",
                         rank=1,
                         base_attack=1,
                         base_defense=2,
                         types=[MinionType.Murloc],
                         **kwargs)


class MurlocTidehunter(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Tidehunter",
                         rank=1,
                         base_attack=2,
                         base_defense=1,
                         types=[MinionType.Murloc],
                         **kwargs)


class RockpoolHunter(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rockpool Hunter",
                         rank=1,
                         base_attack=2,
                         base_defense=3,
                         types=[MinionType.Murloc],
                         **kwargs)


class RedWhelp(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Red Whelp",
                         rank=1,
                         base_attack=1,
                         base_defense=2,
                         types=[MinionType.Dragon],
                         **kwargs)

    def at_beginning_game(self, game_instance, player_starts, own_board, opposing_board):
        number_dragons = own_board.count_minion_type(MinionType.Dragon)
        for _ in range(1 + self.golden):
            minion = opposing_board.random_minion()
            game_instance.deal_damage(minion, opposing_board, number_dragons, False)
            logging.debug(f"{self.minion_string()} deals {number_dragons} damage to {minion.minion_string()}")
        if player_starts:
            game_instance.check_deaths(own_board, opposing_board)
        else:
            game_instance.check_deaths(opposing_board, own_board)


# class RighteousProtector(Minion):
#     def __init__(self, **kwargs):
#         super().__init__(name="Righteous Protector",
#                          rank=1,
#                          base_attack=1,
#                          base_defense=1,
#                          base_taunt=True,
#                          base_divine_shield=True)


class VulgarHomunculus(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Vulgar Homunculus",
                         rank=1,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Demon],
                         base_taunt=True,
                         **kwargs)


class WrathWeaver(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Wrath Weaver",
                         rank=1,
                         base_attack=1,
                         base_defense=3,
                         **kwargs)


class MicroMummy(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Micro Mummy",
                         rank=1,
                         base_attack=1,
                         base_defense=2,
                         types=[MinionType.Mech],
                         base_reborn=True,
                         **kwargs)


class ScavengingHyena(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Scavenging Hyena",
                         rank=1,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_friendly_removal(self, other_minion):
        if MinionType.Beast in other_minion.types:
            multiplier = 2 if self.golden else 1
            self.attack += (2 * multiplier)
            self.defense += multiplier


class AcolyteOfCThun(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Acolyte of C'Thun",
                         rank=1,
                         base_attack=2,
                         base_defense=2,
                         base_taunt=True,
                         base_reborn=True,
                         **kwargs)


class DeckSwabbie(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Deck Swabbie",
                         rank=1,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Pirate],
                         **kwargs)


class RefreshingAnomaly(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Refreshing Anomaly",
                         rank=1,
                         base_attack=1,
                         base_defense=3,
                         types=[MinionType.Elemental],
                         **kwargs)


class Scallywag(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Scallywag",
                         rank=1,
                         base_attack=2,
                         base_defense=1,
                         types=[MinionType.Pirate],
                         base_deathrattle=ScallywagDeathrattle(),
                         **kwargs)


class Sellemental(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Sellemental",
                         rank=1,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Elemental],
                         **kwargs)
