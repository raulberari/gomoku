class Node(object):
    def __init__(self, depth, playerNum, movesRemaining, boardSize, value=0):
        self.depth = depth
        self.playerNum = playerNum
        self.movesRemaining = movesRemaining
        self.boardSize = boardSize
        self.value = value
        self.children = []
        self.createChildren()

    def createChildren(self):
        if self.depth >= 0:
            for i in range(self.boardSize ** 2):
                v = self.movesRemaining - i
