from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import KaboomBot
from ghastcoiler.minions.rank_3 import ArmoftheEmpire, CracklingCyclone,\
    DeflectoBot, ImpGangBoss, InfestedWolf, MonstrousMacaw


def test_arm_of_the_empire(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Taunted creature should get buff. Non taunted creature should not.
    attacker_board.set_minions([PunchingBag(attack=1)])
    defender_board.set_minions([ArmoftheEmpire(), PunchingBag(taunt=True), PunchingBag()])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[1].attack == 3
    assert defender_board.minions[2].attack == 0

    # It should buff itself if it is taunted
    attacker_board.set_minions([PunchingBag(attack=1)])
    defender_board.set_minions([ArmoftheEmpire(taunt=True)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[0].attack == 7
    assert defender_board.minions[0].defense == 4


def test_crackling_cyclone(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Mega wind fury should attack 4 times
    attacker_board.set_minions([CracklingCyclone(golden=True, defense=4)])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert not attacker_board.minions[0].divine_shield
    assert attacker_board.minions[0].defense == 1

    # Wind fury should attack 2 times
    attacker_board.set_minions([CracklingCyclone()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[0].defense == 92


def test_deflectobot(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    deflectobot = DeflectoBot()
    attacker_board.set_minions([deflectobot])
    defender_board.set_minions([PunchingBag(attack=1)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert not deflectobot.divine_shield
    assert deflectobot.defense == 2

    attacker_board.add_minion(DeflectoBot())
    assert deflectobot.divine_shield
    assert deflectobot.attack == 4


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

    attacker_board.set_minions([InfestedWolf()])
    defender_board.set_minions([PunchingBag(attack=3)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 2
    assert attacker_board.minions[0].name == "Spider"
    assert attacker_board.minions[1].name == "Spider"

    attacker_board.set_minions([InfestedWolf(golden=True)])
    defender_board.set_minions([PunchingBag(attack=6)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    for i in range(2):
        assert attacker_board.minions[i].name == "Spider"
        assert attacker_board.minions[i].attack == 2


def test_monstrous_macaw(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([MonstrousMacaw(), InfestedWolf()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    # Make sure tokens spawn in the right spot
    assert len(attacker_board.minions) == 4
    assert attacker_board.minions[2].name == "Spider"
    assert attacker_board.minions[3].name == "Spider"

    # Golden macaw
    attacker_board.set_minions([MonstrousMacaw(golden=True), InfestedWolf()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 6
    # TODO: Test randomness of deathrattles?
    # TODO: Test baron multiplier
    # TODO: Test with goldrinn keeping macaw alive after it takes lethal
    # TODO: Test order of operations with killing an opposing death rattle
    # TODO: Test with minions with multiple deathrattles
