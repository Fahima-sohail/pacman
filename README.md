# AI2002 — Assignment 01: Pacman Search Game

**Course:** Artificial Intelligence (AI2002)
**Total Marks:** 150
**Deadline:** 27th September 2026
**Work Mode:** Group of 2–3

## Team

| Name | Roll Number | Tasks Owned |
|---|---|---|
| _(add your name)_ | _(roll no.)_ | Tasks 1–4 (DFS, BFS, UCS, GBFS) + CSV logging |
| _(add name)_ | _(roll no.)_ | Tasks 5–8 (A*, Corners, Food, Custom Layout) |

## Progress

- [x] **Task 1 — Depth-First Search (DFS)** — `search.py`
- [x] **Task 2 — Breadth-First Search (BFS)** — `search.py`
- [x] **Task 3 — Uniform-Cost Search (UCS)** — `search.py`
- [x] **Task 4 — Greedy Best-First Search (GBFS)** — `search.py`
- [x] **CSV Trace Logging** — every run of DFS/BFS/UCS/GBFS writes to `evidence/`
- [ ] **Task 5 — A\* Search** — `search.py`
- [ ] **Task 6 — Corners Problem** — `searchAgents.py`
- [ ] **Task 7 — Food Search / Closest Dot** — `searchAgents.py`
- [ ] **Custom layout** (`layouts/[YourID]Search.lay`) + experiments + report

> Only `search.py` and `searchAgents.py` should ever be edited (plus adding
> the custom `.lay` file). Every other file — `pacman.py`, `game.py`,
> `util.py`, `layout.py`, `graphicsDisplay.py`, `graphicsUtils.py`,
> `textDisplay.py` — is starter code and must **not** be modified.

## Setup

Requires Python 3.7+.

```bash
python3 --version          # confirm Python 3.7+
cd search/search
python3 pacman.py          # sanity check — should launch a game with a random agent
```

## How to run each algorithm

```bash
# Task 1 — DFS
python3 pacman.py -l tinyMaze  -p SearchAgent -a fn=dfs
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

# Task 2 — BFS
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

# Task 3 — UCS
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python3 pacman.py -l mediumMaze -p StayEastSearchAgent   # variable-cost sanity check
python3 pacman.py -l mediumMaze -p StayWestSearchAgent   # variable-cost sanity check

# Task 4 — GBFS
python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic

# Task 5 — A* (once implemented)
python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

Add `-q` to any command to skip the graphics window and just print the text
result (path cost, nodes expanded, win/lose) — much faster while developing.

## Automated tests

```bash
python3 autograder.py -q q1   # DFS
python3 autograder.py -q q2   # BFS
python3 autograder.py -q q3   # UCS
python3 autograder.py -q q4   # A*  (NOTE: this is A*, not GBFS — see below)
python3 autograder.py -q q5   # Corners problem formulation
python3 autograder.py -q q6   # Corners heuristic
python3 autograder.py -q q7   # Food heuristic
python3 autograder.py -q q8   # Closest dot / AnyFoodSearchProblem
python3 autograder.py         # run everything at once
```

> **⚠️ Important mismatch:** the assignment PDF's task numbering does not
> line up with `autograder.py`'s question numbering. The autograder's `q1`–`q3`
> match Tasks 1–3 exactly, but `q4` in the autograder tests **A\* Search**
> (the PDF's Task 5), not GBFS. **There is no automated test for GBFS
> (the PDF's Task 4)** anywhere in `test_cases/` — it has to be checked
> manually by running the commands above and confirming sensible behaviour
> (heuristic-only ordering, usually fewer expansions than BFS/UCS, not
> guaranteed to be the shortest/cheapest path).

## CSV Trace Logging (Section 3 of the assignment)

Every run of DFS, BFS, UCS, or GBFS writes a step-by-step trace to
`evidence/<algorithm>_trace.csv` (e.g. `evidence/dfs_trace.csv`,
`evidence/gbfs_trace.csv`), with the required columns:

```
iteration, expanded_state, parent, action, generated_successors,
frontier_before, frontier_after, explored, g, h, f
```

The file is overwritten each time you run that algorithm, so grab a copy of
the CSVs you want to keep as evidence before running something else. The
logger lives in `search.py` as `writeSearchLog(...)` — if you add A*, call
it the same way the existing algorithms do (see the comments in
`search.py`), using `"astar"` as the algorithm name.

## Final submission checklist (from the assignment)

- [ ] All 5 algorithms implemented and passing their tests
- [ ] `layouts/[YourID]Search.lay` custom maze added
- [ ] All CSVs for every task saved under `evidence/`
- [ ] Screenshots of maze solutions under `evidence/screenshots/`
- [ ] `report.pdf` (6–10 pages, complexity analysis + custom maze experiments)
- [ ] `README.txt` with Python version, run commands, system specs
- [ ] Everything zipped into a single archive matching the structure in the
      assignment PDF
