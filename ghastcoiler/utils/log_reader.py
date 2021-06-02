from hslog.parser import LogParser, GameTag
from hslog.export import EntityTreeExporter
from hearthstone.entities import Zone, CardType
from time import sleep
from dataclasses import dataclass
from utils.minion_utils import MinionUtils
from heroes.hero_types import HeroType

@dataclass
class BoardState:
    friendlyBoard: [] = None
    friendlyPlayerHealth: int = None
    friendlyHero: HeroType = None
    friendlyTechLevel: int = None
    enemyBoard: [] = None
    enemyHero: HeroType = None
    enemyPlayerHealth: int = None
    enemyTechLevel: int = None
    #allowedMinionTypes: []

class LogReader:
    GAME_STATE_STRING = "GameState"
    STEP_STRING = "tag=STEP value="

    SHOP_STEP_STRING = "tag=STEP value=MAIN_ACTION"
    COMBAT_STEP_STRING = "tag=STEP value=MAIN_READY"
    MAIN_START_TRIGGERS_STRING = "tag=STEP value=MAIN_START_TRIGGERS"
    MAIN_END_STRING = "tag=STEP value=MAIN_END"
    
    # Game start/end tags
    NEW_GAME_STRING = "CREATE_GAME"
    GAME_END_STRING = "tag=STEP value=FINAL_WRAPUP"

    # Hero power related entity IDs
    LICH_KING_REBORN = "TB_BaconShop_HP_024e2"
    ALAKIR = "TB_BaconShop_HP_086"

    # Death rattle entity ids
    REPLICATING_MENACE_DEATHRATTLE = "BOT_312e"
    REPLICATING_MENACE_GOLDEN_DEATHRATTLE = "TB_BaconUps_032e"
    LIVING_SPORES = "UNG_999t2e"

    def __init__(self, log_path):
        self.parser = LogParser()
        self.minion_utils = MinionUtils()

        self.entity_board_state = BoardState()
        
        self.lineCount = 0
        self.turn = 1
        self.inShop = False
        self.boardPending = False

        while True:
            try:
                self.logfile = open(log_path, 'r', encoding="utf-8")
                if self.logfile:
                    break
            except:
                sleep(1)

    def watch_log_file_for_combat_state(self):
        while True:
            line = self.logfile.readline()
        
            if not line:
                sleep(0.5)
                continue

            self.lineCount += 1
            if LogReader.GAME_STATE_STRING in line:

                # Debug: Print every step change
                # if LogReader.STEP_STRING in line:
                #     print(str(lineCount) + " " + line[:-1])

                if LogReader.COMBAT_STEP_STRING in line and self.inShop:
                    print("\n" + str(self.lineCount) + " *** COMBAT #" + str(self.turn))
                    self.turn += 1
                    self.entity_board_state = self.scrape_board_state(self.parser)
                    self.boardPending = True
                elif LogReader.MAIN_START_TRIGGERS_STRING in line and self.boardPending:
                    # Sometimes there is a "start triggers" step that contains the correct combat board state
                    self.entity_board_state = self.scrape_board_state(self.parser)
                elif LogReader.MAIN_END_STRING in line and self.boardPending:
                    self.inShop = False
                    self.boardPending = False
                    return self.convert_board_state(self.entity_board_state)
                elif LogReader.SHOP_STEP_STRING in line:
                    print("\n" + str(self.lineCount) + " *** SHOP   #" + str(self.turn))
                    #TODO: Scrape shop for visible minion types
                    self.inShop = True
                elif LogReader.NEW_GAME_STRING in line:
                    print("\n*** New Game ***")
                    self.turn = 1
                elif LogReader.GAME_END_STRING in line:
                    print("\n*** Game Over ***")

            self.parser.read_line(line)

    def get_hero_tags(self, tags):
        health = tech_level = None
        if GameTag.HEALTH in tags:
            health = tags[GameTag.HEALTH]
        if GameTag.DAMAGE in tags:
            health -= tags[GameTag.DAMAGE]
        if GameTag.PLAYER_TECH_LEVEL in tags:
            tech_level = tags[GameTag.PLAYER_TECH_LEVEL]
        return (health, tech_level)

    def scrape_board_state(self, parser):
        packet_tree = parser.games[len(parser.games)-1]
        exporter = EntityTreeExporter(packet_tree)
        export = exporter.export()

        minions = []
        enchantments = []
        hero_powers = []
        entities = {} # For Debug inspection
        friendly_player = friendly_hero = None
        enemy_player = enemy_hero = None

        for e in export.game.entities:
            entities[e.id] = e

            if e.type == CardType.ENCHANTMENT:
                enchantments.append(e)

            if e.zone == Zone.PLAY:    
                if e.type == CardType.HERO_POWER:
                    hero_powers.append(e)
                elif e.type == CardType.MINION:
                    minions.append(e)
                elif e.type == CardType.PLAYER:
                    if e.is_ai:
                        enemy_player = e
                    else:
                        friendly_player = e
                elif e.type == CardType.HERO:
                    if e.controller == enemy_player:
                        enemy_hero = e
                    elif e.controller == friendly_player:
                        friendly_hero = e
        
        friendlyMinions = []
        enemyMinions = []

        for minion in minions:
            # Create list to hold deathrattle entity ids to convert to ghastcoiler ones
            minion.deathrattle_ids = []
            if GameTag.ATK not in minion.tags:
                # Minions with 0 power dont have an ATK tag. Make sure it exists here
                minion.tags[GameTag.ATK] = 0 
            enemyMinions.append(minion) if minion.controller.is_ai else friendlyMinions.append(minion)

        self.attach_enchantments(enchantments, minions)

        friendlyMinions.sort(key=lambda minion: minion.tags[GameTag.ZONE_POSITION])
        enemyMinions.sort(key=lambda minion: minion.tags[GameTag.ZONE_POSITION])

        friendly_health, friendly_tech_level = self.get_hero_tags(friendly_hero.tags)
        enemy_health, enemy_tech_level = self.get_hero_tags(enemy_hero.tags)
        
        state = BoardState(friendlyBoard=friendlyMinions, friendlyPlayerHealth=friendly_health, friendlyTechLevel=friendly_tech_level,
                            enemyBoard=enemyMinions, enemyPlayerHealth=enemy_health, enemyTechLevel=enemy_tech_level)
        self.apply_hero_powers(state, hero_powers)

        return state

    #TODO: Parse mechanically interesting enchantments -> Like al akir shield
    def attach_enchantments(self, enchantments, minions):
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

                        #TODO: Verify that multiple modular deathrattles are distinct entities
                        #TODO: Refactor this once all deathrattle enchantments are identified
                        elif enchantment.card_id == self.REPLICATING_MENACE_DEATHRATTLE:
                            minion.deathrattle_ids.append(self.REPLICATING_MENACE_DEATHRATTLE)
                        elif enchantment.card_id == self.REPLICATING_MENACE_GOLDEN_DEATHRATTLE:
                            minion.deathrattle_ids.append(self.REPLICATING_MENACE_GOLDEN_DEATHRATTLE)
                        elif enchantment.card_id == self.LIVING_SPORES:
                            minion.deathrattle_ids.append(self.LIVING_SPORES)

    
    def apply_hero_powers(self, state: BoardState, hero_powers):
        for hero_power in hero_powers:
            if hero_power.card_id == LogReader.ALAKIR:
                # Find which player is al akir
                # Find the first minion in their board and give it windfury, taunt, divine shield
                print(hero_power) #TODO
        
    def convert_to_ghastcoiler_minion(self, board):
        ghastcoiler_board = []
        for minion in board:
            windfury = mega_windfury = False
            if GameTag.WINDFURY in minion.tags:
                windfury = True if minion.tags[GameTag.WINDFURY] == 1 else False
                mega_windfury = True if minion.tags[GameTag.WINDFURY] == 3 else False

            ghastcoiler_minion = self.minion_utils.get_ghastcoiler_minion(
                minion.card_id, 
                minion.tags[GameTag.ZONE_POSITION], 
                minion.tags[GameTag.HEALTH], 
                minion.tags[GameTag.ATK],
                True if GameTag.REBORN in minion.tags else False,
                windfury,
                mega_windfury,
                True if GameTag.TAUNT in minion.tags else False,
                True if GameTag.DIVINE_SHIELD in minion.tags else False,
                True if GameTag.POISONOUS in minion.tags else False,
                True if GameTag.PREMIUM in minion.tags and minion.tags[GameTag.PREMIUM] else False)
            if ghastcoiler_minion:
                ghastcoiler_minion.deathrattles += self.minion_utils.get_ghastcoiler_deathrattles(minion.deathrattle_ids)
                ghastcoiler_board.append(ghastcoiler_minion)
        return ghastcoiler_board

    # Convert from entities to ghastcoiler
    def convert_board_state(self, entity_board_state):
        # print("Enemy minions")
        # self.print_board(entity_board_state.enemyBoard)
        
        # print("Friendly minions")
        # self.print_board(entity_board_state.friendlyBoard)

        # Convert the entity tags to ghastcoiler minions before passing back
        ghastcoiler_friendly_board = self.convert_to_ghastcoiler_minion(entity_board_state.friendlyBoard)
        ghastcoiler_enemy_board =  self.convert_to_ghastcoiler_minion(entity_board_state.enemyBoard)

        entity_board_state.friendlyBoard = ghastcoiler_friendly_board
        entity_board_state.enemyBoard = ghastcoiler_enemy_board

        return entity_board_state

    def print_board(self, board):
        for minion in board:
            print(minion.card_id, minion.tags[GameTag.ATK], "/", minion.tags[GameTag.HEALTH])
            # for tag in minion.tags:
            #     print(tag, minion.tags[tag])
            # print("")    
        print("----------------")