# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.


from captureAgents import CaptureAgent
import random
import time
import util
from game import Directions
from util import nearestPoint
import game

#################
# Team creation #
#################
count = 0
originalFood = 0

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveAgent', second='DefensiveAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line indicates which agent is which (offensive or defensive).
    if not isRed:
        second = 'OffensiveAgent'
        first = 'DefensiveAgent'

    first = 'OffensiveAgent'
    second = 'DefensiveAgent'
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########


class BetterCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """

    def registerInitialState(self, gameState):
        global originalFood
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)
        foodList = self.getFood(gameState)
        foodList = foodList.asList()
        originalFood = len(foodList)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)

        # Profile the evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]
        # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        foodLeft = len(self.getFood(gameState).asList())

        if foodLeft <= 2:
            bestDist = 9999
            for action in actions:
                successor = self.getSuccessor(gameState, action)
                pos2 = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(self.start, pos2)
                if dist < bestDist:
                    bestAction = action
                    bestDist = dist
            return bestAction

        return random.choice(bestActions)

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor



class OffensiveAgent(BetterCaptureAgent):

    def evaluate(self, gameState):
        global originalFood
        """
        try to get the Blue side's food
        """

        currState = gameState.getAgentState(self.index)
        currPos = currState.getPosition()
        teamIndex = -1
        for index in self.getTeam(gameState):
          if index != self.index:
            teamIndex = index
        teamState = gameState.getAgentState(teamIndex)
        teamPos = teamState.getPosition()

        currScore = self.getScore(gameState)
        foodList = self.getFood(gameState)
        foodList = foodList.asList()
        numFood = len(foodList)
        numScare = len(gameState.getCapsules())

        ownFood = self.getFoodYouAreDefending(gameState)
        ownFood = ownFood.asList()

        oppoIndex = self.getOpponents(gameState)
        oppoPos = []
        oppoState = []
        for index in oppoIndex:
            oppoPos.append(gameState.getAgentPosition(index))
            oppoState.append(gameState.getAgentState(index))

        foodDist = 999999
        for food in foodList:
            # print(food)
            currDist = self.getMazeDistance(currPos, food)
            foodDist = min([foodDist, currDist])

        ownDist = 999999
        for food in ownFood:
            currDist = self.getMazeDistance(currPos, food)
            ownDist = min([ownDist, currDist])

        ghostDist = 999999
        defenDist = 999999
        for index, ghost in enumerate(oppoPos):
            if not oppoState[index].isPacman and oppoState[index].scaredTimer <= 3:
              currDist = self.getMazeDistance(currPos, ghost)
              ghostDist = min(currDist, ghostDist)
            if oppoState[index].isPacman:
              currDist = self.getMazeDistance(currPos, ghost)
              defenDist = min(currDist, defenDist)

        if originalFood > numFood and ghostDist < 3:
          if ownDist == 0:
            originalFood = numFood
          return currScore + min(ghostDist, 3) * 4 - ownDist * 3 - numFood

        return currScore + min(ghostDist, 3) * 4 - foodDist * 3 - numFood * 80

    def chooseAction(self, gameState):

        legalActions = gameState.getLegalActions(self.index)
        v = -999999
        actionVal = {}
        for action in legalActions:
            successor = gameState.generateSuccessor(self.index, action)
            vt = self.evaluate(successor)
            v = max(v, vt)
            actionVal[action] = vt
        return max(actionVal, key=actionVal.get)

class DefensiveAgent(BetterCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free.
    """

    def evaluate(self, gameState):
        """
        Computes a linear combination of features and feature weights
        """

        # successor = self.getSuccessor(gameState, action)
        currState = gameState.getAgentState(self.index)
        currPos = currState.getPosition()
        currScore = self.getScore(gameState)
        foodList = gameState.getRedFood()
        foodList = foodList.asList()
        numFood = len(foodList)
        numScare = len(gameState.getCapsules())

        oppoIndex = self.getOpponents(gameState)
        oppoPos = []
        for index in oppoIndex:
            oppoPos.append(gameState.getAgentPosition(index))
        pacDist = []
        pacDistHere = []
        for oppo in oppoPos:
            currDist = self.getMazeDistance(currPos, oppo)
            if oppo[0] < gameState.data.layout.width // 2 - 1:
                pacDistHere.append(currDist) 
            pacDist.append(currDist)

        if pacDistHere != []:
            #print(pacDistHere)
            return -min(pacDistHere)
        return - min(pacDist)  

    
    def chooseAction(self, gameState):
        """
        Picks actions that chase the closed opponent.
        """
        oppoIndex = self.getOpponents(gameState)
        oppoPos = []
        
        for index in oppoIndex:
            oppoPos.append(gameState.getAgentPosition(index))
            
        Agents = range(gameState.getNumAgents())
        legalActions = gameState.getLegalActions(self.index)
        v = -999999
        actionVal = {}
        
        if 1 in [self.getMazeDistance(i, gameState.getAgentPosition(self.index)) for i in oppoPos] and gameState.getAgentPosition(self.index)[0] == (gameState.data.layout.width // 2 - 1):
            return random.choice(legalActions)
          
        for action in legalActions:
            successor = gameState.generateSuccessor(self.index, action)
            
            if successor.getAgentPosition(self.index) in oppoPos:
                return action
              
            if successor.getAgentPosition(self.index)[0] > (gameState.data.layout.width // 2 - 1):
                pass
              
            else:
                vt = self.evaluate(successor)
                v = max(v, vt)
                actionVal[action] = vt
                
        return max(actionVal, key=actionVal.get)
