from minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_6 import Amalgadon, DreadAdmiralEliza, \
    GentleDjinni, Ghastcoiler, GoldrinntheGreatWolf, ImpMama, \
    KangorsApprentice, NadinatheRed, TheTideRazor, ZappSlywick
from minions.types import MinionType
import random


def test_amalgadon(initialized_game):
    attacker_board = initialized_game.player_board[0]

    amalgadon = Amalgadon()
    attacker_board.set_minions([amalgadon])
    # TODO: Implement, make sure all the amalgadon buffs are imported correctly
    for type in MinionType:
        assert type in amalgadon.types


def test_dread_admiral_eliza(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    amalgadon = Amalgadon()

    defender_board.set_minions([PunchingBag()])
    attacker_board.set_minions([DreadAdmiralEliza(), GentleDjinni(), amalgadon])

    initialized_game.start_of_game()
    initialized_game.single_round()
    assert amalgadon.attack == 8
    assert amalgadon.health == 7

    initialized_game.single_round()
    initialized_game.single_round()
    assert amalgadon.attack == 8
    assert amalgadon.health == 7

    initialized_game.single_round()
    initialized_game.single_round()
    assert amalgadon.attack == 10
    assert amalgadon.health == 8


def test_gentle_djinni(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    test_runs = 100
    for _ in range(test_runs):
        attacker_board.rank += 1
        if attacker_board.rank == 7:
            attacker_board.rank = 1

        attacker_board.set_minions([GentleDjinni(golden=random.randint(0,1))])
        defender_board.set_minions([PunchingBag(attack=20)])
        
        initialized_game.start_of_game()
        initialized_game.single_round()

        for minion in attacker_board.minions:
            assert MinionType.Elemental in minion.types
            assert minion.rank <= attacker_board.rank


def test_ghastcoiler(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    test_runs = 100
    for _ in range(test_runs):
        attacker_board.rank += 1
        if attacker_board.rank == 7:
            attacker_board.rank = 1

        attacker_board.set_minions([Ghastcoiler(golden=random.randint(0,1))])
        defender_board.set_minions([PunchingBag(attack=20)])
        
        initialized_game.start_of_game()
        initialized_game.single_round()

        for minion in attacker_board.minions:
            assert len(minion.deathrattles) > 0
            assert minion.rank <= attacker_board.rank


def test_goldrinn_the_great_wolf(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    amalgadon = Amalgadon()
    genie = GentleDjinni()

    defender_board.set_minions([PunchingBag(attack=10)])
    attacker_board.set_minions([GoldrinntheGreatWolf(), genie, amalgadon])

    initialized_game.start_of_game()
    initialized_game.single_round()
    assert amalgadon.attack == 11
    assert amalgadon.health == 11
    assert genie.attack == 4
    assert genie.health == 5


def test_imp_mama(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    
    attacker_board.set_minions([ImpMama()])  
    defender_board.set_minions([PunchingBag(attack=10)])

    attacker_board.rank = 6

    initialized_game.start_of_game()
    initialized_game.single_round()

    demon = attacker_board.minions[0]
    assert MinionType.Demon in demon.types    
    assert demon.taunt
    assert demon.rank <= attacker_board.rank


def test_kangors_apprentice(initialized_game):
    attacker_board = initialized_game.player_board[0]

    kangor = KangorsApprentice()
    attacker_board.set_minions([kangor])
    # TODO: Implement
    assert True


def test_nadina_the_red(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    amalgadon = Amalgadon()
    genie = GentleDjinni()

    defender_board.set_minions([PunchingBag(attack=10)])
    attacker_board.set_minions([NadinatheRed(), genie, amalgadon])

    initialized_game.start_of_game()
    initialized_game.single_round()
    assert amalgadon.divine_shield == True
    assert genie.divine_shield == False


def test_the_tide_razor(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    test_runs = 100
    for _ in range(test_runs):
        attacker_board.rank += 1
        if attacker_board.rank == 7:
            attacker_board.rank = 1

        attacker_board.set_minions([TheTideRazor(golden=random.randint(0,1))])
        defender_board.set_minions([PunchingBag(attack=20)])
        
        initialized_game.start_of_game()
        initialized_game.single_round()

        for minion in attacker_board.minions:
            assert MinionType.Pirate in minion.types
            assert minion.rank <= attacker_board.rank


def test_zapp_slywick(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    target = PunchingBag()
    defender_board.set_minions([target, PunchingBag(attack=1, taunt=True)])

    attacker_board.set_minions([ZappSlywick()])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert target.health == 86
