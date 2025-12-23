import pygame
import random
import math
pygame.init()

class Game:

    def __init__(self):
        self.playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.all_monsters = pygame.sprite.Group()
        self.pressed = {}

    def start(self):
        self.playing = True
        self.spawn_monster()
        self.spawn_monster()
        self.player.rect.x = 0

    def game_over(self):
        self.all_monsters = pygame.sprite.Group()
        self.player.health = self.player.max_health
        self.playing = False


    def update(self, screen):
        screen.blit(game.player.image, game.player.rect)
    

        self.player.update_healthbar(screen)
        for projectile in self.player.all_projectiles:
            projectile.move()

        for monster in self.all_monsters:
            monster.forward()
            monster.update_healthbar(screen)
    
        self.player.all_projectiles.draw(screen)

        self.all_monsters.draw(screen)
    
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x>0:
            self.player.move_left()

    
    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 15
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

        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.player.all_projectiles.remove(self)
            monster.damage(self.player.attack)

        if self.rect.x>1080:
            self.player.all_projectiles.remove(self)

class Monster(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 0.4
        self.image = pygame.image.load('assets/syrup.png')
        self.image = pygame.transform.scale(self.image, (270, 310))
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint (-10, 300)
        self.rect.y = 330
        self.velocity = 2 + random.randint(-1, 2)

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 1000 + random.randint (-10, 300)
            self.health = self.max_health

    def update_healthbar(self, surface):
        pygame.draw.rect(surface, (25, 25, 25), [self.rect.x + 75, self.rect.y - 10, self.max_health * 1.2, 10])
        pygame.draw.rect(surface, (200,10, 10), [self.rect.x + 75, self.rect.y - 10, self.health * 1.2, 10])

    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)

        

class Player(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 15
        self.velocity = 7
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image, (210, 210))
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = 430

    def damage(self, amount):
        if self.health - amount > amount:
            self.health -= amount
        else:
            self.game.game_over()
    
    def update_healthbar(self, surface):
        pygame.draw.rect(surface, (25, 25, 25), [self.rect.x + 49, self.rect.y, self.max_health * 1.2, 10])
        pygame.draw.rect(surface, (70, 160, 40), [self.rect.x + 49, self.rect.y, self.health * 1.2, 10])
        

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))


    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
    
    def move_left(self):
        self.rect.x -= self.velocity
    

#generate the game's window
pygame.display.set_caption("random ahh game")
screen = pygame.display.set_mode((1080, 720))

#import visuals
background = pygame.image.load('assets/bg.jpg')
banner = pygame.image.load('assets/banner.png')
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 3.8)
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.28)
play_button_rect.y = math.ceil(screen.get_height() / 1.95)
player = Player(Game)
game = Game()

running = True

# if true loop
while running:
    screen.blit(background, (0, -250))
    if game.playing:
        game.update(screen)
    else:
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)

    
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                game.start()