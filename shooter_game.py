import random
from time import time as time_get
from pygame import*

def show_text(text):
    font.init()
    font1 = font.SysFont('Arial', 40)
    text = font1.render(text, True, (255,255,255))
    window.blit(text, (250, 250))
    return True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Lives():
    def __init__(self, lives, x, y):
        self.lives = lives
        self.x = x
        self.y = y
        self.image = transform.scale(image.load('rocket.png'), (50, 40))
    def draw(self):
        for i in range(self.lives):
            window.blit(self.image, (self.x-i*40, self.y))
lives = Lives(3, 650, 20)

class Player(GameSprite):
    def update(self):
        key_presssed = key.get_pressed()        
        if key_presssed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed            
        if key_presssed[K_d]and self.rect.x < 700 - self.rect.width:
            self.rect.x += self.speed        
        if key_presssed[K_SPACE]:
            try:
                if time_get() - self.shoot_time > .3:
                    self.shoot()
            except:
                self.shoot()
    def shoot(self):
        b2 = Bullet('bullet.png', self.rect.x + 27, self.rect.y, 7, 10, 30,0)
        bullets.add(b2)
        b2 = Bullet('bullet.png', self.rect.x + 27, self.rect.y, 7, 10, 30,1)
        bullets.add(b2)
        b2 = Bullet('bullet.png', self.rect.x + 27, self.rect.y, 7, 10, 30,2)
        bullets.add(b2)
        self.shoot_time = time_get()
               

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = random.randint(1, 635)
            missed.counter += 1
        self.reset()

class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(self.image, (size, size))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = random.randint(1, 635)
        self.reset()

class Counter:
    def __init__(self, text, x, y):
        self.counter = 0
        self.text = text
        self.position = (x, y)

    def show(self):
        font.init()
        font1 = font.SysFont('Arial', 20)
        text = font1.render(self.text + str(self.counter), True, (255,255,255))
        window.blit(text, self.position)

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w,h, direction):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (w, h))
        self.direction = direction
    def update(self):
        if self.direction == 1:
            self.rect.x -= 1
        if self.direction == 2:
            self.rect.x += 1
        self.rect.y -= self.speed
        self.reset()

missed = Counter('Список пропущенных врагов: ', 10,10)
killed = Counter('Список убитых врагов: ', 10,35)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Asteroid('asteroid.png', random.randint(1, 635), 0, random.randint(1, 3), random.randint(30, 50)))

for i in range(10):
    monsters.add(Enemy('ufo.png', random.randint(1, 635), 0, random.randint(1, 3)))
player = Player('rocket.png', 300,435, 5)
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(
    image.load("galaxy.jpg"),
        (700, 500)
)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
game = True
finish = False
clock = time.Clock()
sounds = ('fire.ogg', 'space.ogg')
while game:
    clock.tick(50)
    if finish == False:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        missed.show()
        killed.show()        
        monsters.update()
        asteroids.update()
        bullets.update()
        lives.draw()
        sprites_list = sprite.groupcollide(monsters, bullets, False, True)
        for b in sprites_list:
            b.rect.y = 0
            b.rect.x = random.randint(1, 635)
            file = random.choice(sounds)
            s = mixer.Sound(file)
            s.play()
            killed.counter += 1
        if killed.counter >= 26:
            show_text('you win!!!')
            finish = True
        if missed.counter >= 3 :
            lives.lives -= 1
            missed.counter = 0

        if lives.lives <= 0:
            show_text('you lose!!!!!')
            finish = True
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            for s in sprite.spritecollide(player, monsters, False) + sprite.spritecollide(player,asteroids, False):
                s.rect.y = 0
                s.rect.x = random.randint(1, 635)
                lives.lives -= 1
        display.update()    

    for e in event.get():
        if e.type == QUIT:
            game = False

    