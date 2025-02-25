# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 800
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galactic War")
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Fuente para los textos
font = pygame.font.Font(None, 50)

# Configuración del jugador
jugador_tamaño = 50
jugador_x = ANCHO // 2 - jugador_tamaño // 2
jugador_y = ALTO - 80
jugador_velocidad = 5
jugador_cooldown = 0
jugador_cooldown_max = 20

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Configuración de enemigos
enemigos = []
enemigo_tamaño = 40
enemigo_velocidad = 2
temporizador_spawn = 0
SPAWN_TIEMPO = 90
disparos_enemigos = []
velocidad_disparo_enemigo = 4
TIEMPO_DISPARO_ENEMIGO = 90

# Proyectiles
disparos = []
velocidad_disparo = -7
explosiones = []

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Reloj
clock = pygame.time.Clock()

# Distancia mínima para que los enemigos disparen
DISTANCIA_MINIMA_ATACAR = 200

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Pantallas
def pantalla_inicio():
    screen.fill((0, 0, 0))  # Pantalla negra
    texto = font.render("Presiona ENTER para empezar", True, (255, 255, 255))
    screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 25))
    pygame.display.flip()

def pantalla_perder():
    screen.fill((255, 0, 0))  # Pantalla roja
    texto = font.render("Presiona ENTER para reintentar", True, (0, 0, 0))
    screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 25))
    pygame.display.flip()
    pygame.time.delay(1000)
    
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reiniciar_juego()
                esperando = False

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Estado del juego
def reiniciar_juego():
    global jugador_x, jugador_y, jugador_cooldown, enemigos, disparos, disparos_enemigos, explosiones, temporizador_spawn, en_juego
    jugador_x = ANCHO // 2 - jugador_tamaño // 2
    jugador_y = ALTO - 80
    jugador_cooldown = 0
    enemigos = []
    disparos = []
    disparos_enemigos = []
    explosiones = []
    temporizador_spawn = 0
    en_juego = True

running = True
en_juego = False

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
while running:
    if not en_juego:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reiniciar_juego()

    else:
        screen.fill((0, 0, 0))  # Fondo negro
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controles del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and jugador_x > 0:
            jugador_x -= jugador_velocidad
        if keys[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_tamaño:
            jugador_x += jugador_velocidad
        if keys[pygame.K_SPACE] and jugador_cooldown == 0:
            disparos.append([jugador_x + jugador_tamaño // 2, jugador_y])
            jugador_cooldown = jugador_cooldown_max
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Reducir cooldown del jugador
        if jugador_cooldown > 0:
            jugador_cooldown -= 1

        # Mover enemigos
        temporizador_spawn += 1
        if temporizador_spawn >= SPAWN_TIEMPO:
            enemigos.append([random.randint(0, ANCHO - enemigo_tamaño), 0, 0])
            temporizador_spawn = 0
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        for enemy in enemigos[:]:
            enemy[1] += enemigo_velocidad
            enemy[2] += 1

            # Dibujar enemigo (rectángulo blanco)
            pygame.draw.rect(screen, (255, 255, 255), (enemy[0], enemy[1], enemigo_tamaño, enemigo_tamaño))
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
            # Calcular la distancia entre el enemigo y el jugador
            distance = math.sqrt((enemy[0] - jugador_x) ** 2 + (enemy[1] - jugador_y) ** 2)

            # Solo disparan en la parte inferior
            if enemy[2] >= TIEMPO_DISPARO_ENEMIGO and distance < DISTANCIA_MINIMA_ATACAR:
                direccion_x = jugador_x + jugador_tamaño // 2 - (enemy[0] + enemigo_tamaño // 2)
                direccion_y = jugador_y - enemy[1]
                length = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
                if length != 0:
                    direccion_x /= length
                    direccion_y /= length
                disparos_enemigos.append([enemy[0] + enemigo_tamaño // 2, enemy[1], direccion_x * velocidad_disparo_enemigo, direccion_y * velocidad_disparo_enemigo])
                enemy[2] = 0
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Mover balas del jugador
        for disparo in disparos[:]:
            disparo[1] += velocidad_disparo
            if disparo[1] < 0:
                disparos.remove(disparo)
            for enemy in enemigos[:]:
                if enemy[0] < disparo[0] < enemy[0] + enemigo_tamaño and enemy[1] < disparo[1] < enemy[1] + enemigo_tamaño:
                    explosiones.append([enemy[0], enemy[1], 30])
                    enemigos.remove(enemy)
                    disparos.remove(disparo)
                    break

        # Mover balas de los enemigos
        for disparo_enemigo in disparos_enemigos[:]:
            disparo_enemigo[0] += disparo_enemigo[2]
            disparo_enemigo[1] += disparo_enemigo[3]
            if disparo_enemigo[1] > ALTO or disparo_enemigo[0] < 0 or disparo_enemigo[0] > ANCHO:
                disparos_enemigos.remove(disparo_enemigo)
            elif jugador_x < disparo_enemigo[0] < jugador_x + jugador_tamaño and jugador_y < disparo_enemigo[1] < jugador_y + jugador_tamaño:
                pantalla_perder()
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Dibujar jugador (rectángulo azul)
        pygame.draw.rect(screen, (0, 0, 255), (jugador_x, jugador_y, jugador_tamaño, jugador_tamaño))

        # Dibujar balas del jugador (líneas rojas)
        for disparo in disparos:
            pygame.draw.rect(screen, (255, 0, 0), (disparo[0], disparo[1], 5, 10))
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Dibujar balas de los enemigos (líneas amarillas)
        for disparo_enemigo in disparos_enemigos:
            pygame.draw.rect(screen, (255, 255, 0), (disparo_enemigo[0], disparo_enemigo[1], 10, 10))

        # Dibujar explosiones (círculos naranjas)
        for explosion in explosiones[:]:
            pygame.draw.circle(screen, (255, 165, 0), (explosion[0] + enemigo_tamaño // 2, explosion[1] + enemigo_tamaño // 2), 20)
            explosion[2] -= 1
            if explosion[2] <= 0:
                explosiones.remove(explosion)
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        pygame.display.flip()
        clock.tick(60)

pygame.quit()
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036