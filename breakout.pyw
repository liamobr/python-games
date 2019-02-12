'''
Use left and right arrow keys to move. Once blocks are all cleared map will
reset and balls will move faster. You have 5 lives every new level. You lose
a life every time a ball reaches the bottom. Use 'p' to pause or resume the
game at any point.
'''
import pygame, sys
from random import randint

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)


class Breakout:
    DHEIGHT = 600
    DWIDTH = 800
    HEIGHT = 550
    WIDTH = 800
    score = 0
    level = 1
    lives = 5

    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((Breakout.DWIDTH, Breakout.DHEIGHT))
        icon = pygame.Surface((1, 1))
        icon.set_alpha(0)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Breakout")

    def draw(self):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("comicsansms", 30, True)

        pygame.draw.rect(screen, GREY, (0, Breakout.HEIGHT, Breakout.DWIDTH, Breakout.DHEIGHT - Breakout.HEIGHT))

        for y in range(5):
            for x in range(10):
                if bricks[y][x].isvisible():
                    brect = pygame.draw.rect(screen, bricks[y][x].getcol(y), bricks[y][x].getrect())
                    bricks[y][x].col(brect, x, y)

        pygame.draw.rect(screen, BLACK, paddle.getrect())
        pygame.draw.circle(screen, BLACK, (int(ball.x), int(ball.y)), ball.r)

        textobj_score = font.render("Score: {}".format(Breakout.score), 1, BLACK)
        textrect_score = textobj_score.get_rect()
        textrect_score.topleft = (10, Breakout.HEIGHT)

        textobj_level = font.render("Level: {}".format(Breakout.level), 1, BLACK)
        textrect_level = textobj_level.get_rect()
        textrect_level.topleft = (200, Breakout.HEIGHT)

        screen.blit(textobj_level, textrect_level)
        screen.blit(textobj_score, textrect_score)

        for i in range(Breakout.lives):
            pygame.draw.circle(screen, BLACK, (Breakout.DWIDTH - 30 - 50 * i, int(Breakout.HEIGHT + ((Breakout.DHEIGHT - Breakout.HEIGHT) / 2))), 20)

    def gameover(self):
        self.pausegame("Gameover (p)")
        Breakout.lives = 5
        Breakout.score = 0
        ball.reset()

        for y in range(5):
            for x in range(10):
                bricks[y][x].setvisible()

    def runGame(self):
        FPS = 300
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
                    if event.key == pygame.K_p:
                        self.pausegame("Paused (p)")
                    if event.key == pygame.K_LEFT:
                        paddle.changedir('l')
                    if event.key == pygame.K_RIGHT:
                        paddle.changedir('r')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        paddle.moveleft = False
                    if event.key == pygame.K_RIGHT:
                        paddle.moveright = False

            paddle.move()

            ball.move()
            self.draw()

            if ball.col():
                self.pausegame("Life Lost (p)")

            if Brick.wintest():
                self.pausegame("Next Level (p)")
                Breakout.lives = 5
                Breakout.level += 1
                ball.reset()
                for y in range(5):
                    for x in range(10):
                        bricks[y][x].setvisible()

            if Breakout.lives == -1:
                screen.fill(WHITE)
                self.draw()
                self.gameover()

            pygame.display.update()
            screen.fill(WHITE)
            clock.tick(FPS)

    def pausegame(self, text):
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont("comicsansms", 60, True)

        textobj_paused = font.render(str(text), 1, BLACK)
        textrect_paused = textobj_paused.get_rect()
        textrect_paused.center = (Breakout.WIDTH / 2, Breakout.HEIGHT / 2)

        screen.blit(textobj_paused, textrect_paused)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_p:
                        running = False


class Ball:
    def __init__(self):
        self.x = Breakout.WIDTH / 2
        self.y = Breakout.HEIGHT / 3 * 2
        self.r = 6
        self.speed = 1 + (Breakout.level * 2)
        self.xspeed = randint(-self.speed, self.speed)
        self.yspeed = -self.speed

    def col(self):
        if self.x - self.r <= 0 or self.x + self.r >= Breakout.WIDTH:
            self.xspeed *= -1
        if self.y - self.r <= 0:
            self.yspeed *= -1
        if self.y + self.r >= Breakout.HEIGHT:
            Breakout.score -= 10
            Breakout.lives -= 1
            self.reset()
            return True

        prect = pygame.Rect(paddle.getrect())
        if prect.colliderect(ball.getrect()):
            if self.y > paddle.y:
                self.xspeed = min(self.xspeed, -self.xspeed)
                return False
            d = prect.midtop[0] - self.x
            d *= self.speed / (paddle.w / 2)
            self.xspeed = -d
            self.yspeed *= -1
        return False

    def reset(self):
        self.x = Breakout.WIDTH / 2
        self.y = Breakout.HEIGHT / 3 * 2
        self.speed = 1 + (Breakout.level * 2)
        self.xspeed = randint(-self.speed, self.speed)
        self.yspeed = -self.speed

    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed

    def getrect(self):
        return self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r


class Paddle:
    def __init__(self):
        self.w = 200
        self.h = 20
        self.x = Breakout.WIDTH / 2 - self.w / 2
        self.y = Breakout.HEIGHT - self.h - 15

        self.moveleft = False
        self.moveright = False

    def getrect(self):
        return self.x, self.y, self.w, self.h

    def move(self):
        if self.moveright and self.x < Breakout.WIDTH - self.w:
            self.x += 10
        if self.moveleft and self.x > 0:
            self.x -= 10

    def changedir(self, d):
        if d == 'l':
            self.moveright = False
            self.moveleft = True
        if d == 'r':
            self.moveleft = False
            self.moveright = True


class Brick:
    def __init__(self, x, y):
        self.hb = 4
        self.vb = 4
        self.w = Breakout.WIDTH / 10 - self.hb
        self.h = (Breakout.HEIGHT / 3) / 5 - self.vb
        self.x = x * (Breakout.WIDTH / 10) + (self.hb / 2)
        self.y = y * (Breakout.HEIGHT / 3 / 5) + (self.vb / 2)
        self.visible = True

    @staticmethod
    def wintest():
        for y in range(5):
            for x in range(10):
                if bricks[y][x].visible:
                    return False
        return True

    def setvisible(self):
        self.visible = True

    def getrect(self):
        return self.x, self.y, self.w, self.h

    def col(self, rect, x, y):
        if rect.colliderect(ball.getrect()):
            bricks[y][x].visible = False
            Breakout.score += 1 * Breakout.level

            brect = pygame.Rect(ball.getrect())
            if brect.top in range(rect.bottom - ball.speed - 1, rect.bottom):
                ball.yspeed = max(ball.yspeed, -ball.yspeed)
            if brect.bottom in range(rect.top, rect.top + ball.speed + 1):
                ball.yspeed = min(ball.yspeed, -ball.yspeed)
            if brect.left in range(rect.right - ball.speed - 1, rect.right):
                ball.xspeed = max(ball.xspeed, -ball.xspeed)
            if brect.right in range(rect.left, rect.left + ball.speed + 1):
                ball.xspeed = min(ball.xspeed, -ball.xspeed)

    def isvisible(self):
        if self.visible:
            return True
        else:
            return False

    def getcol(self, y):
        if y == 0: return 255, 0, 0
        if y == 1: return 255, 255, 0
        if y == 2: return 0, 255, 0
        if y == 3: return 0, 255, 255
        if y == 4: return 0, 0, 255

bricks = [[Brick(x, y) for x in range(10)] for y in range(5)]
paddle = Paddle()
ball = Ball()


if __name__ == "__main__":
    game = Breakout()
    game.runGame()
