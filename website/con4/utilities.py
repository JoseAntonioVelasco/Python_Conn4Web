def insideBoard(board, x, y):
    """detecta si la ficha que quieres poner esta dentro de los limites del tablero

    Args:
        board (list): lista que contiene el tablero
        x (int): posicion x en la que quieres poner en el tablero
        y (int): posicion y en la que quieres poner en el tablero

    Returns:
        boolean: si esta dentro true si no false
    """
    columns = len(board[0])
    rows = len(board)

    if x in range(columns) and y in range(rows):
        return True
    else:
        return False


def legalMove(board, x, y):
    """Comprueba si el movimiento es valido, que no se superponga sobre otras fichas,
    este dentro del tablero y que no este flotando la ficha

    Args:
        board (list): lista que contiene el tablero
        x (int): posicion x en la que quieres poner en el tablero
        y (int): posicion y en la que quieres poner en el tablero

    Returns:
        boolean: si el movimiento es valido
    """
    if insideBoard(board, x, y) == False:
        return False

    cond1 = board[y][x] == 'free'
    cond2 = (board[y-1][x] == 'red') or (board[y-1][x] == 'yellow')
    cond3 = (y == 0)

    if (cond1 and cond2) or (cond3):
        return True
    else:
        return False


def win(board, x, y, turn):
    """detecta si en ese movimiento hay victoria

    Args:
        board (list): lista que contiene el tablero
        x (int): posicion x en la que quieres poner en el tablero
        y (int): posicion y en la que quieres poner en el tablero
        turn (string): que jugador ha puesto, ej: 'X'/'O' o 'red'/'yellow'

    Returns:
        boolean: true si hay victoria, false si no hay victoria
    """
    directions = [[[0, 1], [0, -1]], [[1, 1], [-1, -1]],
               [[1, 0], [-1, 0]], [[1, -1], [-1, 1]]]
    for direction in directions:
        counter = 0
        for vector in direction:
            loop = 0
            x_ = x
            y_ = y
            for loop in range(4):
                loop = loop + 1
                x_ = x_ + vector[0]
                y_ = y_ + vector[1]
                cond = insideBoard(board, x_, y_) and board[y_][x_] == turn
                if cond:
                    counter = counter + 1
                else:
                    break
                if counter == 3:
                    return True
    return False