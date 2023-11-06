import pygame, sys, random

def load_asset(path):
    return pygame.image.load(path)

def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    center_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)
    return rotated_image, center_rect

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Flappy Bird')
        pygame.display.set_icon(pygame.image.load('icon.ico'))
        self.window = pygame.display.set_mode((144*3, 256*3))
        self.display = pygame.Surface((144, 256), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.bgscroll = 0
        self.scrollspeed = 1

        self.player = Player(self)
        self.pipes = Pipes(100, 256, self)
        self.pipes2 = Pipes(100, 366, self)
        self.score = -1

    def run(self):
        # Main menu
##        while True:
##            stop = False
##            for i in pygame.event.get():
##                if i.type == pygame.QUIT:
##                    pygame.quit()
##                    sys.exit()
##                if i.type == pygame.KEYDOWN:
##                    if i.key == pygame.K_SPACE:
##                        stop = True
##
##            if stop:
##                break
##
##            self.display.blit(load_asset('sprites/bg.png'), ((0), 0))
##            self.window.blit(pygame.transform.scale_by(self.display, 3), (0, 0))
##            
##            font = pygame.font.Font('font.ttf', 28)
##            score = font.render('press space', True, (255, 255, 255))
##            shadow = font.render('press space', True, (0, 0, 0))
##            scorepos = score.get_rect(center=(432/2, 768/2)) #(15, 768-33)
##            self.window.blit(shadow, (scorepos[0], scorepos[1]+2))
##            self.window.blit(shadow, (scorepos[0], scorepos[1]-2))
##            self.window.blit(shadow, (scorepos[0]-2, scorepos[1]))
##            self.window.blit(shadow, (scorepos[0]+2, scorepos[1]))
##            self.window.blit(score, scorepos)
##            
##            pygame.display.update()
##            self.clock.tick(60)

        # Gameloop
        while True:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_SPACE:
                        self.player.velocity = -3.5

            # Updating
            self.player.update()

            # Rendering
            self.display.fill((86, 86, 86, 0))
            self.pipes.render(self.display)
            self.pipes2.render(self.display)
            self.display.blit(load_asset('sprites/platform.png'), ((0-self.bgscroll%154), 201))
            self.display.blit(load_asset('sprites/platform.png'), ((154-self.bgscroll%154), 201))

            # Finalizing
            self.window.blit(pygame.transform.scale_by(load_asset('sprites/bg.png'), 3), ((0), 0))
            self.window.blit(pygame.transform.scale_by(self.display, 3), (0, 0))
            self.player.render(self.window)
            
            font = pygame.font.Font('font.ttf', 28)
            score = font.render('made by atfx', True, (255, 255, 255))
            shadow = font.render('made by atfx', True, (0, 0, 0))
            scorepos = score.get_rect(center=(432/2, 768-43)) #(15, 768-33)
##            self.window.blit(shadow, (scorepos[0], scorepos[1]+2))
##            self.window.blit(shadow, (scorepos[0], scorepos[1]-2))
##            self.window.blit(shadow, (scorepos[0]-2, scorepos[1]))
##            self.window.blit(shadow, (scorepos[0]+2, scorepos[1]))
##            self.window.blit(score, scorepos)
            
            pygame.display.update()
            self.clock.tick(60)
            self.bgscroll += self.scrollspeed
            if self.bgscroll % 113 == 0:
                self.score += 1

class Player:
    def __init__(self, game):
        self.velocity = 0
        self.height = 60
        self.frames = 10
        self.dead = False
        self.game = game
        self.rect = pygame.Rect(50, self.height, 10, 10)

    def update(self):
        self.rect = pygame.Rect(50, self.height, 10, 10)
        if (self.height > 186 and not self.dead):
            self.dead = True
        if pygame.Rect.colliderect(self.rect, self.game.pipes.bottomrect) or pygame.Rect.colliderect(self.rect, self.game.pipes.toprect) or pygame.Rect.colliderect(self.rect, self.game.pipes2.bottomrect) or pygame.Rect.colliderect(self.rect, self.game.pipes2.toprect):
            self.dead = True
        if not self.dead:
            self.velocity = min(5, self.velocity+0.2)
            self.height += self.velocity

    def render(self, surf):
        img = rot_center(pygame.transform.scale_by(load_asset(f'sprites/player{int(self.frames/10)}.png'), 3), 0-self.velocity*10, 50*3, self.height*3)
        surf.blit(img[0], img[1])
        if not self.dead:
            self.frames += 1
        else:
            self.velocity = 0
            self.height = 60
            self.dead = False
            self.game.pipes.x = 256
            self.game.pipes2.x = 366
        if self.frames == 30:
            self.frames = 10

class Pipes:
    def __init__(self, y, x, game):
        self.x = x
        self.y = y
        self.game = game
        self.bottom = load_asset('sprites/pipe_bottom.png')
        self.top = load_asset('sprites/pipe_top.png')
        self.bottomrect = pygame.Rect(self.x, self.y, 26, 242)
        self.toprect = pygame.Rect(self.x, self.y-330, 26, 270)

    def render(self, surf):
        self.x -= self.game.scrollspeed
        surf.blit(self.top, (self.x, self.y-330))
        surf.blit(self.bottom, (self.x, self.y))
        self.bottomrect = pygame.Rect(self.x, self.y, 26, 242)
        self.toprect = pygame.Rect(self.x, self.y-330, 26, 270)
        if self.x < -26:
            self.x = 200
            self.y = random.randint(50, 130)

if __name__ == '__main__':
    Game().run()
