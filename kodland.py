import pygame
import random
import sys

# Iniciar el modulo de pygame
pygame.init()

# Definir parametros iniciales como los colores o valores estandar
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
WIDTH = 800
HEIGHT = 600

# Parametros y creacion de la ventana de juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ataques sin fin! Esquivalos a todos!")

# Clase jugador, 2D
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 50)

   # Funcion de actualizacion de movimiento con las flechas
    def update(self):
        # Obtener entrada del teclado
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # If adicional para que el jugador no se salga de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Clase Enemigo, 2D
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedy = random.randrange(1, 8)
    #Funcion de actualizacion de los enemigos con random
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speedy = random.randrange(1, 8)
# Clase Menu
class Menu:
    def __init__(self, opciones):
        self.opciones = opciones
        self.font = pygame.font.Font(None, 48)
        self.seleccion = 0
   # Funcion dibujar menu
    def dibujar(self, superficie):
        for i, opcion in enumerate(self.opciones):
            color = BLANCO
            if self.seleccion == i:
                color = NEGRO
            texto = self.font.render(opcion, True, color)
            superficie.blit(texto, (ANCHO/2 - texto.get_width()/2, 200 + 
i*50))

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.seleccion -= 1
                    if self.seleccion < 0:
                        self.seleccion = len(self.opciones) - 1
                elif evento.key == pygame.K_DOWN:
                    self.seleccion += 1
                    if self.seleccion >= len(self.opciones):
                        self.seleccion = 0
                elif evento.key == pygame.K_RETURN:
                    return self.seleccion

opciones = ["Jugar", "Salir"]
# Crear sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Crear enemigos
for i in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Crear reloj
clock = pygame.time.Clock()

# Loop principal del juego
running = True
while running:
    Menu(opciones)
    # Mantener la velocidad de actualización en 60 FPS
    clock.tick(60)

    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar sprites
    all_sprites.update()

    # Choques
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # Dibujar todo
    screen.fill(BLUE)
    all_sprites.draw(screen)

    # Actualizar
    pygame.display.flip()

# Salir del juego
pygame.quit()
