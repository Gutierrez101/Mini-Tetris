from OpenGL.GL import *
from logica_juego import colors, obtener_bloques

tamanio_celda = 30

#dibujar celdas
def dibujar_celda(x, y, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x * tamanio_celda, y * tamanio_celda)
    glVertex2f((x + 1) * tamanio_celda, y * tamanio_celda)
    glVertex2f((x + 1) * tamanio_celda, (y + 1) * tamanio_celda)
    glVertex2f(x * tamanio_celda, (y + 1) * tamanio_celda)
    glEnd()

#dinujar la pantalla del juego
def dibujar_pantalla(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                dibujar_celda(x, y, colors[cell])

#dibujar cada pieza
def dibujar_pieza(piece):
    for x, y in obtener_bloques(piece):
        if y >= 0:
            dibujar_celda(x, y, colors[piece['type']])