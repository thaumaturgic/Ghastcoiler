from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import \
    PackLeader, KindlyGrandmother, SouthseaCaptain, FreedealingGambler
from ghastcoiler.minions.rank_3 import RatPack, ImpGangBoss
from ghastcoiler.minions.rank_4 import Bigfernal, BolvarFireblood, CaveHydra, \
    ChampionofYShaarj, DrakonidEnforcer, HeraldofFlame, MechanoEgg, QirajiHarbinger, \
    RipsnarlCaptain, RingMatron, SavannahHighmane, WildfireElemental


def test_bigfernal(initialized_game):
    attacker_board = initialized_game.player_board[0]

    bigfernal = Bigfernal()
    attacker_board.set_minions([bigfernal])
    attacker_board.add_minion(ImpGangBoss())

    assert bigfernal.attack == 5
    assert bigfernal.health == 5


def test_bolvar_fireblood(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    bolvar = BolvarFireblood()
    attacker_board.set_minions([bolvar])
    defender_board.set_minions([PunchingBag(attack=1)])

    initialized_game.start_of_game()
    initialized_game.single_round()

    assert bolvar.attack == 3
    assert bolvar.health == 7


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
    defender_board.set_minions([FreedealingGambler(health=3), SouthseaCaptain(taunt=True, health=2), FreedealingGambler(health=3)])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender_board.minions[0].health == 1
    assert defender_board.minions[1].health == 1

    # TODO: Test cleave hitting a security bot and deflecto bot (without shield).
    # Damage trigger should be done after damage applied to all units (ie after shield is broken)

    # TODO: Test cleave hitting an imp and rover with room for only one token. Should end up with just imp


def test_champion_of_yshaarj(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    champion = ChampionofYShaarj()

    attacker_board.set_minions([PunchingBag(attack=1)])
    defender_board.set_minions([PunchingBag(taunt=True), champion])

    initialized_game.start_of_game(0)
    initialized_game.single_round()

    assert champion.attack == 5
    assert champion.health == 5


def test_drakonid_enforcer(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    drakonid = DrakonidEnforcer()
    attacker_board.set_minions([BolvarFireblood(), drakonid])
    defender_board.set_minions([PunchingBag(attack=1)])

    initialized_game.start_of_game()
    initialized_game.single_round()

    assert drakonid.attack == 5
    assert drakonid.health == 8


def test_herald_of_flame(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([HeraldofFlame()])
    defender_board.set_minions([PunchingBag(health=1, taunt=False),
                                PunchingBag(health=2, taunt=False),
                                PunchingBag(health=3, taunt=True),
                                PunchingBag(health=4, taunt=False),
                                PunchingBag(health=5, taunt=False)])
    target_minion = defender_board.minions[2]
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert len(defender_board.minions) == 2
    assert defender_board.minions[0].health == 1
    assert target_minion.health == -3 # Fire breath should not breathe on dead minions

    # Dragon attacks and kills middle imp. imp damage triggers spawns imp
    # Dragon overkill trigger resolves, kills bag, spawned imp and procs final imp gang boss
    # board state should be imp boss and one imp
    attacker_board.set_minions([HeraldofFlame()])
    defender_board.set_minions([PunchingBag(health=1, taunt=False),
                                ImpGangBoss(health=1, taunt=True), 
                                ImpGangBoss()])
    
    initialized_game.start_of_game(0)
    initialized_game.single_round()

    assert defender_board.minions[0].name == "Imp Gang Boss"
    assert defender_board.minions[1].name == "Imp"


def test_mechano_egg(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([PunchingBag(attack=10)])
    defender_board.set_minions([MechanoEgg()])

    initialized_game.start_of_game(0)
    initialized_game.single_round()

    assert defender_board.minions[0].name == "Robosaur"
    assert defender_board.minions[0].health == 8
    assert defender_board.minions[0].attack == 8


def test_qiraji_harbinger(initialized_game):
    # TODO: Figure out how killing multiple taunts with cleave works
    # TODO: What if a harbinger is killed by a cleave? Does it still buff? 
    # TODO: Figure out how (if?) order matters with soul juggler and harbinger triggers
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    leftMinion = QirajiHarbinger()
    rightMinion = PunchingBag(taunt=False)
    attacker_board.set_minions([PunchingBag(attack=1, poisonous=True)])
    defender_board.set_minions([leftMinion, PunchingBag(taunt=True), rightMinion])

    initialized_game.start_of_game(0)
    initialized_game.single_round()

    assert leftMinion.attack == 7 and leftMinion.health == 7
    assert rightMinion.attack == 2 and rightMinion.health == 102


def test_ring_matron(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([RingMatron()])
    defender_board.set_minions([PunchingBag(attack=10)])

    initialized_game.start_of_game()
    initialized_game.single_round()

    for i in range(2):
        minion = attacker_board.minions[i]
        assert minion.name == "Fiery Imp"
        assert minion.attack == 3
        assert minion.health == 2


def test_ripsnarl_captain(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    buffPirate = FreedealingGambler()
    nonBuffPirate = RipsnarlCaptain()

    attacker_board.set_minions([buffPirate, nonBuffPirate])
    defender_board.set_minions([PunchingBag()])

    initialized_game.start_of_game()
    initialized_game.single_round()

    assert buffPirate.attack == 5
    assert buffPirate.health == 5

    initialized_game.single_round()
    initialized_game.single_round()

    assert nonBuffPirate.attack == 4
    assert nonBuffPirate.health == 5


def test_savannah_highmane(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([SavannahHighmane()])
    defender_board.set_minions([PunchingBag(attack=10)])

    initialized_game.start_of_game()
    initialized_game.single_round()

    for i in range(2):
        hyena = attacker_board.minions[i]
        assert hyena.name == "Hyena"
        assert hyena.attack == 2
        assert hyena.health == 2


def test_security_rover(initialized_game):
    # TODO: Test when a rover takes damage and dies that the token is in the right spot
    pass


# def test_siegebreaker(initialized_game):
#     attacker_board = initialized_game.player_board[0]
#     defender_board = initialized_game.player_board[1]
#     attacker_board.set_minions([Siegebreaker()])
#     defender_board.set_minions([PunchingBag(attack=10)])

#     imp = ImpGangBoss()
#     attacker_board.add_minion(imp)
#     assert imp.attack == 3
#     assert imp.health == 4

#     initialized_game.start_of_game()
#     initialized_game.single_round()

#     assert imp.attack == 2
#     assert imp.health == 4


def test_wildfire_elemental(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Regular wildfire should only kill one neighbor
    attacker_board.set_minions([WildfireElemental()])
    defender_board.set_minions([PunchingBag(health=1, taunt=False),
                                PunchingBag(health=2, taunt=True),
                                PunchingBag(health=3, taunt=False)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert len(defender_board.minions) == 1

    # Golden wildfire should hit both left and right
    attacker_board.set_minions([WildfireElemental(golden=True)])
    defender_board.set_minions([PunchingBag(taunt=False),
                                PunchingBag(health=1, taunt=True),
                                PunchingBag(taunt=False)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert defender_board.minions[0].health == 87
    assert defender_board.minions[1].health == 87

    # If there are no neighbors nothing should happen
    attacker_board.set_minions([WildfireElemental()])
    defender_board.set_minions([PunchingBag(health=2, taunt=True)])
    initialized_game.start_of_game(0)
    initialized_game.single_round()
    assert len(defender_board.minions) == 0