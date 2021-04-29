def insideBoard(board, x, y):
    columns = len(board[0])
    rows = len(board)

    if x in range(columns) and y in range(rows):
        return True
    else:
        return False

board1 = [['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]

board2 = [['', '', '', 'o', 'x', '', ''],
          ['', '', '', 'x', 'x', '', ''],
          ['', '', '', 'o', 'x', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', ''],
          ['', '', '', '', '', '', '']]


def test_insideBoard_medio():
    assert insideBoard(board1, 3, 3) == True
    assert insideBoard(board1, 5, 5) == True


def test_insideBoard_esquina_inferior_izquierda():
    assert insideBoard(board1, 0, 0) == True
    assert insideBoard(board1, 0, -1) == False
    assert insideBoard(board1, -1, 0) == False


def test_insideBoard_esquina_inferior_derecha():
    assert insideBoard(board1, 6, 0) == True
    assert insideBoard(board1, 7, 0) == False
    assert insideBoard(board1, 6, -1) == False

def test_insideBoard_esquina_superior_izquierda():
    assert insideBoard(board1, 0, 5) == True
    assert insideBoard(board1, 0, 6) == False
    assert insideBoard(board1, -1, 5) == False

def test_insideBoard_esquina_superior_derecha():
    assert insideBoard(board1, 6, 5) == True
    assert insideBoard(board1, 7, 5) == False
    assert insideBoard(board1, 6, 6) == False
    assert insideBoard(board1, 7, 6) == False
