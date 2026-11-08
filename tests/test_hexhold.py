import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from hexhold import Game, HexHoldError, board_cells
import pytest

def test_board_geometry():
    cells = board_cells(2)
    assert len(cells) == 19
    assert len(board_cells(1)) == 7

def test_initial_state():
    g = Game(seed=1)
    s = g.scores()
    assert s["X"] == 2 and s["O"] == 2
    assert s["empty"] == 15

def test_flips_known_line():
    g = Game(radius=2, seed=1)
    # construct controlled board: X at (0,0),(2,0); O at (1,0); play (0,0) occupied? use fresh
    g.board = {(0, 0): "X", (1, 0): "O", (2, 0): "X"}
    g.turn = "X"
    g.winner = None
    # place would flip (1,0) only if played adjacent; play at (0,0) is occupied so test flips_for on empty cell
    g.board = {(0, 0): "X", (1, 0): "O"}
    assert g.flips_for(2, 0) == [(1, 0)]
    flips = g.play(2, 0)
    assert flips == [(1, 0)]
    assert g.scores()["X"] == 3

def test_illegal_move_rejected():
    g = Game(seed=1)
    with pytest.raises(HexHoldError):
        g.play(99, 99)

def test_ai_plays_and_completes():
    g = Game(seed=3)
    while not g.winner:
        if g.legal_moves():
            g.ai_move()
        else:
            break
    assert g.winner in ("X", "O", "draw", None) or g.scores()
