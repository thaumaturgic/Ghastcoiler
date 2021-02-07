from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import \
    PackLeader, KindlyGrandmother, SouthseaCaptain, FreedealingGambler
from ghastcoiler.minions.rank_3 import RatPack
from ghastcoiler.minions.rank_4 import CaveHydra


def test_cave_hydra(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Test simultaneous deaths. Wolf token should not be buffed since pack leader died with the grandmother
    attacker_board.set_minions([CaveHydra(attack=10), PunchingBag(), PunchingBag(), PunchingBag()])
    defender_board.set_minions([KindlyGrandmother(), PunchingBag(taunt=True), PackLeader()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender_board.minions[0].name == "Big Bad Wolf"
    assert defender_board.minions[0].attack == 3

    # Death rattle order on cleave. Rats should fill board and not leave room for wolf token
    attacker_board.set_minions([CaveHydra(attack=10), PunchingBag(), PunchingBag(), PunchingBag()])
    defender_board.set_minions([RatPack(attack=7), KindlyGrandmother()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender_board.minions[6].name == "Rat"

    # When a cleave kills an aura generator with a buffed minion, the damage is applied first, then the aura wears off
    attacker_board.set_minions([CaveHydra(), PunchingBag(), PunchingBag(), PunchingBag()])
    defender_board.set_minions([FreedealingGambler(defense=3), SouthseaCaptain(taunt=True, defense=2), FreedealingGambler(defense=3)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender_board.minions[0].defense == 1
    assert defender_board.minions[1].defense == 1

    # TODO: Test cleave hitting a security bot and deflecto bot (without shield).
    # Damage trigger should be done after damage applied to all units (ie after shield is broken)

    # TODO: Test cleave hitting an imp and rover with room for only one token. Should end up with just imp
