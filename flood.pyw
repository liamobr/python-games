import pygame, sys
from random import randint
#Map is 20 tiles by 12 tiles
SCREENHEIGHT = 325
SCREENWIDTH = 500
TILESIZE = 25

FPS = 125

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
AQUA = (0,255,255)
PURPLE = (255,0,255)

Tilemap = [[0 for x in range(20)]for y in range(12)]
mainClock = pygame.time.Clock()

class App:
    def __init__(self):
        pygame.display.init()
        pygame.font.init()
        pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
        icon = pygame.Surface((32,32))
        icon.set_alpha(0)
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Flood It!")
        
    def genGrid(self):
        for y in range(12):
            for x in range(20):
                n = randint(1,6)
                Tilemap[y][x] = n

    def drawGrid(self):
        screen = pygame.display.get_surface()
        
        for y in range(12):
            for x in range(20):
                rect = (x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
                pygame.draw.rect(screen, self.findColour(x,y), rect)

    def findColour(self, x,y):
        colour = ""
        
        if Tilemap[y][x] == 1: colour = RED
        if Tilemap[y][x] == 2: colour = GREEN
        if Tilemap[y][x] == 3: colour = BLUE
        if Tilemap[y][x] == 4: colour = YELLOW
        if Tilemap[y][x] == 5: colour = AQUA
        if Tilemap[y][x] == 6: colour = PURPLE
        
        return colour
    
    def refreshScreen(self):
        screen = pygame.display.get_surface()
        self.drawGrid()

        font = pygame.font.SysFont("comicsansms",15, True)
        textobj_moves = font.render("Moves: {}".format(moves),1,(0,0,0))
        textrect_moves = textobj_moves.get_rect()
        textrect_moves.topleft = (10, 301)

        textobj_restart = font.render("Restart",1,(0,0,0,))
        textrect_restart = textobj_restart.get_rect()
        textrect_restart.topleft = (435, 301)

        screen.blit(textobj_restart, textrect_restart)
        screen.blit(textobj_moves, textrect_moves)
        pygame.display.update()
        mainClock.tick(FPS)
        screen.fill(WHITE)

    def calcCoords(self, mouse_x, mouse_y):
        subx = mouse_x % 25
        suby = mouse_y % 25
                        
        mouse_x = mouse_x - subx
        mouse_y = mouse_y - suby

        x = mouse_x / 25
        y = mouse_y / 25

        return x,y

    def floodBoard(self, colour, ncolour,x,y):
        if colour == ncolour:
            return

        Tilemap[y][x] = ncolour
        self.refreshScreen()
            
        if x > 0 and Tilemap[y][x-1] == colour:
            self.floodBoard(colour, ncolour, x-1, y)
        if x < 19 and Tilemap[y][x+1] == colour:
            self.floodBoard(colour, ncolour, x+1, y)
        if y > 0 and Tilemap[y-1][x] == colour:
            self.floodBoard(colour, ncolour, x, y-1)
        if y < 11 and Tilemap[y+1][x] == colour:
            self.floodBoard(colour, ncolour, x, y+1)

    def runGame(self):
        global moves
        moves = 0
        self.genGrid()
        
        while True:
            for event in pygame.event.get():
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_x < 500 and mouse_y < 300:
                        moves = moves+1
                        x,y = self.calcCoords(mouse_x,mouse_y)
                        self.floodBoard(Tilemap[0][0],
                                       Tilemap[int(y)][int(x)], 0, 0)
                    if mouse_x > 435 and mouse_y > 305:
                        moves = 0
                        self.genGrid()

            self.refreshScreen()

                    
flood = App()
flood.runGame()
    
