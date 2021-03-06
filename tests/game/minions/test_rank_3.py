from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.tokens import Imp
from ghastcoiler.minions.rank_1 import MicroMummy
from ghastcoiler.minions.rank_2 import KaboomBot, PackLeader, HarvestGolem, SpawnofNZoth
from ghastcoiler.minions.rank_3 import ArmoftheEmpire, CracklingCyclone,\
    DeflectoBot, ImpGangBoss, InfestedWolf, Khadgar, MonstrousMacaw,\
    ReplicatingMenace, RatPack, SoulJuggler
from ghastcoiler.deathrattles.rank_3 import ReplicatingMenaceDeathrattle
from minions.rank_5 import BaronRivendare
from minions.rank_6 import GoldrinntheGreatWolf


def test_arm_of_the_empire(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Taunted creature should get buff. Non taunted creature should not.
    attacker_board.set_minions([PunchingBag(attack=1)])
    defender_board.set_minions([ArmoftheEmpire(), PunchingBag(taunt=True), PunchingBag()])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[1].attack == 2
    assert defender_board.minions[2].attack == 0

    # It should buff itself if it is taunted
    attacker_board.set_minions([PunchingBag(attack=1)])
    defender_board.set_minions([ArmoftheEmpire(taunt=True)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[0].attack == 6
    assert defender_board.minions[0].health == 4

    # Multiple arms stack
    attacker_board.set_minions([PunchingBag(attack=1)])
    defender_board.set_minions([ArmoftheEmpire(taunt=True), ArmoftheEmpire()])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[0].attack == 8
    assert defender_board.minions[0].health == 4


def test_crackling_cyclone(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Mega wind fury should attack 4 times
    attacker_board.set_minions([CracklingCyclone(golden=True, health=4)])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert not attacker_board.minions[0].divine_shield
    assert attacker_board.minions[0].health == 1

    # Wind fury should attack 2 times
    attacker_board.set_minions([CracklingCyclone()])
    defender_board.set_minions([PunchingBag(health=1), PunchingBag(health=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert len(defender_board.minions) == 0


def test_deflectobot(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    deflectobot = DeflectoBot()
    attacker_board.set_minions([deflectobot])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert not deflectobot.divine_shield
    assert deflectobot.health == 2

    attacker_board.add_minion(DeflectoBot())
    assert deflectobot.divine_shield
    assert deflectobot.attack == 5


def test_imp_gang_boss(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Attack damage should make an imp
    attacker_board.set_minions([ImpGangBoss()])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 2
    assert attacker_board.minions[1].name == "Imp"

    # Death rattle damage should make an Imp
    # Death rattle also should be able to target a spawned imp since 'on damage' is triggered first
    attacker_board.set_minions([ImpGangBoss()])
    defender_board.set_minions([KaboomBot()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    if len(attacker_board.minions) == 1:
        assert attacker_board.minions[0].name == "Imp Gang Boss"
    elif len(attacker_board.minions) == 2:
        assert attacker_board.minions[0].name == "Imp"
        assert attacker_board.minions[1].name == "Imp"
    else:
        assert False


def test_infested_wolf(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([PunchingBag(), InfestedWolf()])
    defender_board.set_minions([PunchingBag(attack=3)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert len(attacker_board.minions) == 3
    assert attacker_board.minions[1].name == "Spider"
    assert attacker_board.minions[2].name == "Spider"

    attacker_board.set_minions([InfestedWolf(golden=True)])
    defender_board.set_minions([PunchingBag(attack=6)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    for i in range(2):
        assert attacker_board.minions[i].name == "Spider"
        assert attacker_board.minions[i].attack == 2


def test_khadgar(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Simple test
    attacker_board.set_minions([Khadgar()])
    defender_board.set_minions([PunchingBag()])
    attacker_board.add_minion(PunchingBag())
    assert len(attacker_board.minions) == 3

    # Test copying buffed tokens. Attack and order should be correct
    attacker_board.set_minions([RatPack(attack=3), Khadgar(), PackLeader()])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 7
    assert attacker_board.minions[0].attack == 3
    assert attacker_board.minions[1].attack == 5
    assert attacker_board.minions[2].attack == 3
    assert attacker_board.minions[3].attack == 5

    # Test reborn copying
    attacker_board.set_minions([MicroMummy(), Khadgar()])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 3
    assert attacker_board.minions[0].health == 1
    assert attacker_board.minions[1].health == 1

    # Test golden version
    attacker_board.set_minions([Khadgar(golden=True)])
    defender_board.set_minions([PunchingBag()])
    attacker_board.add_minion(PunchingBag())
    assert len(attacker_board.minions) == 4

    # TODO: Test multiple khadgar interactions
    # TODO: Test with scallywag and admiral
    # TODO: Test with baron


def test_monstrous_macaw(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([MonstrousMacaw(), InfestedWolf(), PunchingBag()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    # Make sure tokens spawn in the right spot
    assert len(attacker_board.minions) == 5
    assert not attacker_board.minions[2].attacked
    assert attacker_board.minions[2].name == "Spider"
    assert attacker_board.minions[3].name == "Spider"

    # Golden macaw
    attacker_board.set_minions([MonstrousMacaw(golden=True), InfestedWolf(), PunchingBag()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 7
    assert attacker_board.minions[6].name == "PunchingBag"

    # Test with minions with multiple deathrattles
    attacker_board.set_minions([MonstrousMacaw(), HarvestGolem(deathrattles=[ReplicatingMenaceDeathrattle()])])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert (len(attacker_board.minions) == 3 or len(attacker_board.minions) == 5)

    # TODO: Test randomness of deathrattles?

    # Test baron multiplier
    # Regular macaw + Regular baron = 2 triggers
    spawn = SpawnofNZoth()
    attacker_board.set_minions([MonstrousMacaw(), spawn, BaronRivendare()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert spawn.health == 4

    # Regular macaw + Golden baron = 3 triggers
    spawn = SpawnofNZoth()
    attacker_board.set_minions([MonstrousMacaw(), spawn, BaronRivendare(golden=True)])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert spawn.health == 5

    # Golden macaw + Regular baron = 4 triggers
    spawn = SpawnofNZoth()
    attacker_board.set_minions([MonstrousMacaw(golden=True), spawn, BaronRivendare()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert spawn.health == 6

    # Golden macaw + Golden baron = 6 triggers
    spawn = SpawnofNZoth()
    attacker_board.set_minions([MonstrousMacaw(golden=True), spawn, BaronRivendare(golden=True)])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert spawn.health == 8

    # TODO: Test order of operations with killing an opposing death rattle

    # Test attack order when spawning minions, ie generating tokens from a minion that has / hasnt attacked yet
    attacker_board.set_minions([InfestedWolf(), MonstrousMacaw(), PunchingBag(attack=5)])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    initialized_game.single_round()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 5
    assert attacker_board.minions[4].name == "PunchingBag"
    initialized_game.single_round()
    initialized_game.single_round()
    assert defender_board.minions[0].health == 87


# def test_piloted_shredder(initialized_game):
#     # TODO: Is there a better way to verify this?
#     # Are there minions shredder wont summon? IE tribes not in current game?
#     attacker_board = initialized_game.player_board[0]
#     defender_board = initialized_game.player_board[1]

#     attacker_board.set_minions([PilotedShredder()])
#     defender_board.set_minions([PunchingBag(attack=10)])
#     initialized_game.start_of_game()
#     initialized_game.single_round()
#     assert attacker_board.minions[0].mana_cost == 2

#     attacker_board.set_minions([PilotedShredder(golden=True)])
#     defender_board.set_minions([PunchingBag(attack=10)])
#     initialized_game.start_of_game()
#     initialized_game.single_round()
#     assert attacker_board.minions[0].mana_cost == 2
#     assert attacker_board.minions[1].mana_cost == 2

def test_rat_pack(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]
    rat = RatPack(reborn=True, attack=4)

    attacker_board.set_minions([rat])
    defender_board.set_minions([PunchingBag(attack=10)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 5
    assert attacker_board.minions[0].name == "Rat"


def test_replicating_menace(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Base minion test
    menace = ReplicatingMenace()
    attacker_board.set_minions([menace])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game()
    initialized_game.single_round()

    for i in range(3):
        assert attacker_board.minions[i].name == "Microbot"
    assert menace.left_neighbor == attacker_board.minions[2]
    assert defender_board.minions[0].health == 97

    # Test multiple death rattles.
    # TODO: They should trigger in order they're added
    attacker_board.set_minions([KaboomBot(deathrattles=[ReplicatingMenaceDeathrattle(golden=True)])])
    defender_board.set_minions([PunchingBag(attack=2)])
    initialized_game.start_of_game()
    initialized_game.single_round()

    for i in range(3):
        assert attacker_board.minions[i].name == "Microbot"
        assert attacker_board.minions[i].attack == 2
        assert attacker_board.minions[i].health == 2
    assert defender_board.minions[0].health == 94

    menace = ReplicatingMenace(reborn=True)
    attacker_board.set_minions([PunchingBag(), menace])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert menace.position == 4
    assert menace.reborn_triggered
    assert not menace.reborn


# TODO: Verify tests
def test_soul_juggler(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    defender = PunchingBag(attack=10)

    # Simple test
    attacker_board.set_minions([Imp(), SoulJuggler()])
    defender_board.set_minions([defender])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender.health == 96

    # Test golden juggler
    defender = PunchingBag(attack=10)
    attacker_board.set_minions([Imp(), SoulJuggler(golden=True)])
    defender_board.set_minions([defender])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender.health == 93

    # Test opposing jugglers
    attacker_board.set_minions([Imp(taunt=True), SoulJuggler()])
    defender_board.set_minions([Imp(taunt=True), SoulJuggler()])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    # Attacking juggler should kill defending juggler and survive
    assert len(attacker_board.minions) == 1

    # Test jugglers triggering an 'on damage' minion

    # Test juggler with reborn minion.
    # Reborn happens after juggle. Mummy should live
    defender = PunchingBag(attack=10)
    attacker_board.set_minions([Imp(), SoulJuggler()])
    defender_board.set_minions([MicroMummy(health=1)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(defender_board.minions) == 1
