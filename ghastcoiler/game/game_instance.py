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

    def kill(self, minion: Minion, minion_board: PlayerBoard, opposing_board: PlayerBoard, minion_defending_player: bool):
        """Kill a minion off and update board using deathrattles and other triggers

        Arguments:
            minion {Minion} -- Minion that will die
            minion_board {PlayerBoard} -- Player board belonging to the minion that will die
            opposing_board {PlayerBoard} -- Board opposing of the minion that dies
            minion_defending_player {bool} -- Whether the minion died is on the defending side for trigger orders
        """
        if minion_defending_player:
            opposing_board.remove_minion(minion)
        else:
            minion_board.remove_minion(minion)

        # TODO: Baron
        for deathrattle in minion.deathrattles:
            if minion_defending_player:
                deathrattle.trigger(minion, opposing_board, minion_board)
            else:
                deathrattle.trigger(minion, minion_board, opposing_board)
        self.check_deaths(minion_board, opposing_board)

    def check_deaths(self, attacking_player_board: PlayerBoard, defending_player_board: PlayerBoard):
        """Check deaths on both sides

        Arguments:
            attacking_player_board {PlayerBoard} -- Player board of attacking player
            defending_player_board {PlayerBoard} -- Player board of defending player
        """
        for minion in attacking_player_board.get_minions():
            if minion.check_death(attacking_player_board, defending_player_board):
                self.kill(minion, attacking_player_board, defending_player_board, minion_defending_player=False)
                return # TODO: Allow multiple units to die at once, ie when cleave happens
        for minion in defending_player_board.get_minions():
            if minion.check_death(defending_player_board, attacking_player_board):
                self.kill(minion, attacking_player_board, defending_player_board, minion_defending_player=True)
                return

    def attack(self, attacking_minion: Minion, defending_minion: Minion):
        """Let one minion attack the other

        Arguments:
            attacking_minion {Minion} -- Minion that attacks
            defending_minion {Minion} -- Minion that is attacked
        """
        # TODO: Cleave
        attacker, defender = self.attacking_player_board(), self.defending_player_board()
        attacking_minion.on_attack(attacker, defender)
        defending_minion.on_attacked(attacker, defender)

        logging.debug(f"{attacking_minion.minion_string()} attacks {defending_minion.minion_string()}") 

        self.deal_damage(attacking_minion, attacker, defending_minion.attack, defending_minion.poisonous)
        self.deal_damage(defending_minion, defender, attacking_minion.attack, attacking_minion.poisonous)

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

    def start(self):
        """Start game instance rollout

        Returns:
            int -- Final score from player 0 perspective
        """
        # TODO: Handle Illidan Stormrage hero power here (before whelp power triggers)

        # TODO: Is attacking player determined before or after a red whelp potentially kills an opposing minion?
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
        while not self.finished():
            self.turn += 1
            logging.debug(f"Turn {self.turn} has started, player {self.player_turn} will attack")
            self.log_current_game()
            logging.debug('-----------------')
            attacking_minion = self.attacking_player_board().select_attacking_minion()
            defending_minion = self.defending_player_board().select_defending_minion()
            if attacking_minion:
                attacks = 2 if attacking_minion.windfury else 1 #TODO: mega windfury
                for _ in range(attacks):
                    self.attack(attacking_minion, defending_minion)
                    self.check_deaths(self.attacking_player_board(), self.defending_player_board())
                # Flag the minion as having attacked. 
                # It may be dead, but we have to set this after all deathrattles have been resolved to maintain correct attack order...
                attacking_minion.attacked = True
            else:
                logging.debug("No eligible attackers")
            logging.debug("=================")
            self.player_turn = 1 - self.player_turn

        logging.debug(f"Ending board score {self.calculate_score_player_0()}")
        return self.calculate_score_player_0()
