# search.py
# ---------


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import os
import csv

# --------------------------------------------------------------------------
# CSV TRACE LOGGER (Section 3 of the assignment)
# --------------------------------------------------------------------------
# Every algorithm below calls this ONE helper function at the very end of its
# run. It just writes out, row by row, everything that happened while the
# algorithm was searching, into a CSV file inside the evidence/ folder.
#
# Each "row" is a small dictionary with the exact column names the
# assignment asks for:
#   iteration, expanded_state, parent, action, generated_successors,
#   frontier_before, frontier_after, explored, g, h, f
# --------------------------------------------------------------------------

CSV_COLUMNS = ["iteration", "expanded_state", "parent", "action",
               "generated_successors", "frontier_before", "frontier_after",
               "explored", "g", "h", "f"]

def writeSearchLog(algorithmName, logRows):
    """
    Saves the trace of one search run to evidence/<algorithmName>_trace.csv

    algorithmName: short string like "dfs", "bfs" or "ucs" -> used as the file name
    logRows: a list of dictionaries, one per expanded node, using the
             column names listed in CSV_COLUMNS above.
    """
    # Make the evidence/ folder if it isn't there yet.
    if not os.path.exists("evidence"):
        os.makedirs("evidence")

    filePath = os.path.join("evidence", algorithmName + "_trace.csv")

    with open(filePath, mode="w", newline="") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in logRows:
            writer.writerow(row)

    print("[search.py] wrote %d rows to %s" % (len(logRows), filePath))


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    HOW THIS WORKS (DFS):
    - We use a Stack (LIFO -> Last In, First Out) as the fringe/frontier.
      That means the most recently discovered state is always the next one
      we explore, which is exactly what "go deep first" means.
    - Every item we push on the stack is a pair: (state, pathOfActionsSoFar).
      Storing the whole path with the state is the easiest way to be able
      to just return the path the moment we reach the goal.
    - "explored" is a set of states we have already expanded. Before we
      expand any state popped off the stack, we check if it's already in
      explored - if so we just skip it. This is what makes it a strict
      GRAPH search (tree search would keep re-expanding the same states
      forever on mazes that have loops).
    """
    # ---------- SET UP THE FRINGE (stack) ----------
    fringe = util.Stack()
    startState = problem.getStartState()
    fringe.push((startState, []))          # (state, path_of_actions_to_reach_it)

    explored = set()                       # states we've already expanded

    # parentOf is ONLY used for the CSV log (Section 3), it does not affect
    # the search itself. It remembers: state -> (parentState, actionUsed)
    parentOf = {startState: (None, None)}

    logRows = []        # collects one row per expansion, written to CSV at the end
    iteration = 0

    while not fringe.isEmpty():
        frontierBefore = len(fringe.list)      # frontier size BEFORE this pop
        state, path = fringe.pop()

        # Same state can be pushed more than once before being popped -
        # if we already expanded it once, just move on.
        if state in explored:
            continue

        iteration += 1
        explored.add(state)
        parentState, actionUsed = parentOf[state]

        # ---- Goal test happens right when we EXPAND (pop) a node ----
        if problem.isGoalState(state):
            logRows.append({
                "iteration": iteration, "expanded_state": state,
                "parent": parentState, "action": actionUsed,
                "generated_successors": [],       # goal reached, nothing new expanded
                "frontier_before": frontierBefore, "frontier_after": frontierBefore,
                "explored": len(explored), "g": len(path), "h": 0, "f": len(path),
            })
            writeSearchLog("dfs", logRows)
            return path

        # ---- Expand: look at every successor of this state ----
        generated = []
        for succState, action, stepCost in problem.getSuccessors(state):
            generated.append(succState)
            if succState not in explored:
                fringe.push((succState, path + [action]))
                if succState not in parentOf:      # first time we've seen it
                    parentOf[succState] = (state, action)

        frontierAfter = len(fringe.list)           # frontier size AFTER pushing successors

        logRows.append({
            "iteration": iteration, "expanded_state": state,
            "parent": parentState, "action": actionUsed,
            "generated_successors": generated,
            "frontier_before": frontierBefore, "frontier_after": frontierAfter,
            "explored": len(explored), "g": len(path), "h": 0, "f": len(path),
        })

    # Fringe emptied out and we never found the goal -> no solution exists.
    writeSearchLog("dfs", logRows)
    return None

def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.

    HOW THIS WORKS (BFS):
    - We use a Queue (FIFO -> First In, First Out) as the fringe/frontier.
      That means states are explored in the exact order they were
      discovered, layer by layer, which is what guarantees BFS finds the
      SHORTEST path (in number of steps) on a maze where every move costs 1.
    - "visited" marks a state as soon as it is DISCOVERED (i.e. the moment
      we push it onto the queue), not when it's later popped/expanded.
      This is the standard BFS trick, and it directly satisfies the
      requirement: "avoid re-enqueuing states already in the frontier or
      explored set" - because a state only ever gets pushed once, the very
      first time we come across it.
    """
    # ---------- SET UP THE FRINGE (queue) ----------
    fringe = util.Queue()
    startState = problem.getStartState()
    fringe.push((startState, []))

    visited = {startState}                 # states already pushed (frontier + explored)
    parentOf = {startState: (None, None)}  # only used for the CSV log

    logRows = []
    iteration = 0

    while not fringe.isEmpty():
        frontierBefore = len(fringe.list)
        state, path = fringe.pop()         # dequeue the oldest discovered state
        iteration += 1
        parentState, actionUsed = parentOf[state]

        # ---- Goal test happens when we EXPAND (pop) a node ----
        if problem.isGoalState(state):
            logRows.append({
                "iteration": iteration, "expanded_state": state,
                "parent": parentState, "action": actionUsed,
                "generated_successors": [],
                "frontier_before": frontierBefore, "frontier_after": frontierBefore,
                "explored": iteration, "g": len(path), "h": 0, "f": len(path),
            })
            writeSearchLog("bfs", logRows)
            return path

        # ---- Expand: look at every successor of this state ----
        generated = []
        for succState, action, stepCost in problem.getSuccessors(state):
            generated.append(succState)
            if succState not in visited:
                visited.add(succState)             # reserve its spot right away
                parentOf[succState] = (state, action)
                fringe.push((succState, path + [action]))

        frontierAfter = len(fringe.list)

        # Since every state is only ever pushed once, the number of states
        # we've popped so far (iteration) is exactly the number of states
        # we've fully explored/expanded.
        logRows.append({
            "iteration": iteration, "expanded_state": state,
            "parent": parentState, "action": actionUsed,
            "generated_successors": generated,
            "frontier_before": frontierBefore, "frontier_after": frontierAfter,
            "explored": iteration, "g": len(path), "h": 0, "f": len(path),
        })

    writeSearchLog("bfs", logRows)
    return None

def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.

    HOW THIS WORKS (UCS):
    - We use a PriorityQueue as the fringe/frontier, ordered by g(n): the
      total accumulated step cost from the start state to that node.
      Whatever is cheapest to reach so far comes out first.
    - bestCost[state] remembers the cheapest g(n) found SO FAR for that
      state. If we later find an even cheaper way to reach a state that's
      already sitting on the fringe, we call fringe.update(...), which
      (see util.py) either lowers its priority if it's already in the
      queue, or pushes it fresh if it isn't there yet. That's exactly the
      "update frontier if a cheaper path is found" requirement.
    - We still keep an "explored" set and skip a state if we pop it after
      it's already been fully expanded once - this stops us from expanding
      the same state twice through two different old, stale queue entries.
    """
    # ---------- SET UP THE FRINGE (priority queue, priority = g(n)) ----------
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    fringe.push(startState, 0)

    bestCost = {startState: 0}             # state -> cheapest g(n) found so far
    bestPath = {startState: []}            # state -> matching path of actions
    parentOf = {startState: (None, None)}  # only used for the CSV log

    explored = set()
    logRows = []
    iteration = 0

    while not fringe.isEmpty():
        frontierBefore = len(fringe.heap)
        state = fringe.pop()               # cheapest g(n) comes out first

        # This state might already have been expanded through an older,
        # more expensive queue entry - if so, skip it.
        if state in explored:
            continue

        iteration += 1
        explored.add(state)

        path = bestPath[state]
        g = bestCost[state]
        parentState, actionUsed = parentOf[state]

        # ---- Goal test happens when we EXPAND (pop) a node ----
        # (Safe to do here because UCS always pops the cheapest node left,
        # so the first time we pop the goal, that IS the optimal path.)
        if problem.isGoalState(state):
            logRows.append({
                "iteration": iteration, "expanded_state": state,
                "parent": parentState, "action": actionUsed,
                "generated_successors": [],
                "frontier_before": frontierBefore, "frontier_after": frontierBefore,
                "explored": len(explored), "g": g, "h": 0, "f": g,
            })
            writeSearchLog("ucs", logRows)
            return path

        # ---- Expand: look at every successor and its step cost ----
        generated = []
        for succState, action, stepCost in problem.getSuccessors(state):
            generated.append(succState)
            newCost = g + stepCost

            # Only bother updating the fringe if this is either a brand new
            # state, or a cheaper way to reach a state we already know about.
            if succState not in explored and (succState not in bestCost or newCost < bestCost[succState]):
                bestCost[succState] = newCost
                bestPath[succState] = path + [action]
                parentOf[succState] = (state, action)
                fringe.update(succState, newCost)   # push new OR lower its priority

        frontierAfter = len(fringe.heap)

        logRows.append({
            "iteration": iteration, "expanded_state": state,
            "parent": parentState, "action": actionUsed,
            "generated_successors": generated,
            "frontier_before": frontierBefore, "frontier_after": frontierAfter,
            "explored": len(explored), "g": g, "h": 0, "f": g,
        })

    writeSearchLog("ucs", logRows)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def greedyBestFirstSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest heuristic value h(n) first.

    HOW THIS WORKS (GBFS):
    - We use a PriorityQueue as the fringe/frontier, but unlike UCS, the
      priority is ONLY the heuristic value h(n) - how close the heuristic
      THINKS this state is to the goal. We completely ignore g(n), the
      cost already spent getting there. That's what makes this "greedy":
      it always jumps toward whatever looks closest to the goal right now,
      even if that path turns out to be expensive overall.
    - Because of that, GBFS is fast but NOT guaranteed to find the
      cheapest path (that's what makes it different from A*, which uses
      g(n) + h(n) together). This is expected, normal behaviour for GBFS.
    - The heuristic function is passed in as an argument (not hardcoded),
      which is what lets the command line switch between heuristics, e.g.
      "-a fn=gbfs,heuristic=manhattanHeuristic".
    - We still do a strict graph search with an explicit explored set,
      exactly like DFS/BFS/UCS, so we never expand the same state twice.
    """
    # ---------- SET UP THE FRINGE (priority queue, priority = h(n) only) ----------
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    startH = heuristic(startState, problem)
    fringe.push(startState, startH)

    bestPath = {startState: []}            # state -> path of actions found so far
    bestG = {startState: 0}                # state -> accumulated cost g(n) (logging only)
    parentOf = {startState: (None, None)}  # only used for the CSV log

    explored = set()
    logRows = []
    iteration = 0

    while not fringe.isEmpty():
        frontierBefore = len(fringe.heap)
        state = fringe.pop()               # lowest h(n) comes out first

        # Skip states we've already fully expanded (can happen if a state
        # was pushed more than once before being popped).
        if state in explored:
            continue

        iteration += 1
        explored.add(state)

        path = bestPath[state]
        g = bestG[state]
        h = heuristic(state, problem)
        parentState, actionUsed = parentOf[state]

        # ---- Goal test happens when we EXPAND (pop) a node ----
        if problem.isGoalState(state):
            logRows.append({
                "iteration": iteration, "expanded_state": state,
                "parent": parentState, "action": actionUsed,
                "generated_successors": [],
                "frontier_before": frontierBefore, "frontier_after": frontierBefore,
                "explored": len(explored), "g": g, "h": h, "f": g + h,
            })
            writeSearchLog("gbfs", logRows)
            return path

        # ---- Expand: look at every successor of this state ----
        generated = []
        for succState, action, stepCost in problem.getSuccessors(state):
            generated.append(succState)
            if succState not in explored and succState not in bestPath:
                bestG[succState] = g + stepCost
                bestPath[succState] = path + [action]
                parentOf[succState] = (state, action)
                succH = heuristic(succState, problem)
                fringe.push(succState, succH)      # priority = h(n) ONLY, g(n) plays no part

        frontierAfter = len(fringe.heap)

        logRows.append({
            "iteration": iteration, "expanded_state": state,
            "parent": parentState, "action": actionUsed,
            "generated_successors": generated,
            "frontier_before": frontierBefore, "frontier_after": frontierAfter,
            "explored": len(explored), "g": g, "h": h, "f": g + h,
        })

    writeSearchLog("gbfs", logRows)
    return None



def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.

    HOW THIS WORKS (A*):
    - This is basically UCS and GBFS mixed together. We use a PriorityQueue
      as the fringe/frontier, but the priority is f(n) = g(n) + h(n):
        g(n) = the real accumulated cost to reach this state so far
        h(n) = the heuristic's ESTIMATE of the remaining cost to the goal
      Using both together is what makes A* smart: it won't wander off
      toward something that just "looks close" (like GBFS can), because
      g(n) still counts how expensive it was to get there.
    - Just like UCS, bestCost[state] remembers the cheapest g(n) seen so
      far for that state, and if we find an even cheaper way to reach a
      state that's already sitting on the fringe, we call fringe.update(...)
      to fix its priority instead of leaving a stale, worse entry behind.
    - We keep an explicit "explored" set exactly like the other algorithms,
      so this is a strict graph search.
    - IMPORTANT for optimality: A* is only guaranteed to find the cheapest
      path if the heuristic is admissible (never overestimates the true
      remaining cost) and consistent. With nullHeuristic (h=0 always),
      this function behaves exactly like UCS.
    """
    # ---------- SET UP THE FRINGE (priority queue, priority = f(n) = g+h) ----------
    fringe = util.PriorityQueue()
    startState = problem.getStartState()
    startH = heuristic(startState, problem)
    fringe.push(startState, 0 + startH)

    bestCost = {startState: 0}             # state -> cheapest g(n) found so far
    bestPath = {startState: []}            # state -> matching path of actions
    parentOf = {startState: (None, None)}  # only used for the CSV log

    explored = set()
    logRows = []
    iteration = 0

    while not fringe.isEmpty():
        frontierBefore = len(fringe.heap)
        state = fringe.pop()               # lowest f(n) = g(n)+h(n) comes out first

        # This state might already have been expanded through an older,
        # more expensive queue entry - if so, skip it.
        if state in explored:
            continue

        iteration += 1
        explored.add(state)

        path = bestPath[state]
        g = bestCost[state]
        h = heuristic(state, problem)
        parentState, actionUsed = parentOf[state]

        # ---- Goal test happens when we EXPAND (pop) a node ----
        # (Safe to do here, same reasoning as UCS, because a consistent
        # heuristic guarantees f(n) never decreases as we go deeper, so the
        # first time the goal is popped, that IS the optimal path.)
        if problem.isGoalState(state):
            logRows.append({
                "iteration": iteration, "expanded_state": state,
                "parent": parentState, "action": actionUsed,
                "generated_successors": [],
                "frontier_before": frontierBefore, "frontier_after": frontierBefore,
                "explored": len(explored), "g": g, "h": h, "f": g + h,
            })
            writeSearchLog("astar", logRows)
            return path

        # ---- Expand: look at every successor and its step cost ----
        generated = []
        for succState, action, stepCost in problem.getSuccessors(state):
            generated.append(succState)
            newCost = g + stepCost

            # Only bother updating the fringe if this is either a brand new
            # state, or a cheaper way to reach a state we already know about.
            if succState not in explored and (succState not in bestCost or newCost < bestCost[succState]):
                bestCost[succState] = newCost
                bestPath[succState] = path + [action]
                parentOf[succState] = (state, action)
                succF = newCost + heuristic(succState, problem)   # f(n) = g(n) + h(n)
                fringe.update(succState, succF)

        frontierAfter = len(fringe.heap)

        logRows.append({
            "iteration": iteration, "expanded_state": state,
            "parent": parentState, "action": actionUsed,
            "generated_successors": generated,
            "frontier_before": frontierBefore, "frontier_after": frontierAfter,
            "explored": len(explored), "g": g, "h": h, "f": g + h,
        })

    writeSearchLog("astar", logRows)
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
gbfs = greedyBestFirstSearch