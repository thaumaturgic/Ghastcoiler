from minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import KindlyGrandmother
from ghastcoiler.minions.rank_5 import BaronRivendare, BristlebackKnight, \
    IronhideDirehorn, KingBagurgle, MalGanis, MamaBear, \
    SeabreakerGoliath, SneedsOldShredder, Voidlord


def test_baronrivendar(initialized_game):
    attacker_board = initialized_game.player_board[0]

    baron = BaronRivendare()
    attacker_board.set_minions([baron])
    # TODO: Implement
    assert True


def test_bristleback_knight(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]
    defender_board.set_minions([PunchingBag(attack=1)])

    bristlebackKnight = BristlebackKnight()
    attacker_board.set_minions([bristlebackKnight])

    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert bristlebackKnight.divine_shield == True
    initialized_game.single_round()
    assert bristlebackKnight.divine_shield == False


def test_ironhide_direhorn(initialized_game):
    attacker_board = initialized_game.player_board[0]

    direhorn = IronhideDirehorn()
    attacker_board.set_minions([direhorn])
    # TODO: Implement
    assert True


def test_king_bagurgle(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]
    defender_board.set_minions([PunchingBag(attack=10)])

    murloc = KingBagurgle()
    non_murloc = IronhideDirehorn()
    attacker_board.set_minions([KingBagurgle(), murloc, non_murloc])
    
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert murloc.attack == 8
    assert murloc.health == 5
    assert non_murloc.attack == 7
    assert non_murloc.health == 7


def test_malganis(initialized_game):
    attacker_board = initialized_game.player_board[0]

    malganis = MalGanis()
    attacker_board.set_minions([malganis])
    # TODO: Implement
    assert True


def test_mama_bear(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]
    defender_board.set_minions([PunchingBag(attack=10)])

    attacker_board.set_minions([KindlyGrandmother(), MamaBear()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    
    assert attacker_board.minions[0].attack == 7
    assert attacker_board.minions[0].health == 6


def test_seabreaker_goliath(initialized_game):
    attacker_board = initialized_game.player_board[0]

    goliath = SeabreakerGoliath()
    attacker_board.set_minions([goliath])
    # TODO: Implement
    assert True


def test_sneeds_old_shredder(initialized_game):
    attacker_board = initialized_game.player_board[0]

    sneeds = SneedsOldShredder()
    attacker_board.set_minions([sneeds])
    # TODO: Implement
    assert True


def test_voidlord(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    defender_board.set_minions([PunchingBag(attack=10)])
    attacker_board.set_minions([Voidlord()])

    initialized_game.start_of_game()
    initialized_game.single_round()
    
    for i in range(3):
        assert attacker_board.minions[i].name == "Voidwalker"
        assert attacker_board.minions[i].attack == 1
        assert attacker_board.minions[i].health == 3
