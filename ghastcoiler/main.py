import logging
import sys, inspect
from collections import Counter
from itertools import repeat
from multiprocessing import Pool
from time import sleep

from utils.profile import Profile
from utils.minion_utils import MinionUtils
from utils.log_reader import LogReader

from game.game_instance import GameInstance
from game.simulation import Simulation, Simulator
from game.player_board import PlayerBoard

from minions.base import Minion
from minions.rank_1 import DragonspawnLieutenant, FiendishServant, RedWhelp, Scallywag, MicroMummy, RockpoolHunter
from minions.rank_2 import YoHoOgre, TormentedRitualist, OldMurkEye, SouthseaCaptain, HarvestGolem, StewardofTime
from minions.rank_3 import InfestedWolf, MonstrousMacaw, DeflectoBot, WardenofOld, SouthseaStrongarm
from deathrattles.rank_3 import ReplicatingMenaceDeathrattle

def main():
    #---------------------
    utils = MinionUtils()
    test = utils.get_ghastcoiler_minion("TB_BaconUps_250", 1, 4, 3, True, True, True, True, True)
    test = utils.get_ghastcoiler_minion("BROKEN", 1, 4, 3, False, True, False, True, True)

    var = utils.get_all_minions()
    # print(len(var))
    # for minion in var:
    #     print(minion.name)

    #---------------------

    #"C:/Users/scott/Desktop/hearthstone_games/Power_game_5_turn15_end.log"
    #"C:\Program Files (x86)\Hearthstone\Logs\Power_old.log"
    #"C:/Users/scott/Desktop/hearthstone_games/Al'Akir_game_log.log"
    
    logPath = "C:/Users/scott/Desktop/hearthstone_games/Power_game_4_turn15_end.log"
    print("Reading Log: ", logPath)
    logreader = LogReader(logPath) 
    turns = 0

    while True:

        board_state = logreader.watch_log_file_for_combat_state()
        print()

        player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=40, rank=1, minions=board_state.friendlyBoard)
        player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=40, rank=1, minions=board_state.enemyBoard)

        print("Enemy board")
        for minion in player_board_1.minions:
            print(minion.id, minion.name, minion.attack, "/", minion.health)
        print("----------------")

        print("Friendly board")
        for minion in player_board_0.minions:
            print(minion.id, minion.name, minion.attack, "/", minion.health)
        print("----------------")

        # turns += 1
        # if turns == 9:
        #     print("break")

        try:
            games = 1000
            game_state = (player_board_0, player_board_1)

            pool = Pool()
            results = pool.map(Simulator.Simulate, repeat(game_state, games))
            pool.close()
            pool.join()

            counter = Counter(results)
            results = sorted(counter.items(), key=lambda x: x[0])

            wins, losses, ties = 0.0, 0.0, 0.0
            for result in results:
                if result[0] > 0:
                    wins += result[1]
                elif result[0] < 0:
                    losses += result[1]
                else:
                    ties += result[1]

            print("Win ", 100*wins/games, "Tie ", 100*ties/games, "Loss ", 100*losses/games)
        except Exception as e:
            print(e)

    #---------------------
    #TODO: Fix deathrattle + reborn interactions
    deflecto = DeflectoBot(attack=6, defense=3, deathrattles=[ReplicatingMenaceDeathrattle()])

    board_0_minions = [deflecto, MicroMummy(), OldMurkEye(), WardenofOld(attack=4), RockpoolHunter(attack=4, health=4), MicroMummy(), RockpoolHunter()]
    board_1_minions = [Scallywag(attack=4, health=3), SouthseaStrongarm(attack=6, health=5), TormentedRitualist(), SouthseaCaptain(attack=6,health=6), StewardofTime(), SouthseaCaptain(attack=4,health=4), HarvestGolem()]

    player_board_0 = PlayerBoard(player_id=0, hero=None, life_total=12, rank=4, minions=board_0_minions)
    player_board_1 = PlayerBoard(player_id=1, hero=None, life_total=12, rank=4, minions=board_1_minions)

    simulation = Simulation(player_board=player_board_0, opponent_board=player_board_1, max_simulations=1)

    # logging.DEBUG will show all steps in combat
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    with Profile():
        print(simulation.simulate()) # List of tuples with outcome and the frequency of that outcome

if __name__ == '__main__':
    main()