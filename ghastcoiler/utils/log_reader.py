from hslog.parser import LogParser, GameTag
from hslog.export import EntityTreeExporter
from hearthstone.entities import Zone, CardType
from threading import Thread, Condition
from time import sleep
from dataclasses import dataclass
from utils.minion_utils import MinionUtils

@dataclass
class BoardState:
    friendlyBoard: []
    #friendlyPlayerHealth
    #friendlyHero
    enemyBoard: []
    #enemyHero
    #enemyPlayerHealth
    #allowedMinions: []

class LogReader:
    GAME_STATE_STRING = "GameState"
    STEP_STRING = "tag=STEP value="

    SHOP_STEP_STRING = "tag=STEP value=MAIN_ACTION"
    COMBAT_STEP_STRING = "tag=STEP value=MAIN_READY"
    MAIN_START_TRIGGERS_STRING = "tag=STEP value=MAIN_START_TRIGGERS"
    MAIN_END_STRING = "tag=STEP value=MAIN_END"
    
    NEW_GAME_STRING = "CREATE_GAME"

    def __init__(self, log_path, board_state_ready_event):
        self.friendlyBoard = []
        self.enemyBoard = []
        self.parser = LogParser()
        self.board_state_ready_event = board_state_ready_event
        self.board_state = BoardState(None,None)
        self.minion_utils = MinionUtils()
    
        watch_file_thread = Thread(target=self.watch_file, args=(log_path, ))
        watch_file_thread.start()

    def convert_to_ghastcoiler(self, board):
        ghastcoiler_board = []
        for minion in board:
            ghastcoiler_minion = self.minion_utils.get_ghastcoiler_minion(
                minion.card_id, 
                minion.tags[GameTag.ZONE_POSITION], 
                minion.tags[GameTag.HEALTH], 
                minion.tags[GameTag.ATK])
            if ghastcoiler_minion:
                ghastcoiler_board.append(ghastcoiler_minion)
        return ghastcoiler_board

    def parse_board_state(self, friendlyBoard, enemyBoard):
        # TODO: Parse mechanically interesting tags -> Like lich king thing too, al akir shield
        # Card ID, Position, Attack, Health, Taunt, Poisonous, Divine Shield, Windfury, Megawindfury, Reborn, Golden, Deathrattles
        print("Friendly minions")
        self.print_board(friendlyBoard)
        print("Enemy minions")
        self.print_board(enemyBoard)

        # Convert the entity tags to ghastcoiler minions before passing back
        ghastcoiler_friendly_board = self.convert_to_ghastcoiler(friendlyBoard)
        ghastcoiler_enemy_board =  self.convert_to_ghastcoiler(enemyBoard)

        self.board_state = BoardState(ghastcoiler_friendly_board, ghastcoiler_enemy_board)
        self.board_state_ready_event.set()

    def watch_file(self, file):
        while True:
            try:
                logfile = open(file, 'r', encoding="utf-8")
                if logfile:
                    break
            except:
                sleep(1)

        lineCount = 0
        turn = 1
        inShop = False
        boardPending = False

        while True:
            line = logfile.readline()
        
            if not line:
                sleep(0.5)
                continue

            lineCount += 1
            if LogReader.GAME_STATE_STRING in line:
                # Log all step changes
                if LogReader.STEP_STRING in line:
                    print(str(lineCount) + " " + line[:-1])

                if LogReader.COMBAT_STEP_STRING in line and inShop:
                    print("\n" + str(lineCount) + " *** COMBAT #" + str(turn) + ": " + line[:-1])
                    turn += 1
                    self.friendlyBoard, self.enemyBoard = self.get_all_minions_in_play(self.parser)
                    boardPending = True
                elif LogReader.MAIN_START_TRIGGERS_STRING in line and boardPending:
                    # Sometimes there is a "start triggers" step that contains the correct combat board state
                    self.friendlyBoard, self.enemyBoard = self.get_all_minions_in_play(self.parser)
                elif LogReader.MAIN_END_STRING in line and boardPending:
                    inShop = False
                    boardPending = False
                    self.parse_board_state(self.friendlyBoard, self.enemyBoard)
                    sleep(1) # artificially slow down historical log parsing for debug
                    
                elif LogReader.SHOP_STEP_STRING in line:
                    print("\n" + str(lineCount) + " *** SHOP   #" + str(turn) + ": " + line[:-1])
                    inShop = True
                elif LogReader.NEW_GAME_STRING in line:
                    print("\n*** New Game ***")
                    turn = 1

            self.parser.read_line(line)


    def get_all_minions_in_play(self, parser):
        packet_tree = parser.games[len(parser.games)-1]
        exporter = EntityTreeExporter(packet_tree)
        export = exporter.export()

        friendlyMinions = []
        enemyMinions = []
        for e in export.game.entities:
                if e.type == CardType.MINION and e.zone == Zone.PLAY:
                    enemyMinions.append(e) if e.controller.is_ai else friendlyMinions.append(e)
        friendlyMinions.sort(key=lambda minion: minion.tags[GameTag.ZONE_POSITION])
        enemyMinions.sort(key=lambda minion: minion.tags[GameTag.ZONE_POSITION])
        return friendlyMinions, enemyMinions

    def print_board(self, board):
        print("----------------")
        for minion in board:
            print(minion.card_id, minion.tags[GameTag.ATK], "/", minion.tags[GameTag.HEALTH])
            # for tag in minion.tags:
            #     print(tag, minion.tags[tag])
            # print("")    
        print("----------------")