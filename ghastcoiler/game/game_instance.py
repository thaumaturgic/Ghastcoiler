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

    def deal_damage(self, minion, board, amount, poisonous):
        """Deal damage to minion

        Arguments:
            minion {Minion} -- Minion that is dealt damage
            board {PlayerBoard} -- Player board of which the minion belongs to
            amount {int} -- Amount of damage dealt
            poisonous {bool} -- Whether it is poisonous damage
        """
        divine_shield_popped = minion.receive_damage(amount, poisonous)
        if divine_shield_popped:
            logging.debug("Divine shield popped")
            board.divine_shield_popped()


    def cleanup_dead_minions(self, board: PlayerBoard):
        """Remove any dead minions, collect their deathrattles for processing
        
        Arguments:
            board {PlayerBoard} -- Player board to check for dead minions
        """
        deathrattle_minions = []
        for minion in [x for x in board.get_minions() if x.dead]:
            deathrattle_minions.append(minion)
            board.remove_minion(minion)
        return deathrattle_minions

    def resolve_extra_attacks(self, attacking_player_board: PlayerBoard, defending_player_board: PlayerBoard ):
        """Resolve any 'attacks immediately' minions and the consequences of those attacks
        
        Arguments:
            attacking_player_board {PlayerBoard} -- Player board of attacking player
            defending_player_board {PlayerBoard} -- Player board of defending player
        """
        for attacker in [x for x in attacking_player_board.minions if x.immediate_attack_pending]:
            attacker.immediate_attack_pending = False
            defender = defending_player_board.select_defending_minion()
            if defender:
                self.attack(attacker, defender)
                self.check_deaths(attacking_player_board, defending_player_board)

    def check_deaths(self, attacking_player_board: PlayerBoard, defending_player_board: PlayerBoard):
        """Check deaths on both sides, collect death rattles, process them and resolve consequences (immediate attacks / reborn triggers)

        Arguments:
            attacking_player_board {PlayerBoard} -- Player board of attacking player
            defending_player_board {PlayerBoard} -- Player board of defending player
        """
        # General flow of resolving death states:
        # Resolve attacker deathrattles from left to right, multiplied by baron
	    #     Resolve extra attacks after each deathrattle resolves (then check deaths)
        # Resolve defender deathrattles from left to right, multiplied by baron
	    #     Resolve extra attacks after each deathrattle resolves (then check deaths)

        # Collect pending death rattles, remove dead minions to free up board space for deathrattles
        attacker_deathrattle_minions = self.cleanup_dead_minions(attacking_player_board)
        defender_deathrattle_minions = self.cleanup_dead_minions(defending_player_board)

        # Resolve death rattles and 'attacks immediately' triggers
        for minion in attacker_deathrattle_minions:
            for deathrattle in minion.deathrattles:
                for _ in range(attacking_player_board.deathrattle_multiplier):
                    # Trigger death rattles in left to right order
                    deathrattle.trigger(minion, attacking_player_board, defending_player_board)
                    # Check for any 'attack immediately' minions, ie scallywag tokens
                    self.resolve_extra_attacks(attacking_player_board, defending_player_board)

        for minion in defender_deathrattle_minions:
            for deathrattle in minion.deathrattles:
                for _ in range(defending_player_board.deathrattle_multiplier):
                    deathrattle.trigger(minion, defending_player_board, attacking_player_board)
                    self.resolve_extra_attacks(defending_player_board, attacking_player_board)

        #TODO: Resolve reborns after deathrattles

    def attack(self, attacking_minion: Minion, defending_minion: Minion):
        """Let one minion attack the other

        Arguments:
            attacking_minion {Minion} -- Minion that attacks
            defending_minion {Minion} -- Minion that is attacked
        """
        # TODO: Cleave
        attacker, defender = self.attacking_player_board(), self.defending_player_board()
        attacking_minion.on_attack(attacker, defender)
        defending_minion.on_attacked(defender, attacker)

        logging.debug(f"{attacking_minion.minion_string()} attacks {defending_minion.minion_string()}") 

        self.deal_damage(attacking_minion, attacker, defending_minion.attack, defending_minion.poisonous)
        self.deal_damage(defending_minion, defender, attacking_minion.attack, attacking_minion.poisonous)

        if attacking_minion.cleave:
            for neighbor in defender.get_minions_neighbors(defending_minion):
                self.deal_damage(neighbor, defender, attacking_minion.attack, attacking_minion.poisonous)

        #TODO: Handle overkill triggers here and other on kill events (ie wagtoggle)
        #TODO: Handle post damage triggers like imp and patrolbot

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
                return 0 # No minions left on either board, game is a tie
            else:
                return - self.player_board[1].score() # player 1 wins
        else:
            return self.player_board[0].score() # player 0 wins

    def start_of_game(self):
        """Do all game actions up until the first attack is do pre-game minion and hero power actions, determine who attacks first, etc. 
        """
        # TODO: Handle Illidan Stormrage hero power here (before whelp power triggers)

        # Attacking player is determined before whelp potentially kills enemy minions. 
        # aka if both boards are full, and a whelp kills an opposing minion, the opposing player can still go first with less minions
        player0minions = len(self.player_board[0].minions)
        player1minions = len(self.player_board[1].minions)
        self.player_turn = 0 if player0minions > player1minions else 1 if player1minions > player0minions else random.randint(0, 1)

        # TODO: Determine red whelp trigger priority 
        current = self.attacking_player_board()
        other = self.defending_player_board()
        for minion in current.get_minions():
            minion.at_beginning_game(self, True, current, other)
        for minion in other.get_minions():
            minion.at_beginning_game(self, False, other, current)

    def single_round(self):
        """Do one attack and resolve consequences. ie one step of the game 
        """
        self.turn += 1
        logging.debug(f"Turn {self.turn} has started, player {self.player_turn} will attack")
        self.log_current_game()
        logging.debug('-----------------')
        attacking_minion = self.attacking_player_board().select_attacking_minion()
        defending_minion = self.defending_player_board().select_defending_minion()
        if attacking_minion and defending_minion:
            attacks = 2 if attacking_minion.windfury else 1 #TODO: mega windfury
            for _ in range(attacks):
                self.attack(attacking_minion, defending_minion)
                self.check_deaths(self.attacking_player_board(), self.defending_player_board())
                # TODO: Resolve extra attacks that werent part of deathrattles?
                # TODO: resolve reborn here?
            # Flag the minion as having attacked. 
            # It may be dead, but we have to set this after all deathrattles have been resolved to maintain correct attack order...
            attacking_minion.attacked = True
        else:
            logging.debug("No attacker or No defender")
        logging.debug("=================")
        self.player_turn = 1 - self.player_turn

    def start(self):
        """Play a game to completion

        Returns:
            int -- Final score from player 0 perspective
        """
        self.start_of_game()
        
        while not self.finished():
            self.single_round()

        logging.debug(f"Ending board score {self.calculate_score_player_0()}")
        return self.calculate_score_player_0()
