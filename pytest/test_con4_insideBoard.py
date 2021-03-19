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
    assert insideBoard(board1, Position(3, 3)) == True
    assert insideBoard(board1, Position(5, 5)) == True


def test_insideBoard_esquina_inferior_izquierda():
    assert insideBoard(board1, Position(0, 0)) == True
    assert insideBoard(board1, Position(0, -1)) == False
    assert insideBoard(board1, Position(-1, 0)) == False


def test_insideBoard_esquina_inferior_derecha():
    assert insideBoard(board1, Position(6, 0)) == True
    assert insideBoard(board1, Position(7, 0)) == False
    assert insideBoard(board1, Position(6, -1)) == False

def test_insideBoard_esquina_superior_izquierda():
    assert insideBoard(board1, Position(0, 5)) == True
    assert insideBoard(board1, Position(0, 6)) == False
    assert insideBoard(board1, Position(-1, 5)) == False

def test_insideBoard_esquina_superior_derecha():
    assert insideBoard(board1, Position(6, 5)) == True
    assert insideBoard(board1, Position(7, 5)) == False
    assert insideBoard(board1, Position(6, 6)) == False
    assert insideBoard(board1, Position(7, 6)) == False

