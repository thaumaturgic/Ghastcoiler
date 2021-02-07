import logging

from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType

from deathrattles.rank_2 import HarvestGolemDeathrattle, ImprisonerDeathrattle, KaboomBotDeathrattle, \
    KindlyGrandmotherDeathrattle, SpawnofNZothDeathrattle, UnstableGhoulDeathrattle, \
    SelflessHeroDeathrattle


class GlyphGuardian(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Glyph Guardian",
                         rank=2,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Dragon],
                         **kwargs)

    def on_attack_before(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        if self.golden:
            self.attack *= 3
        else:
            self.attack *= 2


class HarvestGolem(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Harvest Golem",
                         rank=2,
                         base_attack=2,
                         base_defense=3,
                         types=[MinionType.Mech],
                         base_deathrattle=HarvestGolemDeathrattle(),
                         **kwargs)


class Imprisoner(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Imprisoner",
                         rank=2,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Demon],
                         base_taunt=True,
                         base_deathrattle=ImprisonerDeathrattle(),
                         **kwargs)


class KaboomBot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kaboom Bot",
                         rank=2,
                         base_attack=2,
                         base_defense=2,
                         types=[MinionType.Mech],
                         base_deathrattle=KaboomBotDeathrattle(),
                         **kwargs)


class KindlyGrandmother(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kindly Grandmother",
                         rank=2,
                         base_attack=1,
                         base_defense=1,
                         types=[MinionType.Beast],
                         base_deathrattle=KindlyGrandmotherDeathrattle(),
                         **kwargs)


class MetaltoothLeaper(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Metaltooth Leaper",
                         rank=2,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Mech],
                         **kwargs)


class MurlocWarleader(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Warleader",
                         rank=2,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Murloc],
                         **kwargs)

    # apply or remove the warleader attack bonus to the other minion
    def adjust_murlock_power(self, other_minion: Minion, add_power: bool):
        buffAmount = 4 if self.golden else 2
        if MinionType.Murloc in other_minion.types:
            if add_power:
                other_minion.add_stats(buffAmount, 0)
            else:
                other_minion.remove_stats(buffAmount, 0)

    def on_summon(self, other_minion: Minion):
        self.adjust_murlock_power(other_minion, True)

    def on_friendly_summon(self, other_minion: Minion):
        self.adjust_murlock_power(other_minion, True)

    def on_removal(self, other_minion: Minion):
        self.adjust_murlock_power(other_minion, False)


class NathrezimOverseer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nathrezim Overseer",
                         rank=2,
                         base_attack=2,
                         base_defense=3,
                         types=[MinionType.Demon],
                         **kwargs)


# I think there are two ways to implement murkeye
# 1) Every time a minion is added or removed from any board, check if its a murloc and adjust power accordingly
# 2) Any time murkeye attacks or is attacked (ie the only time power currently matters), check the state of the board to calculate the correct power
# Currently method #2 is implemented
class OldMurkEye(Minion):
    def __init__(self, **kwargs):
        self.bonus_attack = 0
        super().__init__(name="Old Murk Eye",
                         rank=2,
                         base_attack=2,
                         base_defense=4,
                         types=[MinionType.Murloc],
                         **kwargs)

    def update_bonus_attack(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        total_number_other_murlocs = own_board.count_minion_type(MinionType.Murloc) + opposing_board.count_minion_type(MinionType.Murloc) - 1  # Don't count itself
        bonus = total_number_other_murlocs * 2 if self.golden else total_number_other_murlocs

        self.attack -= self.bonus_attack
        self.bonus_attack = bonus
        self.attack += self.bonus_attack

    def on_attack_before(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.update_bonus_attack(own_board, opposing_board)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.update_bonus_attack(own_board, opposing_board)

# class PogoHopper(Minion):
#     def __init__(self, **kwargs):
#         super().__init__(name="Pogo-Hopper",
#                          rank=2,
#                          base_attack=1,
#                          base_defense=1,
#                          types=[MinionType.Mech],
#                          **kwargs)


class SpawnofNZoth(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Spawn of N'Zoth",
                         rank=2,
                         base_attack=2,
                         base_defense=2,
                         base_deathrattle=SpawnofNZothDeathrattle(),
                         **kwargs)


class StewardofTime(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Steward of Time",
                         rank=2,
                         base_attack=3,
                         base_defense=4,
                         types=[MinionType.Dragon],
                         **kwargs)


class UnstableGhoul(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Unstable Ghoul",
                         rank=2,
                         base_attack=1,
                         base_defense=3,
                         base_taunt=True,
                         base_deathrattle=UnstableGhoulDeathrattle(),
                         **kwargs)


class WaxriderTogwaggle(Minion):
    """Whenever a friendly Dragon kills an enemy, gain +2/+2."""
    def __init__(self, **kwargs):
        super().__init__(name="Waxrider Togwaggle",
                         rank=2,
                         base_attack=1,
                         base_defense=2,
                         **kwargs)

    def on_friendly_kill(self, killer_minion: Minion):
        if MinionType.Dragon in killer_minion.types:
            added_bonus = 4 if self.golden else 2
            self.add_stats(added_bonus, added_bonus)


class SelflessHero(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Selfless Hero",
                         rank=2,
                         base_attack=2,
                         base_defense=1,
                         base_deathrattle=SelflessHeroDeathrattle(),
                         **kwargs)


class SouthseaCaptain(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Southsea Captain",
                         rank=2,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Pirate],
                         **kwargs)

    def adjust_pirate_stats(self, other_minion: Minion, add_stats: bool):
        buffAmount = 2 if self.golden else 1
        if MinionType.Pirate in other_minion.types:
            if add_stats:
                other_minion.add_stats(buffAmount, buffAmount)
            else:
                other_minion.remove_stats(buffAmount, buffAmount)
                if other_minion.defense <= 0:
                    other_minion.defense = 1  # Losing pirate buffs cannot kill a minion

    def on_summon(self, other_minion: Minion):
        self.adjust_pirate_stats(other_minion, True)

    def on_friendly_summon(self, other_minion: Minion):
        self.adjust_pirate_stats(other_minion, True)

    def on_removal(self, other_minion: Minion):
        self.adjust_pirate_stats(other_minion, False)


class FreedealingGambler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Freedealing Gambler",
                         rank=2,
                         base_attack=3,
                         base_defense=3,
                         types=[MinionType.Pirate],
                         **kwargs)


class MenagerieMug(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Menagerie Mug",
                         rank=2,
                         base_attack=2,
                         base_defense=2,
                         **kwargs)


class MoltenRock(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Molten Rock",
                         rank=2,
                         base_attack=2,
                         base_defense=3,
                         base_taunt=True,
                         types=[MinionType.Elemental],
                         **kwargs)


class PackLeader(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Pack Leader",
                         rank=2,
                         base_attack=2,
                         base_defense=3,
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion):
        if MinionType.Beast in other_minion.types:
            other_minion.attack += 4 if self.golden else 2


class PartyElemental(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Party Elemental",
                         rank=2,
                         base_attack=3,
                         base_defense=2,
                         types=[MinionType.Elemental],
                         **kwargs)


class TormentedRitualist(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Tormented Ritualist",
                         rank=2,
                         base_attack=2,
                         base_defense=3,
                         base_taunt=True,
                         **kwargs)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        buff_amount = 2 if self.golden else 1
        for minion in own_board.get_minions_neighbors(self):
            minion.add_stats(buff_amount, buff_amount)


class YoHoOgre(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Yo-Ho-Ogre",
                         rank=2,
                         base_attack=2,
                         base_defense=5,
                         base_taunt=True,
                         types=[MinionType.Pirate],
                         **kwargs)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.immediate_attack_pending = True
