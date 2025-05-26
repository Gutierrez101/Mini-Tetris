from OpenGL.GL import *
from logica_juego import colors, get_blocks

CELL_SIZE = 30


def draw_cell(x, y, color):
    """Dibuja un cuadrado en la posición (x, y) con color RGB"""
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x * CELL_SIZE, y * CELL_SIZE)
    glVertex2f((x + 1) * CELL_SIZE, y * CELL_SIZE)
    glVertex2f((x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)
    glVertex2f(x * CELL_SIZE, (y + 1) * CELL_SIZE)
    glEnd()


def draw_board(board):
    """Dibuja todas las celdas fijas en el tablero"""
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                draw_cell(x, y, colors[cell])


def draw_piece(piece):
    """Dibuja la pieza actual"""
    for x, y in get_blocks(piece):
        if y >= 0:
            draw_cell(x, y, colors[piece['type']])