from constants import *


class Tank(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()

        self.x, self.y = WINDOW_WIDTH // 2, WINDOW_HEIGHT - WINDOW_MARGIN - DASHBOARD_HEIGHT - WINDOW_PADDING

    def fire(self, bullets):
        if len(bullets) >= MAX_BULLETS_ON_SCREEN:
            return
        bullet = Bullet(BULLET_TANK, UP_DIRECTION, BULLET_SPEED)
        bullet.x, bullet.y = self.x + int(self.rect.width * .7), self.y
        bullets.append(bullet)

    def position(self):
        return pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)


class Alien:
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.dir = 1
        self.x, self.y = WINDOW_WIDTH // 2, WINDOW_HEIGHT - WINDOW_MARGIN - DASHBOARD_HEIGHT - WINDOW_PADDING

    def fire(self, bullets):
        bullet = Bullet(BULLET, DOWN_DIRECTION, BULLET_SPEED)
        bullet.x, bullet.y = self.x + int(self.rect.width * (random.randint(1, 9) / 10)), self.y + int(
            self.rect.height * .9)
        bullets.append(bullet)

    def move(self):
        increment = self.rect.height
        if self.x > WINDOW_WIDTH - 2 * (WINDOW_MARGIN + WINDOW_PADDING) - self.rect.width // 2:
            self.dir = -1
            self.y += increment
        if self.x < WINDOW_MARGIN + WINDOW_PADDING:
            self.dir = 1
            self.y += increment

        self.x += self.dir * ALIEN_SPEED

    def position(self):
        return pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)


# differences: image, direction
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()

        self.x, self.y = None, None
        self.dir = direction
        self.speed = speed

    def move(self):
        if self.y > WINDOW_HEIGHT - WINDOW_PADDING - WINDOW_MARGIN:
            return
        self.y += self.dir * self.speed

    def position(self):
        return pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)


alienBullets = []
tankBullets = []
enemies = []


def create_enemy() -> None:
    alien = Alien(ALIEN_SHIP)
    alien.x = WINDOW_MARGIN + WINDOW_PADDING
    alien.y = WINDOW_MARGIN + DASHBOARD_HEIGHT + WINDOW_PADDING
    enemies.append(alien)


def run_game():
    # game attrib
    HITS = 0
    BULLETS_USED = 0
    LIVES_LEFT = 10

    # game variables
    create_enemy()
    tank = Tank(TANK)
    running = True
    clock = pygame.time.Clock()
    WINDOW.fill(BLACK)

    font = pygame.font.SysFont('Futura', 25, True, False)

    # utility variables
    deadAliens = []
    before = time.time()
    d = float('inf')

    while running:
        clock.tick(FPS)
        WINDOW.blit(BACKGROUND, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.draw.rect(WINDOW, BORDER_COLOR,
                         (WINDOW_MARGIN, WINDOW_PADDING, WINDOW_WIDTH - 2 * WINDOW_MARGIN + 10, 10 + DASHBOARD_HEIGHT),
                         )
        pygame.draw.rect(WINDOW, BACKGROUND_COLOR,
                         (WINDOW_MARGIN + 5, WINDOW_PADDING + 5, WINDOW_WIDTH - 2 * WINDOW_MARGIN, DASHBOARD_HEIGHT)
                         )

        # draw game metrics here

        WINDOW.blit(font.render(f'HITS: {HITS}', 1, RED),
                    (WINDOW_MARGIN + 3 * WINDOW_PADDING, int(2.5 * WINDOW_PADDING)))
        WINDOW.blit(font.render(f'BULLETS: {BULLETS_USED}', 1, GREEN),
                    (WINDOW_MARGIN + WINDOW_PADDING + 200, int(2.5 * WINDOW_PADDING)))
        WINDOW.blit(font.render(f'LIVES LEFT: {LIVES_LEFT}', 1, YELLOW),
                    (WINDOW_MARGIN + WINDOW_PADDING + 450, int(2.5 * WINDOW_PADDING)))

        pygame.draw.rect(WINDOW, BORDER_COLOR,
                         (0 + WINDOW_MARGIN, 0 + WINDOW_MARGIN + DASHBOARD_HEIGHT, WINDOW_WIDTH - 2 * WINDOW_MARGIN,
                          WINDOW_HEIGHT - 2 * WINDOW_MARGIN - DASHBOARD_HEIGHT),
                         5)

        WINDOW.blit(tank.image, (tank.x, tank.y))

        for enemy in enemies:
            WINDOW.blit(enemy.image, (enemy.x, enemy.y))
            enemy.move()

        bulletsOutOfScreen = []
        for bullet in tankBullets + alienBullets:
            WINDOW.blit(bullet.image, (bullet.x, bullet.y))
            bullet.move()
            if (bullet.dir == UP_DIRECTION and bullet.y < WINDOW_MARGIN + DASHBOARD_HEIGHT + WINDOW_PADDING) or \
                    (bullet.dir == DOWN_DIRECTION and bullet.y > WINDOW_HEIGHT - WINDOW_MARGIN - WINDOW_PADDING):
                bulletsOutOfScreen.append(bullet)

        for bullet in bulletsOutOfScreen:
            if bullet in tankBullets:
                tankBullets.remove(bullet)
            if bullet in alienBullets:
                alienBullets.remove(bullet)

        for bullet in tankBullets:
            for alien in enemies:
                if pygame.Rect.colliderect(bullet.position(), alien.position()) \
                        and (alien not in deadAliens):
                    print("🎯")
                    EXPLODE.play()
                    HITS += 1
                    tankBullets.remove(bullet)
                    alien.image = EXPLOSION
                    deadAliens.append((alien, time.time()))
                    break

        deadAliensCopy = deadAliens[:]

        for alien in deadAliensCopy:
            if time.time() - alien[1] > IMPRESSION_TIME:
                try:
                    enemies.remove(alien[0])
                except ValueError:
                    pass
                else:
                    deadAliens.remove(alien)

        del deadAliensCopy

        # check for bullets hitting player
        for bullet in alienBullets:
            if pygame.Rect.colliderect(bullet.position(), tank.position()):
                alienBullets.remove(bullet)
                if d == float('inf'):
                    LIVES_LEFT -= 1
                    SHOOT_2.play()
                if LIVES_LEFT < 1 and d == float('inf'):
                    tank.image = EXPLOSION
                    EXPLODE.play()
                    d = time.time()

        for alien in enemies:
            if pygame.Rect.colliderect(alien.position(), tank.position()) and d == float('inf'):
                tank.image = EXPLOSION
                alien.image = EXPLOSION
                SHOOT_2.play()
                EXPLODE.play()
                deadAliens.append((alien, time.time()))
                d = time.time()

        # create enemies
        if time.time() - before > IMPRESSION_TIME * 8 and random.random() > ALIEN_CHANCE:
            before = time.time()
            create_enemy()

        # enemies fire at random
        for alien in enemies:
            if time.time() - before > IMPRESSION_TIME * 5 and random.random() > SHOOT_CHANCE:
                alien.fire(alienBullets)
                before = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tank.fire(tankBullets)
                    SHOOT.play()
                    BULLETS_USED += 1

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_RIGHT]:
            if tank.x < WINDOW_WIDTH - WINDOW_MARGIN - WINDOW_PADDING - tank.rect.width:
                tank.x += SPEED
        if keys_pressed[pygame.K_LEFT]:
            if tank.x > WINDOW_MARGIN + WINDOW_PADDING:
                tank.x -= SPEED

        if time.time() - d > IMPRESSION_TIME * 10:
            running = False

        pygame.display.flip()
        pygame.display.update()

    WINDOW.blit(font.render("GAME ENDED!!!", 0, RED),
                (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2))
    pygame.display.update()

    end_game = True
    while end_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP or event.type == pygame.QUIT:
                end_game = False

    WINDOW.blit(font.render("Exiting....... ", 0, RED),
                (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 4))
    pygame.display.update()
    pygame.mixer.music.fadeout(500)
    pygame.time.wait(1000)
    pygame.quit()
