import pygame
import math
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png"))
enemy_img = pygame.image.load(path.join(img_dir, "enemyShip1_orange.png"))

WIDTH = 1200
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (102, 51, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
calibri = pygame.font.SysFont('Calibri', 24, True, False)
clock = pygame.time.Clock()


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt(((self.x - other.x) ** 2) + (self.y - other.y) ** 2)



class Powerup():
    def __init__(self, x, y):
        self.width = 30
        self.heigth = 30
        self.pos = Position(x, y)
        self.type = self.RollType()
        self.fallspeed = 3

    def RollType(self):
        x = random.randint(0, 100)

        if x > 90:
            type = "lazer"
        else:
            type = "none"
        return type

    def update(self):
        self.pos.y += self.fallspeed
        if self.pos.y > HEIGHT or self.type == "none":
            powerups.remove(self)

    def draw(self):
        if self.type == "lazer":
            pygame.draw.rect(screen, BLUE, [self.pos.x - self.width/2, self.pos.y, self.width , self.heigth])

class Lazer():
    def __init__(self, player):
        self.player = player
        self.width = 20
        self.endtime = 5000
        self.now = 0
        self.starttime = pygame.time.get_ticks()
        self.pos = Position(player.pos.x, player.pos.y)

    def update(self):
        self.player.powerup = "lazer"
        self.now = pygame.time.get_ticks()
        print(self.now - self.starttime)
        if self.now -self.starttime > self.endtime:
            self.remove()
        self.pos = player.pos

    def remove(self):
        if self.now - self.starttime > self.endtime:
            player.bullets.remove(self)

            player.powerupactivated = False
            player.powerup = "none"

    def draw(self):
        lazerduration = self.endtime - (self.now - self.starttime)
        print(lazerduration)
        pygame.draw.rect(screen, (BLUE), [self.pos.x - self.width / 2, 0, self.width, self.player.pos.y])
        if player.player == 2:
            pygame.draw.rect(screen, (BLUE), [0, HEIGHT - 20, lazerduration // self.width, 20])
        else:
            pygame.draw.rect(screen, (BLUE), [0, HEIGHT - 40, lazerduration // self.width, 20])



class Bullet():
    def __init__(self, player, direction):
        self.player = player
        self.direction = direction
        self.width = 8
        self.height = 20
        if not self.direction == "up" and not self.direction == "down":
            self.width = 20
            self.height = 8
        self.speed = 8
        self.pos = Position(player.pos.x, player.pos.y)
    def update(self):
        if self.direction == "up":
            self.pos.y -= self.speed
        if self.direction == "down":
            self.pos.y += self.speed
        if self.direction == "left":
            self.pos.x -= self.speed
        if self.direction == "right":
            self.pos.x += self.speed
        if self.pos.y < -10 or self.pos.y > HEIGHT:
            self.player.bullets.remove(self)

    def remove(self):
        if self in player.bullets:
            player.bullets.remove(self)
    def draw(self):
        pygame.draw.rect(screen, (RED), [self.pos.x - self.width/2, self.pos.y, self.width, self.height])

class Movement():
    def __init__(self):
        if len(players) == 0:
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.up = pygame.K_UP
            self.down = pygame.K_DOWN
            self.shoot = pygame.K_KP0
        if len(players) == 1:
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.up = pygame.K_w
            self.down = pygame.K_s
            self.shoot = pygame.K_SPACE


class SpaceShip():
    def __init__(self):
        self.width = 50
        self.heigth = 38
        self.radius = 25
        self.speed = 8
        self.health = 100
        self.pos = Position(0, 0)
        self.bullets = []
        self.image = pygame.transform.scale(player_img, (self.width, self.heigth))


class Player(SpaceShip):
    def __init__(self):
        super().__init__()
        self.player = len(players)+1
        self.pos = Position(WIDTH // 2, HEIGHT - 100)
        self.score = 0
        self.shoot_delay = 250
        self.last_shot = 0
        self.movement = Movement()
        self.powerup = "none"
        self.holdingpowerup = None
        self.powerupactivated = False

    def shoot(self):
        if self.powerup == "none":
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.bullets.append(Bullet(self, "up"))
        elif self.powerup == "lazer" and self.powerupactivated == False:
            self.powerupactivated = True
            self.holdingpowerup = Lazer(self)
            self.bullets.append(self.holdingpowerup)

    def update(self):
        newpos = Position(self.pos.x, self.pos.y)
        keystate = pygame.key.get_pressed()
        if keystate[self.movement.left]:
            newpos.x -= self.speed
        if keystate[self.movement.right]:
            newpos.x += self.speed
        if keystate[self.movement.up]:
            newpos.y -= self.speed
        if keystate[self.movement.down]:
            newpos.y += self.speed

        self.pos = newpos
        if self.pos.x > WIDTH - self.width/2:
            self.pos.x = WIDTH - self.width/2
        if self.pos.x < 0 + self.width/2:
            self.pos.x = 0 +self.width /2
        if self.pos.y > HEIGHT - self.heigth/2:
            self.pos.y = HEIGHT - self.heigth/2
        if self.pos.y < 0 + self.heigth /2:
            self.pos.y = 0 + self.heigth/2

        if keystate[self.movement.shoot]:
            self.shoot()
        for bullet in self.bullets:
            bullet.update()
        for powerup in powerups:
            if powerup.pos.distance(self.pos) - powerup.width/2 < self.radius:
                if powerup.type == self.powerup:
                    self.holdingpowerup.starttime = self.holdingpowerup.now

                self.powerup = powerup.type
                powerups.remove(powerup)


    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

        screen.blit(self.image, (self.pos.x - self.width/2, self.pos.y - self.heigth/2))


class Invader(SpaceShip):
    def __init__(self):
        super().__init__()
        self.direction = "right"
        self.pos = Position(0 -self.width, 0 + self.heigth /2)
        self.image = pygame.transform.scale(enemy_img, (self.width, self.heigth))
        self.shoot_delay = 1000
        self.last_shot = 0

    def update(self):
        self.hit()
        self.move()
        self.shoot()
        for bullet in self.bullets:
            bullet.update()
        if self.health == 0 and self in enemies:
            enemies.remove(self)

    def move(self):
        if self.direction == "right":
            self.pos.x += self.speed
            if self.pos.x > WIDTH:
                self.direction = "left"
        if self.direction == "left":
            self.pos.x -= self.speed
            if self.pos.x < 0:
                self.direction = "right"

    def hit(self):
        for player in players:
            for bullet in player.bullets:
                if player.powerup == "lazer":
                    destroyrequirement = bullet.pos.x + bullet.width / 2 > self.pos.x - self.radius and bullet.pos.x - bullet.width / 2 < self.pos.x + self.radius
                else:
                    destroyrequirement = bullet.pos.distance(self.pos) - bullet.width/2 < self.radius
                if destroyrequirement and bullet in player.bullets:
                    self.health -= 10
                    bullet.remove()

            for bullet in self.bullets:
                if bullet.pos.distance(player.pos) - bullet.width/2 < player.radius:
                    player.health -= 10
                    self.bullets.remove(bullet)

    def shoot(self):

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.bullets.append(Bullet(self, "down"))

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
        screen.blit(self.image, (self.pos.x - self.width / 2, self.pos.y - self.heigth / 2))


class Invader2(Invader):
    def __init__(self):
        super().__init__()
        self.direction = "down"
        self.pos = Position(0 + self.radius, 0)
        self.speed = 4

    def move(self):
        if self.direction == "down":
            self.pos.y += self.speed
        if self.pos.y > HEIGHT:
            self.pos.y = 0 -self.radius
            self.pos.x = self.pos.x + 1 + (self.radius*2)
        if self.pos.x > WIDTH:
            self.pos.x = 0 + self.radius

    def shoot(self):
        for player in players:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay and self.pos.y - player.pos.y > player.radius - player.heigth:
                print(self.pos.y  == player.pos.y)
                self.last_shot = now
                self.bullets.append(Bullet(self, "right"))
                self.bullets.append(Bullet(self, "left"))


class Asteroid():
    def __init__(self):
        self.radius = random.randint(10, 50)
        self.health = 0
        self.pos = Position(random.randint(0, WIDTH - self.radius), - self.radius)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.player_hit = False

    def update(self):
        self.pos.x += self.speedx
        self.pos.y += self.speedy
        for player in players:
            if (self.pos.x > WIDTH + self.radius or self.pos.x < 0 - self.radius) or (self.pos.y > HEIGHT + self.radius) or self.is_destroyed(player):
                self.pos = Position(random.randint(0, WIDTH - self.radius), random.randint(-100, -40))
                self.speedy = random.randrange(1, 8)
                self.speedx = random.randrange(-3, 3)
                self.player_hit = False

            elif player.pos.distance(self.pos) -player.radius < self.radius and not self.player_hit:
                player.health -= self.radius
                self.player_hit = True

    def is_destroyed(self, player):
        for bullet in player.bullets:
            if player.powerup == "lazer":
                destroyrequirement = bullet.pos.x + bullet.width / 2 > self.pos.x - self.radius and bullet.pos.x - bullet.width / 2 < self.pos.x + self.radius
            else:
                destroyrequirement = bullet.pos.distance(self.pos) - bullet.width/2 < self.radius

            if destroyrequirement:
                powerup = Powerup(self.pos.x, self.pos.y)
                powerups.append(powerup)
                player.score += 50 - self.radius
                bullet.remove()
                return True


    def draw(self):

        pygame.draw.circle(screen, (BROWN), (self.pos.x, self.pos.y), self.radius)


playeramount =2
players = []
enemies = []
powerups = []
for i in range(8):
    a = Asteroid()
    enemies.append(a)
for i in range(playeramount):
    players.append(Player())
invader2 = Invader2()
invader = Invader()
enemies.append(invader)
enemies.append(invader2)
amountinvaders = 1
spawninvader = 0
last_spawn = 0
spawn_delay = 1000

# Game loop

running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update


    for powerup in powerups:
        powerup.update()

    for player in players:
        player.update()
        if player.health < 0:
            players.remove(player)

    invaderhealth = 0
    for enemy in enemies:
        invaderhealth += enemy.health
        enemy.update()

    if invaderhealth == 0:
        player.score += 1000 * amountinvaders
        amountinvaders += 1
        spawninvader = amountinvaders

    if spawninvader > 0:
        now = pygame.time.get_ticks()
        if now - last_spawn > spawn_delay:
            invader = Invader()
            invader2 = Invader2()
            enemies.append(invader)
            enemies.append(invader2)
            spawninvader -= 1
            last_spawn = now


    if len(players) == 0:
        screen.blit(calibri.render("You Lose, Press 'r' to restart", True, WHITE), [WIDTH //2 - 150, HEIGHT //2 -50])
        pygame.display.flip()
        if pygame.key.get_pressed()[pygame.K_r]:
            playeramount = 2
            players = []
            enemies = []
            powerups = []
            for i in range(8):
                a = Asteroid()
                enemies.append(a)
            for i in range(playeramount):
                players.append(Player())
            invader2 = Invader2()
            invader = Invader()
            amountinvaders = 1
            enemies.append(invader)
            enemies.append(invader2)
            spawninvader = 1
            last_spawn = 0
            spawn_delay = 1000




    # Draw / render
    else:
        screen.fill(BLACK)

        for enemy in enemies:

            enemy.draw()

        for powerup in powerups:
            powerup.draw()
        for player in players:
            player.draw()
        screen.blit(calibri.render("Health P1: %d " % (players[0].health), True, WHITE), [WIDTH -135, HEIGHT - 40])
        screen.blit(calibri.render("Enemies: %d " % (invaderhealth), True, WHITE), [WIDTH - 135, HEIGHT -60])
        screen.blit(calibri.render("Score P1: %d " % (players[0].score), True, WHITE), [0, HEIGHT - 40])
        if len(players) > 1:
            screen.blit(calibri.render("Score P2: %d " % (players[1].score), True, WHITE), [0, HEIGHT - 20])
            screen.blit(calibri.render("Health P2: %d " % (players[1].health), True, WHITE), [WIDTH -135, HEIGHT - 20])
        # *after* drawing everything, flip the display
        pygame.display.flip()

pygame.quit()
