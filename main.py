import pygame
pygame.init()

class Game:

    def __init__(self):
        self.player = Player()
        self.pressed = {}

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 4
        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 450
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
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False