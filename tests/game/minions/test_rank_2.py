from ghastcoiler.minions.test_minions import PunchingBag
from ghastcoiler.minions.rank_2 import GlyphGuardian, HarvestGolem, Imprisoner, KaboomBot, KindlyGrandmother, MurlocWarleader, OldMurkEye, ScavengingHyena, SpawnofNZoth
from ghastcoiler.minions.rank_1 import MurlocTidehunter, Alleycat

def test_kaboombot_deathrattle(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    kaboom_bot = KaboomBot()
    glyph_guardian = GlyphGuardian()

    attacker_board.add_minion(kaboom_bot)
    defender_board.add_minion(glyph_guardian)

    initialized_game.attack(kaboom_bot, glyph_guardian)
    assert glyph_guardian.defense == 2
    initialized_game.check_deaths(attacker_board, defender_board)
    assert glyph_guardian.defense == -2


def test_murloc_war_leader(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    attacker_board.add_minion(MurlocWarleader())
    attacker_board.add_minion(MurlocWarleader())
    attacker_board.add_minion(KaboomBot())
    defender_board.add_minion(MurlocWarleader())

    # Warleaders should buff each other
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

    attacker_board.add_minion(attacker_murkeye)
    attacker_board.add_minion(MurlocTidehunter())
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

    #TODO: Test golden murkeye?

def test_glyph_guardian(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    glyph_guardian = GlyphGuardian()
    punching_bag = PunchingBag()

    attacker_board.add_minion(glyph_guardian)
    defender_board.add_minion(punching_bag)

    initialized_game.attack(glyph_guardian, punching_bag)
    assert glyph_guardian.attack == 4


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

def test_spawn_of_nzoth(initialized_game):
    attacker_board = initialized_game.player_board[0]
    defender_board = initialized_game.player_board[1]

    spawn = SpawnofNZoth()
    murloc = MurlocTidehunter()

    attacker_board.add_minion(spawn)
    attacker_board.add_minion(murloc)
    spawn.dead = True
    initialized_game.check_deaths(attacker_board, defender_board)
    assert murloc.attack == 3
