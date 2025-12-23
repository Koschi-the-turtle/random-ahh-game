import pygame
pygame.init()

class Game:

    def __init__(self):
        self.player = Player()
        self.pressed = {}

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 6
        self.player = player
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale (self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 20
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 6
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center = self.rect.center)

    def move(self):
        self.rect.x += self.velocity
        self.rotate()
        if self.rect.x>1080:
            self.player.all_projectiles.remove(self)

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 4
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (210, 210))
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 430

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))


    def move_right(self):
        self.rect.x += self.velocity
    def move_left(self):
        self.rect.x -= self.velocity
    

#generate the game's window
pygame.display.set_caption("random ahh game")
screen = pygame.display.set_mode((1080, 720))

#import visuals
background = pygame.image.load('assets/bg.jpg')
player = Player()
game = Game()

running = True

# if true loop
while running:
    screen.blit(background, (0, -250))
    screen.blit(game.player.image, game.player.rect)

    for projectile in game.player.all_projectiles:
        projectile.move()
    
    game.player.all_projectiles.draw(screen)
    
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()
    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x>0:
        game.player.move_left()

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("game closing")
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False