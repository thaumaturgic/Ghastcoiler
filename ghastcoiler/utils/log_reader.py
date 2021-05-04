from hslog.parser import LogParser, GameTag
from hslog.export import EntityTreeExporter
from hearthstone.entities import Zone, CardType
from threading import Thread, Condition
from time import sleep

class LogReader:
    GAME_STATE_STRING = "GameState"
    SHOP_STEP_STRING = "tag=STEP value=MAIN_ACTION"
    #MAIN_START_TRIGGERS
    #MAIN_READY
    #MAIN_END
    COMBAT_STEP_STRING = "tag=STEP value=MAIN_READY" # TODO: Fix bug with incorrect enemy board state parsing. ie why are there two state transitions for combat start    
    MAIN_END_STRING = "tag=STEP value=MAIN_END"
    MAIN_START_TRIGGERS_STRING = "tag=STEP value=MAIN_START_TRIGGERS"

    NEW_GAME_STRING = "CREATE_GAME"

    def __init__(self, log_path):
        self.boardAvailable = False
        self.friendlyBoard = []
        self.enemyBoard = []
        #TODO: friendlyHero, enemyHero parsing from log for hero powers
        self.parser = LogParser()
    
        boardStateLock = Condition()
        watch_file_thread = Thread(target=self.watch_file, args=(log_path, boardStateLock, ))
        watch_file_thread.start()

        parse_board_state_thread = Thread(target=self.parse_board_state, args=(boardStateLock, ))
        parse_board_state_thread.start()

    def parse_board_state(self, boardStateLock):
        while True:
            boardStateLock.acquire()
            boardStateLock.wait_for(self.board_available)

            # TODO: Parse mechanically interesting tags -> Like lich king thing too
            # Attack, Health, Taunt, Poisonous, Divine Shield, Windfury, Megawindfury, Reborn, Golden, Position, Deathrattles
            print("Friendly minions")
            self.print_board(self.friendlyBoard)
            print("Enemy minions")
            self.print_board(self.enemyBoard)
            # TODO: Emit/yield/callback/notify the converted board state back to ghastcoiler

            self.friendlyBoard = []
            self.enemyBoard = []
            self.boardAvailable = False
            boardStateLock.release()

    def watch_file(self, file, boardStateLock):

        while True:
            try:
                fp = open(file, 'r', encoding="utf-8")
                if fp:
                    break
            except:
                sleep(1)

        lineCount = 0
        turn = 1
        inShop = False
        boardPending = False

        while True:
            line = fp.readline()
        
            if not line:
                sleep(0.5)
                continue

            lineCount += 1
            if LogReader.GAME_STATE_STRING in line:
                if "tag=STEP value=" in line: # or "tag=NEXT_STEP value=" in line:
                    print(str(lineCount) + " " +line[:-1])

                if LogReader.COMBAT_STEP_STRING in line and inShop:
                    print("\n" + str(lineCount) + " *** COMBAT #" + str(turn) + ": " + line[:-1])
                    turn += 1
                    self.friendlyBoard, self.enemyBoard = self.get_all_minions_in_play(self.parser)
                    boardPending = True

                elif LogReader.MAIN_START_TRIGGERS_STRING in line and boardPending:
                    # Sometimes there is a "start triggers" step before the combat board state is fully known
                    self.friendlyBoard, self.enemyBoard = self.get_all_minions_in_play(self.parser)

                elif LogReader.MAIN_END_STRING in line and boardPending:
                    boardStateLock.acquire()
                    inShop = False
                    boardPending = False
                    self.boardAvailable = True
                    boardStateLock.notify()
                    boardStateLock.release()
                    sleep(1)

                elif LogReader.SHOP_STEP_STRING in line:
                    print("\n" + str(lineCount) + " *** SHOP   #" + str(turn) + ": " + line[:-1])
                    inShop = True
                elif LogReader.NEW_GAME_STRING in line:
                    print("\n*** new game ***")
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

    def board_available(self):
        return self.boardAvailable

    def print_board(self, board):
        print("----------------")
        for minion in board:
            print(minion.card_id, minion.tags[GameTag.ATK], "/", minion.tags[GameTag.HEALTH])
            # for tag in minion.tags:
            #     print(tag, minion.tags[tag])
            # print("")    
        print("----------------")