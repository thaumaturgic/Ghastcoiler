from game.player_board import PlayerBoard
from heroes.hero_types import HeroType
from minions.rank_2 import HarvestGolem
from minions.test_minions import PunchingBag


def test_deathwing(initialized_game):
    initialized_game.player_board[0] = PlayerBoard(0,HeroType.DEATHWING,1,1,[HarvestGolem()])
    initialized_game.player_board[1] = PlayerBoard(0,None,1,1,[PunchingBag(attack=10)],enemy_is_deathwing=True)

    initialized_game.start_of_game()
    initialized_game.single_round()
    assert initialized_game.player_board[0].minions[0].attack == 4

    initialized_game.player_board[0] = PlayerBoard(0,HeroType.DEATHWING,1,1,[HarvestGolem()],enemy_is_deathwing=True)
    initialized_game.player_board[1] = PlayerBoard(0,HeroType.DEATHWING,1,1,[PunchingBag(attack=10)],enemy_is_deathwing=True)
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert initialized_game.player_board[0].minions[0].attack == 6


def test_greybough(initialized_game):
    initialized_game.player_board[0] = PlayerBoard(0,HeroType.GREYBOUGH,1,1,[HarvestGolem()])
    initialized_game.player_board[1] = PlayerBoard(0,None,1,1,[PunchingBag(attack=10)])

    initialized_game.start_of_game()
    initialized_game.single_round()
    golem_token = initialized_game.player_board[0].minions[0]

    assert golem_token.attack == 3
    assert golem_token.health == 3
    assert golem_token.taunt
