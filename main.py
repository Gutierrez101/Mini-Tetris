import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame.mixer

from logica_juego import (
    pantalla_ancho, pantalla_alto, crear_nueva_pieza,
    validar_posicion, fijar_piezas, limpiar_lineas, rotar_pieza
)
import graficos
from graficos import tamanio_celda

# Parámetros de pantalla con margen para UI
offset_x = 200  # espacio lateral para UI
screen_width = pantalla_ancho * tamanio_celda + offset_x
screen_height = pantalla_alto * tamanio_celda

# Inicialización
pygame.init()
pygame.mixer.init()
# Música de fondo
try:
    pygame.mixer.music.load("tetris_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"No se pudo cargar música: {e}")

# Sonidos de efectos
#effect_line = pygame.mixer.Sound("assets/clear.wav")
#effect_rotate = pygame.mixer.Sound("assets/rotate.wav")

# Fuente para texto (solo para medir tamaño)
font = pygame.font.SysFont("Arial", 24)

# Configuración de OpenGL
pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
gluOrtho2D(0, screen_width, screen_height, 0)
clock = pygame.time.Clock()

# Estado del juego
board = [[""] * pantalla_ancho for _ in range(pantalla_alto)]
current_piece = crear_nueva_pieza()
score = 0
fall_speed = 500  # ms
t_last = pygame.time.get_ticks()
paused = False

# Botón de pausa (posición y tamaño en coordenadas OpenGL)
pause_btn_x = pantalla_ancho* tamanio_celda + offset_x - 60
pause_btn_y = 20
pause_btn_w = 40
pause_btn_h = 40

running = True
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
            if not paused:
                if event.key == K_LEFT and validar_posicion(board, current_piece, (-1, 0)):
                    current_piece['position'][0] -= 1
                elif event.key == K_RIGHT and validar_posicion(board, current_piece, (1, 0)):
                    current_piece['position'][0] += 1
                elif event.key == K_DOWN and validar_posicion(board, current_piece, (0, 1)):
                    current_piece['position'][1] += 1
                elif event.key == K_SPACE:
                    while validar_posicion(board, current_piece, (0, 1)):
                        current_piece['position'][1] += 1
                    current_piece['position'][1] -= 1
                elif event.key == K_UP:
                    rotar_pieza(current_piece, board)
                    #effect_rotate.play()
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos
            # OpenGL y-axis inverted, adaptar coordenada
            my_gl = my
            if (pause_btn_x <= mx <= pause_btn_x + pause_btn_w and
                pause_btn_y <= my_gl <= pause_btn_y + pause_btn_h):
                paused = not paused

    # Lógica de caída
    if not paused and now - t_last > fall_speed:
        if validar_posicion(board, current_piece, (0, 1)):
            current_piece['position'][1] += 1
        else:
            fijar_piezas(board, current_piece)
            board, lines = limpiar_lineas(board)
            if lines > 0:
                score += lines * 100
                #effect_line.play()
            current_piece = crear_nueva_pieza()
            if not validar_posicion(board, current_piece):
                print(f"Game Over - Puntaje final: {score}")
                running = False
        t_last = now

    # Renderizado
    glClear(GL_COLOR_BUFFER_BIT)
    # Dibujar piezas
    graficos.draw_board(board)
    graficos.draw_piece(current_piece)

    # Línea separadora
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)
    x_sep = pantalla_ancho * tamanio_celda
    glVertex2f(x_sep, 0)
    glVertex2f(x_sep, screen_height)
    glEnd()

    # Fondo UI lateral
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(x_sep, 0)
    glVertex2f(screen_width, 0)
    glVertex2f(screen_width, screen_height)
    glVertex2f(x_sep, screen_height)
    glEnd()

    # Texto SCORE
    sombra = font.render("SCORE", True, (  0,   0,   0))
    dato_sombra =  pygame.image.tostring(sombra, "RGBA", True)
    glWindowPos2d(x_sep + 21, 31)
    glDrawPixels(sombra.get_width(), sombra.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, dato_sombra)
    # Texto SCORE - cuadro
    label = font.render("SCORE", True, (255, 255,   0))
    data = pygame.image.tostring(label, "RGBA", True)
    glWindowPos2d(x_sep+20, 30)
    glDrawPixels(label.get_width(), label.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data)

    # Valor del puntaje debajo
    value = font.render(str(score), True, (50, 205, 50))
    vd = pygame.image.tostring(value, "RGBA", True)
    glWindowPos2d(x_sep + 20, 60)
    glDrawPixels(value.get_width(), value.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, vd)

    # Botón Pausa - cuadro
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(pause_btn_x, pause_btn_y)
    glVertex2f(pause_btn_x + pause_btn_w, pause_btn_y)
    glVertex2f(pause_btn_x + pause_btn_w, pause_btn_y + pause_btn_h)
    glVertex2f(pause_btn_x, pause_btn_y + pause_btn_h)
    glEnd()
    # Dibujar '||'
    glColor3f(1, 1, 1)
    gap = 8
    bar_w = 6
    bar_h = pause_btn_h - 10
    bx = pause_btn_x + gap
    # primera barra
    glBegin(GL_QUADS)
    glVertex2f(bx, pause_btn_y + 5)
    glVertex2f(bx + bar_w, pause_btn_y + 5)
    glVertex2f(bx + bar_w, pause_btn_y + 5 + bar_h)
    glVertex2f(bx, pause_btn_y + 5 + bar_h)
    glEnd()
    # segunda barra
    bx2 = bx + bar_w + gap
    glBegin(GL_QUADS)
    glVertex2f(bx2, pause_btn_y + 5)
    glVertex2f(bx2 + bar_w, pause_btn_y + 5)
    glVertex2f(bx2 + bar_w, pause_btn_y + 5 + bar_h)
    glVertex2f(bx2, pause_btn_y + 5 + bar_h)
    glEnd()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()