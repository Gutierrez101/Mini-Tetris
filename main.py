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

# Inicialización
pygame.init()
pygame.mixer.init()
font = pygame.font.SysFont("Arial", 24)

screen_size = (BOARD_WIDTH * graficos.CELL_SIZE, BOARD_HEIGHT * graficos.CELL_SIZE)
pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
gluOrtho2D(0, screen_size[0], screen_size[1], 0)
clock = pygame.time.Clock()

# Carga de sonidos
effect_line = pygame.mixer.Sound("tetris_music.wav")
#effect_rotate = pygame.mixer.Sound("assets/rotate.wav")

# Estado del juego
board = [[""] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
current_piece = create_new_piece()
score = 0
fall_speed = 500  # milisegundos
last_fall = pygame.time.get_ticks()
paused = False

running = True
while running:
    now = pygame.time.get_ticks()

    # Eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
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
                    # Caída instantánea
                    while is_valid_position(board, current_piece, (0, 1)):
                        current_piece['position'][1] += 1
                    current_piece['position'][1] -= 1
                elif event.key == K_UP:
                    rotate_piece(current_piece, board)
                    #effect_rotate.play()

    # Lógica de caída automática
    if not paused and now - last_fall > fall_speed:
        if is_valid_position(board, current_piece, (0, 1)):
            current_piece['position'][1] += 1
        else:
            fix_piece_to_board(board, current_piece)
            board, lines = clear_lines(board)
            if lines > 0:
                score += lines * 100
                effect_line.play()
            current_piece = create_new_piece()
            if not is_valid_position(board, current_piece):
                print("Game Over - Puntaje final:", score)
                running = False
        last_fall = now

    # Renderizado
    glClear(GL_COLOR_BUFFER_BIT)
    graficos.draw_board(board)
    graficos.draw_piece(current_piece)

    # Dibujar puntaje
    score_surf = font.render(f"Puntaje: {score}", True, (255, 255, 255))
    score_data = pygame.image.tostring(score_surf, "RGBA", True)
    glWindowPos2d(10, 10)
    glDrawPixels(score_surf.get_width(), score_surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, score_data)

    # Dibujar pausa
    if paused:
        pause_surf = font.render("PAUSA", True, (255, 255, 0))
        pause_data = pygame.image.tostring(pause_surf, "RGBA", True)
        glWindowPos2d((BOARD_WIDTH * graficos.CELL_SIZE)//2 - 40, (BOARD_HEIGHT * graficos.CELL_SIZE)//2)
        glDrawPixels(pause_surf.get_width(), pause_surf.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, pause_data)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()