import pygame
import random
import math
pygame.init()
pygame.mixer_music.load('assets/sounds/pancake-song.mp3')

clock = pygame.time.Clock()
FPS = 100

class Game:

    def __init__(self):
        self.playing = False
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.comet_event = CometEvent(self)
        self.all_monsters = pygame.sprite.Group()
        self.all_monsters2 = pygame.sprite.Group()
        self.all_comets = pygame.sprite.Group()
        self.score = 0
        self.sound_manager = SoundManager()
        self.pressed = {}

    def start(self):
        self.playing = True
        self.spawn_monster()
        self.spawn_monster()
        self.spawn_monster2()
        self.player.rect.x = 0
        pygame.mixer.music.play(-1)

    def game_over(self):
        self.comet_event.all_comets = pygame.sprite.Group()
        self.all_monsters = pygame.sprite.Group()
        self.all_monsters2 = pygame.sprite.Group()
        self.comet_event.all_comets.remove()
        self.player.health = self.player.max_health
        self.comet_event.reset_percent()
        self.playing = False
        self.font = pygame.font.Font('assets/font/custom_font.ttf', 120)
        self.score = 0
        self.sound_manager.play('game_over')
        pygame.mixer.music.stop()


    def update(self, screen):
        font = pygame.font.Font('assets/font/custom_font.ttf', 120)
        score_text = font.render(f"{self.score}", 1, (255, 255, 255))
        screen.blit(score_text, (screen.get_width() / 2, 20))

        screen.blit(game.player.image, game.player.rect)
    
        self.player.update_healthbar(screen)

        self.comet_event.update_bar(screen)

        for projectile in self.player.all_projectiles:
            projectile.move()

        for monster in self.all_monsters:
            monster.forward()
            monster.update_healthbar(screen)

        for monster2 in self.all_monsters2:
            monster2.forward()
            monster2.update_healthbar(screen)

        for comet in self.comet_event.all_comets:
            comet.fall()
    
        self.player.all_projectiles.draw(screen)

        self.all_monsters.draw(screen)

        self.all_monsters2.draw(screen)

        self.comet_event.all_comets.draw(screen)
    
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x>0:
            self.player.move_left()

    
    def spawn_monster(self):
        monster = Monster(self)
        self.all_monsters.add(monster)

    def spawn_monster2(self):
        monster2 = Monster2(self)
        self.all_monsters2.add(monster2)

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

        for monster2 in self.player.game.check_collision(self, self.player.game.all_monsters2):
            self.player.all_projectiles.remove(self)
            monster2.damage(self.player.attack)

        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.player.all_projectiles.remove(self)
            monster.damage(self.player.attack)

        if self.rect.x>1080:
            self.player.all_projectiles.remove(self)


class Monster2(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 50
        self.max_health = 50
        self.attack = 30
        self.image = pygame.image.load('assets/regilait.png')
        self.image = pygame.transform.scale(self.image, (270, 310))
        self.rect = self.image.get_rect()
        self.rect.x = 1000 + random.randint (-10, 800)
        self.rect.y = 350
        self.velocity = 5

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 1000 + random.randint (-10, 300)
            self.health = self.max_health
            self.game.score += 10
            self.game.sound_manager.play('point')

    def update_healthbar(self, surface):
        pygame.draw.rect(surface, (25, 25, 25), [self.rect.centerx - 30, self.rect.y - 10, self.max_health * 1.2, 10])
        pygame.draw.rect(surface, (200,10, 10), [self.rect.centerx - 30, self.rect.y - 10, self.health * 1.2, 10])

    def forward(self):
        if not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)
            self.rect.x = 1000 + random.randint (-10, 300)

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
        self.velocity = 1 + random.randint(0, 2)

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.game.sound_manager.play('point')
            self.rect.x = 1000 + random.randint (-10, 300)
            self.health = self.max_health
            self.game.score += 50

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
        self.attack = 20
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
        self.game.sound_manager.play('pew')


    def move_right(self):
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
    
    def move_left(self):
        self.rect.x -= self.velocity

class CometEvent:
    def __init__(self, game):
        self.percent = 0
        self.percent_speed = 20
        self.game = game
        self.player = self.game.player

        self.all_comets = pygame.sprite.Group()
    def add_percent(self):
            self.percent += self.percent_speed / 100
    
    def loaded(self):
        return self.percent >= 100
    
    def reset_percent(self):
        self.percent = 0

    def meteor_fall(self):
        self.all_comets.add(Comet(self))

    def attempt_fall(self):
        if self.loaded():
            self.meteor_fall()
            self.reset_percent()

    def update_bar(self, surface):
        self.add_percent()
        self.attempt_fall()
        pygame.draw.rect(surface, (2, 2, 2), [195, 0, 700, 20])
        pygame.draw.rect(surface, (160, 160, 60), [195, 0, 7 * self.percent, 20])

class Comet(pygame.sprite.Sprite):
    def __init__(self, comet_event):
        super().__init__()
        self.comet_event = comet_event
        self.game = self.comet_event.game
        self.player = self.game.player
        self.image = pygame.image.load('assets/comet.png')
        self.image = pygame.transform.scale (self.image, (200, 125))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.player.rect.centerx
        self.rect.y = - random.randint(0, 500)
        self.velocity = random.randint (1,4)
        self.comet_event = comet_event
    def remove(self):
        self.comet_event.all_comets.remove(self)
        self.comet_event.game.sound_manager.play('meteorite')
        self.comet_event.game.sound_manager.play('point')
    def fall(self):
        self.rect.y += self.velocity
        if self.rect.y>= 500:
            self.remove()
            self.game.score += 20
        
        elif self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            self.remove()
            self.comet_event.game.player.damage(30)
            self.game.score -= 200
        
class SoundManager:
    def __init__(self):
        self.sounds = {
            'click': pygame.mixer.Sound("assets/sounds/click.mp3"),
            'game_over': pygame.mixer.Sound("assets/sounds/game_over.mp3"),
            'meteorite': pygame.mixer.Sound("assets/sounds/meteorite.mp3"),
            'pew': pygame.mixer.Sound("assets/sounds/pew.mp3"),
            'point': pygame.mixer.Sound("assets/sounds/success.mp3"),
            'song' : pygame.mixer.Sound("assets/sounds/pancake-song.mp3"),
        }

    def play(self, name):
        self.sounds[name].play()


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
                game.sound_manager.play('click')
    
    clock.tick(FPS)