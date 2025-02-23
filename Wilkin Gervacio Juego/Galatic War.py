# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 800
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galactic War")

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Configuración del jugador
jugador_tamaño = 50
jugador_x = ANCHO // 2 - jugador_tamaño // 2
jugador_y = ALTO - 80
jugador_velocidad = 5
jugador_cooldown = 0
jugador_cooldown_max = 20

# Configuración de enemigos
enemigos = []
enemigo_tamaño = 40
enemigo_velocidad = 2
temporizador_spawn = 0
SPAWN_TIEMPO = 90
disparos_enemigos = []
velocidad_disparo_enemigo = 4
TIEMPO_DISPARO_ENEMIGO = 90

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Proyectiles
disparos = []
velocidad_disparo = -7

# Reloj
clock = pygame.time.Clock()

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Bucle principal
running = True
while running:
    screen.fill((0, 0, 0))  # Fondo negro

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wilkins Ismael Gervacio Carpio 23-EISN-2-036
    # Controles del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jugador_x > 0:
        jugador_x -= jugador_velocidad
    if keys[pygame.K_RIGHT] and jugador_x < ANCHO - jugador_tamaño:
        jugador_x += jugador_velocidad
    if keys[pygame.K_SPACE] and jugador_cooldown == 0:
        disparos.append([jugador_x + jugador_tamaño // 2, jugador_y])
        jugador_cooldown = jugador_cooldown_max

    # Reducir cooldown del jugador
    if jugador_cooldown > 0:
        jugador_cooldown -= 1

    # Wilkins Ismael Gervacio Carpio 23-EISN-2-036
    # Generar enemigos
    temporizador_spawn += 1
    if temporizador_spawn >= SPAWN_TIEMPO:
        enemigo_x = random.randint(0, ANCHO - enemigo_tamaño)
        enemigos.append([enemigo_x, 0, 0])
        # Enemigos disparan inmediatamente al aparecer
        disparos_enemigos.append([enemigo_x + enemigo_tamaño // 2, 0, 0, velocidad_disparo_enemigo])
        temporizador_spawn = 0

    # Mover enemigos
    for enemigo in enemigos[:]:
        enemigo[1] += enemigo_velocidad

        # Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Dibujar enemigo (rectángulo blanco)
        pygame.draw.rect(screen, (255, 255, 255), (enemigo[0], enemigo[1], enemigo_tamaño, enemigo_tamaño))

    # Mover balas del jugador
    for disparo in disparos[:]:
        disparo[1] += velocidad_disparo
        if disparo[1] < 0:
            disparos.remove(disparo)
        for enemigo in enemigos[:]:
            if enemigo[0] < disparo[0] < enemigo[0] + enemigo_tamaño and enemigo[1] < disparo[1] < enemigo[1] + enemigo_tamaño:
                enemigos.remove(enemigo)
                disparos.remove(disparo)
                break

    # Wilkins Ismael Gervacio Carpio 23-EISN-2-036
    # Mover balas de los enemigos (solo bajan en línea recta)
    for disparo_enemigo in disparos_enemigos[:]:
        disparo_enemigo[1] += velocidad_disparo_enemigo
        if disparo_enemigo[1] > ALTO:
            disparos_enemigos.remove(disparo_enemigo)

    # Dibujar jugador (rectángulo azul)
    pygame.draw.rect(screen, (0, 0, 255), (jugador_x, jugador_y, jugador_tamaño, jugador_tamaño))

    # Wilkins Ismael Gervacio Carpio 23-EISN-2-036
    # Dibujar balas del jugador (rectángulos rojos)
    for disparo in disparos:
        pygame.draw.rect(screen, (255, 0, 0), (disparo[0], disparo[1], 5, 10))

    # Dibujar balas de los enemigos (rectángulos amarillos)
    for disparo_enemigo in disparos_enemigos:
        pygame.draw.rect(screen, (255, 255, 0), (disparo_enemigo[0], disparo_enemigo[1], 10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036