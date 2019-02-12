import pygame, sys, random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Game:
    WIDTH = 600
    HEIGHT = 400

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
        icon = pygame.Surface((1, 1))
        icon.set_alpha(0)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Pong")

        self.rungame()

    def update(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("comicsansms", 60, True)

        textobj_p1 = font.render(str(p1.score), 1, WHITE)
        textobj_p2 = font.render(str(p2.score), 1, WHITE)
        textrect_p1 = textobj_p1.get_rect()
        textrect_p2 = textobj_p2.get_rect()
        textrect_p1.topright = (Game.WIDTH / 2 - 15, 5)
        textrect_p2.topleft = (Game.WIDTH / 2 + 15, 5)
        screen.blit(textobj_p1, textrect_p1)
        screen.blit(textobj_p2, textrect_p2)

        pygame.draw.line(screen, WHITE, (Game.WIDTH / 2, 0), (Game.WIDTH / 2, Game.HEIGHT), 3)
        pygame.draw.circle(screen, WHITE, Ball.getloc(b), 10)
        pygame.draw.rect(screen, WHITE, Bat.getrect(p1))
        pygame.draw.rect(screen, WHITE, Bat.getrect(p2))

    def rungame(self):
        FPS = 100
        clock = pygame.time.Clock()
        screen = pygame.display.get_surface()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_DOWN:
                        Bat.movestate(p2, 'd', True)
                    if event.key == pygame.K_UP:
                        Bat.movestate(p2, 'u', True)
                    if event.key == pygame.K_w:
                        Bat.movestate(p1, 'u', True)
                    if event.key == pygame.K_s:
                        Bat.movestate(p1, 'd', True)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        Bat.movestate(p2, 'd', False)
                    if event.key == pygame.K_UP:
                        Bat.movestate(p2, 'u', False)
                    if event.key == pygame.K_w:
                        Bat.movestate(p1, 'u', False)
                    if event.key == pygame.K_s:
                        Bat.movestate(p1, 'd', False)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            Ball.move(b)
            Ball.walls(b)

            Bat.move(p1)
            Bat.move(p2)

            if Ball.wintest(b) == "left":
                p1.score += 1
                Ball.reset(b)
            elif Ball.wintest(b) == "right":
                p2.score += 1
                Ball.reset(b)

            self.update()

            pygame.display.update()
            screen.fill(BLACK)
            clock.tick(FPS)

class Bat:
    def __init__(self, l):
        self.score = 0
        self.w = 15
        self.h = 90
        self.moveup = False
        self.movedown = False
        if l == True:
            self.x = 10
            self.y = Game.HEIGHT / 2 - self.h / 2
        elif l == False:
            self.x = Game.WIDTH - 10 - self.w
            self.y = Game.HEIGHT / 2 - self.h / 2

    def getrect(self):
        return self.x, self.y, self.w, self.h

    def getline(self, l):
        if l == True:
            return self.x + self.w, self.y, 1, self. h
        if l == False:
            return self.x, self.y, 1, self.h

    def movestate(self, dir, s):
        if dir == 'd':
            self.movedown = s
        if dir == 'u':
            self.moveup = s

    def move(self):
        if self.y <= 0:
            self.moveup = False
        if self.y >= Game.HEIGHT - self.h:
            self.movedown = False
        if self.moveup:
            self.y -= 6
        if self.movedown:
            self.y += 6


class Ball:
    x = Game.WIDTH / 2
    y = Game.HEIGHT / 2
    xspeed = random.choice([-5, 5])
    yspeed = random.uniform(-3, 3)

    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed

    def walls(self):
        if self.y < 0 or self.y > Game.HEIGHT:
            self.yspeed *= -1

        lrect = pygame.Rect(Bat.getline(p1, True))
        rrect = pygame.Rect(Bat.getline(p2, False))

        if lrect.collidepoint(Ball.getloc(b)):
            ry = lrect.midright[1]
            d = ry - self.y
            self.yspeed = -d / 9
            self.xspeed *= -1

        if rrect.collidepoint(Ball.getloc(b)):
            ry = rrect.midright[1]
            d = ry - self.y
            self.yspeed = -d / 9
            self.xspeed *= -1

    def wintest(self):
        if self.x < -500:
            return "right"
        elif self.x > Game.WIDTH + 500:
            return "left"
        else:
            return

    def getloc(self):
        return int(self.x), int(self.y)

    def reset(self):
        self.x = Game.WIDTH / 2
        self.y = Game.HEIGHT / 2
        self.xspeed = random.choice([-5, 5])
        self.yspeed = random.uniform(-3, 3)

p1 = Bat(True)
p2 = Bat(False)
b = Ball()
g = Game()
