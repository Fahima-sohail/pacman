AI2002 — Artificial Intelligence Assignment 01
Pacman Search Game

TEAM
Fahima Sohail Ahmed — 24i-3116
Wania Bakhat — 24i-3040

COURSE
Artificial Intelligence (AI2002)
Submitted to: Dr. Muhammad Bilal
FAST-NUCES Islamabad

SYSTEM / ENVIRONMENT
Operating System: Windows 11
Python: Python 3.13.x (the supplied project contains CPython 3.13 bytecode)
CPU / RAM: Not recorded in the submitted project evidence; add the exact values before final submission if required.

PROJECT STRUCTURE
- search.py              Core search algorithms and CSV trace logging
- searchAgents.py        Corners, Food Search, heuristics, and agent wrappers
- layouts/i243116Search.lay   Original custom maze
- evidence/              CSV traces and screenshots
- report.pdf             Assignment report
- README.txt             This file

IMPLEMENTED SEARCH ALGORITHMS
1. Depth-First Search (DFS)
2. Breadth-First Search (BFS)
3. Uniform-Cost Search (UCS)
4. Greedy Best-First Search (GBFS)
5. A* Search

MULTI-GOAL / FOOD TASKS
- CornersProblem
- cornersHeuristic
- FoodSearchProblem
- foodHeuristic
- AnyFoodSearchProblem
- ClosestDotSearchAgent

TRACE LOGGING
The evidence/ directory contains:
- dfs_trace.csv
- bfs_trace.csv
- ucs_trace.csv
- gbfs_trace.csv
- astar_trace.csv

Each trace uses the required fields:
iteration, expanded_state, parent, action, generated_successors,
frontier_before, frontier_after, explored, g, h, f

MAIN RUN COMMANDS
Sanity check:
python pacman.py

DFS:
python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=dfs

BFS:
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=bfs

UCS:
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDenselyMaze -p SearchAgent -a fn=ucs
python pacman.py -l stayEastSearch -p StayEastSearchAgent

GBFS:
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=gbfs,heuristic=manhattanHeuristic

A*:
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=nullHeuristic
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

Corners:
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z .5

Food:
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent

AUTOGRADER COMMANDS
python autograder.py -q q1
python autograder.py -q q2
python autograder.py -q q3
python autograder.py -q q4
python autograder.py -q q5
python autograder.py -q q6
python autograder.py -q q7
python autograder.py -q q8
python autograder.py

NOTE
The assignment handout and the supplied autograder use different task/question numbering.
In the supplied autograder, q4 tests A* rather than GBFS.

SUBMISSION CHECKLIST
- Modified search.py
- Modified searchAgents.py
- Custom layout i243116Search.lay
- evidence CSV trace files
- evidence screenshots
- report.pdf
- README.txt
