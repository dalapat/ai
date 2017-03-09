# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

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

def genericSearch(problem, container, push):
    
    visited = {}
    push(container, (problem.getStartState(), [], 0), 0)
    
    while not container.isEmpty():
        state, path, cost = container.pop()
        
        if problem.isGoalState(state):
            return path

        if not state in visited:
            visited[state] = state
            for successor in problem.getSuccessors(state):
                state = (successor[0], path + [successor[1]], cost + successor[2])
                push(container, state, cost + successor[2])
                
    return []

def depthFirstSearch(problem):
    """Search the deepest nodes in the search tree first."""

    container = util.Stack()
    def push(container, state, cost):
        container.push(state)
    return genericSearch(problem, container, push)

    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    container = util.Queue()
    def push(container, state, cost):
        container.push(state)
    return genericSearch(problem, container, push)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    container = util.PriorityQueue()
    def push(container, state, cost):
        container.push(state, cost)
    return genericSearch(problem, container, push)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    container = util.PriorityQueue()
    def push(container, state, cost):
        cost = cost + heuristic(state[0], problem)
        container.push(state, cost)
    return genericSearch(problem, container, push)

def iterativeDeepening(problem):
    limit = 0
    found = False
    path = []
    while not found:
        path, found = depthLimitedSearch(problem, limit)
        limit += 1
    return path

def depthLimitedSearch(problem, limit):
    curr_level = 0
    stack = util.Stack()
    start_state = problem.getStartState()
    path = []
    found = False
    stack.push((start_state, path, 0, 0))
    visited = {}
    while not stack.isEmpty():
        curr_state, path, cost, curr_depth = stack.pop()
        if curr_depth > limit:
            break
        if problem.isGoalState(curr_state):
            found = True
            break
        visited[curr_state] = curr_state
        successors = problem.getSuccessors(curr_state)
        for successor in successors:
            state, p, cost = successor
            if state not in visited:
                visited[state] = state
                stack.push((state, path + [p], cost, curr_depth + 1))
    return [path, found]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
