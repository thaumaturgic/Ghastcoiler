import sys
import inspect

# We explicitly want to import all Minion classes
from minions.base import *  # noqa: F403
from minions.tokens import * # noqa: F403
from minions.rank_1 import *  # noqa: F403
from minions.rank_2 import *  # noqa: F403
from minions.rank_3 import *  # noqa: F403
from minions.rank_4 import *  # noqa: F403
from minions.rank_5 import *  # noqa: F403
from minions.rank_6 import *  # noqa: F403

from deathrattles.rank_3 import ReplicatingMenaceDeathrattle
from deathrattles.rank_6 import LivingSporesDeathrattle

def is_minion_class(class_object):
        return inspect.isclass(class_object) and issubclass(class_object, Minion) and (class_object is not Minion)

# Build list of all the declared minion class types
minion_classes = inspect.getmembers(sys.modules[__name__], is_minion_class)
minions_dictionary = {}
minions_instantiated = []
for minion_class in minion_classes:
    minion = minion_class[1]()
    minions_instantiated.append(minion)
    minions_dictionary[minion.id] = minion_class[1]
    minions_dictionary[minion.gold_id] = minion_class[1]
    
def get_minions(criteria = None):
    """Returns a List of minion classes that meet the given criteria, or all minions if no criteria is given

    Returns:
        Minion[] -- List of minion classes that match the given criteria
    """
    if not criteria:
        return minion_classes

    minions = []
    for minion in minions_instantiated:
        if criteria(minion):
            minions.append(minion.__class__)
    return minions

# Method to return a ghastcoiler minion using ID and parsed board parameters
def get_ghastcoiler_minion(id, position, health, attack, reborn, windfury, mega_windfury, taunt, divine_shield, poisonous, golden):
    minion = None
    if id in minions_dictionary:
        minion = minions_dictionary[id](position=position, 
        health=health, 
        attack=attack, 
        reborn=reborn,
        windfury=windfury,
        mega_windfury=mega_windfury,
        taunt=taunt,
        divine_shield=divine_shield,
        poisonous=poisonous,
        golden=golden)
    return minion

def get_ghastcoiler_deathrattles(entity_ids):
    deathrattles = []
    for entity in entity_ids:
        if entity == "BOT_312e":
            deathrattles.append(ReplicatingMenaceDeathrattle())
        elif entity == "TB_BaconUps_032e":
            deathrattles.append(ReplicatingMenaceDeathrattle(golden=True)) # TODO: Test this import
        elif entity == "UNG_999t2e":
            deathrattles.append(LivingSporesDeathrattle())
    return deathrattles
