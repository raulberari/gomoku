from point import Point


class Board:
    def __init__(self, boardSize):
        self._boardSize = boardSize
        self._data = []
        self._moves = 0

        line = ["+"] * self._boardSize

        for i in range(self._boardSize):
            self._data.append(line[:])

    def __str__(self):
        boardString = "   1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n"

        for i in range(self._boardSize):
            if i < 9:
                boardString += " "
            boardString += str(i + 1) + " "
            for j in range(self._boardSize):
                boardString += str(self._data[i][j]) + " "
            boardString += "\n"

        return boardString

    @staticmethod
    def pieceFromPlayerCharacter(character):
        if character == "b":
            return "●"
        if character == "w":
            return "○"

    @staticmethod
    def playerFromPiece(piece):
        if piece == "●":
            return "Black"
        if piece == "○":
            return "White"

    def makeMove(self, point, player):
        if 1 <= point.getX() <= self._boardSize and 1 <= point.getY() <= self._boardSize:
            if self._data[point.getX() - 1][point.getY() - 1] == "+":
                if player == "b" or player == "w":
                    self._data[point.getX() - 1][point.getY() - 1] = self.pieceFromPlayerCharacter(player)
                    self._moves += 1
                else:
                    raise ValueError("Invalid character")
            else:
                raise ValueError("Invalid move. The point is already used")
        else:
            raise ValueError("Invalid move. Wrong coordinates")

    def removeMove(self, point):
        self._data[point.getX() - 1][point.getY() - 1] = "+"
        self._moves -= 1

    def freePoints(self):
        return [Point(i + 1, j + 1) for i in range(0, self._boardSize)
                for j in range(0, self._boardSize) if self._data[i][j] == "+"]

    def isTheGameWon(self, numberInARow):
        """horizontal check"""
        for i in range(self._boardSize):
            for j in range(self._boardSize - (numberInARow - 1)):
                row = self._data[i][j: j + numberInARow]

                if len(set(row)) == 1 and row[0] != "+":
                    return True, row[0]

        """vertical check"""
        for i in range(self._boardSize):
            fullColumn = [row[i] for row in self._data]

            for j in range(len(fullColumn) - (numberInARow - 1)):
                column = fullColumn[j: j + numberInARow]

                if len(set(column)) == 1 and column[0] != "+":
                    return True, column[0]

        """diagonal check"""
        """first diagonal and its parallels"""
        for i in range(self._boardSize - (numberInARow - 1)):
            for j in range(self._boardSize - (numberInARow - 1)):
                diagonal = [self._data[i + k][j + k] for k in range(numberInARow)]

                if len(set(diagonal)) == 1 and diagonal[0] != "+":
                    return True, diagonal[0]

        """second diagonal and its parallels"""
        for i in range(self._boardSize - (numberInARow - 1)):
            for j in range(numberInARow - 1, self._boardSize):
                diagonal = [self._data[i + k][j - k] for k in range(numberInARow)]

                if len(set(diagonal)) == 1 and diagonal[0] != "+":
                    return True, diagonal[0]

        return False, ""

    def longestSequence(self, numberInARow):
        for i in range(numberInARow, 0, -1):
            if self.isTheGameWon(i)[0] is True:
                return i

    def getBoardSize(self):
        return self._boardSize

    def getMoves(self):
        return self._moves

    def getData(self):
        return self._data
