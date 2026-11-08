# Results — hexhold
## Environment
- OS: Windows, Runtime: Python 3.14.3
## Validation
- install: PASS
- unit tests: PASS (5 tests)
- demo run: PASS (non-interactive AI move)
## Commands executed
```
pip install -e .
python -m pytest tests -q
python -c "from hexhold import Game, render; g=Game(seed=7); print(render(g)); print(g.ai_move()); print(render(g))"
```
## Observed result
Board renders 19-cell hex grid, scores X2/O2, AI move (-1,1) flips to X4/O1, winner None (game continues).
## Generated artifacts
- `results/demo.txt`
## Known limitations
Terminal UI; greedy AI; interactive play not automated in demo.
