"""hexhold — hex-tile flipping puzzle (Reversi-style, hex grid)."""
import random

# q,r axial coords for radius-2 hex board (19 cells)
def board_cells(radius=2):
    cells = []
    for q in range(-radius, radius + 1):
        for r in range(-radius, radius + 1):
            s = -q - r
            if abs(s) <= radius:
                cells.append((q, r))
    return sorted(cells)

DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]

class HexHoldError(ValueError):
    pass

class Game:
    def __init__(self, radius=2, seed=0):
        self.cells = set(board_cells(radius))
        self.board = {}
        # seed a 2x2 center cluster so the game always has moves (rotated by seed)
        cluster = [(0, 0), (1, 0), (0, 1), (1, 1)]
        rot = seed % 4
        cluster = cluster[rot:] + cluster[:rot]
        self.board[cluster[0]] = "X"
        self.board[cluster[1]] = "X"
        self.board[cluster[2]] = "O"
        self.board[cluster[3]] = "O"
        self.turn = "X"
        self.winner = None
        self._check()

    def flips_for(self, q, r, player=None):
        player = player or self.turn
        other = "O" if player == "X" else "X"
        if (q, r) not in self.cells or (q, r) in self.board:
            return []
        flips = []
        for dq, dr in DIRS:
            line = []
            cq, cr = q + dq, r + dr
            while (cq, cr) in self.cells and self.board.get((cq, cr)) == other:
                line.append((cq, cr)); cq += dq; cr += dr
            if line and self.board.get((cq, cr)) == player:
                flips.extend(line)
        return flips

    def legal_moves(self, player=None):
        player = player or self.turn
        return sorted(c for c in self.cells if self.flips_for(*c, player))

    def play(self, q, r):
        if self.winner: raise HexHoldError("game over")
        flips = self.flips_for(q, r)
        if not flips: raise HexHoldError("illegal move")
        self.board[(q, r)] = self.turn
        for c in flips: self.board[c] = self.turn
        self.turn = "O" if self.turn == "X" else "X"
        self._check()
        return flips

    def ai_move(self):
        moves = self.legal_moves()
        if not moves: return None
        other = "O" if self.turn == "X" else "X"
        best, best_score = None, -1
        for m in moves:
            score = len(self.flips_for(*m))
            # tie-break: prefer cell with more neighbours
            score += sum(1 for d in DIRS if (m[0]+d[0], m[1]+d[1]) in self.cells) * 0.01
            if score > best_score: best, best_score = m, score
        self.play(*best)
        return best

    def scores(self):
        return {"X": sum(1 for v in self.board.values() if v == "X"),
                "O": sum(1 for v in self.board.values() if v == "O"),
                "empty": len(self.cells) - len(self.board)}

    def _check(self):
        if not self.board:
            return
        if not self.legal_moves("X") and not self.legal_moves("O"):
            s = self.scores()
            self.winner = "draw" if s["X"] == s["O"] else ("X" if s["X"] > s["O"] else "O")
            return
        # side that cannot move passes
        if not self.legal_moves(self.turn):
            self.turn = "O" if self.turn == "X" else "X"
            if not self.legal_moves(self.turn):
                s = self.scores()
                self.winner = "draw" if s["X"] == s["O"] else ("X" if s["X"] > s["O"] else "O")

def render(g):
    rows = {}
    for (q, r) in g.cells:
        rows.setdefault(r, {})[q] = g.board.get((q, r), ".")
    lines = []
    for r in sorted(rows):
        indent = " " * (r + 2)
        cells = [rows[r].get(q, " ") for q in sorted(rows[r])]
        lines.append(f"{indent}" + " ".join(cells))
    lines.append(f"scores: {g.scores()}  turn: {g.turn}" + (f"  winner: {g.winner}" if g.winner else ""))
    return "\n".join(lines)

def main():
    g = Game()
    print("HexHold — flip enemy hexes by sandwiching them. You are X.")
    print(render(g))
    while not g.winner:
        moves = g.legal_moves()
        if not moves:
            print("No moves for X."); break
        print("Legal:", moves)
        raw = input("move q,r > ").strip()
        try:
            q, r = map(int, raw.split(","))
        except ValueError:
            print("Format: q,r  (e.g. 0,0)"); continue
        try:
            g.play(q, r)
        except HexHoldError as e:
            print(e); continue
        print(render(g))
        if g.winner: break
        m = g.ai_move()
        print(f"AI plays {m}")
        print(render(g))
    print("Game over:", g.winner, g.scores())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
