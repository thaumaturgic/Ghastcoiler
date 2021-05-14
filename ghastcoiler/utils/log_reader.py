from hslog.parser import LogParser, GameTag
from hslog.export import EntityTreeExporter
from hearthstone.entities import Zone, CardType
from threading import Thread, Condition
from time import sleep
from dataclasses import dataclass
from utils.minion_utils import MinionUtils

@dataclass
class BoardState:
    friendlyBoard: [] = None
    #friendlyPlayerHealth
    #friendlyHero
    #friendlyTier
    enemyBoard: [] = None
    #enemyHero
    #enemyPlayerHealth
    #enemyTier
    #allowedMinions: []

class LogReader:
    GAME_STATE_STRING = "GameState"
    STEP_STRING = "tag=STEP value="

    SHOP_STEP_STRING = "tag=STEP value=MAIN_ACTION"
    COMBAT_STEP_STRING = "tag=STEP value=MAIN_READY"
    MAIN_START_TRIGGERS_STRING = "tag=STEP value=MAIN_START_TRIGGERS"
    MAIN_END_STRING = "tag=STEP value=MAIN_END"
    
    NEW_GAME_STRING = "CREATE_GAME"
    GAME_END_STRING = "tag=STEP value=FINAL_WRAPUP"

    LICH_KING_REBORN = "TB_BaconShop_HP_024e2"

    def __init__(self, log_path, board_state_ready_event):
        self.parser = LogParser()
        self.board_state_ready_event = board_state_ready_event
        self.minion_utils = MinionUtils()

        self.ghastcoiler_board_state = BoardState()
        self.entity_board_state = BoardState()
        
        watch_file_thread = Thread(target=self.watch_file, args=(log_path, ))
        watch_file_thread.start()

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

                # if LogReader.STEP_STRING in line:
                #     print(str(lineCount) + " " + line[:-1])

                if LogReader.COMBAT_STEP_STRING in line and inShop:
                    print("\n" + str(lineCount) + " *** COMBAT #" + str(turn) + ": " + line[:-1])
                    turn += 1
                    self.entity_board_state = self.scrape_board_state(self.parser)
                    boardPending = True
                elif LogReader.MAIN_START_TRIGGERS_STRING in line and boardPending:
                    # Sometimes there is a "start triggers" step that contains the correct combat board state
                    self.entity_board_state = self.scrape_board_state(self.parser)
                elif LogReader.MAIN_END_STRING in line and boardPending:
                    inShop = False
                    boardPending = False
                    self.convert_board_state(self.entity_board_state)
                    sleep(2) # artificially slow down historical log parsing for debug
                elif LogReader.SHOP_STEP_STRING in line:
                    print("\n" + str(lineCount) + " *** SHOP   #" + str(turn) + ": " + line[:-1])
                    inShop = True
                elif LogReader.NEW_GAME_STRING in line:
                    print("\n*** New Game ***")
                    turn = 1
                elif LogReader.GAME_END_STRING in line:
                    print("\n*** Game Over ***")

            self.parser.read_line(line)

    def scrape_board_state(self, parser):
        packet_tree = parser.games[len(parser.games)-1]
        exporter = EntityTreeExporter(packet_tree)
        export = exporter.export()

        minions = []
        enchantments = []
        #entities = []

        for e in export.game.entities:
            #entities.append(e)

            if e.type == CardType.ENCHANTMENT:
                enchantments.append(e)
            elif e.type == CardType.MINION and e.zone == Zone.PLAY:
                minions.append(e)
                    
        self.apply_enchantments(enchantments, minions)
    
        friendlyMinions = []
        enemyMinions = []

        for minion in minions:
            enemyMinions.append(minion) if minion.controller.is_ai else friendlyMinions.append(minion)

        friendlyMinions.sort(key=lambda minion: minion.tags[GameTag.ZONE_POSITION])
        enemyMinions.sort(key=lambda minion: minion.tags[GameTag.ZONE_POSITION])
        
        state = BoardState(friendlyBoard=friendlyMinions, enemyBoard=enemyMinions)
        return state

    #TODO: Find deathrattles, modular stuff like annoy o module
    #TODO: Parse mechanically interesting tags -> Like al akir shield
    # Microbot death rattle = "BOT_312e" 
    # Annoy o module = 
    # Living Spores = UNG_999t2
    def apply_enchantments(self, enchantments, minions):
        for enchantment in enchantments:
            if GameTag.ATTACHED in enchantment.tags:
                attached_entity_id = enchantment.tags[GameTag.ATTACHED]
                for minion in minions:
                    if minion.id == attached_entity_id:
                        # DEBUG: Collect all the parsed enchantments for a given minion entity for inspection
                        if hasattr(minion, 'enchantments'):
                            minion.enchantments.append(enchantment)
                        else:
                            minion.enchantments = [enchantment]
                        if enchantment.card_id == LogReader.LICH_KING_REBORN:
                            minion.tags[GameTag.REBORN] = 1
                        #elif enchantment.card_id == BLAH

    def convert_to_ghastcoiler_minion(self, board):
        ghastcoiler_board = []
        for minion in board:
            # Card ID, Position, Attack, Health, 
            # Taunt, Poisonous, Divine Shield, Windfury, Megawindfury, Reborn, Golden, Deathrattles 

            if GameTag.WINDFURY in minion.tags:
                windfury = True if minion.tags[GameTag.WINDFURY] == 1 else False
                mega_windfury = True if minion.tags[GameTag.WINDFURY] == 3 else False
                
            ghastcoiler_minion = self.minion_utils.get_ghastcoiler_minion(
                minion.card_id, 
                minion.tags[GameTag.ZONE_POSITION], 
                minion.tags[GameTag.HEALTH], 
                minion.tags[GameTag.ATK],
                True if GameTag.REBORN in minion.tags else False,
                #windfury,
                #megawindfury,
                True if GameTag.TAUNT in minion.tags else False,
                True if GameTag.DIVINE_SHIELD in minion.tags else False,
                True if GameTag.POISONOUS in minion.tags else False,
                True if GameTag.PREMIUM in minion.tags else False  #Golden
                )
            if ghastcoiler_minion:
                ghastcoiler_board.append(ghastcoiler_minion)
        return ghastcoiler_board

    # Convert from entities to ghastcoiler, set the board notification event
    def convert_board_state(self, entity_board_state):
        print("Enemy minions")
        self.print_board(entity_board_state.enemyBoard)
        
        print("Friendly minions")
        self.print_board(entity_board_state.friendlyBoard)

        # Convert the entity tags to ghastcoiler minions before passing back
        ghastcoiler_friendly_board = self.convert_to_ghastcoiler_minion(entity_board_state.friendlyBoard)
        ghastcoiler_enemy_board =  self.convert_to_ghastcoiler_minion(entity_board_state.enemyBoard)

        self.ghastcoiler_board_state = BoardState(ghastcoiler_friendly_board, ghastcoiler_enemy_board)
        self.board_state_ready_event.set()

    def print_board(self, board):
        for minion in board:
            print(minion.card_id, minion.tags[GameTag.ATK], "/", minion.tags[GameTag.HEALTH])
            # for tag in minion.tags:
            #     print(tag, minion.tags[tag])
            # print("")    
        print("----------------")