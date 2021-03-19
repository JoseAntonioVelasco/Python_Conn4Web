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


board1 = [['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]

board2 = [['', 'x', '', 'x', 'x', '', ''],
          ['', '', '', 'o', 'x', '', ''],
          ['', '', '', 'x', 'x', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]

board4 = [['o', 'o', 'o', 'x', 'x', 'o', 'o'],
          ['o', 'o', '', 'o', 'x', 'o', 'o'],
          ['o', 'x', '', 'x', 'o', 'x', 'o'],
          ['x', '', '', '', '', 'x', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]

board3 = [['00', '10', '20', '30', '40', '50', '60'],
          ['01', '11', '21', '31', '41', '51', '61'],
          ['02', '12', '22', '32', '42', '52', '62'],
          ['03', '13', '23', '33', '43', '53', '63'],
          ['04', '14', '24', '34', '44', '54', '64'],
          ['05', '15', '25', '35', '45', '55', '65']]

def test_win():
    assert win(board2,Position(4,3),'x') == True
    assert win(board2,Position(2,0),'x') == True
    assert win(board2,Position(6,0),'x') == False
    assert win(board2,Position(8,8),'x') == False
    assert win(board2,Position(5,5),'x') == False

    assert win(board4,Position(6,3),'x') == True
    assert win(board4,Position(2,1),'x') == True
    assert win(board4,Position(2,3),'x') == False

