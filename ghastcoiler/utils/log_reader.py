from hslog.parser import LogParser, GameTag
from hslog.export import EntityTreeExporter
from hearthstone.entities import Zone, CardType
from threading import Thread
from time import sleep

class LogReader:
    GAME_STATE_STRING = "GameState"
    SHOP_STEP_STRING = "tag=STEP value=MAIN_ACTION"
    COMBAT_STEP_STRING = "tag=STEP value=MAIN_READY"

    def watch_file(file):
        fp = open(file, 'r')
        while True:
            new = fp.readline()
            if new:
                print(new)
            else:
                sleep(0.5)

    def get_all_minions_in_play(game):
        minions = []
        for e in game.entities:
                if e.type == CardType.MINION and e.zone == Zone.PLAY:
                    minions.append(e)
        return minions

    @classmethod
    def log_reader_test(self):
        thread = Thread(target=self.watch_file, args=("C:/Users/scott/Desktop/test.txt", ))
        thread.start()

        parser = LogParser()

        # TODO: HANDLE UTF8 characters in player names? 
        # TODO: Parse mechanically interesting tags -> Like lich king thing too
        # Attack, Health, Taunt, Poisonous, Divine Shield, Windfury, Megawindfury, Reborn, Golden, Position, Deathrattles
        with open("C:/Users/scott/Desktop/hearthstone_games/Power_game_4_turn2.log", encoding="utf-8") as f:
            lineCount = 0
            inShop = False
            friendlyBoard = []
            enemyBoard = []

            for line in f:
                lineCount += 1
                if LogReader.GAME_STATE_STRING in line:
                    if LogReader.COMBAT_STEP_STRING in line and inShop:
                        print("LINE #: " + str(lineCount) + " " + line)
                        packet_tree = parser.games[len(parser.games)-1] # TODO: Make parser work for multiple games
                        exporter = EntityTreeExporter(packet_tree)
                        export = exporter.export()
                        minionsInCombat = self.get_all_minions_in_play(export.game)
                        for minion in minionsInCombat:
                            if minion.controller.is_ai:
                                enemyBoard.append(minion)
                            else:
                                friendlyBoard.append(minion)
                        inShop = False
                        break
                    elif LogReader.SHOP_STEP_STRING in line:
                        inShop = True

                parser.read_line(line)

        print("Friendly minions")
        for minion in friendlyBoard:
            print(minion.card_id, minion.tags[GameTag.ATK], "/", minion.tags[GameTag.HEALTH])
            # for tag in minion.tags:
            #     print(tag, minion.tags[tag])
            # print("")    
        print("----------------")

        print("Enemy minions")
        for minion in enemyBoard:
            print(minion.card_id, minion.tags[GameTag.ATK], "/", minion.tags[GameTag.HEALTH])
            # for tag in minion.tags:
            #     print(tag, minion.tags[tag])
            # print("")    
        print("----------------")
        
        # TODO: Is there a better way to automate generation of minions from HeartstongJSON import or filreplace CardXML?? 