import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tetromino shapes and rotations
tetromino_shapes = {
    'O': [[(0,0), (1,0), (0,1), (1,1)]],
    'I': [[(0,0), (0,1), (0,2), (0,3)], [(0,0), (1,0), (2,0), (3,0)]],
    'T': [
        [(1,0), (0,1), (1,1), (2,1)],
        [(1,0), (1,1), (2,1), (1,2)],
        [(0,1), (1,1), (2,1), (1,2)],
        [(1,0), (0,1), (1,1), (1,2)]
    ],
    'L': [
        [(0,0), (0,1), (0,2), (1,2)],
        [(0,1), (1,1), (2,1), (2,0)],
        [(0,0), (1,0), (1,1), (1,2)],
        [(0,1), (1,1), (2,1), (0,2)]
    ],
    'J': [
        [(1,0), (1,1), (1,2), (0,2)],
        [(0,0), (0,1), (1,1), (2,1)],
        [(0,0), (1,0), (0,1), (0,2)],
        [(0,0), (1,0), (2,0), (2,1)]
    ],
    'S': [[(1,0), (2,0), (0,1), (1,1)], [(0,0), (0,1), (1,1), (1,2)]],
    'Z': [[(0,0), (1,0), (1,1), (2,1)], [(1,0), (0,1), (1,1), (0,2)]]
}

# Color map for each tetromino type
colors = {
    'O': (1.0, 1.0, 0.0),
    'I': (0.0, 1.0, 1.0),
    'T': (1.0, 0.0, 1.0),
    'L': (1.0, 0.5, 0.0),
    'J': (0.0, 0.0, 1.0),
    'S': (0.0, 1.0, 0.0),
    'Z': (1.0, 0.0, 0.0)
}

def create_new_piece():
    """Genera una nueva pieza aleatoria en la parte superior del tablero"""
    piece_type = random.choice(list(tetromino_shapes.keys()))
    return {
        'type': piece_type,
        'rotation': 0,
        'position': [BOARD_WIDTH // 2 - 1, 0]
    }


def get_blocks(piece):
    """Devuelve las coordenadas absolutas de los bloques de la pieza"""
    shape = tetromino_shapes[piece['type']][piece['rotation']]
    px, py = piece['position']
    return [(px + x, py + y) for x, y in shape]


def is_valid_position(board, piece, offset=(0, 0)):
    """Verifica colisiones con bordes y celdas fijadas"""
    for x, y in get_blocks(piece):
        nx, ny = x + offset[0], y + offset[1]
        if nx < 0 or nx >= BOARD_WIDTH or ny >= BOARD_HEIGHT:
            return False
        if ny >= 0 and board[ny][nx] != "":
            return False
    return True


def fix_piece_to_board(board, piece):
    """Fija la pieza actual al tablero"""
    for x, y in get_blocks(piece):
        if y >= 0:
            board[y][x] = piece['type']


def clear_lines(board):
    """Detecta y elimina filas completas, retorna tablero modificado y cantidad de líneas borradas"""
    new_board = [row for row in board if any(cell == "" for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [""] * BOARD_WIDTH)
    return new_board, lines_cleared


def rotate_piece(piece, board):
    """Rota la pieza y revierte si la rotación no es válida"""
    old_rotation = piece['rotation']
    piece['rotation'] = (piece['rotation'] + 1) % len(tetromino_shapes[piece['type']])
    if not is_valid_position(board, piece):
        piece['rotation'] = old_rotation