# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
import pygame
import random
import math
import heapq

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
jugador_velocidad = 7
jugador_cooldown = 0
jugador_cooldown_max = 20
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Configuración de enemigos
enemigos = []
enemigo_tamaño = 40
enemigo_velocidad = 3
enemigo_velocidad_especial = 5
probabilidad_especial = 0.1  # 10% de probabilidad de que un enemigo sea especial
temporizador_spawn = 0
SPAWN_TIEMPO = 75
velocidad_disparo_enemigo = 6
TIEMPO_DISPARO_ENEMIGO = 90

# Proyectiles
disparos = []
velocidad_disparo = -7
explosiones = []
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Puntuación y vidas
puntos = 0
PUNTOS_MAXIMOS = 250
vidas = 3

# Reloj
clock = pygame.time.Clock()
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Distancia mínima para que los enemigos disparen
DISTANCIA_MINIMA_ATACAR = 800

# Pantallas
def pantalla_inicio():
    screen.fill((0, 0, 0))  
    texto = font.render("Presiona ENTER para empezar", True, (255, 255, 255))
    screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 25))
    pygame.display.flip()
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
def pantalla_perder():
    screen.fill((255, 0, 0))  
    texto = font.render(f"¡Perdiste! Puntos: {puntos}", True, (0, 0, 0))
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
def pantalla_victoria():
    screen.fill((0, 255, 0))  
    texto = font.render("¡Ganaste! Presiona ENTER para jugar de nuevo", True, (0, 0, 0))
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
    global jugador_x, jugador_y, jugador_cooldown, enemigos, disparos, disparos_enemigos, explosiones, temporizador_spawn, puntos, vidas, en_juego
    jugador_x = ANCHO // 2 - jugador_tamaño // 2
    jugador_y = ALTO - 80
    jugador_cooldown = 0
    enemigos = []
    disparos = []
    disparos_enemigos = []
    explosiones = []
    temporizador_spawn = 0
    puntos = 0
    vidas = 3
    en_juego = True

running = True
en_juego = False
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Configuración del grid para A*
GRID_ANCHO = ANCHO // 20
GRID_ALTO = ALTO // 20
grid = [[0 for _ in range(GRID_ANCHO)] for _ in range(GRID_ALTO)]

# Función para calcular la heurística (distancia euclidiana)
def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# Algoritmo A* para calcular la ruta óptima
def Astar(inicio, objetivo, grid):
    frontera = []
    heapq.heappush(frontera, (0, inicio))
    viene_de = {}
    cost_so_far = {}
    viene_de[inicio] = None
    cost_so_far[inicio] = 0

    while frontera:
        _, actual = heapq.heappop(frontera)

        if actual == objetivo:
            break

        for next in get_vecinos(actual, grid):
            new_cost = cost_so_far[actual] + 1  # Costo uniforme
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(objetivo, next)
                heapq.heappush(frontera, (priority, next))
                viene_de[next] = actual

    # Reconstruir el camino
    camino = []
    actual = objetivo
    while actual != inicio:
        camino.append(actual)
        actual = viene_de[actual]
    camino.reverse()
    return camino
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Función para obtener vecinos válidos en el grid
def get_vecinos(pos, grid):
    vecinos = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimientos en 4 direcciones
        x = pos[0] + dx
        y = pos[1] + dy
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0:  # 0 = espacio libre
            vecinos.append((x, y))
    return vecinos

while running:
    if not en_juego:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reiniciar_juego()
    else:
        if puntos >= PUNTOS_MAXIMOS:
            pantalla_victoria()

        screen.fill((0, 0, 0))  

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

        # Reducir cooldown del jugador
        if jugador_cooldown > 0:
            jugador_cooldown -= 1

        # Mover enemigos
        temporizador_spawn += 1
        if temporizador_spawn >= SPAWN_TIEMPO:
            # Decidir si el enemigo es especial (probabilidad de 5%)
            if random.random() < probabilidad_especial:
                enemigos.append([random.randint(0, ANCHO - enemigo_tamaño), 0, 0, True])  # True indica que es especial
            else:
                enemigos.append([random.randint(0, ANCHO - enemigo_tamaño), 0, 0, False])  # False indica que es normal
            temporizador_spawn = 0

        for enemigo in enemigos[:]:
            enemigo[1] += enemigo_velocidad if not enemigo[3] else enemigo_velocidad_especial  # Velocidad especial si es el enemigo morado
            enemigo[2] += 1

            # Dibujar enemigos (en color morado si es especial)
            if enemigo[3]:  # Si es el enemigo especial
                pygame.draw.rect(screen, (128, 0, 128), (enemigo[0], enemigo[1], enemigo_tamaño, enemigo_tamaño))  # Morado
            else:
                pygame.draw.rect(screen, (255, 255, 255), (enemigo[0], enemigo[1], enemigo_tamaño, enemigo_tamaño))  # Blanco para los enemigos normales

            # Verificar si el enemigo está cerca del jugador y puede disparar
            distance = math.sqrt((enemigo[0] - jugador_x) ** 2 + (enemigo[1] - jugador_y) ** 2)
            if distance < DISTANCIA_MINIMA_ATACAR and enemigo[2] >= TIEMPO_DISPARO_ENEMIGO:
                # Calcular la dirección del disparo hacia el jugador
                direccion_x = jugador_x - enemigo[0]
                direccion_y = jugador_y - enemigo[1]
                length = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
                if length != 0:
                    direccion_x /= length
                    direccion_y /= length
                disparos_enemigos.append([enemigo[0] + enemigo_tamaño // 2, enemigo[1], direccion_x * velocidad_disparo_enemigo, direccion_y * velocidad_disparo_enemigo])
                enemigo[2] = 0  # Reiniciar el temporizador de disparo

        # Mover balas del jugador
        for disparo in disparos[:]:
            disparo[1] += velocidad_disparo
            if disparo[1] < 0:
                disparos.remove(disparo)
            for enemigo in enemigos[:]:
                if enemigo[0] < disparo[0] < enemigo[0] + enemigo_tamaño and enemigo[1] < disparo[1] < enemigo[1] + enemigo_tamaño:
                    explosiones.append([enemigo[0], enemigo[1], 30])
                    enemigos.remove(enemigo)
                    disparos.remove(disparo)
                    if enemigo[3]:  # Si el enemigo es especial
                        puntos += 50  # 50 puntos por el enemigo morado
                    else:
                        puntos += 10  # 10 puntos por los enemigos normales
                    break

        # Mover balas de los enemigos
        for disparo_enemigo in disparos_enemigos[:]:
            disparo_enemigo[0] += disparo_enemigo[2]
            disparo_enemigo[1] += disparo_enemigo[3]
            if disparo_enemigo[1] > ALTO or disparo_enemigo[0] < 0 or disparo_enemigo[0] > ANCHO:
                disparos_enemigos.remove(disparo_enemigo)
            elif jugador_x < disparo_enemigo[0] < jugador_x + jugador_tamaño and jugador_y < disparo_enemigo[1] < jugador_y + jugador_tamaño:
                vidas -= 1  # Restar una vida
                disparos_enemigos.remove(disparo_enemigo)
                if vidas <= 0:
                    pantalla_perder()

        # Dibujar jugador
        pygame.draw.rect(screen, (0, 0, 255), (jugador_x, jugador_y, jugador_tamaño, jugador_tamaño))

        # Dibujar balas del jugador (líneas rojas)
        for disparo in disparos:
            pygame.draw.rect(screen, (255, 0, 0), (disparo[0], disparo[1], 5, 10))

        # Dibujar balas de los enemigos (líneas amarillas)
        for disparo_enemigo in disparos_enemigos:
            pygame.draw.rect(screen, (255, 255, 0), (disparo_enemigo[0], disparo_enemigo[1], 10, 10))

        # Dibujar explosiones (círculos naranjas)
        for explosion in explosiones[:]:
            pygame.draw.circle(screen, (255, 165, 0), (explosion[0] + enemigo_tamaño // 2, explosion[1] + enemigo_tamaño // 2), 20)
            explosion[2] -= 1
            if explosion[2] <= 0:
                explosiones.remove(explosion)

        # Dibujar las vidas en la esquina superior derecha
        for i in range(vidas):
            pygame.draw.rect(screen, (255, 105, 180), (ANCHO - 40 * (i + 1), 10, 30, 30))  # Cuadros rosas

        # Mostrar puntos
        texto_puntos = font.render(f"Puntos: {puntos}", True, (255, 255, 255))
        screen.blit(texto_puntos, (10, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()