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
    # Account for 
    # -Regular deathrattle: minion is dead, insertion position follows the left neighbor rule
    # -Triggered by macaw: minion is alive, position is to right of it
    # -Either combination with khadgar: Subsequent summoned minions will have a different left neighbor position
    def summon_deathrattle_minions(own_board, summoning_minion, summoned_minion_class, summon_golden_minion: Optional[bool] = None, minions_to_spawn: int = 1, triggered_from_macaw: bool = False, should_attack: bool = False):
        insert_position = summoning_minion.position+1 if triggered_from_macaw else summoning_minion.find_deathrattle_reborn_position()
        if summon_golden_minion is not None:
            summon_golden = summon_golden_minion
        else:
            summon_golden = summoning_minion.golden

        new_minion = None
        for _ in range(minions_to_spawn):
            new_minion = own_board.add_minion(
                summoned_minion_class(attacked = summoning_minion.attacked, golden = summon_golden, immediate_attack_pending = should_attack),
                position = insert_position, 
                summoning_minion = summoning_minion if summoning_minion.dead else None)
            if new_minion:
                insert_position = new_minion.position+1
            else:
                break
        return new_minion

    @staticmethod
    def summon_random_minions(summoning_minion, own_board, minions_to_summon: int, criteria, triggered_from_macaw: bool):
        from utils.minion_utils import MinionUtils        
        minions = MinionUtils().get_minions(criteria)

        insert_position = summoning_minion.position+1 if triggered_from_macaw else summoning_minion.find_deathrattle_reborn_position()

        for _ in range(minions_to_summon):
            new_minion_class = minions[random.randint(0, len(minions) - 1)].__class__

            new_minion = own_board.add_minion(
                new_minion_class(attacked = summoning_minion.attacked, golden = False),
                position = insert_position, 
                summoning_minion = summoning_minion if summoning_minion.dead else None)
            if new_minion:
                insert_position = new_minion.position+1
            else:
                break

