from minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_6 import Amalgadon, DreadAdmiralEliza, \
    GentleDjinni, Ghastcoiler, GoldrinntheGreatWolf, ImpMama, \
    KangorsApprentice, NadinatheRed, TheTideRazor, ZappSlywick
from minions.types import MinionType


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

    djinni = GentleDjinni()
    attacker_board.set_minions([djinni])
    # TODO: Implement
    assert True


def test_ghastcoiler(initialized_game):
    attacker_board = initialized_game.player_board[0]

    ghastcoiler = Ghastcoiler()
    attacker_board.set_minions([ghastcoiler])
    # TODO: Implement
    assert True


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

    impmama = ImpMama()
    attacker_board.set_minions([impmama])
    # TODO: Implement
    assert True


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


def test_the_thede_razor(initialized_game):
    attacker_board = initialized_game.player_board[0]

    boat = TheTideRazor()
    attacker_board.set_minions([boat])
    # TODO: Implement
    assert True


def test_zapp_slywick(initialized_game):
    attacker_board = initialized_game.player_board[0]

    zapp = ZappSlywick()
    attacker_board.set_minions([zapp])
    # TODO: Implement
    assert True
