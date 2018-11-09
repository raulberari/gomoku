from point import Point
import random


class Game:
    def __init__(self, board, numberInARow):
        self._board = board
        self._numberInARow = numberInARow
        self._movesList = []

    def getMovesList(self):
        return self._movesList

    def movePlayer(self, point, character):
        self._board.makeMove(point, character)

    def moveComputerDumbest(self, character):
        freePoints = self._board.freePoints()
        randomPoint = int(random.random() * len(freePoints))
        self._board.makeMove(freePoints[randomPoint], character)

    def isMatrixEmpty(self, matrix):
        for row in matrix:
            if set(row) != 0:
                return False
        return True

    def moveComputerDumb(self, character, movesList):
        boardCopy = self._board
        boardSize = self._board.getBoardSize()
        line = [0] * boardSize
        pointValues = []
        maxValue = -1

        for i in range(boardSize):
            pointValues.append(line[:])

        freePoints = self._board.freePoints()

        for i in range(self._board.longestSequence(self._numberInARow), 0, -1):
            for point in freePoints:
                for num in range(self._numberInARow, i, -1):
                    boardCopy.makeMove(point, character)

                    if boardCopy.isTheGameWon(num) == (True, boardCopy.pieceFromPlayerCharacter(character)):
                        pointValues[point.getX() - 1][point.getY() - 1] += 100 * num
                        if num == self._numberInARow:
                            pointValues[point.getX() - 1][point.getY() - 1] += 100 * num

                    boardCopy.removeMove(point)

                    boardCopy.makeMove(point, self.getTheOtherCharacter(character))

                    if boardCopy.isTheGameWon(num) == (True, boardCopy.pieceFromPlayerCharacter(
                                                             self.getTheOtherCharacter(character))):
                        pointValues[point.getX() - 1][point.getY() - 1] += 120 * num

                    boardCopy.removeMove(point)

            for row in pointValues:
                for element in row:
                    if element > maxValue:
                        maxValue = element

        maxValuePoints = [Point(i + 1, j + 1) for i in range(boardSize) for j in range(boardSize)
                          if pointValues[i][j] == maxValue]

        randomPoint = int(random.random() * len(maxValuePoints))
        self._board.makeMove(maxValuePoints[randomPoint], character)

        movesList.append(maxValuePoints[randomPoint])

    def evaluateShapeScore(self, consecutive, openEnds, currentTurn):
        if openEnds == 0 and consecutive < 5:
            return 0

        if consecutive == 4:
            if openEnds == 1:
                if currentTurn is True:
                    return 100000000
                return 50

            if openEnds == 2:
                if currentTurn is True:
                    return 100000000
                return 500000

        if consecutive == 3:
            if openEnds == 1:
                if currentTurn is True:
                    return 7
                return 5
            if openEnds == 2:
                if currentTurn is True:
                    return 10000
                return 50

        if consecutive == 2:
            if openEnds == 1:
                return 2
            if openEnds == 2:
                return 5

        if consecutive == 1:
            if openEnds == 1:
                return 0.5
            if openEnds == 2:
                return 1

        return 200000000

    def evaluateBoard(self, board, character):
        score = 0
        countConsecutive = 0
        openEnds = 0
        currentTurn = None

        if character == "○":
            currentTurn = True
        if character == "●":
            currentTurn = False

        """horizontal"""
        for i in range(board.getBoardSize()):
            for j in range(board.getBoardSize()):
                if board.getData()[i][j] == character:
                    countConsecutive += 1

                elif board.getData()[i][j] == "+" and countConsecutive > 0:
                    openEnds += 1
                    score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                    countConsecutive = 0
                    openEnds = 1

                elif board.getData()[i][j] == "+":
                    openEnds = 1

                elif countConsecutive > 0:
                    score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                    countConsecutive = 0
                    openEnds = 0
                else:
                    openEnds = 0

            if countConsecutive > 0:
                score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)

            countConsecutive = 0
            openEnds = 0

        """vertical"""
        for j in range(board.getBoardSize()):
            for i in range(board.getBoardSize()):
                if board.getData()[i][j] == character:
                    countConsecutive += 1

                elif board.getData()[i][j] == "+" and countConsecutive > 0:
                    openEnds += 1
                    score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                    countConsecutive = 0
                    openEnds = 1

                elif board.getData()[i][j] == "+":
                    openEnds = 1

                elif countConsecutive > 0:
                    score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                    countConsecutive = 0
                    openEnds = 0
                else:
                    openEnds = 0

            if countConsecutive > 0:
                score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)

            countConsecutive = 0
            openEnds = 0

        """first diagonal"""
        for i in range(board.getBoardSize()):
            for j in range(board.getBoardSize() - 1, -1, -1):
                for k in range(board.getBoardSize()):
                    if (i > 0 and j < 1) or i == 0:
                        if i + k < board.getBoardSize() and j + k < board.getBoardSize():
                            # element i + k, j + k
                            if board.getData()[i + k][j + k] == character:
                                countConsecutive += 1

                            elif board.getData()[i + k][j + k] == "+" and countConsecutive > 0:
                                openEnds += 1
                                score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                                countConsecutive = 0
                                openEnds = 1

                            elif board.getData()[i + k][j + k] == "+":
                                openEnds = 1

                            elif countConsecutive > 0:
                                score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                                countConsecutive = 0
                                openEnds = 0
                            else:
                                openEnds = 0

                if countConsecutive > 0:
                    score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)

                countConsecutive = 0
                openEnds = 0

        """second diagonal"""
        for i in range(board.getBoardSize()):
            for j in range(board.getBoardSize()):
                for k in range(board.getBoardSize()):
                    if (i > 0 and j == board.getBoardSize() - 1) or i == 0:
                        if i + k < board.getBoardSize() and j - k >= 0:
                            # element i + k, j - k
                            if board.getData()[i + k][j - k] == character:
                                countConsecutive += 1

                            elif board.getData()[i + k][j - k] == "+" and countConsecutive > 0:
                                openEnds += 1
                                score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                                countConsecutive = 0
                                openEnds = 1

                            elif board.getData()[i + k][j - k] == "+":
                                openEnds = 1

                            elif countConsecutive > 0:
                                score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)
                                countConsecutive = 0
                                openEnds = 0
                            else:
                                openEnds = 0

                if countConsecutive > 0:
                    score += self.evaluateShapeScore(countConsecutive, openEnds, currentTurn)

                countConsecutive = 0
                openEnds = 0

        return score

    def moveComputerEasy(self, board, character):
        freePoints = board.freePoints()

        boardSize = self._board.getBoardSize()
        line = [0] * boardSize
        pointValues = []
        maxValue = -1

        for i in range(boardSize):
            pointValues.append(line[:])

        for point in freePoints:
            board.makeMove(point, character)

            pointValues[point.getX() - 1][point.getY() - 1] += self.evaluateBoard(
                board, board.pieceFromPlayerCharacter(character))

            board.removeMove(point)

            board.makeMove(point, self.getTheOtherCharacter(character))
            pointValues[point.getX() - 1][point.getY() - 1] += self.evaluateBoard(
                board, board.pieceFromPlayerCharacter(self.getTheOtherCharacter(character)))
            board.removeMove(point)

        for row in pointValues:
            for element in row:
                if element > maxValue:
                    maxValue = element

        maxValuePoints = [Point(i + 1, j + 1) for i in range(boardSize) for j in range(boardSize)
                          if pointValues[i][j] == maxValue]
        randomPoint = int(random.random() * len(maxValuePoints))
        self._board.makeMove(maxValuePoints[randomPoint], character)
        self._movesList.append(maxValuePoints[randomPoint])

    def minimax(self, depth, maximizingPlayer):
        if maximizingPlayer is True:
            character = "w"
        else:
            character = "b"

        if depth == 0 or self._board.isTheGameWon(5) == (True, "○"):
            return self.evaluateBoard(self._board, "○")

        if maximizingPlayer is True:
            bestValue = -10000000000
            freePoints = self._board.freePoints()

            for point in freePoints:
                self._board.makeMove(point, character)
                value = self.minimax(depth - 1, False)
                if value > bestValue:
                    bestValue = value

                self._board.removeMove(point)

            return bestValue

        else:
            bestValue = 10000000000
            freePoints = self._board.freePoints()

            for point in freePoints:
                self._board.makeMove(point, character)
                value = self.minimax(depth - 1, True)
                if value < bestValue:
                    bestValue = value
                self._board.removeMove(point)

            return bestValue

    @staticmethod
    def getTheOtherCharacter(character):
        if character == "b":
            return "w"
        if character == "w":
            return "b"
