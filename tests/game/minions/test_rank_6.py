from deathrattles.rank_6 import LivingSporesDeathrattle
from minions.rank_3 import Khadgar, MonstrousMacaw
from minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_6 import Amalgadon, DreadAdmiralEliza, \
    GentleDjinni, Ghastcoiler, GoldrinntheGreatWolf, ImpMama, \
    NadinatheRed, TheTideRazor, ZappSlywick
from minions.types import MinionType
import random


def test_amalgadon(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    amalgadon = Amalgadon(deathrattles=[LivingSporesDeathrattle(), LivingSporesDeathrattle()])
    attacker_board.set_minions([amalgadon])
    defender_board.set_minions([PunchingBag(attack=10)])

    for type in MinionType:
        assert type in amalgadon.types

    initialized_game.start_of_game()
    initialized_game.single_round()
    for i in range(4):
        assert attacker_board.minions[i].name == "Plant"


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


def test_ghastcoiler(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    test_runs = 100
    for _ in range(test_runs):
        attacker_board.set_minions([Ghastcoiler(golden=random.randint(0,1))])
        defender_board.set_minions([PunchingBag(attack=20)])
        initialized_game.start_of_game()
        initialized_game.single_round()

        for minion in attacker_board.minions:
            assert len(minion.deathrattles) > 0

        # Test with khadgar, should spawn 4 minions, then reborn itself for two copies
        attacker_board.set_minions([Ghastcoiler(golden=False, reborn=True), Khadgar()])
        defender_board.set_minions([PunchingBag(attack=20)])
        initialized_game.start_of_game()
        initialized_game.single_round()
        for i in range(6):
            assert len(attacker_board.minions[i].deathrattles) == 1
        

def test_goldrinn_the_great_wolf(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    amalgadon = Amalgadon()
    genie = GentleDjinni()

    attacker_board.set_minions([GoldrinntheGreatWolf(), genie, amalgadon, GoldrinntheGreatWolf()])
    defender_board.set_minions([PunchingBag(attack=10)])

    initialized_game.start_of_game()
    initialized_game.single_round()
    assert amalgadon.attack == 11
    assert amalgadon.health == 11
    assert genie.attack == 4
    assert genie.health == 5

    # Macaw should live if triggering goldrin brings its health above zero
    macaw = MonstrousMacaw()
    goldrinn = GoldrinntheGreatWolf()

    attacker_board.set_minions([macaw, goldrinn])
    defender_board.set_minions([PunchingBag(attack=3)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert not macaw.dead
    assert macaw.attack == 10 and macaw.health == 5
    assert goldrinn.attack == 9 and goldrinn.health == 9

    # Macaw should die even if health > 0 if it is killed by poison
    dead_macaw = MonstrousMacaw()
    attacker_board.set_minions([dead_macaw, GoldrinntheGreatWolf()])
    defender_board.set_minions([PunchingBag(attack=3, poisonous=True)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert dead_macaw.dead and dead_macaw.dead_by_poison


def test_imp_mama(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([ImpMama()])  
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()

    demon = attacker_board.minions[0]
    assert MinionType.Demon in demon.types    
    assert demon.taunt


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

    # Test with khadgar
    attacker_board.set_minions([TheTideRazor(), Khadgar()])
    defender_board.set_minions([PunchingBag(attack=20)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    for i in range(0,5,2):
        assert attacker_board.minions[i] != attacker_board.minions[i+1]
        assert attacker_board.minions[i].__class__ == attacker_board.minions[i+1].__class__


def test_zapp_slywick(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Zap should ignore taunts and attack lowest attack
    attacker_board.set_minions([ZappSlywick()])

    target = PunchingBag(attack=1)
    defender_board.set_minions([target, PunchingBag(attack=2, taunt=True)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert target.health == 86

    target = PunchingBag(attack=0)
    defender_board.set_minions([target, PunchingBag(attack=1, taunt=True)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert target.health == 86