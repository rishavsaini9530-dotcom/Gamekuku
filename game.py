import pygame
import random
import sys
import winsound  # विंडोज की पक्की और आसान आवाज़ के लिए!

# Pygame की शुरुआत करें
pygame.init()

# स्क्रीन की साइज
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Shooter - Final Edition")

# रंग (Colors)
BLACK = (10, 10, 25)
GREEN = (0, 255, 100)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)

# क्लॉक और फॉन्ट
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

def main():
    # खिलाड़ी (Player / हीरो)
    player_x = WIDTH // 2
    player_y = HEIGHT - 80
    player_size = 40
    player_speed = 7

    # गोलियां (Bullets)
    bullets = []

    # दुश्मन (Enemies / बंदे)
    enemies = []
    spawn_timer = 0

    # स्कोर और लाइफ
    score = 0
    lives = 3

    running = True
    while running:
        screen.fill(BLACK)

        # इवेंट्स चेक करें
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # स्पेसबार दबाने पर गोली चलेगी और आवाज़ आएगी
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append({"x": player_x + player_size // 2 - 4, "y": player_y})
                    try:
                        winsound.Beep(800, 50) # गोली चलने की आवाज़ (Frequency, Duration)
                    except:
                        pass

        # कीबोर्ड से चलना (बाएं और दाएं, आगे-पीछे)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > HEIGHT // 2:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
            player_y += player_speed

        # गोलियों को आगे बढ़ाना
        for b in bullets[:]:
            b["y"] -= 12
            if b["y"] < 0:
                bullets.remove(b)

        # दुश्मनों को पैदा करना (Spawning Enemies)
        spawn_timer += 1
        if spawn_timer > 25: 
            enemy_width = 40
            enemy_height = 40
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemy_y = -50
            enemy_speed = random.randint(3, 6) + (score // 50)
            enemies.append({"rect": pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height), "speed": enemy_speed})
            spawn_timer = 0

        # दुश्मनों की चाल और टक्कर (Collision) चेक करना
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        for enemy in enemies[:]:
            enemy["rect"].y += enemy["speed"]

            # अगर दुश्मन नीचे निकल जाए तो जान कम होगी
            if enemy["rect"].y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1
                try:
                    winsound.Beep(200, 150) # नुकसान की आवाज़
                except:
                    pass
                if lives <= 0:
                    running = False

            # गोली और दुश्मन की टक्कर (दुश्मन को मारना!)
            for b in bullets[:]:
                bullet_rect = pygame.Rect(b["x"], b["y"], 8, 15)
                if bullet_rect.colliderect(enemy["rect"]):
                    if enemy in enemies:
                        enemies.remove(enemy)
                    if b in bullets:
                        bullets.remove(b)
                    score += 10
                    try:
                        winsound.Beep(1200, 80) # दुश्मन के मरने की आवाज़
                    except:
                        pass
                    break

            # अगर दुश्मन सीधे खिलाड़ी से टकरा जाए
            if player_rect.colliderect(enemy["rect"]):
                enemies.remove(enemy)
                lives -= 1
                try:
                    winsound.Beep(150, 200)
                except:
                    pass
                if lives <= 0:
                    running = False

        # --- स्क्रीन पर सब कुछ बनाना ---
        pygame.draw.rect(screen, BLUE, player_rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, (player_x + player_size // 2 - 3, player_y - 10, 6, 12))

        for b in bullets:
            pygame.draw.rect(screen, YELLOW, (b["x"], b["y"], 8, 15), border_radius=3)

        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy["rect"], border_radius=6)
            pygame.draw.rect(screen, WHITE, (enemy["rect"].x + 8, enemy["rect"].y + 10, 6, 6))
            pygame.draw.rect(screen, WHITE, (enemy["rect"].x + 26, enemy["rect"].y + 10, 6, 6))

        score_text = font.render(f"Score: {score}", True, YELLOW)
        lives_text = font.render(f"Lives: {lives}", True, RED)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 55))

        pygame.display.flip()
        clock.tick(60)

    # --- गेम ओवर स्क्रीन ---
    while True:
        screen.fill((40, 0, 0))
        game_over_surf = big_font.render("GAME OVER", True, RED)
        score_surf = font.render(f"Final Score: {score}", True, WHITE)
        restart_surf = font.render("Press 'R' to Restart or 'ESC' to Quit", True, YELLOW)

        screen.blit(game_over_surf, (WIDTH // 2 - 140, HEIGHT // 2 - 60))
        screen.blit(score_surf, (WIDTH // 2 - 110, HEIGHT // 2))
        screen.blit(restart_surf, (WIDTH // 2 - 200, HEIGHT // 2 + 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

main()
