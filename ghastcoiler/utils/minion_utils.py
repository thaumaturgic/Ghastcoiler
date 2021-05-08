import sys
import inspect

# We explicitly want to import all Minion classes
from minions.base import *  # noqa: F403
from minions.tokens import * # noqa: F403
from minions.rank_1 import *  # noqa: F403
from minions.rank_2 import *  # noqa: F403
from minions.rank_3 import *  # noqa: F403
from minions.rank_4 import *  # noqa: F403
# from minions.rank_5 import *
# from minions.rank_6 import *

def is_minion_class(class_object):
        return inspect.isclass(class_object) and issubclass(class_object, Minion) and (class_object is not Minion)

class MinionUtils:
    def __init__(self):
        self.minion_classes = inspect.getmembers(sys.modules[__name__], is_minion_class)
        self.minions_dictionary = {}
        for minion_class in self.minion_classes:
            minion = minion_class[1]()
            self.minions_dictionary[minion.id] = minion_class[1]
            self.minions_dictionary[minion.gold_id] = minion_class[1]

    # Method to return a ghastcoiler minion using ID and parsed board parameters
    def get_ghastcoiler_minion(self, id, position, health, attack):
        minion = None
        if id in self.minions_dictionary:
            minion = self.minions_dictionary[id](position=position, defense=health, attack=attack) #TODO: other tags
        return minion

    def get_all_minions(self):
        """Returns a List of all implemented minions initialized to their base state

        Returns:
            Minion[] -- Collection of all defined minions
        """
        # TODO: Consider filtering out minion tribes that are not present in current game
        minions_instantiated = []
        for minion_class in self.minion_classes:
            minions_instantiated.append(minion_class[1]())
        return minions_instantiated
