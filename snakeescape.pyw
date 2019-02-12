import pygame, sys

FPS = 10

SCREENHEIGHT = 525
SCREENWIDTH = 650
MAPHEIGHT = 20
MAPWIDTH = 26
TILESIZE = 25
GRIDTHICKNESS = 1

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
DRED = (125,0,0)
GREEN = (0,255,0)
DGREEN = (0,125,0)
DPURPLE = (125,0,125)
PURPLE = (255,0,255)

class Game:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        icon = pygame.Surface((1,1))
        icon.set_alpha(0)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Snake Escape")

        self.runGame()

    def gameOver(l):
        if l == 1:
            for i in range(len(p1.snake)):
                x, y = p1.snake[i]
                if i == len(p1.snake) - 1:
                    Board.tilemap[y][x] = 5
                else:
                    Board.tilemap[y][x] = 6
        if l == 2:
            for i in range(len(p2.snake)):
                x, y = p2.snake[i]
                if i == len(p2.snake) - 1:
                    Board.tilemap[y][x] = 5
                else:
                    Board.tilemap[y][x] = 6
        
        Board.printMap()
        Board.printGrid()
        pygame.display.update()
        
        pygame.time.delay(3000)
        Game.restart()

    def restart():
        p1.direction = 1
        p2.direction = 1

        Board.tilemap = [[0 for x in range(MAPWIDTH)]for y in range(MAPHEIGHT)]

        for i in range(len(p1.snake)):
            p1.snake.pop()
        for i in range(len(p2.snake)):
            p2.snake.pop()

        Snake.placePlayers()
        Game.runGame()
        
    def runGame():
        pygame.event.clear()
        ADDLENGTH = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDLENGTH ,3000)
        screen = pygame.display.get_surface()
        clock = pygame.time.Clock()
        Snake.placePlayers()
        p1.addLength()
        p2.addLength()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == ADDLENGTH:
                    p1.addLength()
                    p2.addLength()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        p2.changeDir(1)
                    if event.key == pygame.K_DOWN:
                        p2.changeDir(3)
                    if event.key == pygame.K_LEFT:
                        p2.changeDir(4)
                    if event.key == pygame.K_RIGHT:
                        p2.changeDir(2)
                    if event.key == pygame.K_w:
                        p1.changeDir(1)
                    if event.key == pygame.K_s:
                        p1.changeDir(3)
                    if event.key == pygame.K_a:
                        p1.changeDir(4)
                    if event.key == pygame.K_d:
                        p1.changeDir(2)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x > 585 and mouse_y > 500:
                        Game.restart()                    
                        
            p1.moveSnake()
            p2.moveSnake()

            if Snake.testDraw() == True:
                Game.gameOver(0)
            if p1.testCol(p2) == True:
                Game.gameOver(1)
            if p2.testCol(p1) == True:
                Game.gameOver(2)

            p1.updateTilemap(1)
            p2.updateTilemap(2)
            
            Board.printMap()
            Board.printGrid()
            pygame.display.update()
            screen.fill(WHITE)
            clock.tick(FPS)
        

class Snake:
    def __init__(self):
        self.direction = 1
        self.snake = []
        self.posx = 0
        self.posy = 0

    def placePlayers():
        p1.posx = 6
        p1.posy = 9
        p2.posx = 19
        p2.posy = 9
        
        p1.snake.append((p1.posx, p1.posy))
        p2.snake.append((p2.posx, p2.posy))

    def testDraw():
        if (p1.snake[-1] in p2.snake) and (p2.snake[-1] in p1.snake):
            return True
        if p1.snake[-1] == p2.snake[-1]:
            return True

    def testCol(self, obj):
        tail = list(self.snake)
        tail.pop(-1)
        if self.snake[-1] in tail:
            return True
        if self.snake[-1] in obj.snake:
            return True
        
    def addLength(self):
        self.snake.append((self.posx, self.posy))

    def changeDir(self, d):
        if d == 1 and self.direction != 3:
            self.direction = d
        if d == 2 and self.direction != 4:
            self.direction = d
        if d == 3 and self.direction != 1:
            self.direction = d
        if d == 4 and self.direction != 2:
            self.direction = d

    def updateTilemap(self, pn):
        for i in range(len(self.snake)):
            x, y = self.snake[i]
    
            if pn == 1:
                if i == len(self.snake) - 1:
                    Board.tilemap[y][x] = 1
                else:
                    Board.tilemap[y][x] = 2
            elif pn == 2:
                if i == len(self.snake) - 1:
                    Board.tilemap[y][x] = 3
                else:
                    Board.tilemap[y][x] = 4

    def moveSnake(self):
        if self.direction == 1:
            if self.posy > 0:
                self.posy -= 1
                self.snake.append((self.posx, self.posy))
            elif self.posy == 0:
                self.posy = MAPHEIGHT - 1
                self.snake.append((self.posx, self.posy))
        if self.direction == 2:
            if self.posx < MAPWIDTH - 1:
                self.posx += 1
                self.snake.append((self.posx, self.posy))
            elif self.posx == MAPWIDTH - 1:
                self.posx = 0 
                self.snake.append((self.posx, self.posy))
        if self.direction == 3:
            if self.posy < MAPHEIGHT - 1:
                self.posy += 1
                self.snake.append((self.posx, self.posy))
            elif self.posy == MAPHEIGHT - 1:
                self.posy = 0
                self.snake.append((self.posx, self.posy))
        if self.direction == 4:
            if self.posx > 0:
                self.posx -= 1
                self.snake.append((self.posx, self.posy))
            elif self.posx == 0:
                self.posx = MAPWIDTH - 1 
                self.snake.append((self.posx, self.posy))

        x, y = self.snake[0]
        Board.tilemap[y][x] = 0
        self.snake.pop(0)

class Board:
    tilemap = [[0 for x in range(MAPWIDTH)]for y in range(MAPHEIGHT)]

    def printGrid():
        screen = pygame.display.get_surface()
        
        for y in range(MAPHEIGHT):
            for x in range(MAPWIDTH):
                rect = (x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, BLACK, rect, GRIDTHICKNESS)

    def printMap():
        screen = pygame.display.get_surface()

        def fColour(c):
            if c == 0: return WHITE
            if c == 1: return DRED
            if c == 2: return RED
            if c == 3: return DGREEN
            if c == 4: return GREEN
            if c == 5: return DPURPLE
            if c == 6: return PURPLE
        
        for y in range(MAPHEIGHT):
            for x in range(MAPWIDTH):
                rect = (x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, fColour(Board.tilemap[y][x]), rect)

        font = pygame.font.SysFont("comicsansms",15,True)
        textobj_restart = font.render("Restart",1,BLACK)
        textrect_restart = textobj_restart.get_rect()
        textrect_restart.topleft = (585, 500)

        screen.blit(textobj_restart, textrect_restart)    

p1 = Snake()
p2 = Snake()

b = Board()
g = Game()
