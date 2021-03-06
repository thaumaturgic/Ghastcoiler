import random
import logging

from typing import Optional

from game.player_board import PlayerBoard
from minions.base import Minion


class GameInstance:
    def __init__(self, player_board_0: PlayerBoard, player_board_1: PlayerBoard, player_turn: Optional[int] = None):
        """Instance of a single game rollout

        Arguments:
            player_board_0 {PlayerBoard} -- Player board of the first player
            player_board_1 {PlayerBoard} -- Player board of the second player

        Keyword Arguments:
            player_turn {Optional[int]} -- Player that starts, if None choose at random (default: {None})
        """
        self.player_board = {0: player_board_0, 1: player_board_1}
        # TODO: Player turn is determined by minion count, should we use that here? Or determine it at start of first combat?
        self.player_turn = player_turn if player_turn else random.randint(0, 1)
        self.turn = 0

    def log_current_game(self):
        """Log current game state"""
        logging.debug("Player 0 board:")
        logging.debug(self.player_board[0].minions_string())
        logging.debug("Player 1 board:")
        logging.debug(self.player_board[1].minions_string())

    def __str__(self):
        """String representation of current game state

        Returns:
            string -- Representation
        """
        return_string = "Player 0:\n"
        return_string += str(self.player_board[0]) + "\n\n"
        return_string += "Player 1:\n"
        return_string += str(self.player_board[1])
        return return_string

    def attacking_player_board(self):
        """Return board of currently attacking player

        Returns:
            PlayerBoard -- PlayerBoard of the current attacking player
        """
        return self.player_board[self.player_turn]

    def defending_player_board(self):
        """Return board of currently defending player

        Returns:
            PlayerBoard -- PlayerBoard of the current defending player
        """
        return self.player_board[1 - self.player_turn]

    def finished(self):
        """Check if the game is finished

        Returns:
            bool -- Is the game finished?
        """
        draw = self.player_board[0].select_attacking_minion() is None and self.player_board[1].select_attacking_minion() is None
        return len(self.player_board[0].minions) == 0 or len(self.player_board[1].minions) == 0 or draw

    def deal_attack_damage(self, defending_minion, defending_board, attacking_minion, attacking_board, defer_damage_trigger: Optional[bool] = False):
        """Deal damage to minion

        Arguments:
            minion {Minion} -- Minion that is dealt damage
            board {PlayerBoard} -- Player board of which the minion belongs to
            amount {int} -- Amount of damage dealt
            poisonous {bool} -- Whether it is poisonous damage
            defer_damage_trigger {bool} -- Flag to trigger 'on damage' now or later. Used when minion is damaged by cleave
        """
        divine_shield_popped, defending_minion_health = defending_minion.receive_damage(attacking_minion.attack, attacking_minion.poisonous, defending_board, defer_damage_trigger)

        # Detect minion killing here, notify board (ie wagtoggle)
        if defending_minion_health <= 0:
            attacking_minion.on_kill()
            attacking_board.on_friendly_kill(attacking_minion)
            if defending_minion_health < 0:
                attacking_minion.on_overkill(attacking_board, defending_minion, defending_board)

        if divine_shield_popped:
            #logging.debug(f"Divine shield from {defending_minion.minion_string()} popped")
            defending_board.divine_shield_popped()

    def set_aside_dead_minions(self, board: PlayerBoard):
        """Remove any dead minions. Return the List of minions to process any deathrattles and reborn triggers.

        Arguments:
            board {PlayerBoard} -- Player board to check for dead minions
        """
        dead_minions = board.select_dead()
        left_neighors = []
        for minion in dead_minions:
            left_neighors.append(minion.left_neighbor)

        # Dead minions care about their left neighbor for deathrattle/reborn positioning
        for index,minion in enumerate(dead_minions):
            board.remove_minion(minion)
            minion.left_neighbor = left_neighors[index]

        return dead_minions

    def resolve_extra_attacks(self, attacking_player_board: PlayerBoard, defending_player_board: PlayerBoard):
        """Resolve any 'attacks immediately' minions and the consequences of those attacks

        Arguments:
            attacking_player_board {PlayerBoard} -- Player board of attacking player
            defending_player_board {PlayerBoard} -- Player board of defending player
        """
        for attacker in attacking_player_board.get_immediate_attack_minions():
            attacker.immediate_attack_pending = False
            defender = defending_player_board.select_defending_minion()
            if defender:
                self.attack(attacker, defender)
                self.check_deaths(attacking_player_board, defending_player_board)
            else:
                return

    def check_deaths(self, attacking_player_board: PlayerBoard, defending_player_board: PlayerBoard):
        """Check deaths on both sides, collect death rattles, process them and resolve consequences (immediate attacks / reborn triggers)

        Arguments:
            attacking_player_board {PlayerBoard} -- Player board of attacking player
            defending_player_board {PlayerBoard} -- Player board of defending player
        """
        # General flow of resolving death states:
        # Resolve attacker deathrattles from left to right, multiplied by baron
        #     Resolve extra attacks after each deathrattle resolves (then recursively check deaths)
        # Resolve defender deathrattles from left to right, multiplied by baron
        #     Resolve extra attacks after each deathrattle resolves (then recursively check deaths)

        # There are some DRY vibes here but for now this is fine
        attacker_dead_minions = self.set_aside_dead_minions(attacking_player_board)
        defender_dead_minions = self.set_aside_dead_minions(defending_player_board)

        # Resolve death rattles and 'attacks immediately' triggers. Attacker first, then defender
        # TODO: immediate attacks on defender side resolve before attacks deathrattles?
        # TODO: Is there a consistent order to deathrattles??
        for minion in attacker_dead_minions:
            for deathrattle in minion.deathrattles:
                for _ in range(attacking_player_board.deathrattle_multiplier):
                    deathrattle.trigger(minion, attacking_player_board, defending_player_board)
                    self.resolve_extra_attacks(attacking_player_board, defending_player_board)

        # Resolve "after a friendly minion dies" triggers. ie soul juggles after deathrattles
        for minion in attacking_player_board.get_living_minions():
            for dead_minion in attacker_dead_minions:
                minion.on_friendly_removal_after(dead_minion, attacking_player_board, defending_player_board)

        for minion in defender_dead_minions:
            for deathrattle in minion.deathrattles:
                for _ in range(defending_player_board.deathrattle_multiplier):
                    deathrattle.trigger(minion, defending_player_board, attacking_player_board)
                    self.resolve_extra_attacks(defending_player_board, attacking_player_board)

        for minion in defending_player_board.get_living_minions():
            for dead_minion in defender_dead_minions:
                minion.on_friendly_removal_after(dead_minion, defending_player_board, attacking_player_board)

        # Process deaths here again to see if death rattles resulted in more deaths
        if len(attacking_player_board.select_dead()) > 0 or len(defending_player_board.select_dead()):
            self.check_deaths(attacking_player_board, defending_player_board)

        # Resolve reborns after deathrattles
        for minion in attacker_dead_minions:
            if minion.reborn and not minion.reborn_triggered:
                minion.trigger_reborn(attacking_player_board)

        for minion in defender_dead_minions:
            if minion.reborn and not minion.reborn_triggered:
                minion.trigger_reborn(defending_player_board)

        # Continue to resolve extra attacks until all are done
        while attacking_player_board.get_immediate_attack_minions() or defending_player_board.get_immediate_attack_minions():
            # TODO: Is there a priority for resolving pirate attacks on each other? Are they queued up?
            self.resolve_extra_attacks(attacking_player_board, defending_player_board)
            self.resolve_extra_attacks(defending_player_board, attacking_player_board)

    def attack(self, attacking_minion: Minion, defending_minion: Minion):
        """Let one minion attack the other

        Arguments:
            attacking_minion {Minion} -- Minion that attacks
            defending_minion {Minion} -- Minion that is attacked
        """
        attacker, defender = self.attacking_player_board(), self.defending_player_board()
        #logging.debug(f"{attacking_minion.minion_string()} attacks {defending_minion.minion_string()}")

        # Pre-attack triggers
        attacking_minion.on_attack_before(attacker, defender)
        for minion in attacker.minions:
            if minion.position != attacking_minion.position:
                minion.on_friendly_attack_before(attacking_minion, attacker)

        defending_minion.on_attacked(defender, attacker)
        for minion in defender.minions:
            if minion.position != defending_minion.position:
                minion.on_friendly_attacked(defending_minion)

        # Deal attack damage
        if attacking_minion.cleave:
            # Minions hit with cleave should take damage all at once, but triggers resolve after
            neighbors = defender.get_minions_neighbors(defending_minion)
            defenders = [neighbors[0], defending_minion, neighbors[1]]
            for minion in [x for x in defenders if x]:
                self.deal_attack_damage(minion, defender, attacking_minion, attacker, True)
            self.deal_attack_damage(attacking_minion, attacker, defending_minion, defender)
        else:
            self.deal_attack_damage(defending_minion, defender, attacking_minion, attacker)
            self.deal_attack_damage(attacking_minion, attacker, defending_minion, defender)

        # Damage triggers from cleave and herald of flame should be resolved after attack and overkill trigger resolution
        for minion in defender.minions:
            minion.process_deferred_damage_trigger(defender)

        # Post attack triggers (macaw)
        attacking_minion.on_attack_after(attacker, defender)

    def calculate_score_player_0(self):
        """Calculate final score from player 0 perspective, negative is lost by X, 0 is a tie and positive is won by X

        Returns:
            int -- Amount by which player 0 won or lost
        """
        player0Minions = self.player_board[0].minions
        player1Minions = self.player_board[1].minions

        # If the only minions left on both sides all have zero attack power, game is a tie
        if len(player0Minions) != 0 and len(player1Minions) != 0:
            if all(minion.attack == 0 for minion in player0Minions) and all(minion.attack == 0 for minion in player1Minions):
                return 0

        if len(player0Minions) == 0:
            if len(player1Minions) == 0:
                return 0  # No minions left on either board, game is a tie
            else:
                return - self.player_board[1].score()  # player 1 wins
        else:
            return self.player_board[0].score()  # player 0 wins

    def start_of_game(self, starting_player: Optional[int] = None):
        """Do all game actions up until the first attack is do pre-game minion and hero power actions, determine who attacks first, etc.
        """
        # TODO: Handle Illidan Stormrage hero power here (before whelp power triggers)

        # Attacking player is determined before whelp potentially kills enemy minions.
        # aka if both boards are full, and a whelp kills an opposing minion, the opposing player can still go first with less minions
        player0minions = len(self.player_board[0].minions)
        player1minions = len(self.player_board[1].minions)
        if starting_player is not None:
            self.player_turn = starting_player
        else:
            self.player_turn = 0 if player0minions > player1minions else 1 if player1minions > player0minions else random.randint(0, 1)

        # TODO If both sides have whelps, they trade off whelp attacks from one side to the other, resolving deathrattles after each firebreath
        # Golden whelp will fire both before yielding to other dragons. Deaths are checked after golden dragon finishes
        current = self.attacking_player_board()
        other = self.defending_player_board()
        for minion in current.get_living_minions():
            minion.at_beginning_game(self, True, current, other)
        for minion in other.get_living_minions():
            minion.at_beginning_game(self, False, other, current)

    def single_round(self):
        """Do one attack and resolve consequences. ie one step of the game"""
        attacker_board = self.attacking_player_board()
        defender_board = self.defending_player_board()

        self.turn += 1
        #logging.debug(f"Turn {self.turn} has started, player {self.player_turn} will attack")
        #self.log_current_game()
        #logging.debug('-----------------')
        attacking_minion = attacker_board.select_attacking_minion()
        defending_minion = defender_board.select_defending_minion(False if not attacking_minion else attacking_minion.attacks_lowest_power)
        if attacking_minion and defending_minion:
            attacks = 4 if attacking_minion.mega_windfury else 2 if attacking_minion.windfury else 1
            for _ in range(attacks):
                if not attacking_minion.dead and defending_minion:
                    self.attack(attacking_minion, defending_minion)
                    self.check_deaths(self.attacking_player_board(), self.defending_player_board())
                    defending_minion = defender_board.select_defending_minion(attacking_minion.attacks_lowest_power)
            # Flag the minion as having attacked.
            # It may be dead, but we have to set this after combat has resolved to maintain correct attack order...
            attacking_minion.attacked = True
        #else:
        #logging.debug("No attacker or No defender")
        #logging.debug("=================")
        self.player_turn = 1 - self.player_turn

    def start(self):
        """Play a game to completion

        Returns:
            int -- Final score from player 0 perspective
        """
        self.start_of_game()

        while not self.finished():
            self.single_round()

        #logging.debug(f"Ending board score {self.calculate_score_player_0()}")
        return self.calculate_score_player_0()
