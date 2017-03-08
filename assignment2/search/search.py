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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    stack = util.Stack()
    start_state = problem.getStartState()
    path = []
    visited = {}
    stack.push((start_state, path, 1))
    while not stack.isEmpty():
        curr_state, path, cost = stack.pop()
        visited[curr_state] = curr_state
        if problem.isGoalState(curr_state): break
        successors = problem.getSuccessors(curr_state)
        for successor in successors:
            if successor[0] not in visited:
                stack.push((successor[0], path + [successor[1]], 1))
                # visited[curr_state] = curr_state
    return path

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    queue = util.Queue()
    start_state = problem.getStartState()
    path = []
    visited = {}
    queue.push((start_state, path, 1))
    while not queue.isEmpty():
        curr_state, path, cost = queue.pop()
        visited[curr_state] = curr_state
        if problem.isGoalState(curr_state): break
        successors = problem.getSuccessors(curr_state)
        for successor in successors:
            if successor[0] not in visited:
                visited[successor[0]] = successor[0]
                queue.push((successor[0], path + [successor[1]], 1))
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    q = util.PriorityQueue()
    start_state = problem.getStartState()
    path = []
    visited = {}
    q.push((start_state, path, 0), 0)
    while not q.isEmpty():
        #curr_state, path, cost = q.pop()
        temp = q.pop()
        curr_state = temp[0]
        path = temp[1]
        cost = temp[2]
        if curr_state in visited:
            prior_node = visited[curr_state]
            if problem.getCostOfActions(path) < prior_node[2]:
                prior_node[1] = path
                prior_node[2] = problem.getCostOfActions(path)
                visited[curr_state] = prior_node
        else:
            visited[curr_state] = [curr_state, path, cost]
        if problem.isGoalState(curr_state): break
        successors = problem.getSuccessors(curr_state)
        for successor in successors:
            state, p, c = successor
            to_push = [state, path + [p], cost + c]
            if state not in visited:
                visited[state] = to_push
                q.push(to_push, cost + c)

            else:
                if cost + c < visited[state][2]:
                    visited[state] = to_push
                    q.push(to_push, cost + c)

    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    q = util.PriorityQueue()
    start_state = problem.getStartState()
    path = []
    visited = {}
    q.push((start_state, path, 0), 0)
    while not q.isEmpty():
        curr_state, path, cost = q.pop()

        if curr_state in visited:
            prior_node = visited[curr_state]
            if problem.getCostOfActions(path) < prior_node[2]:
                prior_node[1] = path
                prior_node[2] = problem.getCostOfActions(path)
                visited[curr_state] = prior_node
        else:
            visited[curr_state] = [curr_state, path, cost]
        if problem.isGoalState(curr_state): break
        successors = problem.getSuccessors(curr_state)
        for successor in successors:
            state, p, c = successor
            to_push = [state, path + [p], \
                       problem.getCostOfActions(path + [p]) + heuristic(state, problem)]
            if state not in visited:
                visited[state] = to_push
                q.push(to_push, \
                       problem.getCostOfActions(path + [p]) + heuristic(state, problem))

            else:
                if problem.getCostOfActions(path + [p]) < visited[state][2]:
                    visited[state] = to_push
                    q.push(to_push, problem.getCostOfActions(path + [p]) + heuristic(state, problem))

    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
