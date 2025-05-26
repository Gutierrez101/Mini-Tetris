import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame.mixer

from logica_juego import (
    BOARD_WIDTH, BOARD_HEIGHT, create_new_piece,
    is_valid_position, fix_piece_to_board, clear_lines, rotate_piece
)
import graficos
from graficos import CELL_SIZE

# Parámetros de pantalla con margen para UI
offset_x = 200  # espacio lateral para UI
screen_width = BOARD_WIDTH * CELL_SIZE + offset_x
screen_height = BOARD_HEIGHT * CELL_SIZE

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

# Fuente para texto
font = pygame.font.SysFont("Arial", 24)
# Configuración de pantalla / OpenGL
display = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
gluOrtho2D(0, screen_width, screen_height, 0)
clock = pygame.time.Clock()

# Estado del juego
board = [[""] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
current_piece = create_new_piece()
score = 0
fall_speed = 500  # ms
t_last = pygame.time.get_ticks()
paused = False

# Botón de pausa (Rectángulo y símbolo '||')
pause_btn = pygame.Rect(BOARD_WIDTH * CELL_SIZE + 50, 100, 40, 40)

running = True
while running:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if pause_btn.collidepoint(event.pos):
                paused = not paused
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
            if not paused:
                if event.key == K_LEFT and is_valid_position(board, current_piece, (-1, 0)):
                    current_piece['position'][0] -= 1
                elif event.key == K_RIGHT and is_valid_position(board, current_piece, (1, 0)):
                    current_piece['position'][0] += 1
                elif event.key == K_DOWN and is_valid_position(board, current_piece, (0, 1)):
                    current_piece['position'][1] += 1
                elif event.key == K_SPACE:
                    while is_valid_position(board, current_piece, (0, 1)):
                        current_piece['position'][1] += 1
                    current_piece['position'][1] -= 1
                elif event.key == K_UP:
                    rotate_piece(current_piece, board)
                    #effect_rotate.play()

    # Lógica de caída
    if not paused and now - t_last > fall_speed:
        if is_valid_position(board, current_piece, (0, 1)):
            current_piece['position'][1] += 1
        else:
            fix_piece_to_board(board, current_piece)
            board, lines = clear_lines(board)
            if lines:
                score += lines * 100
                #effect_line.play()
            current_piece = create_new_piece()
            if not is_valid_position(board, current_piece):
                print(f"Game Over - Puntaje final: {score}")
                running = False
        t_last = now

    # Renderizado OpenGL de piezas
    glClear(GL_COLOR_BUFFER_BIT)
    graficos.draw_board(board)
    graficos.draw_piece(current_piece)

    # Superponer UI con Pygame
    screen = pygame.display.get_surface()
    # Fondo UI lateral
    ui_rect = pygame.Rect(BOARD_WIDTH * CELL_SIZE, 0, offset_x, screen_height)
    pygame.draw.rect(screen, (30, 30, 30), ui_rect)

    # Puntaje (estilo Tetris: arriba izquierda)
    score_label = font.render("SCORE", True, (255, 255, 255))
    score_value = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_label, (BOARD_WIDTH * CELL_SIZE + 20, 20))
    screen.blit(score_value, (BOARD_WIDTH * CELL_SIZE + 20, 50))

    # Botón pausa con símbolo '||'
    pygame.draw.rect(screen, (70, 70, 70), pause_btn)
    # Dibujar dos barras verticales
    bar_width = 8
    bar_height = 30
    bar_x = pause_btn.x + 8
    bar_y = pause_btn.y + 5
    pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (bar_x + bar_width + 5, bar_y, bar_width, bar_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()