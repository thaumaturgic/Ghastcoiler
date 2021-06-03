import logging
from collections import Counter
from itertools import repeat
from multiprocessing import Pool
import time

from utils.profile import Profile
from utils.minion_utils import MinionUtils
from utils.log_reader import LogReader

from game.game_instance import GameInstance
from game.simulation import Simulation, Simulator
from game.player_board import PlayerBoard

def main():
    #---------------------
    utils = MinionUtils()
    test = utils.get_ghastcoiler_minion("TB_BaconUps_250", 1, 4, 3, True, True, False, False, True, True, True)
    test = utils.get_ghastcoiler_minion("BROKEN", 1, 4, 3, False, True, False, False, False, True, True)

    var = sorted(utils.get_minions(), key = lambda x: x.rank)
    # print(len(var))
    # for minion in var:
    #     print(minion.name)

    #---------------------

    #"C:/Users/scott/Desktop/hearthstone_games/Power_game_5_turn15_end.log"
    #"C:\Program Files (x86)\Hearthstone\Logs\Power_old.log"
    #"C:/Users/scott/Desktop/hearthstone_games/Al'Akir_game_log.log"
    #"C:/Users/scott/Desktop/hearthstone_games/Recorded_games/Power_game_3.log"
    
    logPath = "C:\Program Files (x86)\Hearthstone\Logs\Power_old.log"
    print("Reading Log: ", logPath)
    logreader = LogReader(logPath) 
    turns = 0

    while True:
        print("------------------------------------------------")
        board_state = logreader.watch_log_file_for_combat_state()

        player_board_0 = PlayerBoard(player_id=0, hero=board_state.friendlyHero, life_total=board_state.friendlyPlayerHealth, rank=board_state.friendlyTechLevel, minions=board_state.friendlyBoard)
        player_board_1 = PlayerBoard(player_id=1, hero=board_state.enemyHero, life_total=board_state.enemyPlayerHealth, rank=board_state.enemyTechLevel, minions=board_state.enemyBoard)

        print("Enemy board")
        print(player_board_1)

        print("Friendly board")
        print(player_board_0)

        # turns += 1
        # if turns == 6:
        #     print("")

        try:
            games = 100
            game_state = (player_board_0, player_board_1)

            # Single process
            # results = []
            # start = time.time()
            # #with Profile():
            # for _ in range(games):
            #     results.append(Simulator.Simulate(game_state))

            # Parallel processes
            start = time.time()
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
            end = time.time()

            print("Win ", 100*wins/games, "Tie ", 100*ties/games, "Loss ", 100*losses/games, "Elapsed: ", end - start)
            nop = True
            print("------------------------------------------------\n")
        except Exception as e:
            print(e)

    #---------------------
    # logging.DEBUG will show all steps in combat
    # logging.basicConfig(level=logging.DEBUG, format="%(message)s")

    # with Profile():
    #    print(simulation.simulate()) # List of tuples with outcome and the frequency of that outcome

if __name__ == '__main__':
    main()