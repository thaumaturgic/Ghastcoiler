from typing import Optional
from game.player_board import PlayerBoard
from minions.base import Minion
from minions.types import MinionType
from minions.tokens import Voidwalker
from deathrattles.base import Deathrattle


class KingBagurgleDeathrattle(Deathrattle):
    "Give your other Murlocs +2/+2."
    def __init__(self):
        super().__init__(name="KingBagurgleDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for other_minion in own_board.minions:
            if MinionType.Murloc in other_minion.types and other_minion != minion:
                stats = 4 if minion.golden else 2
                other_minion.add_stats(stats,stats)


class SneedsOldShredderDeathrattle(Deathrattle):
    "Summon a random Legendary minion."
    def __init__(self):
        super().__init__(name="SneedsOldShredderDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        # TODO: Filter minions from tribes not in the game
        not_allowed_minions = ["Sneed's Old Shredder"]
        isSpawnable = lambda x: (x.legendary) and \
                            (x.name not in not_allowed_minions) and \
                            (x.rank <= own_board.rank)
        
        minions_to_summon = 2 if minion.golden else 1
        Deathrattle.spawn_random_minions(minion, own_board, minions_to_summon, isSpawnable, macaw_trigger)
        

class VoidlordDeathrattle(Deathrattle):
    "Summon three 1/3 Demons with Taunt."
    def __init__(self):
        super().__init__(name="VoidlordDeathrattle")

    def trigger(self, minion: Minion, own_board: PlayerBoard, opposing_board: PlayerBoard, macaw_trigger: Optional[bool] = False):
        for _ in range(3):
            own_board.add_minion(Voidwalker(golden=minion.golden, attacked=minion.attacked), position=minion.position, to_right=macaw_trigger)