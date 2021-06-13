import pygame
from entities.obstacle import Obstacle
from pygame import Rect
import sys
from entities.monster import Monster

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

TILE_SIZE = 32
TILE_SHEET_WIDTH = 15
TILE_SHEET_HEIGHT = 9
TILESHEET_SIZE = (TILE_SHEET_WIDTH, TILE_SHEET_HEIGHT)
TILESHEET_PIXEL_SIZE = (TILE_SHEET_WIDTH * 16, TILE_SHEET_HEIGHT * 16)
TILESHEET_PATH = BASE_PATH + "/res/tiled/CosmicLilac_Tiles_greyscale.png"

# [level1, level2, ...]
CSV_PATHS_BG = [BASE_PATH + "/res/tiled/testmap_background_layer.csv", BASE_PATH + "/res/tiled/testmap_background_layer.csv"]
CSV_PATHS_OB = [BASE_PATH + "/res/tiled/testmap_obstacle_layer.csv", BASE_PATH + "/res/tiled/testmap_obstacle_layer.csv"]
CSV_PATHS_EN = [BASE_PATH + "/res/tiled/testmap_entity_layer.csv", BASE_PATH + "/res/tiled/testmap_entity_layer.csv"]

DICT_HITBOX_SIZES = {
    10 : [32, 32, 0, 0],
    14 : [32, 32, 0, 0],
    29 : [32, 32, 0, 0],
    43 : [32, 28, 0, 0],
    44 : [32, 28, 0, 0],
    58 : [32, 28, 0, 0],
    59 : [32, 28, 0, 0],
    73 : [32, 16, 0, 7],
    74 : [16, 32, 7, 0],
    88 : [16, 16, 7, 7]
}

OBSTACLES = []

class GameWorld():
    def __init__(self, currentLevel):
        self.tile_size = TILE_SIZE
        self.screenSize = pygame.display.get_window_size()
        self.tileSheet = pygame.image.load(TILESHEET_PATH).convert_alpha()
        self.tileSheet = pygame.transform.scale(self.tileSheet, (TILESHEET_PIXEL_SIZE[0] * 2, TILESHEET_PIXEL_SIZE[1] * 2))

        self.currentLevel = currentLevel

        self.monsters = {}
        self.LoadTileCSV()
        self.obstacles = []

        self.screenNbTilesY = int(self.screenSize[1] / TILE_SIZE) + 2
        self.startOffsetY = (-self.backgroundSize[1] + self.screenSize[1]) / 2
        self.offsetY = self.startOffsetY
        self.middleY = 0

    def GetTileImage(self, posX, posY):
        rect = pygame.Rect(posX * TILE_SIZE, posY * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.tileSheet, (0, 0), rect)
        return image

    def LoadTileCSV(self):
        self.tileLayoutBG = []
        self.tileLayoutOB = []
        self.tileLayoutEN = []
        self.tileImagesBG = {}
        self.tileImagesOB = {}
        self.monsters = {}
        csvFile = open(CSV_PATHS_BG[self.currentLevel], 'r')

        for line in csvFile:
            currentRow = []
            
            for tileNum in line.split(','):
                intTileNum = int(tileNum)
                currentRow.append(intTileNum)

                # Load tile image in memory if it's not already loaded
                if (intTileNum not in self.tileImagesBG):
                    tilePosY = int(intTileNum / TILESHEET_SIZE[0])
                    tilePosX = intTileNum - (tilePosY * TILESHEET_SIZE[0])
                    self.tileImagesBG.update({intTileNum: self.GetTileImage(tilePosX, tilePosY)})

            self.tileLayoutBG.append(currentRow)

        csvFile = open(CSV_PATHS_OB[self.currentLevel], 'r')
        for line in csvFile:
            currentRow = []
            
            for tileNum in line.split(','):
                intTileNum = int(tileNum)
                currentRow.append(intTileNum)

                # Load tile image in memory if it's not already loaded
                if (intTileNum not in self.tileImagesOB):
                    tilePosY = int(intTileNum / TILESHEET_SIZE[0])
                    tilePosX = intTileNum - (tilePosY * TILESHEET_SIZE[0])
                    # Load image from assets to a dictionary
                    self.tileImagesOB.update({intTileNum: self.GetTileImage(tilePosX, tilePosY)})

            self.tileLayoutOB.append(currentRow)

        csvFile = open(CSV_PATHS_EN[self.currentLevel], 'r')
        for line in csvFile:
            currentRow = []
            
            for tileNum in line.split(','):
                currentRow.append(int(tileNum))

            self.tileLayoutEN.append(currentRow)
            
        self.backgroundSize = (len(self.tileLayoutBG[0]) * TILE_SIZE, len(self.tileLayoutBG) * TILE_SIZE)

    def SetPlayer(self, player):
        self.player = player
        self.playerSize = player.GetSize()

    def IncreaseOffsetY(self, offsetY):
        self.offsetY += offsetY
        for monster in self.monsters:
            self.monsters[monster].posY += offsetY

    def GetOffsetY(self):
        return self.offsetY

    def Draw(self, screen):
        self.middleY = (self.backgroundSize[1] - (self.offsetY - self.startOffsetY) - (self.screenSize[1] / 2)) / TILE_SIZE
        self.obstacles = []

        for y in range(int(max(0, self.middleY - (self.screenNbTilesY / 2))), int(min(len(self.tileLayoutBG), self.middleY + (self.screenNbTilesY / 2)))):
            for x in range(len(self.tileLayoutBG[y])):
                posX = (x * TILE_SIZE) + (self.screenSize[0] / 2) - (self.backgroundSize[0] / 2)
                posY = (y * TILE_SIZE) + (self.screenSize[1] / 2) - (self.backgroundSize[1] / 2) + self.offsetY
                screen.blit(self.tileImagesBG[self.tileLayoutBG[y][x]], (posX, posY))

                if(self.tileLayoutOB[y][x] != -1):
                    screen.blit(self.tileImagesOB[self.tileLayoutOB[y][x]], (posX, posY))
                    
                    # Est-ce que la key est gérée par le dictionary de tiles?
                    found = False
                    try:
                        DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[0]
                        found = True
                    except:
                        found = False

                    if found:
                        self.obstacles.append(
                            Obstacle(
                                True, False, False,
                                posX, posY, 
                                DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[0], 
                                DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[1],
                                DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[2],
                                DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[3]
                        ))
                        # Uncomment to show hitboxes : 
                        ''' 
                        pygame.draw.rect(screen, (255,0,0), Rect(
                            posX + DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[2],
                            posY + DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[3],
                            DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[0], 
                            DICT_HITBOX_SIZES.get(self.tileLayoutOB[y][x])[1]), 2
                            )
                        '''

                    else:
                        self.obstacles.append(
                            Obstacle(
                                True, False, False, posX, posY, 
                                32, 32, 0, 0
                        ))
                        # Uncomment to show hitboxes : 
                        ''' 
                        pygame.draw.rect(screen, (255,0,0), Rect(posX,posY,32, 32), 2)
                        '''

                tileId = y*self.screenNbTilesY + x

                if(self.tileLayoutEN[y][x] != -1 and not tileId in self.monsters):
                    self.monsters[tileId] = Monster(tileId, (self.tileLayoutEN[y][x]), [posX, posY], self)