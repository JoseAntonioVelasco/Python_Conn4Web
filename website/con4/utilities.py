class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def insideBoard(board, pos):
    columns = len(board[0])
    rows = len(board)

    if pos.x in range(columns) and pos.y in range(rows):
        return True
    else:
        return False


def legalMove(board, pos):

    if insideBoard(board, pos) != True:
        return False

    cond1 = board[pos.y][pos.x] == ''
    cond2 = board[pos.y-1][pos.x] == ('x' or 'o')

    if cond1 and cond2:
        return True
    else:
        return False


def win(board, pos, turn):
    directions = [[[0, 1], [0, -1]], [[1, 1], [-1, -1]],
               [[1, 0], [-1, 0]], [[1, -1], [-1, 1]]]
    for direction in directions:
        counter = 0
        for vector in direction:
            loop = 0
            x = pos.x
            y = pos.y
            for loop in range(4):
                loop = loop + 1
                x = x + vector[0]
                y = y + vector[1]
                cond = insideBoard(board,Position(x,y)) and board[y][x] == turn
                if cond:
                    counter = counter + 1
                else:
                    break
                if counter == 3:
                    return True
    return False