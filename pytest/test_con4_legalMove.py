def insideBoard(board, x, y):
    columns = len(board[0])
    rows = len(board)

    if x in range(columns) and y in range(rows):
        return True
    else:
        return False


def legalMove(board, x, y):

    if insideBoard(board, x, y) != True:
        return False

    cond1 = board[y][x] == ''
    cond2 = board[y-1][x] == ('x' or 'o')

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
    # a un lado
    assert legalMove(board2, 4, 3) == True
    # arriba
    assert legalMove(board2, 3, 3) == True
    # abajo
    assert legalMove(board2, 3, 2) == False
    

    # board1
    # Dentro del tablero
    assert legalMove(board1, 5, 5) == False
    # Fuera del tablero
    assert legalMove(board1, 7, 7) == False

