import logging
from collections import Counter
from itertools import repeat
from multiprocessing import Pool
import time

from utils.profile import Profile
from utils.log_reader import LogReader
from utils.regression_tester import run_regressions

from game.simulation import Simulator
from game.player_board import PlayerBoard

def main():
    logPath = "C:/Users/scott/Desktop/hearthstone_games/Recorded_games/Power_game_2.log"
    #logPath = "C:/Program Files (x86)/Hearthstone/Logs/Power_old.log"

    print("Reading Log: ", logPath)
    logreader = LogReader(logPath) 
    turns = 0

    while True:
        print("------------------------------------------------------------------------")
        board_state = logreader.watch_log_file_for_combat_state()

        if not board_state:
            print("\n*** Game Over ***")
            continue

        player_board_0 = PlayerBoard(player_id=0, hero=board_state.friendlyHero, life_total=board_state.friendlyPlayerHealth, rank=board_state.friendlyTechLevel, minions=board_state.friendlyBoard)
        player_board_1 = PlayerBoard(player_id=1, hero=board_state.enemyHero, life_total=board_state.enemyPlayerHealth, rank=board_state.enemyTechLevel, minions=board_state.enemyBoard)

        print("Enemy board")
        print(player_board_1)

        print("Friendly board")
        print(player_board_0)

        # turns += 1
        # if turns < 6:
        #     #print("")
        #     continue

        try:
            single_threaded = False
            games = 10_000
            game_state = (player_board_0, player_board_1)

            if single_threaded:
                results = []
                start = time.time()
                #with Profile():
                #logging.basicConfig(level=logging.DEBUG, format="%(message)s")
                for _ in range(games):
                    results.append(Simulator.Simulate(game_state))
            else:
                start = time.time()
                pool = Pool()
                results = pool.map(Simulator.Simulate, repeat(game_state, games))
                pool.close()
                pool.join()

            counter = Counter(results)
            results = sorted(counter.items(), key=lambda x: x[0])

            wins, losses, ties, enemy_lethal, friendly_lethal = 0.0, 0.0, 0.0, 0.0, 0.0
            for result in results:
                damage = result[0]
                game_count = result[1]

                if damage > 0:
                    wins += game_count
                    if damage > player_board_1.life_total:
                        enemy_lethal += game_count
                elif damage < 0:
                    losses += game_count
                    if (damage * -1) > player_board_0.life_total:
                        friendly_lethal += game_count
                else:
                    ties += game_count
            end = time.time()

            print("Win", 100*wins/games, "Tie", 100*ties/games, "Loss", 100*losses/games, "Elapsed:", end - start)
            print("We kill enemy:", 100 * enemy_lethal / games, "Enemy kills us:", 100 * friendly_lethal / games)
            print("------------------------------------------------------------------------\n")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    #turn_results = run_regressions("C:/Users/scott/Desktop/hearthstone_games/Recorded_games/")
    main()