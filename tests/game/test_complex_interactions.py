from deathrattles.base import Deathrattle
from deathrattles.rank_3 import ReplicatingMenaceDeathrattle
from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_1 import AcolyteOfCThun, MicroMummy, Scallywag
from ghastcoiler.minions.rank_2 import HarvestGolem, Imprisoner, KaboomBot
from minions.rank_3 import ReplicatingMenace, SoulJuggler
from minions.rank_4 import CaveHydra

def test_baron_rivendare(initialized_game):
    # TODO: Test baron and golden baron interactions with
    # -Khadgar
    # -Bomb (ie generic deathrattle)
    # -Macaw
    # -Deathrattle multiples when baron itself and neighbors is killed by cleave (ie [bomb, baron, bomb])
    assert True


def test_khadgar(initialized_game):
    # TODO: Test khadgar and interactions with
    # -Reborn
    # -Tokens that are buffed and then copied and re-buffed
    assert True


def test_scallywag(initialized_game):
    # TODO: Test scallywag and interactions with
    # -Khadgar
    # -Baron
    # -Eliza
    assert True


def test_deathrattle_order(initialized_game):
    # TODO: Test order of operations with deathrattles and interactions with
    # -reborn
    # -pirate attacks
    assert True


def test_reborn_mechanic(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Deathrattle + reborn order
    reborn_bomb = KaboomBot(reborn=True)
    attacker_board.set_minions([reborn_bomb])
    defender_board.set_minions([KaboomBot()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 1
    assert reborn_bomb.health == 1 and reborn_bomb.reborn_triggered

    # Reborn with golden minions
    gold_acolyte = AcolyteOfCThun(reborn=True, golden=True)
    attacker_board.set_minions([gold_acolyte])
    defender_board.set_minions([PunchingBag(attack=10)])
    assert gold_acolyte.attack == 4
    assert gold_acolyte.health == 4
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert gold_acolyte.attack == 4
    assert gold_acolyte.health == 1

    # Deathrattle + reborn when not enough space for reborn
    attacker_board.set_minions([PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag(), PunchingBag(), HarvestGolem(reborn=True, taunt=True)])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game(1)
    initialized_game.single_round()
    assert attacker_board.minions[6].name == "Damaged Golem"


def test_reborn_position_tracking(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Deathrattle + reborn position when adding minions
    attacker_board.add_minion(HarvestGolem(reborn=True))
    defender_board.add_minion(PunchingBag(attack=10))
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert attacker_board.minions[0].name == "Damaged Golem"
    assert attacker_board.minions[1].name == "Harvest Golem"
    assert attacker_board.minions[1].health == 1

    # Death trigger + reborn position when killing minions
    # Mummy attacks imp, imp and mummy die, 
    # soul juggler kills punching bag, mummy should be reborn at position 0
    attacker_board.set_minions([PunchingBag(health=1), MicroMummy()])
    defender_board.set_minions([Imprisoner(health=1), SoulJuggler()])
    initialized_game.start_of_game(starting_player=0)
    initialized_game.single_round()
    assert attacker_board.minions[0].position == 0

    # Multiple spawning deathrattles and reborn
    # Harvest Golemn + Replicating menace + reborn
    # Golem should trigger its deathrattle, then the menace, then its own reborn
    # It should be reborn WITHOUT the menace deathrattle
    golemn = HarvestGolem(deathrattles=[ReplicatingMenaceDeathrattle()], reborn=True)
    attacker_board.set_minions([golemn])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game(starting_player=0)
    initialized_game.single_round()
    assert attacker_board.minions[0].name == "Damaged Golem"
    assert attacker_board.minions[1].name == "Microbot"
    assert attacker_board.minions[4].name == "Harvest Golem"
    assert attacker_board.minions[4].reborn_triggered

    attacker_board.set_minions([CaveHydra(attack=10)])
    defender_board.set_minions([ReplicatingMenace(), MicroMummy(taunt=True), HarvestGolem(health=1, reborn=True)])
    initialized_game.start_of_game(starting_player=0)
    initialized_game.single_round()
    assert defender_board.minions[0].name == "Microbot"
    assert defender_board.minions[3].name == "Micro Mummy"
    assert defender_board.minions[3].reborn_triggered
    assert defender_board.minions[4].name == "Damaged Golem"
    assert defender_board.minions[5].name == "Harvest Golem"
    assert defender_board.minions[5].reborn_triggered

    # TODO: Consider a dead, living, dead sequence and ensure order is correct
    # TODO: Do all deathrattles resolve before any reborns?
    attacker_board.set_minions([CaveHydra(attack=10)])
    defender_board.set_minions([ReplicatingMenace(reborn=True), MicroMummy(taunt=True, health=999), ReplicatingMenace()])
    initialized_game.start_of_game(starting_player=0)
    initialized_game.single_round()
    assert True

    # Order of on damage triggers
    attacker_board.set_minions([PunchingBag(health=1), MicroMummy()])
    defender_board.set_minions([Imprisoner(health=1), SoulJuggler()])
    initialized_game.start_of_game(starting_player=0)
    initialized_game.single_round()
    reborn_mummy = attacker_board.minions[0]
    assert reborn_mummy.position == 0
    assert reborn_mummy.reborn


def test_golden_tokens(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.add_minion(Scallywag(golden=True))
    defender_board.add_minion(PunchingBag(attack=10, health=1))
    initialized_game.start_of_game()
    initialized_game.single_round()

    pirate_token = attacker_board.minions[0]
    assert pirate_token.golden
    assert pirate_token.name == "Sky Pirate"
    assert pirate_token.attack == 2
    assert pirate_token.health == 2


def test_on_attack_trigger_order(initialized_game):
    # TODO: Two imps attack each other, which side creates the imp first?
    # TODO: How does something like security bot + deflecto + bomb work
    assert True
