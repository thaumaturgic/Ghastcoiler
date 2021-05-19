from typing import Optional
import copy
import random

class Deathrattle:
    def __init__(self, name):
        """Base Deathrattle class that should be inherited from by all deathrattle triggers

        Arguments:
            name {string} -- [name of the Deathrattle, when of specific minion use MinionNameDeathrattle]
        """
        self.name = name

    def trigger(self, minion, own_board, opposing_board, macaw_trigger: Optional[bool] = False):
        """Trigger that is called once or multiple times (with Deathbaron) when minion that has this Deathrattle dies

        Arguments:
            minion {Minion} -- Minion that died with this Deathrattle, certain features could be important, for example the attack on the Fiendish Servant
            own_board {PlayerBoard} -- Player board of the minion that died
            opposing_board {PlayerBoard} -- Player board of the opposing player of the minion that died
            macaw_trigger {bool} -- Is this deathrattle being triggered by macaw. Used for token spawn position
        """
        pass

    @staticmethod
    def spawn_random_minions(spawning_minion, own_board, minions_to_spawn: int, criteria, triggered_from_macaw: bool):
        from utils.minion_utils import MinionUtils        
        minions = MinionUtils().get_minions(criteria)

        # TODO: Test the details of this implementation, especially with macaw and attack order etc
        for i in range(minions_to_spawn):
            new_minion = copy.deepcopy(minions[random.randint(0, len(minions) - 1)])
            new_minion.attacked = spawning_minion.attacked
            own_board.add_minion(new_minion, position=spawning_minion.position + i, to_right=triggered_from_macaw)