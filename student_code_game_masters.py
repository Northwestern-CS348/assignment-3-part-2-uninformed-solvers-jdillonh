from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster): #--------------T.O. HANOI-------------#
    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        def tuplefy(liOfli):
            """ [HELPER]
            turns a list of list (useful)
            into a tuple of tuples (garbage)
            """
            return tuple(tuple(li) for li in liOfli)

        # 'DONE'
        
        result = [ [], [], [] ]
        for fact in self.kb.facts:
            #if not isinstance(fact, Fact):
            #    continue
            if fact.statement.predicate == 'on':
                diskN = int(str(fact.statement.terms[0])[4]) 
                pegN = int(str(fact.statement.terms[1])[3])
                if diskN not in result[pegN-1]: #avoid redundant facts?
                    result[pegN-1].append(diskN)

        for pegL in result:
            pegL.sort()

        #make sure there are the right elements
        #total = sum(sum(e) for e in result) 
        #assert(total == 15)

        #turn into a tuple 
        return tuplefy(result)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """

        # 'DONE' - And Tested!
        
        #assert the new posisiton
        disk = str(movable_statement.terms[0])
        fro  = str(movable_statement.terms[1]) # from is taken, 
        to   = str(movable_statement.terms[2]) # how about 'to and fro'

        #move from old position: rectract old position
        self.kb.kb_retract(parse_input('fact: (on '+ disk + ' ' + fro + ')'))

        #remove all movables, no longer nescesarily correct
        #for fact in self.kb.facts:
        #    if fact.statement.predicate == 'movable':
        #        self.kb.kb_retract(fact)

        #make the move: assert new pos fact
        newPos = parse_input('fact: (on '+ disk + ' ' + to + ')') 
        self.kb.kb_add(newPos)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster): #----------------PUZZLE 8---------------#
    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Done and tested working I think

        def tuplefy(liOfli):
            """ [HELPER]
            turns a list of list (useful)
            into a tuple of tuples (garbage)
            """
            return tuple(tuple(li) for li in liOfli)

        result = [[None, None, None], [None, None, None], [None, None, None]]

        for fact in self.kb.facts:
            if fact.statement.predicate == 'pos':

                try:
                    disk = None
                    disk = int(str(fact.statement.terms[0])[4])
                except: #empty case
                    disk = -1
                xPos = int(str(fact.statement.terms[1])[3])
                yPos = int(str(fact.statement.terms[2])[3])

                result[yPos-1][xPos-1] = disk

            
        for li in result: #BANDAID - who has time
            li = [e if e is not None else -1 for e in li]

        for i in range(0, 3):  #BANDAID pt.2 - noone does
            for j in range(0, 3):
                if result[i][j] is None:
                    result[i][j] = -1
        return tuplefy(result)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        # 'DONE'

        #assert the new posisiton
        tile = str(movable_statement.terms[0]) 
        froX = str(movable_statement.terms[1])  #going to use fro again for consistency
        froY = str(movable_statement.terms[2]) 
        toX  = str(movable_statement.terms[3])
        toY  = str(movable_statement.terms[4])


        #move from old position: rectract old position
        self.kb.kb_retract(
            parse_input('fact: (pos ' + tile + ' ' + froX + ' ' + froY + ')'))

        #make the move: assert new pos fact
        self.kb.kb_assert(
            parse_input('fact: (pos ' + tile + ' ' + toX + ' ' + toY + ')'))



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
