import random
from minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import KindlyGrandmother, SpawnofNZoth
from ghastcoiler.minions.rank_5 import BaronRivendare, BristlebackKnight, \
    IronhideDirehorn, KingBagurgle, MalGanis, MamaBear, \
    SeabreakerGoliath, SneedsOldShredder, Voidlord


def test_baronrivendar(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Basic test
    attacker_board.set_minions([Voidlord(), Voidlord(), BaronRivendare()])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    for i in range(5):
        assert attacker_board.minions[i].name == "Voidwalker"

    # Golden baron
    baron =  BaronRivendare(golden=True)
    attacker_board.set_minions([SpawnofNZoth(), baron])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert baron.attack == 5

    # Test adding and removing baron(s)
    attacker_board.set_minions([])
    assert attacker_board.deathrattle_multiplier == 1

    regular_baron = BaronRivendare()
    attacker_board.add_minion(regular_baron)
    assert attacker_board.deathrattle_multiplier == 2

    golden_baron = BaronRivendare(golden=True)
    attacker_board.add_minion(golden_baron)
    assert attacker_board.deathrattle_multiplier == 3

    attacker_board.remove_minion(regular_baron)
    assert attacker_board.deathrattle_multiplier == 3

    attacker_board.remove_minion(golden_baron)
    assert attacker_board.deathrattle_multiplier == 1

    attacker_board.add_minion(BaronRivendare())
    attacker_board.add_minion(BaronRivendare())
    assert attacker_board.deathrattle_multiplier == 2

    attacker_board.add_minion(BaronRivendare(golden=True))
    attacker_board.add_minion(BaronRivendare(golden=True))
    assert attacker_board.deathrattle_multiplier == 3


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
    defender_board = initialized_game.player_board[1]

    test_runs = 100
    for _ in range(test_runs):
        attacker_board.rank += 1
        if attacker_board.rank == 7:
            # No legendary minions at rank 1
            attacker_board.rank = 2 

        attacker_board.set_minions([SneedsOldShredder(golden=random.randint(0,1))])
        defender_board.set_minions([PunchingBag(attack=20)])
        
        initialized_game.start_of_game()
        initialized_game.single_round()

        for minion in attacker_board.minions:
            assert minion.legendary


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
