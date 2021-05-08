import logging
import sys, inspect
from threading import Thread, Event
from time import sleep

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

#---------------------
utils = MinionUtils()
test = utils.get_ghastcoiler_minion("BGS_106", 1, 4, 3)
test = utils.get_ghastcoiler_minion("BROKEN", 1, 4, 3)

var = utils.get_all_minions()
# print(len(var))
# for minion in var:
#     print(minion.name)

#---------------------
board_state_ready_event = Event()

#"C:/Users/scott/Desktop/hearthstone_games/Power_game_4_turn1.log"
#"C:\Program Files (x86)\Hearthstone\Logs\Power_old.log"
logPath = "C:\Program Files (x86)\Hearthstone\Logs\Power_old.log"
logreader = LogReader(logPath, board_state_ready_event) 

while True:
    board_state_ready_event.wait()
    print()
    
    player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=40, rank=1, minions=logreader.board_state.friendlyBoard)
    player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=40, rank=1, minions=logreader.board_state.enemyBoard)

    print("Friendly board")
    for minion in player_board_0.minions:
        print(minion.id, minion.name, minion.attack, "/", minion.defense)
    print("----------------")

    print("Enemy board")
    for minion in player_board_1.minions:
        print(minion.id, minion.name, minion.attack, "/", minion.defense)
    print("----------------")

    simulation = Simulation(player_board=player_board_0, opponent_board=player_board_1, max_simulations=10)

    print(simulation.simulate())

    board_state_ready_event.clear()
#---------------------

# player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=12, rank=4, minions=[FiendishServant(), DragonspawnLieutenant(), DragonspawnLieutenant(), RedWhelp(), RedWhelp()])
# player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=12, rank=4, minions=[DragonspawnLieutenant(), FiendishServant(), DragonspawnLieutenant(), FiendishServant()])

deflecto = DeflectoBot(attack=6, defense=3, deathrattles=[ReplicatingMenaceDeathrattle()])

board_0_minions = [deflecto, MicroMummy(), OldMurkEye(), WardenofOld(attack=4), RockpoolHunter(attack=4, defense=4), MicroMummy(), RockpoolHunter()]
board_1_minions = [Scallywag(attack=4, defense=3), SouthseaStrongarm(attack=6, defense=5), TormentedRitualist(), SouthseaCaptain(attack=6,defense=6), StewardofTime(), SouthseaCaptain(attack=4,defense=4), HarvestGolem()]

player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=12, rank=4, minions=board_0_minions)
player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=12, rank=4, minions=board_1_minions)

simulation = Simulation(player_board=player_board_0, opponent_board=player_board_1, max_simulations=1)

# logging.DEBUG will show all steps in combat
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

with Profile():
    print(simulation.simulate()) # List of tuples with outcome and the frequency of that outcome
