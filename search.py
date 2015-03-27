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
from util import PriorityQueueWithFunction, Stack


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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # Factory creating appropriate Nodes given parent-Node and successor (state, action, cost)
    nodeFactory = lambda parentNode, successor: Node(parentNode, successor)
    
    # fringe is for DFS, i.e. Nodes with HIGHER depth have lower priority-value and will be popped of the fringe first.
    fringeDFS = PriorityQueueWithFunction(lambda node: -node.depth)
    # Strategy: Already using a DFS fringe; no extra strategy needed, just pop from fringe.
    strategyDFS = lambda fringe: fringe.pop()
    
    result = genericGraphSearch(problem, fringeDFS, strategyDFS, nodeFactory, True)
    return getActionsToThisNode(result)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Factory creating appropriate Nodes given parent-Node and successor (state, action, cost)
    nodeFactory = lambda parentNode, successor: Node(parentNode, successor)
    
    # fringe is for BFS, i.e. Nodes with LOWER depth have lower priority-value and will be popped of the fringe first.
    fringeBFS = PriorityQueueWithFunction(lambda node: node.depth)
    # Strategy: Already using a BFS fringe; no extra strategy needed, just pop from fringe.
    strategyBFS = lambda fringe: fringe.pop()
    
    result = genericGraphSearch(problem, fringeBFS, strategyBFS, nodeFactory, True)
    return getActionsToThisNode(result)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Factory creating appropriate Nodes given parent-Node and successor (state, action, cost)
    nodeFactory = lambda parentNode, successor: UCSNode(parentNode, successor)
    
    # fringe is for UCS, i.e. Nodes with LOWER total-path-cost have lower priority-value and will be popped of the fringe first.
    fringeUCS = PriorityQueueWithFunction(lambda node: node.totalPathCost)
    # Strategy: Already using a BFS fringe; no extra strategy needed, just pop from fringe.
    strategyUCS = lambda fringe: fringe.pop()
    
    result = genericGraphSearch(problem, fringeUCS, strategyUCS, nodeFactory, True)
    return getActionsToThisNode(result)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    # Curry the heuristic to the problem.
    problemHeuristic = lambda state: heuristic(state, problem)
    
    # Factory creating appropriate Nodes given parent-Node and successor (state, action, cost)
    nodeFactory = lambda parentNode, successor: AStarNode(parentNode, successor, problemHeuristic)
    
    # fringe is for AStar, i.e. Nodes with LOWER (total-path-cost+heuristic) have lower priority-value and will be popped of the fringe first.
    fringeAStar = PriorityQueueWithFunction(lambda node: node.totalCost)
    # Strategy: Already using a BFS fringe; no extra strategy needed, just pop from fringe.
    strategyAStar = lambda fringe: fringe.pop()
    
    result = genericGraphSearch(problem, fringeAStar, strategyAStar, nodeFactory, True)
    return getActionsToThisNode(result)


# ---------------- Begin Anton Spaans code: ----------------

class Node:
    def __init__(self, parentNode, successor):
        self.parentNode = parentNode
        self.successor = successor
        
        self.depth = (parentNode.depth + 1) if (parentNode != None) else 0
        
    def getState(self):
        return self.successor[0]
    
    def getAction(self):
        return self.successor[1]
    
    def getCost(self):
        return self.successor[2]
    
class UCSNode(Node):
    def __init__(self, parentNode, successor):
        Node.__init__(self, parentNode, successor)
        self.totalPathCost = (parentNode.totalPathCost + self.getCost()) if (parentNode != None) else self.getCost()

class AStarNode(UCSNode):
    def __init__(self, parentNode, successor, heuristic):
        UCSNode.__init__(self, parentNode, successor)
        self.totalCost = self.totalPathCost + heuristic(self.getState())

def genericGraphSearch(problem, fringe, strategicPop, nodeFactory, isFringeQueue):
    from sets import Set
    
    startState = nodeFactory(None, (problem.getStartState(), None, 0))
    fringe.push(startState)
    closed = Set([])

    while True:
        if fringe.isEmpty():
            return None
        
        node = strategicPop(fringe)
        
        if (problem.isGoalState(node.getState())):
            return node
        
        if node.getState() not in closed:
            closed.add(node.getState())
            successors = problem.getSuccessors(node.getState())

            if isFringeQueue:
                successors.reverse()
                
            for successor in successors:
                fringe.push(nodeFactory(node, successor))
            
    return None

def getActionsToThisNode(node):
    if node == None:
        return None
    
    actions = []
    while True:
        action = node.getAction()
        if action != None:
            actions.append(action)
            node = node.parentNode
        else:
            break;
            
    actions.reverse()
    return actions

# ---------------- End Anton Spaans code ----------------
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
