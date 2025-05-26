import random

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Base tetromino shapes (single orientation)
base_shapes = {
    'O': [(0,0), (1,0), (0,1), (1,1)],
    'I': [(0,0), (0,1), (0,2), (0,3)],
    'T': [(1,0), (0,1), (1,1), (2,1)],
    'L': [(0,0), (0,1), (0,2), (1,2)],
    'J': [(1,0), (1,1), (1,2), (0,2)],
    'S': [(1,0), (2,0), (0,1), (1,1)],
    'Z': [(0,0), (1,0), (1,1), (2,1)]
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
    """Genera una nueva pieza con forma base y posición inicial"""
    piece_type = random.choice(list(base_shapes.keys()))
    # Copy base shape offsets
    shape = base_shapes[piece_type].copy()
    return {
        'type': piece_type,
        'shape': shape,
        'position': [BOARD_WIDTH // 2 - 1, 0]
    }


def get_blocks(piece):
    """Devuelve las coordenadas absolutas de los bloques de la pieza"""
    px, py = piece['position']
    return [(px + x, py + y) for x, y in piece['shape']]


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
    """Rota la pieza 90° CW usando matriz de rotación en torno a pivote específico y revierte si no cabe"""
    # Definir pivote para cada tipo (en coordenadas de bloque)
    pivots = {
        'O': (0.5, 0.5),
        'I': (1.5, 1.5),
        'T': (1, 1),
        'L': (1, 1),
        'J': (1, 1),
        'S': (1, 1),
        'Z': (1, 1)
    }
    pivot = pivots.get(piece['type'], (1, 1))
    px, py = pivot

    new_shape = []
    for x, y in piece['shape']:
        # trasladar al pivote
        tx, ty = x - px, y - py
        # rotar 90° CW
        rx, ry = -ty, tx
        # trasladar de vuelta
        new_x = int(round(rx + px))
        new_y = int(round(ry + py))
        new_shape.append((new_x, new_y))

    # Probar validez
    old_shape = piece['shape']
    piece['shape'] = new_shape
    if not is_valid_position(board, piece):
        piece['shape'] = old_shape  # revertir si falla
