import sys, inspect

from minions.base import *
from minions.rank_1 import *
from minions.rank_2 import *
from minions.rank_3 import *
from minions.rank_4 import *
#from minions.rank_5 import *
#from minions.rank_6 import *

def is_minion_class(class_object):
    return inspect.isclass(class_object) and issubclass(class_object, Minion) and (class_object is not Minion)

def get_all_minions():
    """Returns a List of all implemented minions initialized to their base state

    Returns:
        Minion[] -- Collection of all defined minions
    """
    #TODO: Consider filtering out minion tribes that are not present in current game
    minion_classes = inspect.getmembers(sys.modules[__name__], is_minion_class)
    minions_instantiated = []
    for minion_class in minion_classes:
        minions_instantiated.append(minion_class[1]())
    return minions_instantiated
