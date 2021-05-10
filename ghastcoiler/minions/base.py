from __future__ import annotations

from typing import Optional, List, TYPE_CHECKING

from deathrattles.base import Deathrattle
from minions.types import MinionType

if TYPE_CHECKING:
    from game.player_board import PlayerBoard
    from game.game_instance import GameInstance


class Minion:
    def __init__(self,
                 name: str,
                 id: str,
                 gold_id: str,
                 rank: int,
                 base_attack: int,
                 base_defense: int,
                 attack: Optional[int] = None,
                 defense: Optional[int] = None,
                 dead: bool = False,
                 types: Optional[List[MinionType]] = None,
                 base_poisonous: bool = False,
                 poisonous: bool = False,
                 base_divine_shield: bool = False,
                 divine_shield: bool = False,
                 base_taunt: bool = False,
                 taunt: bool = False,
                 base_cleave: bool = False,
                 cleave: bool = False,
                 base_reborn: bool = False,
                 reborn: bool = False,
                 base_windfury: bool = False,
                 windfury: bool = False,
                 base_mega_windfury: bool = False,
                 mega_windfury: bool = False,
                 golden: bool = False,
                 base_deathrattle: Optional[Deathrattle] = None,
                 deathrattles: Optional[Deathrattle] = None,
                 position: Optional[int] = None,
                 player_id: Optional[int] = None,
                 mana_cost: Optional[int] = None,
                 attacked: bool = False,
                 immediate_attack_pending: bool = False,
                 token: bool = False,
                 reborn_triggered: bool = False):
        """Base minion class of which all normal minions and tokens should inherit from, and they can override certain triggers to implement custom behaviour.
        Important to note is that all the "base_*" arguments should be used in implementing the normal minions and that the non-base versions should be used
        for specific instances of the normal minions, so for the simulations itself in which case they can be different than their base type.

        Arguments:
            name {str} -- Name of the minion
            rank {int} -- Rank of the minion
            base_attack {int} -- Base attack of the non-golden version
            base_defense {int} -- Base defense of the non-golden version

        Keyword Arguments:
            attack {Optional[int]} -- Optional overwritten attack (default: {None})
            defense {Optional[int]} -- Optional overwritten defense (default: {None})
            dead {bool} -- Has the minion been killed (default: {False})
            types {Optional[List[MinionType]]} -- Optional list of MinionTypes (default: {None})
            base_poisonous {bool} -- Standard poisonous (default: {False})
            poisonous {bool} -- Poisonous (default: {False})
            base_divine_shield {bool} -- Standard divine shield (default: {False})
            divine_shield {bool} -- Divine shield (default: {False})
            base_taunt {bool} -- Standard taunt (default: {False})
            taunt {bool} -- Taunt (default: {False})
            base_cleave {bool} -- Standard cleave (default: {False})
            cleave {bool} -- Cleave (default: {False})
            base_reborn {bool} -- Standard reborn (default: {False})
            reborn {bool} -- Reborn (default: {False})
            base_windfury {bool} -- Standard windfury (default: {False})
            windfury {bool} -- Windfury (default: {False})
            base_mega_windfury {bool} -- Standard mega windfury (default: {False})
            mega_windfury {bool} -- Mega Windfury (default: {False})
            base_deathrattle {Optional[Deathrattle]} -- Standard deathrattle (default: {None})
            deathrattles {Optional[List[Deathrattle]]} -- Additional deathrattles (default: {None})
            golden {bool} -- Golden version (default: {False})
            position {Optional[int]} -- Position on the player board (default: {None})
            player_id {Optional[int]} -- ID of player minion belongs to (default: {None})
            attacked {bool} -- Has this minion been passed in the attack order this round (i.e. has it or the minion who spawned it attacked already) (default: {False})
            immediate_attack_pending {bool} -- When bonus attacks are checked, should this minion attack (default: {False})
            token {bool} -- Is this a token spawned by another minion (default: {False})
            reborn_triggered {bool} -- If this minion has reborn, has it been triggered yet (default: {False})
        """
        self.name = name
        self.rank = rank
        self.id = id
        self.gold_id = gold_id
        self.base_attack = base_attack * 2 if golden else base_attack
        self.base_defense = base_defense * 2 if golden else base_defense
        self.attack = attack if attack else self.base_attack
        self.defense = defense if defense else self.base_defense
        self.dead = dead
        self.types = types if types else []
        self.base_divine_shield = base_divine_shield
        self.divine_shield = divine_shield if divine_shield else base_divine_shield
        self.base_taunt = base_taunt
        self.taunt = taunt if taunt else base_taunt
        self.base_cleave = base_cleave
        self.cleave = cleave if cleave else base_cleave
        self.base_reborn = base_reborn
        self.reborn = reborn if reborn else base_reborn
        self.base_windfury = base_windfury
        self.windfury = windfury if windfury else base_windfury
        self.base_mega_windfury = base_mega_windfury
        self.mega_windfury = mega_windfury if mega_windfury else base_mega_windfury
        self.base_poisonous = base_poisonous
        self.poisonous = poisonous if poisonous else base_poisonous
        self.base_deathrattles = [base_deathrattle] if base_deathrattle else []
        self.deathrattles = self.base_deathrattles + deathrattles if deathrattles else self.base_deathrattles
        self.golden = golden
        self.position = position
        self.player_id = player_id
        self.mana_cost = mana_cost
        self.attacked = attacked
        self.immediate_attack_pending = immediate_attack_pending
        self.token = token
        self.reborn_triggered = reborn_triggered
        self.damage_trigger_pending = False

        if self.reborn_triggered:
            self.defense = 1

    def minion_string(self):
        """String representation of minion

        Returns:
            str -- String representation
        """
        attributes = []
        if self.taunt:
            attributes += "[Ta]"
        if self.windfury:
            attributes += "[Wf]"
        if self.poisonous:
            attributes += "[Po]"
        if self.divine_shield:
            attributes += "[Di]"
        if self.cleave:
            attributes += "[Cl]"
        if self.reborn:
            attributes += "[Re]"
        return_string = f"{self.attack}/{self.defense} {''.join(attributes)} ({self.name})"
        positional_part = f"<P{self.player_id} {self.position}> "
        return_string = positional_part + return_string
        return return_string

    def __str__(self):
        """String representation of minion

        Returns:
            str -- String representation
        """
        return self.minion_string()

    def add_stats(self, attack: int, defense: int):
        """Add minion attack/defense
        """
        self.attack += attack
        self.defense += defense

    def remove_stats(self, attack: int, defense: int):
        """Remove minion attack/defense
        """
        self.attack -= attack
        self.defense -= defense

    def receive_damage(self, amount: int, poisonous: bool, own_board: PlayerBoard, defer_damage_trigger: Optional[bool] = False):
        """Receive amount of damage which can be poisonous

        Arguments:
            amount {int} -- Amount of damage to receive
            poisonous {bool} -- Whether the damage is poisonous
            own_board {PlayerBoard} -- The board belonging to the minion taking damage

        Returns 3 item list:
            bool -- Whether the minion has popped a shield
            bool -- Whether the attacked minion died or not
            int -- Current health of the attacked minion (will be negative if its dead, can be used for overkill amount)
        """
        if amount <= 0:
            return [False, self.dead, self.defense]

        popped_shield = False
        if self.divine_shield:
            popped_shield = True
            self.divine_shield = False
        else:  # Minion took damage
            self.defense -= amount
            if self.defense <= 0 or poisonous:
                self.dead = True
            if not defer_damage_trigger:
                self.on_receive_damage(own_board)
            self.damage_trigger_pending = defer_damage_trigger

        return [popped_shield, self.dead, self.defense]

    def process_deferred_damage_trigger(self, own_board: PlayerBoard):
        if self.damage_trigger_pending:
            self.on_receive_damage(own_board)
        self.damage_trigger_pending = False

    def at_beginning_game(self, game_instance: GameInstance, player_starts: bool, own_board: PlayerBoard, opposing_board: PlayerBoard):
        """Trigger that can be implemented to do things at the beginning of the game

        Arguments:
            game_instance {GameInstance} -- The instance of the game we are working in
            player_starts {bool} -- Whether this minion belongs to the starting player
            own_board {PlayerBoard} -- Player board belonging to minion
            opposing_board {PlayerBoard} -- Player board not belonging to minion
        """
        pass

    def on_attack_before(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        """Trigger that can be implemented before the minion attacks
        """
        pass

    def on_friendly_attack_before(self, attacking_minion: Minion, own_board: PlayerBoard):
        """Trigger when a friendly minion attacks
        """
        pass

    def on_attack_after(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        """Trigger that can be implemented after the minion attacks
        """
        pass

    def on_attacked(self, own_board: PlayerBoard, opposing_board: PlayerBoard):
        """Trigger that can be implemented when the minion is attacked
        """
        pass

    def on_friendly_attacked(self, friendly_minion: Minion):
        """Trigger for when another friendly minion on the board is attacked

        Arguments:
            friendly_minion {Minion} -- The minion that is being attacked
        """
        pass

    def on_kill(self):
        """Trigger that happens when this minion kills another minion"""
        pass

    def on_friendly_kill(self, killer_minion: Minion):
        """Trigger that happens when a friendly minion kills an enemy minion

        Arguments:
            killer_minion {Minion} -- The enemy minion that was killed"""
        pass

    def on_overkill(self):
        """Trigger that happens when this minion overkills another minion"""
        pass

    def on_receive_damage(self, own_board: PlayerBoard):
        """Trigger that happens when this minion receives damage"""
        pass

    def on_summon(self, other_minion: Minion, own_board: PlayerBoard):
        """Trigger that happens when this minion enters the board"""
        pass

    def on_friendly_summon(self, other_minion: Minion):
        """Trigger that happens when another minion enters the friendly player board

        Arguments:
            other_minion {Minion} -- Minion entering the friendly player board
        """
        pass

    def on_removal(self, other_minion: Minion, own_board: PlayerBoard):
        """What the minion should do to other minion on the player board when it exits (NOT a deathrattle)

        Arguments:
            other_minion {Minion} -- Friendly minion that is remaining on the board
            own_board {PlayerBoard} -- Board the minion belongs to
        """
        pass

    def on_friendly_removal(self, other_minion: Minion):
        """Trigger that happens when another minion on the player board dies

        Arguments:
            other_minion {Minion} -- Other minion that died
        """
        pass

    def on_friendly_removal_after(self, other_minion: Minion, enemy_board: PlayerBoard):
        """Trigger that happens after another minion on the player board dies """
        pass

    def on_friendly_minion_loses_divine_shield(self):
        """Trigger that happens when a friendly minion loses divine shield"""
        pass

    def shift_left(self):
        """Shift position of minion left because a space cleared up"""
        self.position -= 1

    def shift_right(self):
        """Shift position of minion right because a minion was added to the left"""
        self.position += 1

    def trigger_reborn(self, own_board: PlayerBoard, insert_position: int):
        """If the minion has reborn and has not triggered, trigger it"""
        # TODO: Account for shifted position due to deathrattle minions entering and/or dieing
        # IDEA: Track how many minions were inserted from friendly deathrattles, check how many are still alive when reborn is handled
        if self.reborn and not self.reborn_triggered:
            self.__init__(reborn_triggered=True, token=True, attacked=self.attacked, golden=self.golden)
            own_board.add_minion(new_minion=self, position=insert_position)
