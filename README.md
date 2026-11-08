# hexhold — hex-tile flipping puzzle

Original Reversi-style puzzle game on a hex grid (radius-2 board, 19 cells). Sandwich enemy hexes to flip them; beat the AI.

**Problem:** Casual players want a compact, original board game with clear win/lose and a real challenge without installs.

**Key features:** axial hex coordinates, sandwich-flip rules, legal-move hints, greedy AI opponent with neighbour tie-break, pass handling, draw detection.

## Quick start
```bash
pip install -e .
python -m hexhold
# enter a move as q,r (e.g. 0,0)
```

## How it works
Play X; AI plays O. A move is legal only if it brackets ≥1 enemy hex between the new tile and an existing friendly hex. Game ends when neither side can move; majority wins.

## Testing
```bash
python -m pytest tests -q
```

## Limitations
Terminal UI only; greedy AI (no search); fixed radius-2 board.

## License
MIT (see LICENSE).
