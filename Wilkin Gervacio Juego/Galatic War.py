# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
import pygame
import random
import math
import heapq

# Inicialización de Pygame
pygame.init()

# Inicializar el módulo de joystick
pygame.joystick.init()

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Configuración de pantalla
ANCHO, ALTO = 800, 800
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Galactic War")

# Cargar imágenes
fondo_imagen = pygame.image.load("Imágenes/fondo.png")
jugador_imagen = pygame.image.load("Imágenes/nave.png")
vida_imagen = pygame.image.load("Imágenes/vida.png")
enemigo_1 = pygame.image.load("Imágenes/alien 1.png")
enemigo_2 = pygame.image.load("Imágenes/alien 2.png")
disparo_jugador_imagen = pygame.image.load("Imágenes/disparo jugador.png")
disparo_enemigo_imagen = pygame.image.load("Imágenes/disparo enemigo.png")
explosion_img = pygame.image.load("Imágenes/explosion.png")
pantalla_inicio_img = pygame.image.load("Imágenes/pantalla inicio.png")
pantalla_perder_img = pygame.image.load("Imágenes/pantalla muerte.png")
pantalla_ganar_img = pygame.image.load("Imágenes/pantalla victoria.png")
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Cargar sonidos
disparo_jugador_sonido = pygame.mixer.Sound("Audio/jugador disparo.mp3")
disparo_enemigo_sonido = pygame.mixer.Sound("Audio/enemigo disparo.mp3")
explosion_sonido = pygame.mixer.Sound("Audio/explosion enemigo.mp3")
pygame.mixer.music.load("Audio/musica.mp3")
pygame.mixer.music.set_volume(1)

# Fuente para los textos
font = pygame.font.Font(None, 50)
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036

# Detectar y conectar un joystick si hay uno disponible
if pygame.joystick.get_count() > 0:
    mando = pygame.joystick.Joystick(0)  # Usar el primer joystick detectado
    mando.init()
else:
    mando = None  # No hay joystick conectado

# Configuración del jugador
jugador_rect = jugador_imagen.get_rect()
jugador_tamaño = jugador_rect.width, jugador_rect.height
jugador_rect.centerx = ANCHO // 2
jugador_rect.bottom = ALTO - 80
jugador_velocidad = 7
jugador_cooldown = 0
jugador_cooldown_max = 20

# Configuración de enemigos
enemigos = []
enemigo_1_rect = enemigo_1.get_rect()
enemigo_2_rect = enemigo_2.get_rect()
enemigo_tamaño = enemigo_1_rect.width, enemigo_1_rect.height
enemigo_velocidad = 3
enemigo_velocidad_especial = 5
probabilidad_especial = 0.1  # 10% de probabilidad de que un enemigo sea especial
temporizador_spawn = 0
SPAWN_TIEMPO = 75
velocidad_disparo_enemigo = 8
TIEMPO_DISPARO_ENEMIGO = 120
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Proyectiles
disparos = []
velocidad_disparo = -7
explosiones = []

# Puntuación y vidas
puntos = 0
PUNTOS_MAXIMOS = 500
vidas = 3
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Reloj
clock = pygame.time.Clock()

# Distancia mínima para que los enemigos disparen
DISTANCIA_MINIMA_ATACAR = 800
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Pantallas
def pantalla_inicio():
    screen.blit(pantalla_inicio_img, (0, 0))
    pygame.display.flip()

def pantalla_perder():
    screen.blit(pantalla_perder_img, (0, 0))
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
        if mando and mando.get_button(9):
            reiniciar_juego()
            esperando = False

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
def pantalla_victoria():
    screen.blit(pantalla_ganar_img, (0, 0))
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
        if mando and mando.get_button(9):
            reiniciar_juego()
            esperando = False

# Estado del juego
def reiniciar_juego():
    global jugador_rect, jugador_cooldown, enemigos, disparos, disparos_enemigos, explosiones, temporizador_spawn, puntos, vidas, en_juego
    jugador_rect.centerx = ANCHO // 2
    jugador_rect.bottom = ALTO - 80
    jugador_cooldown = 0
    enemigos = []
    disparos = []
    disparos_enemigos = []
    explosiones = []
    temporizador_spawn = 0
    puntos = 0
    vidas = 3
    en_juego = True
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
running = True
en_juego = False

# Configuración del grid para A*
GRID_ANCHO = ANCHO // 20
GRID_ALTO = ALTO // 20
grid = [[0 for _ in range(GRID_ANCHO)] for _ in range(GRID_ALTO)]

# Función para calcular la heurística (distancia euclidiana)
def heuristic(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
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

# Árbol de comportamiento
class ArbolComportamiento:
    def __init__(self, root_node):
        self.root_node = root_node

    def run(self):
        return self.root_node.execute()

class Node:
    def execute(self):
        raise NotImplementedError

class Sequence(Node):
    def __init__(self, nodes):
        self.nodes = nodes

    def execute(self):
        for node in self.nodes:
            if not node.execute():
                return False
        return True

class Action(Node):
    def __init__(self, action_func):
        self.action_func = action_func

    def execute(self):
        return self.action_func()

class EliminarSiFueraDePantalla(Node):
    def __init__(self, enemigo):
        self.enemigo = enemigo

    def execute(self):
        if self.enemigo[1] > ALTO:  # Si el enemigo está fuera de la pantalla
            enemigos.remove(self.enemigo)
            return False  # Indicar que el enemigo fue eliminado
        return True  # El enemigo sigue en la pantalla

def crear_arbol_comportamiento(enemigo, jugador_rect):
    accion_mover = Action(lambda: mover_hacia_abajo(enemigo))
    accion_disparar = Action(lambda: disparar_hacia_jugador(enemigo, jugador_rect))
    accion_eliminar = EliminarSiFueraDePantalla(enemigo)

    # Secuencia: eliminar si está fuera de la pantalla, mover hacia abajo y luego disparar
    secuencia = Sequence([accion_eliminar, accion_mover, accion_disparar])

    return ArbolComportamiento(secuencia)

def mover_hacia_abajo(enemigo):
    enemigo[1] += enemigo_velocidad if not enemigo[3] else enemigo_velocidad_especial
    return True

def disparar_hacia_jugador(enemigo, jugador_rect):
    # Verificar si el enemigo puede disparar
    if enemigo[2] >= TIEMPO_DISPARO_ENEMIGO:
        # Calcular la dirección del disparo hacia el jugador
        direccion_x = jugador_rect.centerx - enemigo[0]
        direccion_y = jugador_rect.centery - enemigo[1]
        length = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
        if length != 0:
            direccion_x /= length
            direccion_y /= length
        disparos_enemigos.append([enemigo[0] + enemigo_tamaño[0] // 2, enemigo[1], direccion_x * velocidad_disparo_enemigo, direccion_y * velocidad_disparo_enemigo])
        disparo_enemigo_sonido.play()
        enemigo[2] = 0  # Reiniciar el temporizador de disparo

def calcular_direccion_disparo(enemigo, jugador_rect):
    inicio = (enemigo[0] // 20, enemigo[1] // 20)  # Posición del enemigo en el grid
    objetivo = (jugador_rect.centerx // 20, jugador_rect.centery // 20)  # Posición del jugador en el grid
    camino = Astar(inicio, objetivo, grid)
    if camino:
        # Calcular la dirección hacia el primer paso del camino
        dx = camino[0][0] - inicio[0]
        dy = camino[0][1] - inicio[1]
        return dx, dy
    return 0, 1  # Si no hay camino, disparar en línea recta hacia abajo

# Reproducir música de fondo
pygame.mixer.music.play(-1)
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
# Búcle principal
while running:
    if not en_juego:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reiniciar_juego()
            if mando and mando.get_button(9):  # Botón Start para iniciar
                reiniciar_juego()
    else:
        if puntos >= PUNTOS_MAXIMOS:
            pantalla_victoria()

        # Dibujar fondo
        screen.blit(fondo_imagen, (0, 0))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controles del jugador
        if mando:
            eje_x = mando.get_axis(0)  # Eje izquierdo horizontal
            if eje_x < -0.3 and jugador_rect.left > 0:  # Mover a la izquierda
                jugador_rect.x -= jugador_velocidad
            if eje_x > 0.3 and jugador_rect.right < ANCHO:  # Mover a la derecha
                jugador_rect.x += jugador_velocidad

            if mando.get_button(0) and jugador_cooldown == 0:  # Botón A / X para disparar
                disparos.append([jugador_rect.centerx, jugador_rect.top])
                disparo_jugador_sonido.play()
                jugador_cooldown = jugador_cooldown_max
        else:
            # Controles normales con teclado
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and jugador_rect.left > 0:
                jugador_rect.x -= jugador_velocidad
            if keys[pygame.K_RIGHT] and jugador_rect.right < ANCHO:
                jugador_rect.x += jugador_velocidad
            if keys[pygame.K_SPACE] and jugador_cooldown == 0:
                disparos.append([jugador_rect.centerx, jugador_rect.top])
                disparo_jugador_sonido.play()
                jugador_cooldown = jugador_cooldown_max

        # Reducir cooldown del jugador
        if jugador_cooldown > 0:
            jugador_cooldown -= 1
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Mover enemigos
        temporizador_spawn += 1
        if temporizador_spawn >= SPAWN_TIEMPO:
            # Decidir si el enemigo es especial (probabilidad de 10%)
            if random.random() < probabilidad_especial:
                enemigos.append([random.randint(0, ANCHO - enemigo_tamaño[0]), 0, TIEMPO_DISPARO_ENEMIGO, True])  # True indica que es especial
            else:
                enemigos.append([random.randint(0, ANCHO - enemigo_tamaño[0]), 0, TIEMPO_DISPARO_ENEMIGO, False])  # False indica que es normal
            temporizador_spawn = 0

        # Mover enemigos y disparar usando el árbol de comportamiento
        for enemigo in enemigos[:]:
            arbol = crear_arbol_comportamiento(enemigo, jugador_rect)
            arbol.run()

            # Dibujar enemigos
            if enemigo[3]:  # Si es el enemigo especial
                screen.blit(enemigo_2, (enemigo[0], enemigo[1]))
            else:
                screen.blit(enemigo_1, (enemigo[0], enemigo[1]))

            # Verificar si el enemigo puede disparar
            if enemigo[2] >= TIEMPO_DISPARO_ENEMIGO:
                # Calcular la dirección del disparo hacia el jugador
                direccion_x = jugador_rect.centerx - enemigo[0]
                direccion_y = jugador_rect.centery - enemigo[1]
                length = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
                if length != 0:
                    direccion_x /= length
                    direccion_y /= length
                disparos_enemigos.append([enemigo[0] + enemigo_tamaño[0] // 2, enemigo[1], direccion_x * velocidad_disparo_enemigo, direccion_y * velocidad_disparo_enemigo])
                disparo_enemigo_sonido.play()
                enemigo[2] = 0  # Reiniciar el temporizador de disparo
            else:
                enemigo[2] += 1  # Incrementar el temporizador

# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
            # Verificar si el enemigo está cerca del jugador y puede disparar
            distance = math.sqrt((enemigo[0] - jugador_rect.centerx) ** 2 + (enemigo[1] - jugador_rect.centery) ** 2)
            if distance < DISTANCIA_MINIMA_ATACAR and enemigo[2] >= TIEMPO_DISPARO_ENEMIGO:
                # Calcular la dirección del disparo hacia el jugador
                direccion_x = jugador_rect.centerx - enemigo[0]
                direccion_y = jugador_rect.centery - enemigo[1]
                length = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
                if length != 0:
                    direccion_x /= length
                    direccion_y /= length
                disparos_enemigos.append([enemigo[0] + enemigo_tamaño[0] // 2, enemigo[1], direccion_x * velocidad_disparo_enemigo, direccion_y * velocidad_disparo_enemigo])
                disparo_enemigo_sonido.play()
                enemigo[2] = 0  # Reiniciar el temporizador de disparo

        # Mover balas del jugador
        for disparo in disparos[:]:
            disparo[1] += velocidad_disparo
            if disparo[1] < 0:
                disparos.remove(disparo)
            for enemigo in enemigos[:]:
                if enemigo[0] < disparo[0] < enemigo[0] + enemigo_tamaño[0] and enemigo[1] < disparo[1] < enemigo[1] + enemigo_tamaño[1]:
                    explosiones.append([enemigo[0], enemigo[1], 30])
                    enemigos.remove(enemigo)
                    disparos.remove(disparo)
                    explosion_sonido.play()
                    if enemigo[3]:  # Si el enemigo es especial
                        puntos += 50  # 50 puntos por el enemigo morado
                    else:
                        puntos += 10  # 10 puntos por los enemigos normales
                    break
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Mover balas de los enemigos
        for disparo_enemigo in disparos_enemigos[:]:
            disparo_enemigo[0] += disparo_enemigo[2]
            disparo_enemigo[1] += disparo_enemigo[3]
            if disparo_enemigo[1] > ALTO or disparo_enemigo[0] < 0 or disparo_enemigo[0] > ANCHO:
                disparos_enemigos.remove(disparo_enemigo)
            elif jugador_rect.collidepoint(disparo_enemigo[0], disparo_enemigo[1]):
                vidas -= 1  # Restar una vida
                disparos_enemigos.remove(disparo_enemigo)
                if vidas <= 0:
                    pantalla_perder()

        # Dibujar jugador
        screen.blit(jugador_imagen, jugador_rect.topleft)
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Dibujar balas del jugador
        for disparo in disparos:
            screen.blit(disparo_jugador_imagen, (disparo[0], disparo[1]))

        # Dibujar balas de los enemigos
        for disparo_enemigo in disparos_enemigos:
            screen.blit(disparo_enemigo_imagen, (disparo_enemigo[0], disparo_enemigo[1]))
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Dibujar explosiones
        for explosion in explosiones[:]:
            screen.blit(explosion_img, (explosion[0], explosion[1]))
            explosion[2] -= 1
            if explosion[2] <= 0:
                explosiones.remove(explosion)

        # Dibujar las vidas en la esquina superior derecha
        for i in range(vidas):
            screen.blit(vida_imagen, (ANCHO - 40 * (i + 1), 10))
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036
        # Mostrar puntos
        texto_puntos = font.render(f"Puntos: {puntos}", True, (255, 255, 255))
        screen.blit(texto_puntos, (10, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
# Wilkins Ismael Gervacio Carpio 23-EISN-2-036