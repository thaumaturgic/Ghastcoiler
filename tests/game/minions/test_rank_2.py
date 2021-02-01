from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_1 import \
    MurlocTidehunter, Alleycat
from ghastcoiler.minions.rank_2 import \
    GlyphGuardian, KaboomBot, MurlocWarleader, OldMurkEye, SpawnofNZoth,\
    SelflessHero, PackLeader, TormentedRitualist, YoHoOgre


def test_kaboombot_deathrattle(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.add_minion(KaboomBot())
    defender_board.add_minion(PunchingBag(attack=2))
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender_board.minions[0].defense == 94

    # TODO: Test more complicated scenarios where boom bot kills other deathrattle minions
    attacker_board.set_minions([KaboomBot(), KaboomBot()])
    defender_board.set_minions([KaboomBot(), KaboomBot()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(defender_board.minions) == 0
    assert len(attacker_board.minions) == 0

    # TODO: Test golden bomb, make sure it doesnt bomb already dead minions


def test_murloc_war_leader(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.add_minion(MurlocWarleader())
    attacker_board.add_minion(MurlocWarleader())
    attacker_board.add_minion(KaboomBot())
    defender_board.add_minion(MurlocWarleader())

    # Friendly Warleaders should buff each other
    assert attacker_board.minions[0].attack == 5
    assert attacker_board.minions[1].attack == 5
    # Warleader should not buff non-murlocs
    assert attacker_board.minions[2].attack == 2

    initialized_game.attack(attacker_board.minions[0], defender_board.select_defending_minion())
    initialized_game.check_deaths(attacker_board, defender_board)
    # Warleader buff should wear off
    assert attacker_board.minions[0].attack == 3


def test_old_murk_eye(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_murkeye = OldMurkEye()
    punching_bag = PunchingBag()

    attacker_board.set_minions([attacker_murkeye, MurlocTidehunter()])
    defender_board.add_minion(punching_bag)

    # Friendly board murlocs should buff
    initialized_game.attack(attacker_murkeye, punching_bag)
    assert attacker_murkeye.attack == 3

    # Enemy board murlocs should buff
    defender_board.add_minion(MurlocTidehunter())
    initialized_game.attack(attacker_murkeye, punching_bag)
    assert attacker_murkeye.attack == 4

    # Removal of enemy board murlocs should lower attack
    defender_board.minions[1].dead = True
    initialized_game.check_deaths(attacker_board, defender_board)
    initialized_game.attack(attacker_murkeye, punching_bag)
    assert attacker_murkeye.attack == 3

    # Removal of friendly board murlocs should lower attack (note: murlock is the one attacked, to test on_attacked)
    attacker_board.minions[1].dead = True
    initialized_game.check_deaths(attacker_board, defender_board)
    initialized_game.attack(punching_bag, attacker_murkeye)
    assert attacker_murkeye.attack == 2

    # TODO: Test golden murkeye?


def test_glyph_guardian(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([GlyphGuardian(), GlyphGuardian()])
    defender_board.set_minions([PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert attacker_board.minions[0].attack == 4


def test_spawn_of_nzoth(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    spawn = SpawnofNZoth()
    attacker_board.set_minions([spawn, MurlocTidehunter(), MurlocTidehunter()])
    spawn.dead = True
    initialized_game.check_deaths(attacker_board, defender_board)
    assert attacker_board.minions[0].attack == 3 and attacker_board.minions[0].defense == 2
    assert attacker_board.minions[1].attack == 3 and attacker_board.minions[1].defense == 2


def test_selfless_hero(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    hero = SelflessHero()
    attacker_board.set_minions([hero, SpawnofNZoth(), SpawnofNZoth(), SpawnofNZoth()])
    hero.dead = True
    initialized_game.check_deaths(attacker_board, defender_board)
    shielded_minions = sum(1 for minion in attacker_board.minions if minion.divine_shield)
    assert shielded_minions == 1

    # Test golden hero
    golden_hero = SelflessHero(golden=True)
    attacker_board.set_minions([golden_hero, SpawnofNZoth(), SpawnofNZoth(), SpawnofNZoth()])
    golden_hero.dead = True
    initialized_game.check_deaths(attacker_board, defender_board)
    shielded_minions = sum(1 for minion in attacker_board.minions if minion.divine_shield)
    assert shielded_minions == 2


def test_pack_leader(initialized_game):
    attacker_board = initialized_game.player_board[0]
    beast = Alleycat()
    attacker_board.add_minion(PackLeader())
    attacker_board.add_minion(beast)
    assert beast.attack == 3


def test_tormented_ritualist(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.set_minions([Alleycat(), Alleycat(), Alleycat(), Alleycat()])
    defender_board.set_minions([Alleycat(), TormentedRitualist(), Alleycat()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert defender_board.minions[0].attack == 2 and defender_board.minions[0].defense == 2
    assert defender_board.minions[2].attack == 2 and defender_board.minions[2].defense == 2
    # TODO: Test when no minions are to the left and/or right


def test_yo_ho_ogre(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    # Ogre should attack twice in a single round
    attacker_board.set_minions([PunchingBag(attack=1), PunchingBag(taunt=True), PunchingBag()])
    defender_board.set_minions([YoHoOgre(), PunchingBag()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert attacker_board.minions[0].defense == 98
    assert attacker_board.minions[1].defense == 98

    # Two pirates, they should kill each other in repeated attacks in one round
    attacker_board.set_minions([YoHoOgre()])
    defender_board.set_minions([YoHoOgre()])
    initialized_game.start_of_game()
    initialized_game.single_round()
    assert len(attacker_board.minions) == 0 and len(defender_board.minions) == 0
