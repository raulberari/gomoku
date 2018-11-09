from point import Point
from board import Board
from game import Game

boardSize = 15  # default is 15
numberInARow = 5  # default is 5
board = Board(boardSize)
game = Game(board, numberInARow)
playerColour = "b"
computerColour = "w"
movesList = []

# Add some default pieces if you want

# board.makeMove(Point(1, 1), "w")
# board.makeMove(Point(1, 2), "b")
# board.makeMove(Point(1, 3), "w")
# board.makeMove(Point(2, 1), "b")
# board.makeMove(Point(2, 2), "w")
# board.makeMove(Point(2, 3), "b")
# board.makeMove(Point(3, 1), "w")
# board.makeMove(Point(3, 2), "b")
# board.makeMove(Point(3, 3), "w")
# board.makeMove(Point(6, 6), "w")
# board.makeMove(Point(7, 5), "w")
# board.makeMove(Point(8, 4), "w")
# board.makeMove(Point(10, 2), "w")
# board.makeMove(Point(4, 12), "b")
# board.makeMove(Point(5, 12), "b")
# board.makeMove(Point(6, 12), "b")
# board.makeMove(Point(7, 12), "b")
# board.makeMove(Point(11, 15), "b")
# board.makeMove(Point(15, 1), "b")
# board.makeMove(Point(15, 15), "w")
# board.makeMove(Point(14, 15), "w")

while board.isTheGameWon(numberInARow)[0] is False:
    print(board)

    cmd = input(">>")

    if cmd == "exportMoves":
        for point in movesList:
            print(point)

    else:
        cmd = cmd.split()
        row = int(cmd[0])
        column = int(cmd[1])

        try:
            point = Point(row, column)
            movesList.append(point)
            game.movePlayer(point, playerColour)

            if board.isTheGameWon(numberInARow)[0] is False:
                print("Thinking...")

                game.moveComputerEasy(board, computerColour)

                print("Computer moved " + str(game.getMovesList()[-1]))

        except ValueError as ve:
            print(ve)

print(board)
print(board.playerFromPiece(board.isTheGameWon(numberInARow)[1]) + " won the game.")
