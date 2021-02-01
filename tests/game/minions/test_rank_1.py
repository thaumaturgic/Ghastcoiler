from ghastcoiler.minions.rank_1 import FiendishServant, DragonspawnLieutenant, RabidSaurolisk, ScavengingHyena, Alleycat, AcolyteOfCThun, Scallywag, VulgarHomunculus
from ghastcoiler.minions.test_minions import PunchingBag

def test_fiendish_servant_deathrattle(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([FiendishServant(), DragonspawnLieutenant()])
    defender_board.set_minions([FiendishServant()])

    initialized_game.start_of_game()
    initialized_game.single_round()

    assert len(attacker_board.minions) == 1
    assert len(defender_board.minions) == 0
    assert attacker_board.minions[0].attack == 4


def test_rabid_saurolisk(initialized_game):
    rabid_saurolisk = RabidSaurolisk()
    initialized_game.player_board[0].add_minion(rabid_saurolisk)
    assert rabid_saurolisk.attack == 3
    assert rabid_saurolisk.defense == 1
    initialized_game.player_board[0].add_minion(FiendishServant())
    assert rabid_saurolisk.attack == 4
    assert rabid_saurolisk.defense == 2
    initialized_game.player_board[0].add_minion(DragonspawnLieutenant())
    assert rabid_saurolisk.attack == 4
    assert rabid_saurolisk.defense == 2

def test_scavenging_hyena(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    hyena = ScavengingHyena()
    attacker_board.add_minion(hyena)
    attacker_board.add_minion(Alleycat())
    attacker_board.minions[1].dead = True
    initialized_game.check_deaths(attacker_board, defender_board)

    assert hyena.attack == 4
    assert hyena.defense == 3

def test_acolyte_of_cthun(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_acolyte = AcolyteOfCThun()
    defender_acolyte = AcolyteOfCThun()
    attacker_board.add_minion(attacker_acolyte)
    defender_board.add_minion(defender_acolyte)
    initialized_game.start_of_game()
    initialized_game.single_round()

    assert attacker_acolyte.defense == 1 and attacker_acolyte.reborn_triggered
    assert defender_acolyte.defense == 1 and defender_acolyte.reborn_triggered


def test_red_whelp(initialized_game):
    # TODO: Test start of game actions
    assert True

def test_scallywag(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Test 'attacks immediately' mechanic
    defender = VulgarHomunculus()
    attacker_board.add_minion(Scallywag())
    defender_board.add_minion(defender)
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender.defense == 1

    # Test golden tokens
    defender = PunchingBag(attack = 10)
    attacker_board.set_minions([Scallywag(golden=True)])
    defender_board.set_minions([defender])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender.defense == 94

    #TODO: Test scallywag on scallywag

    