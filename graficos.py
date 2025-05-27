from OpenGL.GL import *
from logica_juego import colors, obtener_bloques,pantalla_alto, pantalla_ancho

tamanio_celda = 30

#dibujar celdas
def dibujar_celda(x, y, color):
    # Relleno
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x * tamanio_celda, y * tamanio_celda)
    glVertex2f((x + 1) * tamanio_celda, y * tamanio_celda)
    glVertex2f((x + 1) * tamanio_celda, (y + 1) * tamanio_celda)
    glVertex2f(x * tamanio_celda, (y + 1) * tamanio_celda)
    glEnd()
    # Borde negro
    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
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


def dibujar_fondo_tablero():
    glColor3f(0.08, 0.08, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(pantalla_ancho * tamanio_celda, 0)
    glVertex2f(pantalla_ancho * tamanio_celda, pantalla_alto * tamanio_celda)
    glVertex2f(0, pantalla_alto * tamanio_celda)
    glEnd()


def dibujar_preview(piece, px, py):
    # Dibuja fondo para la preview (opcional, ajusta tamaño si quieres)
    glColor3f(0.08, 0.08, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(px - 10, py - 10)
    glVertex2f(px + tamanio_celda * 4 + 10, py - 10)
    glVertex2f(px + tamanio_celda * 4 + 10, py + tamanio_celda * 4 + 10)
    glVertex2f(px - 10, py + tamanio_celda * 4 + 10)
    glEnd()

    shape = piece['shape']
    min_x = min(x for x, y in shape)
    max_x = max(x for x, y in shape)
    min_y = min(y for x, y in shape)
    max_y = max(y for x, y in shape)
    ancho = max_x - min_x + 1
    alto = max_y - min_y + 1

    offset_x = (4 - ancho) // 2 - min_x
    offset_y = (4 - alto) // 2 - min_y

    for x, y in shape:
        dibujar_celda_preview(
            px + (x + offset_x) * tamanio_celda,
            py + (y + offset_y) * tamanio_celda,
            colors[piece['type']]
        )


def dibujar_celda_preview(x, y, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + tamanio_celda, y)
    glVertex2f(x + tamanio_celda, y + tamanio_celda)
    glVertex2f(x, y + tamanio_celda)
    glEnd()
    # Borde negro
    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)
    glVertex2f(x + tamanio_celda, y)
    glVertex2f(x + tamanio_celda, y + tamanio_celda)
    glVertex2f(x, y + tamanio_celda)
    glEnd()