import pygame
from firebase_admin import db
from profile_manager import current_profile

WIDTH, HEIGHT = 800, 600
PAD_WIDTH, PAD_HEIGHT = 20, 100
BALL_SIZE = 20
BALL_SPEED = 5

def get_config(config_type):
    if current_profile:
        ref = db.reference(f'profiles/{current_profile}/config/{config_type}')
        return ref.get()
    return {}

def run_pong_inverted_controls():
    config = get_config('inverted_controls')
    ball_speed = config.get('ball_speed', BALL_SPEED)
    invert_time = config.get('invert_time', 5000)
    paddle_speed = ball_speed

    def game_loop():
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Controles Invertidos")

        left_pad_pos = HEIGHT // 2 - PAD_HEIGHT // 2
        right_pad_pos = HEIGHT // 2 - PAD_HEIGHT // 2
        ball_pos = [WIDTH // 2, HEIGHT // 2]
        ball_vel = [ball_speed, ball_speed]
        score_left = 0
        score_right = 0
        invert_controls = False
        last_invert_time = pygame.time.get_ticks()

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        font = pygame.font.Font(None, 36)

        running = True
        clock = pygame.time.Clock()

        def draw_winner(winner):
            screen.fill(BLACK)
            winner_text = font.render(f"{winner} es el ganador", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - 60))
            pygame.display.flip()
            pygame.time.wait(3000)

        while running:
            screen.fill(BLACK)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            current_time = pygame.time.get_ticks()
            if current_time - last_invert_time >= invert_time:
                invert_controls = not invert_controls
                last_invert_time = current_time

            if invert_controls:
                if keys[pygame.K_w] and left_pad_pos < HEIGHT - PAD_HEIGHT:
                    left_pad_pos += paddle_speed
                if keys[pygame.K_s] and left_pad_pos > 0:
                    left_pad_pos -= paddle_speed
                if keys[pygame.K_UP] and right_pad_pos < HEIGHT - PAD_HEIGHT:
                    right_pad_pos += paddle_speed
                if keys[pygame.K_DOWN] and right_pad_pos > 0:
                    right_pad_pos -= paddle_speed
            else:
                if keys[pygame.K_w] and left_pad_pos > 0:
                    left_pad_pos -= paddle_speed
                if keys[pygame.K_s] and left_pad_pos < HEIGHT - PAD_HEIGHT:
                    left_pad_pos += paddle_speed
                if keys[pygame.K_UP] and right_pad_pos > 0:
                    right_pad_pos -= paddle_speed
                if keys[pygame.K_DOWN] and right_pad_pos < HEIGHT - PAD_HEIGHT:
                    right_pad_pos += paddle_speed

            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]

            if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_SIZE:
                ball_vel[1] = -ball_vel[1]

            if (ball_pos[0] <= PAD_WIDTH and left_pad_pos < ball_pos[1] < left_pad_pos + PAD_HEIGHT) or \
               (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_SIZE and right_pad_pos < ball_pos[1] < right_pad_pos + PAD_HEIGHT):
                ball_vel[0] = -ball_vel[0]

            if ball_pos[0] < 0 or ball_pos[0] > WIDTH:
                if ball_pos[0] < 0:
                    score_right += 1
                else:
                    score_left += 1
                ball_pos = [WIDTH // 2, HEIGHT // 2]
                ball_vel = [ball_speed, ball_speed] if ball_pos[0] < 0 else [-ball_speed, -ball_speed]

            if score_left == 7:
                draw_winner("Jugador Izquierdo")
                running = False
            elif score_right == 7:
                draw_winner("Jugador Derecho")
                running = False

            pygame.draw.rect(screen, WHITE, (0, left_pad_pos, PAD_WIDTH, PAD_HEIGHT))
            pygame.draw.rect(screen, WHITE, (WIDTH - PAD_WIDTH, right_pad_pos, PAD_WIDTH, PAD_HEIGHT))
            pygame.draw.ellipse(screen, WHITE, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))

            score_text = font.render(f"{score_left}  -  {score_right}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 30, 20))

            invert_timer_text = font.render(f"Inversión en: {(invert_time - (current_time - last_invert_time)) // 1000}s", True, WHITE)
            screen.blit(invert_timer_text, (WIDTH // 2 - invert_timer_text.get_width() // 2, HEIGHT - 30))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    game_loop()

if __name__ == "__main__":
    run_pong_inverted_controls()