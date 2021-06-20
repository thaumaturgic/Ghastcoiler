import logging
from collections import Counter
from itertools import repeat
from multiprocessing import Pool
import time
import csv
import glob
import os
from typing import List

from utils.profile import Profile
from utils.log_reader import BoardState, LogReader

from game.simulation import Simulator
from game.player_board import PlayerBoard

def read_game_results(csvPath):
    with open(csvPath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        turn_results = {}
        for index,row in enumerate(csvreader):
            results_float = []
            for result in row:
                results_float.append(float(result))
            turn_results[index] = results_float

        return turn_results


def simulate_game_from_log(logPath):
    logreader = LogReader(logPath) 
    turns = 0
    turn_results = {}

    while True:
        board_state = logreader.watch_log_file_for_combat_state()

        if not board_state:
            break

        player_board_0 = PlayerBoard(player_id=0, hero=board_state.friendlyHero, life_total=board_state.friendlyPlayerHealth, rank=board_state.friendlyTechLevel, minions=board_state.friendlyBoard)
        player_board_1 = PlayerBoard(player_id=1, hero=board_state.enemyHero, life_total=board_state.enemyPlayerHealth, rank=board_state.enemyTechLevel, minions=board_state.enemyBoard)

        try:
            single_threaded = False
            games = 10_000
            game_state = (player_board_0, player_board_1)

            if single_threaded:
                results = []
                #with Profile():
                #logging.basicConfig(level=logging.DEBUG, format="%(message)s")
                for _ in range(games):
                    results.append(Simulator.Simulate(game_state))
            else:
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

            turn_results[turns] = [100*enemy_lethal/games, 100*wins/games, 100*ties/games, 100*losses/games, 100*friendly_lethal/games]
        except Exception as e:
            print(e)
        turns += 1

    return turn_results

def compare_results(known_results: List, simulated_results: List):
    # Compare the results of the simulation with the known results file, flag differences of +/- 2%
    error_range = 2
    results_string = ""
    for i in range(len(known_results)):
        all_results_match = True
        for j in range(len(known_results[i])):
            # TODO: Skip lethal comparisions for now, just do win,tie,lose
            if j == 0 or j == 4:
                continue
            known_result = known_results[i][j]
            simulated_result = simulated_results[i][j]
            if not ((simulated_result > known_result - error_range) and (simulated_result < known_result + error_range)):
                all_results_match=False
                break
        results_string += "Y," if all_results_match else "N,"
    return results_string[:-1]

def run_regressions(logDirectoryPath):
    # Look for all .log files in the directory
    for file in os.listdir(logDirectoryPath):
        # For each log file, see if there is a csv file
        # TODO: Sort the log files to print results in game order
        if file.endswith(".log"):
            # If there is a csv file, read it for results
            log_path = logDirectoryPath + file
            csv_path = logDirectoryPath + file[:-3] + "csv"
            csv_exists = os.path.exists(csv_path)

            if csv_exists:
                known_results = read_game_results(csv_path)
                simulated_results = simulate_game_from_log(log_path)
                print(compare_results(known_results, simulated_results))
    pass