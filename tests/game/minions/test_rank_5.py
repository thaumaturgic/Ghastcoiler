import random
from minions.rank_3 import DeflectoBot, IronSensei, ScrewjankClunker
from minions.rank_4 import Junkbot
from minions.rank_6 import Amalgadon, FoeReaper4000
from minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import Imprisoner, KindlyGrandmother, SpawnofNZoth
from ghastcoiler.minions.rank_5 import BaronRivendare, BristlebackKnight, \
    IronhideDirehorn, KingBagurgle, MalGanis, MamaBear, \
    SeabreakerGoliath, SneedsOldShredder, Voidlord, KangorsApprentice


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
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([IronhideDirehorn()])
    defender_board.set_minions([PunchingBag(health=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert attacker_board.minions[1].name == "Ironhide Runt"

    attacker_board.set_minions([IronhideDirehorn(golden=True)])
    defender_board.set_minions([PunchingBag(health=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert attacker_board.minions[1].attack == 10
    assert attacker_board.minions[1].health == 10

    attacker_board.set_minions([IronhideDirehorn(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag()])
    defender_board.set_minions([PunchingBag(attack=10, health=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert attacker_board.minions[0].name == "PunchingBag"
    assert len(attacker_board.minions) == 6

    attacker_board.set_minions([IronhideDirehorn(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag()])
    defender_board.set_minions([PunchingBag(attack=10, health=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert len(attacker_board.minions) == 6


def test_kangors_apprentice(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([Junkbot(), FoeReaper4000(), KangorsApprentice(), PunchingBag(taunt=True)])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    for _ in range(5):
        initialized_game.single_round()
    assert attacker_board.minions[0].name == "Junkbot"
    assert attacker_board.minions[1].name == "Foe Reaper 4000"
    
    attacker_board.set_minions([Junkbot(), FoeReaper4000(golden=True), Amalgadon(), ScrewjankClunker(golden=True), IronSensei(), KangorsApprentice(golden=True), PunchingBag(taunt=True, health=999)])
    defender_board.set_minions([PunchingBag(attack=20)])
    initialized_game.start_of_game()
    for _ in range(11):
        initialized_game.single_round()
    assert attacker_board.minions[0].name == "Junkbot"
    assert attacker_board.minions[1].name == "Foe Reaper 4000"
    assert attacker_board.minions[1].golden
    assert attacker_board.minions[2].name == "Amalgadon"
    assert attacker_board.minions[3].name == "Screwjank Clunker"
    assert attacker_board.minions[3].golden
    assert attacker_board.minions[4].name == "PunchingBag"
    
    # A kangor that is summoned (ie via ghastcoiler) after friendly mechs have died should spawn those mechs
    attacker_board.set_minions([Junkbot(), FoeReaper4000(), PunchingBag(taunt=True)])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    for _ in range(3):
        initialized_game.single_round()

    attacker_board.add_minion(KangorsApprentice(), position=0)
    initialized_game.single_round()
    initialized_game.single_round()
    assert attacker_board.minions[0].name == "Junkbot"
    assert attacker_board.minions[1].name == "Foe Reaper 4000"


    # TODO: Test cleave killing 3 mechs, which 2 are recorded? Left most? or target + left? 


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
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([Imprisoner(), MalGanis(taunt=True)])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert attacker_board.minions[0].attack == 3
    assert attacker_board.minions[0].health == 3
    
    initialized_game.single_round()
    assert attacker_board.minions[0].attack == 1
    assert attacker_board.minions[0].health == 1


def test_mama_bear(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]
    defender_board.set_minions([PunchingBag(attack=10)])

    attacker_board.set_minions([KindlyGrandmother(), MamaBear()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    
    assert attacker_board.minions[0].attack == 8
    assert attacker_board.minions[0].health == 7


def test_seabreaker_goliath(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    self_goliath = SeabreakerGoliath()
    other_goliath = SeabreakerGoliath()
    non_pirate = PunchingBag()
    attacker_board.set_minions([self_goliath, other_goliath, non_pirate])
    defender_board.set_minions([PunchingBag(health=1)])

    initialized_game.start_of_game()
    initialized_game.single_round()
    
    assert self_goliath.attack == 6
    assert self_goliath.health == 7
    assert other_goliath.attack == 8
    assert other_goliath.health == 9
    assert non_pirate.attack == 0
    assert non_pirate.health == 100


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
