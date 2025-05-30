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
ancho_pantalla = pantalla_ancho * tamanio_celda + offset_x
alto_pantalla = pantalla_alto * tamanio_celda

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
#linea_efecto = pygame.mixer.Sound("assets/clear.wav")
#efecto_rotar = pygame.mixer.Sound("assets/rotate.wav")

# Fuente para texto (solo para medir tamaño)
font = pygame.font.SysFont("Arial", 24)

# Configuración de OpenGL
pygame.display.set_mode((ancho_pantalla, alto_pantalla), DOUBLEBUF | OPENGL)
gluOrtho2D(0, ancho_pantalla, alto_pantalla, 0)
clock = pygame.time.Clock()

# Estado del juego
board = [[""] * pantalla_ancho for _ in range(pantalla_alto)]
current_piece = crear_nueva_pieza()
next_piece = crear_nueva_pieza()  # Nueva pieza
score = 0
fall_speed = 500  # ms
t_last = pygame.time.get_ticks()
paused = False

# Botón de pausa (posición y tamaño en coordenadas OpenGL)
pause_btn_x = pantalla_ancho* tamanio_celda + offset_x - 60
pause_btn_y = 20
pause_btn_w = 40
pause_btn_h = 40

x_sep = pantalla_ancho * tamanio_celda

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
            current_piece = next_piece  # Cambiar a la siguiente pieza
            next_piece = crear_nueva_pieza()  # Crear nueva pieza
            if not validar_posicion(board, current_piece):
                print(f"Game Over - Puntaje final: {score}")
                running = False
        t_last = now

    # Renderizado
    glClear(GL_COLOR_BUFFER_BIT)
    x_sep = pantalla_ancho * tamanio_celda  # <--- Agrega esto aquí
    graficos.dibujar_pantalla(board)
    graficos.dibujar_pieza(current_piece)
    graficos.dibujar_preview(next_piece, x_sep + 40, 150)  # Solo esta línea para la preview

    # Línea separadora
    glColor3f(1, 1, 1)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex2f(x_sep, 0)
    glVertex2f(x_sep, alto_pantalla)
    glEnd()

    # Fondo UI lateral
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(x_sep, 0)
    glVertex2f(ancho_pantalla, 0)
    glVertex2f(ancho_pantalla, alto_pantalla)
    glVertex2f(x_sep, ancho_pantalla)
    glEnd()

    # Texto SCORE
    sombra = font.render("SCORE", True, (  0,   0,   0))
    dato_sombra =  pygame.image.tostring(sombra, "RGBA", True)
    glWindowPos2d(x_sep + 21, 31)
    # Activa el blending para que el texto se vea
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
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

    # Botón Pausa - cuadro (cambia color si está pausado)
    if paused:
        glColor3f(0.8, 0.3, 0.3)
    else:
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

    # Si está pausado, muestra texto grande en el centro
    if paused:
        pausa_label = font.render("PAUSA", True, (255, 0, 0))
        pausa_data = pygame.image.tostring(pausa_label, "RGBA", True)
        glWindowPos2d(ancho_pantalla // 2 - pausa_label.get_width() // 2, alto_pantalla // 2 - pausa_label.get_height() // 2)
        glDrawPixels(pausa_label.get_width(), pausa_label.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pausa_data)

    # Texto "SIGUIENTE"
    sombra_next = font.render("SIGUIENTE", True, (0, 0, 0))
    dato_sombra_next = pygame.image.tostring(sombra_next, "RGBA", True)
    glWindowPos2d(x_sep + 21, 111)
    glDrawPixels(sombra_next.get_width(), sombra_next.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, dato_sombra_next)
    label_next = font.render("SIGUIENTE", True, (0, 255, 255))
    data_next = pygame.image.tostring(label_next, "RGBA", True)
    glWindowPos2d(x_sep + 20, 110)
    glDrawPixels(label_next.get_width(), label_next.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, data_next)

    # Vista previa de la siguiente pieza
    graficos.dibujar_preview(next_piece, x_sep + 40, 150)  # Puedes ajustar el 150 para mover la figura

    pygame.display.flip()
    clock.tick(60)
    # Perdida
    if not running:
        # Mostrar mensaje en pantalla
        game_over_label = font.render("GAME OVER", True, (255, 0, 0))
        game_over_data = pygame.image.tostring(game_over_label, "RGBA", True)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glWindowPos2d(
            ancho_pantalla // 2 - game_over_label.get_width() // 2,
            alto_pantalla // 2 - 100
        )
        glDrawPixels(
            game_over_label.get_width(),
            game_over_label.get_height(),
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            game_over_data
        )

        # Botón Reintentar
        retry_x = ancho_pantalla // 2 - 110
        retry_y = alto_pantalla// 2
        retry_w = 100
        retry_h = 50

        # Botón Cerrar
        close_x = ancho_pantalla // 2 + 10
        close_y = alto_pantalla // 2
        close_w = 100
        close_h = 50

        # Dibujar botones
        # Reintentar
        glColor3f(0.2, 0.6, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(retry_x, retry_y)
        glVertex2f(retry_x + retry_w, retry_y)
        glVertex2f(retry_x + retry_w, retry_y + retry_h)
        glVertex2f(retry_x, retry_y + retry_h)
        glEnd()

        # Texto "Reintentar" centrado
        retry_label = font.render("Reintentar", True, (255, 255, 255))
        retry_data = pygame.image.tostring(retry_label, "RGBA", True)
        retry_text_x = retry_x + (retry_w - retry_label.get_width()) // 2
        retry_text_y = retry_y + (retry_h - retry_label.get_height()) // 2
        glWindowPos2d(retry_text_x, retry_text_y)
        glDrawPixels(retry_label.get_width(), retry_label.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, retry_data)

        # Cerrar
        glColor3f(0.7, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex2f(close_x, close_y)
        glVertex2f(close_x + close_w, close_y)
        glVertex2f(close_x + close_w, close_y + close_h)
        glVertex2f(close_x, close_y + close_h)
        glEnd()

        # Texto "Cerrar" centrado
        close_label = font.render("Cerrar", True, (255, 255, 255))
        close_data = pygame.image.tostring(close_label, "RGBA", True)
        close_text_x = close_x + (close_w - close_label.get_width()) // 2
        close_text_y = close_y + (close_h - close_label.get_height()) // 2
        glWindowPos2d(close_text_x, close_text_y)
        glDrawPixels(close_label.get_width(), close_label.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, close_data)

        pygame.display.flip()

        # Esperar click en botón
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == QUIT:
                    esperando = False
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if retry_x <= mx <= retry_x + retry_w and retry_y <= my <= retry_y + retry_h:
                        # Reintentar: reiniciar variables y volver al juego
                        board = [[""] * pantalla_ancho for _ in range(pantalla_alto)]
                        current_piece = crear_nueva_pieza()
                        next_piece = crear_nueva_pieza()
                        score = 0
                        fall_speed = 500
                        t_last = pygame.time.get_ticks()
                        paused = False
                        running = True
                        esperando = False
                    elif close_x <= mx <= close_x + close_w and close_y <= my <= close_y + close_h:
                        esperando = False
                        running = False
            pygame.time.wait(10)
        if not running:
            break
pygame.quit()