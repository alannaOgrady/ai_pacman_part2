# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import time

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """
    global max_time
    max_time = -999

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        start = time.time()
        global max_time
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        end = time.time()
        max_time = max(max_time, (end - start))
        print max_time
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        start = time.time()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        timer = ghostState.scaredTimer
        #print dist_to_ghost
        
        #print timer
        #to stop pacman getting stuck in corners
        capsulePositions = currentGameState.getCapsules()
        currentFood = currentGameState.getFood().asList()
        currentPosition = currentGameState.getPacmanPosition()
        distance_to_capsule = -999
        east_count = 0
        west_count = 0
        north_count = 0
        south_count = 0

        score = -99999
        for state in newGhostStates:
          position_of_ghost = state.getPosition()
          if newPos == position_of_ghost or manhattanDistance(position_of_ghost, newPos) <=1:
            #print "B"
            return score
          

        if len(newFood.asList()) < len(currentFood):
          #print "A"
          #this action would mean you get to eat
          return 50#check direction of  most food food

        numCurrentFood = len(currentFood)
        for food in currentFood:
          if food[0] > currentPosition[0]:
            east_count += 1
          if food[1] > currentPosition[1]:
            north_count += 1


        west_count = numCurrentFood - east_count
        south_count = numCurrentFood - north_count


        for food in currentFood:
          score = min(score, manhattanDistance(food, newPos))
          if action == "stop":
            #print "D"
            return -99999
          if east_count == 0:
            #decrease chance of going in this direction by increasing score (which will decrease value returned from function)
            if action == Directions.EAST:
              score += 0.2
          if north_count == 0:
            if action == Directions.NORTH:
              score += 0.2
          if west_count == 0:
            if action == Directions.WEST:
              score += 0.2
          if south_count == 0:
            if action == Directions.SOUTH:
              score += 0.2
        # if len(capsulePositions) > 0:
        #   for capsule in capsulePositions:
        #     distance_to_capsule = min(distance_to_capsule, manhattanDistance(newPos, capsule ))
        #     if distance_to_capsule < 50 and distance_to_capsule > -999:
        #       #print "here"
        #       return 50
          

            # if action == Directions.WEST:
            #   score -= 0.01*west_count

        

        # end = time.time()
        # print(end - start)
        return 1.0/(1.0 + score) - (100*len(newFood.asList()))


        # curPos = currentGameState.getPacmanPosition()
        # curFoodList = currentGameState.getFood().asList()
        # curGhostStates = currentGameState.getGhostStates()
        # curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]

        # distance = float("inf")
        # for ghostState in newGhostStates:
        #   ghostPos = ghostState.getPosition()
        #   if ghostPos == newPos:
        #     return float("-inf")
        
        # for food in curFoodList:
        #   distance = min(distance,manhattanDistance(food,newPos))
        #   if Directions.STOP in action:  
        #     return float("-inf")

        # return 1.0/(1.0 + distance) 
        
        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """

    return currentGameState.getScore() 

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    global max_time
    max_time = -999
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        
        num_agents = gameState.getNumAgents()
        pacman_actions = []

        def value(state, count):
          #if value is terminal state - no more sucessors
          if state.isWin() or state.isLose() or count >= self.depth*num_agents:
            return self.evaluationFunction(state)
          
          if count % num_agents == 0:
            #if value max (pacman) 
            return max_value(state, count)
          elif count % num_agents != 0:
            #if value min (ghost)
            return min_value(state, count)

        #pacmans turn
        def max_value(state, count):
          the_value = -9999
          #how to get index and action
          index = count % num_agents
          actions = state.getLegalActions(index)
          #print actions
          filter(lambda a: a != "Stop", actions)
          for action in actions:
            successor = state.generateSuccessor(index, action)
            the_value = max(the_value, value(successor, count + 1))
            if count == 0:
              pacman_actions.append(the_value)
          return the_value

        def min_value(state, count):
          the_value = 9999
          #how to get index and action
          index = count % num_agents
          actions = state.getLegalActions(index)
          filter(lambda a: a != "Stop", actions)
          for action in actions:
            successor = state.generateSuccessor(index, action)
            the_value = min(the_value, value(successor, count + 1))
          return the_value

        start = time.time()
        iteration_count = 0
        result = value(gameState, iteration_count)
        print result
        best_action = pacman_actions.index(max(pacman_actions))
        result_actions = gameState.getLegalActions(0)[best_action]
        print result_actions
        filter(lambda a: a != "Stop", result_actions)

        end = time.time()
        global max_time
        max_time = max(max_time, (end - start))
        print max_time

        return result_actions

    
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    global max_time
    max_time = -999

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        num_agents = gameState.getNumAgents()
        pacman_actions = []
        alpha = -9999
        beta = 9999

        def alpha_beta_pruning(state, count, alpha, beta):
          #if value is terminal state - no more sucessors
          if state.isWin() or state.isLose() or count >= self.depth*num_agents:
            return self.evaluationFunction(state)
          
          if count % num_agents == 0:
            #if value max (pacman) 
            return max_value(state, count, alpha, beta)
          elif count % num_agents != 0:
            #if value min (ghost)
            return min_value(state, count, alpha, beta)

        #pacmans turn
        def max_value(state, count, alpha, beta):
          the_value = -9999
          #how to get index and action
          index = count % num_agents
          actions = state.getLegalActions(index)
          #print actions
          filter(lambda a: a != "Stop", actions)
          for action in actions:
            successor = state.generateSuccessor(index, action)
            the_value = max(the_value, alpha_beta_pruning(successor, count + 1, alpha, beta))
            if count == 0:
              pacman_actions.append(the_value)
            if the_value > beta:
              return the_value
            alpha = max(alpha, the_value)
          return the_value

        def min_value(state, count, alpha, beta):
          the_value = 9999
          #how to get index and action
          index = count % num_agents
          actions = state.getLegalActions(index)
          filter(lambda a: a != "Stop", actions)
          for action in actions:
            successor = state.generateSuccessor(index, action)
            the_value = min(the_value, alpha_beta_pruning(successor, count + 1, alpha, beta))
            if the_value < alpha:
              return the_value
            beta = min(beta, the_value)
          return the_value


        iteration_count = 0
        
        start = time.time()

        result = alpha_beta_pruning(gameState, iteration_count, alpha, beta)
        
        best_action = pacman_actions.index(max(pacman_actions))
        result_actions = gameState.getLegalActions(0)[best_action]
        filter(lambda a: a != "Stop", result_actions)

        end = time.time()
        global max_time
        max_time = max(max_time, (end - start))
        print max_time

        return result_actions



        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

"""
ATTEMPTS AT QUESTION 5

def scoreEvaluationFunction(currentGameState):
    
    currentFood = currentGameState.getFood().asList()
    currentPosition = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    
    ghost_score = 0
    max_ghost_dist = -99
    for ghost in ghostStates:
      timer = ghost.scaredTimer
      if timer > 0:
        ghost_score = 50
      else:
        #get max distance from ghost
        max_ghost_dist = max(max_ghost_dist, manhattanDistance(ghost.getPosition(), currentPosition))
        ghost_score -= 0.001/(1 + max_ghost_dist)

    food_score = 99999
    for food in currentFood:
      food_score = min(food_score, manhattanDistance(food, currentPosition))
      if len(food) == 0 or food_score == 0:
        food_score = 0
      else:
        food_score = 1/ food_score
    
    return ghost_score + food_score

"""
