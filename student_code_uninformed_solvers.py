from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def findNextStepDFS(self):
        """ [helper] finds next node to work on, in DFS order """
            #if this node has children we havent visited
        if self.currentState.nextChildToVisit < len(self.currentState.children):
            #visit one of the children
            curr = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            self.currentState = curr
            self.gm.makeMove(self.currentState.requiredMovable)
            return
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            
            self.currentState = self.currentState.parent
            self.findNextStepDFS()
        
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state shouldteta conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code 
        self.visited[ self.currentState ] = True

        if self.currentState == GameState(self.victoryCondition, 0, None):
            return True

        if self.gm.getMovables() is False: 
            return False
        for move in self.gm.getMovables():
            self.gm.makeMove(move)
            newState = GameState(self.gm.getGameState, self.currentState.depth + 1, move)
            newState.parent = self.currentState
            self.currentState.children.append(newState)
            self.gm.reverseMove(move)

        self.findNextStepDFS()

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
