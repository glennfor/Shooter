from distutils.command.build import build
from grpc import alts_server_credentials
from matplotlib.pyplot import fill
from constants import *


class Tank(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        
        self.x , self.y = WINDOW_WIDTH//2 , WINDOW_HEIGHT-WINDOW_MARGIN-DASHBOARD_HEIGHT-WINDOW_PADDING
   
    def fire(self, tankBullets):
        bullet = Bullet(BULLET_TANK, UP_DIRECTION, BULLET_SPEED)
        bullet.x , bullet.y = self.x + int(self.rect.width*.7) , self.y
        tankBullets.append(bullet)

    def position(self):
        return pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)



class Alien:
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.x , self.y = WINDOW_WIDTH//2 , WINDOW_HEIGHT-WINDOW_MARGIN-DASHBOARD_HEIGHT-WINDOW_PADDING
    
    def fire(self, alienBullets):
        bullet = Bullet(BULLET, DOWN_DIRECTION, BULLET_SPEED)
        bullet.x , bullet.y = self.x + int(self.rect.width*.5) ,self.y + int(self.rect.height*.9)
        alienBullets.append(bullet)
    
    def position(self):
        return pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)



#differences: image, direction
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, direction, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()

        self.x , self.y = None, None
        self.dir = direction
        self.speed = speed
    
    def move(self):
        if self.y > WINDOW_HEIGHT - WINDOW_PADDING -WINDOW_MARGIN:
            return
        self.y += self.dir*self.speed

    def position(self):
        return pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
    
alienBullets = []

alienShips = []
tankBullets = []

def createAliens() -> None:
    alienShips.clear()
    for i in range(6):
        alien = Alien(ALIEN_SHIP)
        alien.x = WINDOW_MARGIN + WINDOW_PADDING + (i%6)*alien.rect.width
        alien.y = WINDOW_MARGIN+DASHBOARD_HEIGHT+WINDOW_PADDING + i//6*alien.rect.height
        alienShips.append(alien)


def runGame():
    createAliens()
    tank = Tank(TANK) 


    running = True
    clock = pygame.time.Clock()
    WINDOW.fill(BLACK)  
    
    dls = []
    before = 0
    while running:
        clock.tick(FPS)
        WINDOW.blit(BACKGROUND, (0, 0, WINDOW_WIDTH,WINDOW_HEIGHT))

        pygame.draw.rect(WINDOW, getColor(GAME_BOX_BORDER_COLOR),
            (WINDOW_MARGIN, WINDOW_PADDING, WINDOW_WIDTH-2*WINDOW_MARGIN, DASHBOARD_HEIGHT),
            10,1
        )

        #draw game metrics here
        #score = pygame.font.Font()

        pygame.draw.rect(WINDOW, getColor(GAME_BOX_BORDER_COLOR),
         (0+WINDOW_MARGIN, 0+WINDOW_MARGIN+DASHBOARD_HEIGHT, WINDOW_WIDTH-2*WINDOW_MARGIN, WINDOW_HEIGHT-2*WINDOW_MARGIN-DASHBOARD_HEIGHT),
         5)

        WINDOW.blit(tank.image, (tank.x, tank.y))

        for alien in alienShips:
            WINDOW.blit(alien.image, (alien.x, alien.y))
        
        bulletsOutOfScreen = []
        for bullet in tankBullets+alienBullets:
            WINDOW.blit(bullet.image, (bullet.x, bullet.y))
            bullet.move()
            if (bullet.dir==UP_DIRECTION and  bullet.y <  WINDOW_MARGIN + DASHBOARD_HEIGHT + WINDOW_PADDING) or\
                (bullet.dir==DOWN_DIRECTION and  bullet.y > WINDOW_HEIGHT - WINDOW_MARGIN - WINDOW_PADDING):
                bulletsOutOfScreen.append(bullet)

        for bullet in bulletsOutOfScreen:
            if bullet in tankBullets:
                tankBullets.remove(bullet)
            if bullet in alienBullets:
                alienBullets.remove(bullet)



        for bullet in tankBullets:
            for alien in alienShips:
                if pygame.Rect.colliderect(bullet.position(), alien.position()) \
                    and (alien not in dls):

                    print("🎯")
                    EXPLODE.play()
                    tankBullets.remove(bullet)
                    alien.image = EXPLOSION
                    dls.append((alien, time.time()))
                    break
        
        l = len(dls)
        cp = dls[:]

        for alien in cp:
            if time.time()-alien[1] > IMPRESSION_TIME:
                try: 
                    alienShips.remove(alien[0])
                except ValueError:
                    pass
                else:
                    dls.remove(alien)
        
        del cp

        for bullet in alienBullets:
            if pygame.Rect.colliderect(bullet.position(), tank.position()):
                tank.image = EXPLOSION

        if len(alienShips) and time.time() - before > 10*IMPRESSION_TIME:
            ship = random.choice(alienShips)
            ship.fire(alienBullets)
            SHOOT_2.play()
            before = time.time()

        if len(alienShips) < 4:
            createAliens() 


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tank.fire(tankBullets)
                    SHOOT.play()
        
        keysPressed = pygame.key.get_pressed()

        if keysPressed[pygame.K_RIGHT]:
            if (tank.x < WINDOW_WIDTH - WINDOW_MARGIN - WINDOW_PADDING - tank.rect.width):
                tank.x += SPEED
        if keysPressed[pygame.K_LEFT]:
                    if(tank.x > WINDOW_MARGIN + WINDOW_PADDING):
                        tank.x -= SPEED

        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
    