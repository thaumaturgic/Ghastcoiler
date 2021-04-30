import logging
import sys, inspect

from utils.profile import Profile
from utils.minion_utils import MinionUtils
from utils.log_reader import LogReader

from game.game_instance import GameInstance
from game.simulation import Simulation
from game.player_board import PlayerBoard

from minions.base import Minion
from minions.rank_1 import DragonspawnLieutenant, FiendishServant, RedWhelp, Scallywag, MicroMummy, RockpoolHunter
from minions.rank_2 import YoHoOgre, TormentedRitualist, OldMurkEye, SouthseaCaptain, HarvestGolem, StewardofTime
from minions.rank_3 import InfestedWolf, MonstrousMacaw, DeflectoBot, WardenofOld, SouthseaStrongarm
from deathrattles.rank_3 import ReplicatingMenaceDeathrattle

# player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=12, rank=4, minions=[FiendishServant(), DragonspawnLieutenant(), DragonspawnLieutenant(), RedWhelp(), RedWhelp()])
# player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=12, rank=4, minions=[DragonspawnLieutenant(), FiendishServant(), DragonspawnLieutenant(), FiendishServant()])

LogReader.log_reader_test()

deflecto = DeflectoBot(attack=6, defense=3, deathrattles=[ReplicatingMenaceDeathrattle()])

board_0_minions = [deflecto, MicroMummy(), OldMurkEye(), WardenofOld(attack=4), RockpoolHunter(attack=4, defense=4), MicroMummy(), RockpoolHunter()]
board_1_minions = [Scallywag(attack=4, defense=3), SouthseaStrongarm(attack=6, defense=5), TormentedRitualist(), SouthseaCaptain(attack=6,defense=6), StewardofTime(), SouthseaCaptain(attack=4,defense=4), HarvestGolem()]

player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=12, rank=4, minions=board_0_minions)
player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=12, rank=4, minions=board_1_minions)

simulation = Simulation(player_board=player_board_0, opponent_board=player_board_1, max_simulations=1)

# logging.DEBUG will show all steps in combat
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

# var = MinionUtils.get_all_minions()
# print(len(var))
# for minion in var:
#     print(minion.name)

#testMinion = RedWhelp(reborn=True, attack=999, position=5)
#testMinion.trigger_reborn()

with Profile():
    print(simulation.simulate()) # List of tuples with outcome and the frequency of that outcome
