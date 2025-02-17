import pygame

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong en Python")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Propiedades de las paletas y la pelota
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

# Posiciones iniciales
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5  # Velocidad de la pelota

left_paddle_y = right_paddle_y = (HEIGHT - PADDLE_HEIGHT) // 2
paddle_speed = 6

# Puntuaciones
score_left = 0
score_right = 0

# Fuente para el marcador
font = pygame.font.Font(None, 36)

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Manejo de eventos
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento de las paletas
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += paddle_speed

    # Movimiento de la pelota
    ball_x += ball_dx
    ball_y += ball_dy

    # Rebote en las paredes superior e inferior
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # Detección de colisión con las paletas
    if (ball_x <= PADDLE_WIDTH and left_paddle_y < ball_y < left_paddle_y + PADDLE_HEIGHT) or \
       (ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE and right_paddle_y < ball_y < right_paddle_y + PADDLE_HEIGHT):
        ball_dx = -ball_dx

    # Si la pelota sale por la izquierda o derecha
    if ball_x < 0:
        score_right += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx = -ball_dx
    if ball_x > WIDTH:
        score_left += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx = -ball_dx

    # Dibujar elementos
    pygame.draw.rect(screen, WHITE, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Mostrar marcador
    score_text = font.render(f"{score_left}  -  {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 30, 20))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
