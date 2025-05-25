#Modulo principla y el cual ejecuta el juego
#Encargado: Mateo Gutierrez
#Fecha: 23/05/2025
#Version: 1.0

#importar librerias
import pygame 
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
#from figura import generar_figura,mover,bajar
#from tablero import crear_tablero,validar_posicion,fijar_figura,limpiar_lineas

#variables globales
ancho_celda=30
tablero_ancho=10
tablero_alto=20
velocidad_caida=500 #milisegundos

#Funciones para el tablero
def dibujar_tablero(tablero):
    for y,fila in enumerate(tablero):
        for x,celda in enumerate(fila):
            if celda:
                dibujar_celda(x,y)

#funcion para dibujar una figura
def dibujar_figura(figura,pos):
    for x,i in figura:
        dibujar_celda(x+pos[0],y+pos[0])

#funcion para dibujar las celdas
def dibujar_celda(x,y):
    glBegin(GL_QUADS)
    glColor3f(1,0,0)
    glVertex2f(x*ancho_celda, y*ancho_celda)
    glVertex2f((x+1)*ancho_celda,y*ancho_celda)
    glVertex2f((x+1)*ancho_celda,(y+1)*ancho_celda)
    glVertex2f(x*ancho_celda,(y+1)*ancho_celda)
    glEnd()


#funcion principales y logica del juegp
def main():
    pygame.init()
    pantalla=pygame.display.set_mode((tablero_ancho*ancho_celda,tablero_alto*ancho_celda),DOUBLEBUF|OPENGL)
    gluOrtho2D(0,tablero_ancho*ancho_celda,tablero_alto*ancho_celda,0)

    tablero=crear_tablero(tablero_ancho,tablero_alto)
    figura=generar_figura()
    pos=[tablero_ancho//2-1,0]  # Posición inicial de la figura
    tiempo_caida=pygame.time.get_ticks()

    running=True
    while running:
        glClear(GL_COLOR_BUFFER_BIT)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                running = False
            if evento.type == KEYDOWN:
                if evento.key == K_LEFT:
                    nueva_pos= [pos[0]-1, pos[1]]
                    if validar_posicion(tablero, figura, nueva_pos):
                        pos = nueva_pos
                elif evento.key == K_RIGHT:
                    nueva_pos = [pos[0]+1, pos[1]]
                    if validar_posicion(tablero, figura, nueva_pos):
                        pos = nueva_pos
                elif evento.key == K_DOWN:
                    nueva_pos = [pos[0], pos[1]+1]
                    if validar_posicion(tablero, figura, nueva_pos):
                        pos = nueva_pos
                elif evento.key == K_SPACE:
                    fijar_figura(tablero,figura,pos)
                    tablero,_=limpiar_lineas(tablero)
                    figura=generar_figura()
                    pos=[tablero_ancho//2-1,0]
        if pygame.time.get_ticks() - tiempo_caida > velocidad_caida:   
            tiempo_caida= pygame.time.get_ticks()
            nueva_pos = [pos[0], pos[1]+1]
            if validar_posicion(tablero, figura, nueva_pos):
                pos = nueva_pos
            else:
                fijar_figura(tablero, figura, pos)
                tablero, _ = limpiar_lineas(tablero)
                figura = generar_figura()
                pos = [tablero_ancho//2-1, 0]
                if not validar_posicion(tablero,figura,pos):
                    print("Juego terminado")
                    running = False
        
        dibujar_tabler(tablero)
        dibujar_figura(figura, pos)
        pygame.display.flip()
        pygame.time.delay(50)
    
    pygame.quit()



main()
