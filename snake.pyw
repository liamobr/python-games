import pygame, sys
from random import randint

FPS = 10

SCREENHEIGHT = 425
SCREENWIDTH = 400
MAPHEIGHT = 16
MAPWIDTH = 16
TILESIZE = 25
GRIDTHICKNESS = 1

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

tilemap = [[0 for x in range(MAPWIDTH)]for y in range(MAPHEIGHT)]
mainClock = pygame.time.Clock()

class Snake:
    addLength = False
    direction = 0
    length = 1
    posx = 7
    posy = 7
    snake = []
    
    def __init__(self):
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

    def addLength(self):
        self.snake.append((self.posx, self.posy))
        self.length = self.length + 1

    def tailCol(self):
        tail = list(self.snake)
        tail.pop(-1)
        if self.snake[-1] in tail:
            return True

    def resetSnake(self):
        self.posx = 7
        self.posy = 7
        self.direction = 0
        self.length = 1
        
        for i in range(len(self.snake)):
            self.snake.pop()
        self.snake.append((self.posx, self.posy))
        

    def moveSnake(self):
        if self.direction == 1:
            if self.posy > 0:
                self.posy = self.posy - 1
                self.snake.append((self.posx, self.posy))
            elif self.posy == 0:
                self.posy = MAPHEIGHT - 1
                self.snake.append((self.posx, self.posy))
        if self.direction == 2:
            if self.posx < MAPWIDTH - 1:
                self.posx = self.posx + 1
                self.snake.append((self.posx, self.posy))
            elif self.posx == MAPWIDTH - 1:
                self.posx = 0
                self.snake.append((self.posx, self.posy))
        if self.direction == 3:
            if self.posy < MAPHEIGHT - 1:
                self.posy = self.posy + 1
                self.snake.append((self.posx, self.posy))
            elif self.posy == MAPHEIGHT - 1:
                self.posy = 0
                self.snake.append((self.posx, self.posy))
        if self.direction == 4:
            if self.posx > 0:
                self.posx = self.posx - 1
                self.snake.append((self.posx, self.posy))
            elif self.posx == 0:
                self.posx = MAPWIDTH - 1
                self.snake.append((self.posx, self.posy))

        if self.direction != 0:
            x, y = self.snake[0]
            tilemap[y][x] = 0
            self.snake.pop(0)
        
        for i in range(len(self.snake)):
            x, y = self.snake[i]
            if i == len(self.snake) - 1:
                tilemap[y][x] = 2
            else:
                tilemap[y][x] = 1

class Food:
    foodx = 0
    foody = 0
    
    def __init__(self, snake):
        self.genFood(snake)

    def genFood(self, snake):
        done = False
        while done == False:
            x = randint(0,15)
            y = randint(0,15)

            if (x,y) not in snake.snake:
                tilemap[y][x] = 3
                Food.foodx = x
                Food.foody = y
                done = True

    def foodCol(self, snake):
        if (Food.foodx, Food.foody) in snake.snake:
            return True

def initGame():
    pygame.display.init()
    pygame.font.init()
    pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
    icon = pygame.Surface((1,1))
    icon.set_alpha(0)
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Snake")

def findColour(c):
    if c == 0: return WHITE
    if c == 1: return BLACK
    if c == 2: return GREEN
    if c == 3: return RED

def gameOver():
    pygame.time.delay(5000)
    pygame.event.clear()
    gameRestart(snake, food)

def gameRestart(snake, food):
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            tilemap[y][x] = 0
    
    snake.resetSnake()
    food.genFood()

def drawBoard(snake, food):
    screen = pygame.display.get_surface()
    screen.fill(WHITE)

    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            rect = (x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, findColour(tilemap[y][x]), rect)
            
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            rect = (x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, BLACK, rect, GRIDTHICKNESS)

    font = pygame.font.SysFont("comicsansms",15, True)
    textobj_length = font.render("Length: {}".format(snake.length),1,BLACK)
    textrect_length = textobj_length.get_rect()
    textrect_length.topleft = (10, 401)

    textobj_restart = font.render("Restart",1,BLACK)
    textrect_restart = textobj_restart.get_rect()
    textrect_restart.topleft = (335, 401)

    screen.blit(textobj_length, textrect_length)
    screen.blit(textobj_restart, textrect_restart)

    pygame.display.update()
    mainClock.tick(FPS)
    
def runGame(snake, food):
    initGame()
    
    while True:
        event = pygame.event.poll()
        if len(pygame.event.get()) > 4:
            pygame.event.clear()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.changeDir(1)
            if event.key == pygame.K_DOWN:
                snake.changeDir(3)
            if event.key == pygame.K_LEFT:
                snake.changeDir(4)
            if event.key == pygame.K_RIGHT:
                snake.changeDir(2)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > 335 and mouse_y > 401:
                gameRestart(snake, food)
        
        snake.moveSnake()
                    
        if snake.tailCol() == True:
            gameOver(snake, food)
        if food.foodCol(snake) == True:
            snake.addLength()
            food.genFood(snake)
        
        drawBoard(snake, food)
           
snake = Snake()
food = Food(snake)
runGame(snake, food)


