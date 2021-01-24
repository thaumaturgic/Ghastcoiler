import random
import logging

from typing import List, Optional

from minions.base import Minion
from minions.types import MinionType

class PlayerBoard:
    def __init__(self, player_id: int, hero: None, life_total: int, rank: int, minions: List[Minion]):
        """The board of one the players in a game instance

        Arguments:
            player_id {int} -- Whether the board belongs to player 0 or 1
            hero {None} -- Not implemented yet but will contain the hero power
            life_total {int} -- Current life total determined for checking if player died
            rank {int} -- Rank used for determining amount of damage at a win
            minions {List[Minion]} -- List of minions on the initial board
        """
        self.player_id = player_id
        self.hero = hero
        self.life_total = life_total
        self.rank = rank
        self.attack_position = 0
        self.set_minions(minions)
        self.deathrattle_multiplier = 1 # TODO: Implement baron minion to adjust this value
        self.token_creation_multiplier = 1 #TODO: Implement khadgar minion to adjust this value

    def set_minions(self, minions: List[Minion]):
        """String representation of all minions in player board

        Returns:
            string -- Generated representation
        """
        self.minions: List[Minion] = minions
        for index, minion in enumerate(minions):
            minion.position = index
            minion.player_id = self.player_id

    def copy(self):
        """Deep copy PlayerBoard instance to not carry state over multiple simulations

        Returns:
            PlayerBoard -- Deep copy of current PlayerBoard
        """
        return PlayerBoard(player_id=self.player_id, hero=self.hero, life_total=self.life_total, rank=self.rank, minions=[minion.copy() for minion in self.minions])

    def minions_string(self):
        """String representation of all minions in player board

        Returns:
            string -- Generated representation
        """
        minion_string = []
        for minion in self.minions:
            minion_string.append(minion.minion_string())
        return "\n".join(minion_string)

    def __str__(self):
        """String representation of PlayerBoard

        Returns:
            string -- Generated representation
        """
        return_string = f"Hero: {self.hero}\nLife: {self.life_total}\nRank: {self.rank}\n"
        for minion in self.minions:
            return_string += str(minion) + "\n"
        return return_string

    def score(self):
        """Count score based on rank and remaining minions

        Returns:
            int -- Total score
        """
        if len(self.minions) == 0:
            return 0
        return sum([minion.rank for minion in self.minions]) + self.rank

    def count_minion_type(self, minion_type):
        """Count the number of minions of specific type on the board

        Arguments:
            minion_type {MinionType} -- The MinionType to count

        Returns:
            int -- Number of minions of type MinionType
        """
        return len([minion for minion in self.minions if minion_type in minion.types])

    def select_taunts(self):
        """Return all minions with Taunt for defending minion selection

        Returns:
            List[Minion] -- List of all minions with Taunt
        """
        return [minion for minion in self.minions if minion.taunt and not minion.dead]

    def divine_shield_popped(self):
        """Called when a divine shield pops on this board to execute possible triggers on other minions"""
        for minion in self.minions:
            minion.on_any_minion_loses_divine_shield()

    def select_attacking_minion(self):
        """Select next minion that should attack

        Returns:
            Minion -- Minion that will attack next or None if there are no minions with attack > 0
        """
        # Is there at least one possible attacker on the board
        eligibleAttacker = False

        for minion in self.minions:
            eligibleAttacker = minion.attack > 0
            if not minion.attacked:
                if minion.attack == 0:
                    minion.attacked = True # Skip zero attack minions
                    continue
                return minion

        # All minions have zero attack
        if not eligibleAttacker:
            return None

        # All minions must have attacked this round, reset their flags
        for minion in self.minions:
            minion.attacked = False

        return self.select_attacking_minion()
        #return None if not eligibleAttacker else self.select_attacking_minion()

    def generate_possible_defending_minions(self, attacks_lowest=False):
        """Generate list of minions that can be currently attacked

        Keyword Arguments:
            attacks_lowest {bool} -- Whether we should ignore taunts and select the lowest attack units (default: {False})

        Returns:
            List[Minion] -- List of minions that can be attacked
        """
        # TODO: Rank 6 windfury guy
        possible_minions = self.select_taunts()
        if len(possible_minions) == 0:
            possible_minions = [minion for minion in self.minions if not minion.dead]
        return possible_minions

    def select_defending_minion(self, attacks_lowest=False):
        """Choose a random minion to be attacked

        Keyword Arguments:
            attacks_lowest {bool} -- Whether we should ignore taunts and select the lowest attack units (default: {False})

        Returns:
            Minion -- Minion that will be attacked or None if the board is empty
        """
        # TODO: Rank 6 windfury guy
        if len(self.minions) == 0:
            return None

        possible_minions = self.generate_possible_defending_minions()
        defending_minion_index = random.randint(0, len(possible_minions) - 1)
        return possible_minions[defending_minion_index]

    def get_minions(self):
        """Return a list of all minions, this will likely need to be smarter using some generator for cases where minions can die or spawn in between

        Returns:
            List[Minion] -- List of all minions on board
        """
        return self.minions

    def get_minions_neighbors(self, minion: Minion):
        position = minion.position
        neighbors = []
        left_position = position - 1
        right_position = position + 1
        if left_position >= 0:
            neighbors.append(self.minions[left_position])
        if right_position < len(self.minions):
            neighbors.append(self.minions[right_position])
        return neighbors

    def random_minion(self):
        """Return a random minion from the player board. In some game states its possible to have a dead minion that has not been removed from the board yet.
        For example, while a bomb or soul juggler has triggered. In these cases we want to not target already dead units

        Returns:
            Minion -- Randomly selected minion
        """
        if len(self.minions) > 0:
            live_minions = [minion for minion in self.minions if not minion.dead]
            position = live_minions[random.randint(0, len(live_minions) - 1)].position
            return self.minions[position]

    def remove_minion(self, minion: Minion):
        """Remove minion from board

        Arguments:
            minion {Minion} -- Minion to be removed from board
        """
        logging.debug(f"Removing {minion.minion_string()}")
        position = minion.position
        self.minions.pop(position)
        for other_minion in self.minions[position:]:
            other_minion.shift_left()

        for other_minion in self.minions:
            minion.on_removal(other_minion)
            other_minion.on_friendly_removal(minion)
            
    def add_minion(self, new_minion: Minion, position: Optional[int] = None, token: Optional[bool] = False) -> Optional[Minion]:
        """Add minion to the board if there is space

        Arguments:
            new_minion {Minion} -- Instance of minion to be added
            token {Bool} -- is this minion being added a token (including reborns)? For khadgar multipliers

        Keyword Arguments:
            position {Optional[int]} -- Optional position to insert the minion at, if None add at the end (default: {None})

        Returns:
            Optional[Minion] -- Return the updated Minion if inserted succesfully, otherwise return None
        """
        if len(self.minions) < 7:
            if position is None:
                position = len(self.minions)

            #TODO: Implement khadgar multiplier

            for minion in self.minions:
                minion.on_friendly_summon(other_minion=new_minion)
                new_minion.on_summon(minion)

            new_minion.position = position
            new_minion.player_id = self.player_id
            self.minions.insert(position, new_minion)
            for minion in self.minions[position + 1:]:
                minion.shift_right()
            logging.debug(f"Adding {new_minion.minion_string()}")
            return new_minion
        else:
            logging.debug(f"Did not add {new_minion.minion_string()} because of a lack of space")
