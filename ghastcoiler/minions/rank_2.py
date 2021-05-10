import logging

from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType

from deathrattles.rank_2 import HarvestGolemDeathrattle, ImprisonerDeathrattle, KaboomBotDeathrattle, \
    KindlyGrandmotherDeathrattle, SpawnofNZothDeathrattle, UnstableGhoulDeathrattle, \
    SelflessHeroDeathrattle


class FreedealingGambler(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Freedealing Gambler",
                         id="BGS_049",
                         gold_id="TB_BaconUps_127",
                         rank=2,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Pirate],
                         **kwargs)


class GlyphGuardian(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Glyph Guardian",
                         id="BGS_045",
                         gold_id="TB_BaconUps_115",
                         rank=2,
                         base_attack=2,
                         base_health=4,
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
                         id="EX1_556",
                         gold_id="TB_BaconUps_006",
                         base_attack=2,
                         base_health=3,
                         types=[MinionType.Mech],
                         base_deathrattle=HarvestGolemDeathrattle(),
                         **kwargs)


class Imprisoner(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Imprisoner",
                         id="BGS_014",
                         gold_id="TB_BaconUps_113",
                         rank=2,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Demon],
                         base_taunt=True,
                         base_deathrattle=ImprisonerDeathrattle(),
                         **kwargs)


class KaboomBot(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kaboom Bot",
                         id="BOT_606",
                         gold_id="TB_BaconUps_028",
                         rank=2,
                         base_attack=2,
                         base_health=2,
                         types=[MinionType.Mech],
                         base_deathrattle=KaboomBotDeathrattle(),
                         **kwargs)


class KindlyGrandmother(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Kindly Grandmother",
                         id="KAR_005",
                         gold_id="TB_BaconUps_004",
                         rank=2,
                         base_attack=1,
                         base_health=1,
                         types=[MinionType.Beast],
                         base_deathrattle=KindlyGrandmotherDeathrattle(),
                         mana_cost=2,
                         **kwargs)


class MenagerieMug(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Menagerie Mug",
                         id="BGS_082",
                         gold_id="TB_BaconUps_144",
                         rank=2,
                         base_attack=2,
                         base_health=2,
                         **kwargs)


class MetaltoothLeaper(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Metaltooth Leaper",
                         id="GVG_048",
                         gold_id="TB_BaconUps_066",
                         rank=2,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Mech],
                         **kwargs)


class MoltenRock(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Molten Rock",
                         id="BGS_127",
                         gold_id="TB_Baconups_202",
                         rank=2,
                         base_attack=2,
                         base_health=3,
                         base_taunt=True,
                         types=[MinionType.Elemental],
                         **kwargs)


class MurlocWarleader(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Murloc Warleader",
                         id="EX1_507",
                         gold_id="TB_BaconUps_008",
                         rank=2,
                         base_attack=3,
                         base_health=3,
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

    def on_summon(self, other_minion: Minion, own_board: PlayerBoard):
        self.adjust_murlock_power(other_minion, True)

    def on_friendly_summon(self, other_minion: Minion):
        self.adjust_murlock_power(other_minion, True)

    def on_removal(self, other_minion: Minion, own_board: PlayerBoard):
        self.adjust_murlock_power(other_minion, False)


class NathrezimOverseer(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Nathrezim Overseer",
                         id="BGS_001",
                         gold_id="TB_BaconUps_062",
                         rank=2,
                         base_attack=2,
                         base_health=3,
                         types=[MinionType.Demon],
                         **kwargs)


# I think there are two ways to implement murkeye
# 1) Every time a minion is added or removed from any board, check if its a murloc and adjust power accordingly
# 2) Any time murkeye attacks or is attacked (ie the only time power currently matters), check the state of the board to calculate the correct power
# Currently method #2 is implemented
class OldMurkEye(Minion):
    def __init__(self, **kwargs):
        self.bonus_attack = 0
        super().__init__(name="Old Murk-Eye",
                         id="EX1_062",
                         gold_id="TB_BaconUps_036",
                         rank=2,
                         base_attack=2,
                         base_health=4,
                         types=[MinionType.Murloc],
                         **kwargs)

    def update_bonus_attack(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        #TODO: Fix this with actual game import log. Minion comes with buffs already applied to attack
        total_number_other_murlocs = own_board.count_minion_type(MinionType.Murloc) + opposing_board.count_minion_type(MinionType.Murloc) - 1  # Don't count itself
        bonus = total_number_other_murlocs * 2 if self.golden else total_number_other_murlocs

        self.attack -= self.bonus_attack
        self.bonus_attack = bonus
        self.attack += self.bonus_attack

    def on_attack_before(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.update_bonus_attack(own_board, opposing_board)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.update_bonus_attack(own_board, opposing_board)


class PackLeader(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Pack Leader",
                         id="BGS_017",
                         gold_id="TB_BaconUps_086",
                         rank=2,
                         base_attack=3,
                         base_health=3,
                         **kwargs)

    def on_friendly_summon(self, other_minion: Minion):
        if MinionType.Beast in other_minion.types:
            other_minion.attack += 4 if self.golden else 2


class PartyElemental(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Party Elemental",
                         id="BGS_120",
                         gold_id="TB_BaconUps_160",
                         rank=2,
                         base_attack=3,
                         base_health=2,
                         types=[MinionType.Elemental],
                         **kwargs)


class ProphetoftheBoar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Prophet of the Boar",
                         id="BG20_203",
                         gold_id="BG20_203_G",
                         rank=2,
                         base_attack=3,
                         base_health=3,
                         **kwargs)


class RabidSaurolisk(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Rabid Saurolisk",
                         id="BGS_075",
                         gold_id="TB_BaconUps_125",
                         rank=2,
                         base_attack=3,
                         base_health=1,
                         types=[MinionType.Beast],
                         **kwargs)

    def on_friendly_summon(self, other_minion):
        if other_minion.deathrattles:
            increase_amount = 2 if self.golden else 1
            self.attack += increase_amount
            self.health += increase_amount


class Roadboar(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Roadboar",
                         id="BG20_101",
                         gold_id="BG20_101_G",
                         rank=2,
                         base_attack=2,
                         base_health=4,
                         types=[MinionType.Quilboar],
                         **kwargs)


class SelflessHero(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Selfless Hero",
                         id="OG_221",
                         gold_id="TB_BaconUps_014",
                         rank=2,
                         base_attack=2,
                         base_health=1,
                         base_deathrattle=SelflessHeroDeathrattle(),
                         **kwargs)


class SouthseaCaptain(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Southsea Captain",
                         id="NEW1_027",
                         gold_id="TB_BaconUps_136",
                         rank=2,
                         base_attack=3,
                         base_health=3,
                         types=[MinionType.Pirate],
                         **kwargs)

    def adjust_pirate_stats(self, other_minion: Minion, add_stats: bool):
        buffAmount = 2 if self.golden else 1
        if MinionType.Pirate in other_minion.types:
            if add_stats:
                other_minion.add_stats(buffAmount, buffAmount)
            else:
                other_minion.remove_stats(buffAmount, buffAmount)
                if other_minion.health <= 0:
                    other_minion.health = 1  # Losing pirate buffs cannot kill a minion

    def on_summon(self, other_minion: Minion, own_board: PlayerBoard):
        self.adjust_pirate_stats(other_minion, True)

    def on_friendly_summon(self, other_minion: Minion):
        self.adjust_pirate_stats(other_minion, True)

    def on_removal(self, other_minion: Minion, own_board: PlayerBoard):
        self.adjust_pirate_stats(other_minion, False)


class SpawnofNZoth(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Spawn of N'Zoth",
                         id="OG_256",
                         gold_id="TB_BaconUps_025",
                         rank=2,
                         base_attack=2,
                         base_health=2,
                         base_deathrattle=SpawnofNZothDeathrattle(),
                         **kwargs)


class StewardofTime(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Steward of Time",
                         id="BGS_037",
                         gold_id="TB_BaconUps_107",
                         rank=2,
                         base_attack=3,
                         base_health=4,
                         types=[MinionType.Dragon],
                         **kwargs)


class TormentedRitualist(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Tormented Ritualist",
                         id="BGS_201",
                         gold_id="TB_BaconUps_257",
                         rank=2,
                         base_attack=2,
                         base_health=3,
                         base_taunt=True,
                         **kwargs)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        buff_amount = 2 if self.golden else 1
        for minion in own_board.get_minions_neighbors(self):
            minion.add_stats(buff_amount, buff_amount)


class ToughTusk(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Tough Tusk",
                         id="BG20_102",
                         gold_id="BG20_102_G",
                         rank=2,
                         base_attack=4,
                         base_health=3,
                         types=[MinionType.Quilboar],
                         **kwargs)


class UnstableGhoul(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Unstable Ghoul",
                         id="FP1_024",
                         gold_id="TB_BaconUps_118",
                         rank=2,
                         base_attack=1,
                         base_health=3,
                         base_taunt=True,
                         base_deathrattle=UnstableGhoulDeathrattle(),
                         mana_cost=2,
                         **kwargs)


class WaxriderTogwaggle(Minion):
    """Whenever a friendly Dragon kills an enemy, gain +2/+2."""
    def __init__(self, **kwargs):
        super().__init__(name="Waxrider Togwaggle",
                         id="BGS_035",
                         gold_id="TB_BaconUps_105",
                         rank=2,
                         base_attack=1,
                         base_health=2,
                         **kwargs)

    def on_friendly_kill(self, killer_minion: Minion):
        if MinionType.Dragon in killer_minion.types:
            added_bonus = 4 if self.golden else 2
            self.add_stats(added_bonus, added_bonus)


class YoHoOgre(Minion):
    def __init__(self, **kwargs):
        super().__init__(name="Yo-Ho-Ogre",
                         id="BGS_060",
                         gold_id="TB_BaconUps_150",
                         rank=2,
                         base_attack=2,
                         base_health=5,
                         base_taunt=True,
                         types=[MinionType.Pirate],
                         **kwargs)

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        self.immediate_attack_pending = True
