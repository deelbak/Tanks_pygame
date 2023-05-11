import pygame
from random import randint
pygame.init()
WIDTH, HEIGHT = 1150, 700
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
TILE_X = 70
TILE_Y = 75

fontUI = pygame.font.Font(None, 30)


imgBrick = pygame.image.load('tank-assets/tank-assets/PNG/Environment/treeSmall.png')
imgTanks = [
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/tankBeige.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/tankBlack.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/tankBlue.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/tankGreen.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/tankRed.png')
]
imgBarrels = [
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/barrelBeige.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/barrelBlack.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/barrelBlue.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/barrelGreen.png'),
    pygame.image.load('tank-assets/tank-assets/PNG/Tanks/barrelRed.png')
] 

imgSmokes = pygame.image.load('tank-assets/tank-assets/PNG/Smoke/smokeGrey4.png') 
DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

background = pygame.image.load('tank-assets/tank-assets/PNG/Environment/dirt.png')

class UI:
    def __init__(self):
        pass
    
    def update(self):
        pass


    def draw(self):
        j = 0
        for i in objects:
            if i.type == 'tank':
                pygame.draw.rect(window, i.color, (5 + j * 70, 5, 22, 22))


                text = fontUI.render(str(i.hp), 1, i.color)
                rect = text.get_rect(center = (5 + j * 70 +32, 5 + 11))
                window.blit(text, rect)
                j += 1


class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'
        self.hp = 5

        self.shotTimer= 0
        self.shotDelay = 60

        self.color = color
        self.rect = pygame.Rect(px, py, TILE_X, TILE_Y)
        self.direct = direct
        self.moveSpeed = 3

        self.bulletDamage = 1
        self.bulletSpeed = 5

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
        self.tankSkin = 0
        self.imageTank = pygame.transform.rotate(imgTanks[self.tankSkin], -self.direct * 90)
        self.rect = self.imageTank.get_rect(center = self.rect.center)
        self.imgBarrel = imgBarrels[0]
    def update(self):
        self.imageTank = pygame.transform.rotate(imgTanks[self.tankSkin], -self.direct * 90)
        self.rect = self.imageTank.get_rect(center = self.rect.center)
        

        oldX, oldY = self.rect.topleft

        if keys[self.keyLEFT]:
            self.rect.x -=self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x +=self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -=self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y +=self.moveSpeed
            self.direct = 2

        for i in objects:
            if i != self and self.rect.colliderect(i.rect):
                self.rect.topleft = oldX, oldY


        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
        
        if self.shotTimer > 0 : 
            self.shotTimer -= 1

    def draw(self):
        window.blit(self.imageTank, self.rect)
        # pygame.draw.rect(window, self.color, self.rect)
        # window.blit(self.imgBarrel, (self.rect.centerx + DIRECTS[self.direct][0] * -50, self.rect.centery + DIRECTS[self.direct][1] * -50))
        x = self.rect.centerx + DIRECTS[self.direct][0] * 50
        y = self.rect.centery + DIRECTS[self.direct][1] * 50
        pygame.draw.line(window, 'gray', self.rect.center, (x, y), 16)

    def damage(self, value):
        self.hp -=value
        if self.hp <=0:
            objects.remove(self)
            print(self.color, 'died')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        


    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py <0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break


    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 5)



class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1


    def update(self):
        pass


    def draw(self):
        

        window.blit(imgBrick, self.rect)


    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

bullets = []

objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE,))
Tank('red', 850, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER,))

ui = UI()


for i in range(30):
    while True:
        x = randint(0, WIDTH // TILE_X - 1)  * TILE_X
        y = randint(1, HEIGHT// TILE_Y - 1)  * TILE_Y
        rect = pygame.Rect(x, y, TILE_X, TILE_Y)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True
        if not fined:
            break
    Block(x, y, TILE_X + 7)


esc = True
while esc:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esc = False
    
    keys = pygame. key.get_pressed()

    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()
    ui.update()


    window.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()

    



    pygame.display.update()
    clock.tick(FPS)

pygame.quit()