import random
import logging
import copy
import sys

from typing import List, Optional

from minions.base import Minion


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
        self.deathrattle_multiplier = 1
        self.token_creation_multiplier = 0
        self.set_minions(minions)

    def set_minions(self, minions: List[Minion]):
        """Initialize the board to the list of minions given.
        """
        self.minions: List[Minion] = minions
        self.token_creation_multiplier = 0
        self.deathrattle_multiplier = 1

        if minions:
            left_neighbor = None
            for index, minion in enumerate(minions):
                minion.left_neighbor = left_neighbor
                minion.right_neighbor = None if (index + 1 >= len(minions)) else minions[index+1] 
                left_neighbor = minion

                if minion.name == "Khadgar":
                    # Multiple khadgars DO stack
                    self.token_creation_multiplier += 2 if minion.golden else 1
                elif minion.name == "Baron Rivendare":
                    # Multiple barons do not stack. If there is a golden baron and regular baron, golden takes priority
                    deathrattle_multiplier = 3 if minion.golden else 2
                    if self.deathrattle_multiplier < deathrattle_multiplier:
                        self.deathrattle_multiplier = deathrattle_multiplier
                minion.position = index
                minion.player_id = self.player_id


    def copy(self):
        """Deep copy PlayerBoard instance to not carry state over multiple simulations

        Returns:
            PlayerBoard -- Deep copy of current PlayerBoard
        """
        return PlayerBoard(player_id=self.player_id, hero=self.hero, life_total=self.life_total, rank=self.rank, minions=copy.deepcopy(self.minions))

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
        """Return all living minions with Taunt

        Returns:
            List[Minion] -- List of all living minions with Taunt
        """
        return [minion for minion in self.minions if minion.taunt and not minion.dead]

    def select_dead(self):
        """Return all minions that are dead

        Returns:
            List[Minion] -- List of all currently dead minions
        """
        return [minion for minion in self.minions if minion.dead]

    def divine_shield_popped(self):
        """Called when a divine shield pops on this board to execute possible triggers on other minions"""
        for minion in self.minions:
            minion.on_friendly_minion_loses_divine_shield()

    def on_friendly_kill(self, killer_minion: Minion):
        """Called when a friendly minion kills an enemy
        TODO: 'on_friendly_kill' is only called during attack damage, a deathrattle that kills something wont trigger this...

        Arguments:
            minion {Minion} -- Minion that dealt the killing damage
        """
        for minion in self.minions:
            if minion.position != killer_minion.position:
                minion.on_friendly_kill(killer_minion)

    def select_attacking_minion(self):
        """Select next minion that should attack

        Returns:
            Minion -- Minion that will attack next or None if there are no eligible minions
        """
        # Is there at least one possible attacker on the board
        eligibleAttacker = False

        for minion in self.minions:
            eligibleAttacker = minion.attack > 0
            if not minion.attacked:
                if minion.attack == 0:
                    minion.attacked = True  # Skip zero attack minions
                    continue
                return minion # We found the left-most non-zero power minion that hasnt attacked this round

        # All minions have zero attack
        if not eligibleAttacker:
            return None

        # All minions must have attacked this round, reset their flags, search again
        for minion in self.minions:
            minion.attacked = False
        return self.select_attacking_minion()

    def generate_possible_defending_minions(self):
        """Generate list of minions that can be currently attacked

        Returns:
            List[Minion] -- List of minions that can be attacked
        """
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
        if len(self.minions) == 0:
            return None

        if attacks_lowest:
            lowest_attack = sys.maxsize
            lowest_attack_minions = []
            for minion in self.minions:
                if minion.attack < lowest_attack:
                    lowest_attack = minion.attack
                    lowest_attack_minions = [minion]
                elif minion.attack == lowest_attack:
                    lowest_attack_minions.append(minion)
            return lowest_attack_minions[random.randint(0, len(lowest_attack_minions) - 1)]
        else:
            possible_minions = self.generate_possible_defending_minions()
            defending_minion_index = random.randint(0, len(possible_minions) - 1)
            return possible_minions[defending_minion_index]

    def get_living_minions(self):
        """Return a list of all minions

        Returns:
            List[Minion] -- List of all minions on board
        """
        return [minion for minion in self.minions if not minion.dead]

    def get_minions_neighbors(self, minion: Minion):
        """Return a list of minions to the left and right of the minions position

        Returns:
            List[Minion] -- List of all minions next to the minion
        """
        return [minion.left_neighbor, minion.right_neighbor]

    def get_immediate_attack_minions(self,):
        """ Return a list of minions that should attack 'immediately'

        Returns:
            List[Minion] -- Minions with pending attack triggers
        """
        return [x for x in self.minions if x.immediate_attack_pending]

    def random_minion(self):
        """Return a random living minion from the player board. In some game states its possible to have a dead minion that has not been removed from the board yet.
        For example, while a bomb or soul juggler has triggered. In these cases we want to not target already dead units

        Returns:
            Minion -- Randomly selected minion, or None
        """
        if len(self.minions) > 0:
            live_minions = self.get_living_minions()
            if len(live_minions) > 0:
                position = live_minions[random.randint(0, len(live_minions) - 1)].position
                return self.minions[position]

    def remove_minion(self, minion: Minion):
        """Remove minion from board

        Arguments:
            minion {Minion} -- Minion to be removed from board
        """
        logging.debug(f"Removing {minion.minion_string()}")
        position = minion.position
        neighbors = self.get_minions_neighbors(minion)
        if neighbors[0]:
            neighbors[0].right_neighbor = neighbors[1]
        if neighbors[1]:
            neighbors[1].left_neighbor = neighbors[0]

        self.minions.pop(position)
        for other_minion in self.minions[position:]:
            other_minion.shift_left()

        for other_minion in self.minions:
            minion.on_removal(other_minion, self)
            other_minion.on_friendly_removal(minion)

        minion.on_self_removal(self)

    def add_minion(self, new_minion: Minion, position: Optional[int] = None, to_right: Optional[bool] = False, allow_copy: Optional[bool] = True) -> Optional[Minion]:
        """Add minion to the board if there is space

        Arguments:
            new_minion {Minion} -- Instance of minion to be added
            token {Bool} -- is this minion being added a token (including reborns)? For khadgar multipliers

        Keyword Arguments:
            position {Optional[int]} -- Optional position to insert the minion at, if None add at the end (default: {None})
            to_right {Optional[bool]} -- Optional flag to insert minion to right of the indicated position if possible
        """
        if len(self.minions) < 7:
            if position is None:
                position = len(self.minions)

            if to_right:
                position += 1

            new_minion.on_self_summon(self)

            for minion in self.minions:
                minion.on_friendly_summon(other_minion=new_minion)
                new_minion.on_summon(minion, self)

            # Set neighbors for new minion and existing minions
            left_neighbor, right_neighbor = None, None
            if len(self.minions) == 0:
                # left and right are None
                test = 1 
            elif position > len(self.minions)-1:
                # left exists, right is None
                left_neighbor = self.minions[position-1]
                left_neighbor.right_neighbor = new_minion
            elif position == 0 and len(self.minions) > 0:
                # right exists, left is None
                right_neighbor = self.minions[position]
                right_neighbor.left_neighbor = new_minion
            else:
                # left and right exist
                left_neighbor = self.minions[position-1]
                right_neighbor = self.minions[position]
                left_neighbor.right_neighbor = new_minion
                right_neighbor.left_neighbor = new_minion

            new_minion.position = position
            new_minion.player_id = self.player_id
            new_minion.left_neighbor = left_neighbor
            new_minion.right_neighbor = right_neighbor

            self.minions.insert(position, new_minion)
            for minion in self.minions[position + 1:]:
                minion.shift_right()
            logging.debug(f"Adding {new_minion.minion_string()}")

            if allow_copy:
                for _ in range(self.token_creation_multiplier):
                    copied_minion = copy.deepcopy(new_minion)
                    self.add_minion(copied_minion, copied_minion.position, to_right=True, allow_copy=False)

        else:
            logging.debug(f"Did not add {new_minion.minion_string()} because of a lack of space")
