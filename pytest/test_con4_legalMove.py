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

board1 = [['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]

board2 = [['', '', '', 'x', 'x', '', ''],
          ['', '', '', 'o', 'x', '', ''],
          ['', '', '', 'x', 'x', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]

board3 = [['00', '10', '20', '30', '40', '50', '60'],
          ['01', '11', '21', '31', '41', '51', '61'],
          ['02', '12', '22', '32', '42', '52', '62'],
          ['03', '13', '23', '33', '43', '53', '63'],
          ['04', '14', '24', '34', '44', '54', '64'],
          ['05', '15', '25', '35', '45', '55', '65']]

def test_legalMove():
    # board2
    # side
    assert legalMove(board2,Position(4,3)) == True
    # up
    assert legalMove(board2,Position(3,3)) == True
    # down
    assert legalMove(board2,Position(3,2)) == False
    

    # board1
    # Inside board
    assert legalMove(board1,Position(5,5)) == False
    # Outside board
    assert legalMove(board1,Position(7,7)) == False





pos = Position(4,3)
print(board2[pos.y][pos.x])
inside = insideBoard(board2,pos)

