import pygame
from pygame.constants import KEYDOWN, K_ESCAPE, K_RETURN, QUIT, VIDEORESIZE
from utils.constants import MENU_BG_COLOR, LEVEL_BG_COLOR, TEXT_COLOR, CREDITS_PAGE, DATA_PATH
from utils.story import STORY

MEDIUM_BTN_SIZE = [300, 75]
SMALL_BTN_SIZE = [200, 50]

class Menu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.screenSize = game.screenSize

        self.menuInitialized = False
        self.creditsInitialized = False
        self.selectLevelInitialized = False

    def InitMainMenu(self):
        self.menuInitialized = True
        buttonBasePos = [self.screenSize[0] / 2, (self.screenSize[1] / 2 - 75) + (self.screenSize[0] / 16)]

        self.menuButtons = {
            "select": Button(buttonBasePos[0] + 20, buttonBasePos[1], MEDIUM_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Select Level"),
            "newGame": Button(buttonBasePos[0] - 150, buttonBasePos[1] + 120, MEDIUM_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "New Game"),
            "controls": Button(5, self.screenSize[1] - 55, SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Controls"),
            "stats": Button(213, self.screenSize[1] - 55, SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Stats"),
            "exit": Button(self.screenSize[0] - 205, self.screenSize[1] - 55, SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Exit")
        }

        if (self.game.levelController.savedProgress): # If a save was found
            self.menuButtons["continue"] = Button(buttonBasePos[0] - 320, buttonBasePos[1], MEDIUM_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Continue")
        else:
            self.menuButtons["continueDisabled"] = Button(buttonBasePos[0] - 320, buttonBasePos[1], MEDIUM_BTN_SIZE, MENU_BG_COLOR, LEVEL_BG_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Continue")
        
    def InitCredits(self):
        self.creditsInitialized = True
        self.menuScrollY = self.screenSize[1] / 7 + self.screenSize[1]
        self.creditsFont = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", int(self.screenSize[0] / 45))
        self.creditsFontLarge = pygame.font.Font(DATA_PATH + "/fonts/FreeSansBold.ttf", int(self.screenSize[0] / 35))
        self.creditsSpace = self.screenSize[1] / 6

    def InitSelectLevel(self):
        self.selectLevelInitialized = True
        self.selectLevelButtons = []

        for i in range(CREDITS_PAGE - 1):
            btnPos = [(self.screenSize[0] / 2 - 300) + (i % 3 * 300) - (SMALL_BTN_SIZE[0] / 2), int(i / 3) * 100 + 100]

            if (i <= self.game.levelController.savedProgress[0]):
                self.selectLevelButtons.append(Button(btnPos[0], btnPos[1], SMALL_BTN_SIZE, LEVEL_BG_COLOR, TEXT_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Level " + str(i + 1)))
            else:
                self.selectLevelButtons.append(Button(btnPos[0], btnPos[1], SMALL_BTN_SIZE, MENU_BG_COLOR, LEVEL_BG_COLOR, MENU_BG_COLOR, self.game.fontMedium, "Level " + str(i + 1)))

    def CheckInputs(self):
        for event in pygame.event.get():
            if (event.type == QUIT):
                self.game.running = False

            elif (event.type == VIDEORESIZE): # Can only resize in menus (between levels)
                self.game.ResizeWindow(event.w, event.h)

            elif (self.game.menuPage == -1): # Main menu
                if (not self.menuInitialized):
                    self.InitMainMenu()

                mousePos = pygame.mouse.get_pos()
                mouseLeftClick = pygame.mouse.get_pressed()[0]

                for key in list(self.menuButtons):
                    if (self.menuButtons[key].IsMouseOver(mousePos) and mouseLeftClick):
                        if (key == "continue"):
                            self.game.currentLevel = self.game.levelController.savedProgress[0]
                            self.game.menuPage = self.game.levelController.savedProgress[1]
                        elif (key == "select"):
                            self.game.menuPage = -5
                        elif (key == "newGame"):
                            self.game.currentLevel = 0
                            self.game.menuPage = 0
                            self.game.levelController.savedProgress = None
                        elif (key == "controls"):
                            self.game.menuPage = -3
                        elif (key == "stats"):
                            self.game.menuPage = -4
                        elif (key == "exit"):
                            self.game.running = False

            elif (self.game.menuPage == -5 and event.type != KEYDOWN): # Select level
                if (not self.selectLevelInitialized):
                    self.InitSelectLevel()

                mousePos = pygame.mouse.get_pos()
                mouseLeftClick = pygame.mouse.get_pressed()[0]

                for i in range(len(self.selectLevelButtons)):
                    if (self.selectLevelButtons[i].IsMouseOver(mousePos) and mouseLeftClick and i <= self.game.levelController.savedProgress[0]):
                        self.game.currentLevel = i
                        self.game.menuPage = i
                        break

            elif (event.type == KEYDOWN):
                if (self.game.menuPage < -1): # Press any key on title screen, in controls, in select level or in stats to go to the main menu
                    self.game.menuPage = -1
                elif (self.game.menuPage == CREDITS_PAGE): # Press any key on credits to go to title screen
                    self.menuScrollY = self.screenSize[1] / 7 + self.screenSize[1] # Reset scroll
                    self.game.menuPage = -2

                elif (event.key == K_RETURN):
                    if (self.game.menuPage != self.game.currentLevel or self.game.menuPage == CREDITS_PAGE - 1):
                        self.game.menuPage += 1
                    else: # Start of a level
                        self.game.InitLevel()

                elif (event.key == K_ESCAPE):
                    self.game.menuPage = -1

    def Draw(self):
        self.screen.fill(MENU_BG_COLOR)

        if (self.game.menuPage == -5): # Select Level
            if (not self.selectLevelInitialized):
                self.InitSelectLevel()

            text = self.game.fontLarge.render("Select Level", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            mousePos = pygame.mouse.get_pos()

            for button in self.selectLevelButtons:
                button.Draw(self.screen, button.IsMouseOver(mousePos))

            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -4): # Stats
            text = self.game.fontLarge.render("Stats", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Kills: " + str(self.game.levelController.savedKills), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 - 125, 125))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Deaths: " + str(self.game.levelController.savedDeaths), True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2 + 125, 125))
            self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Best Times", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 225))
            self.screen.blit(text, textRect)

            for key in list(self.game.levelController.savedTimes):
                level = int(key)
                text = self.game.fontMedium.render("Level " + str(level + 1) + ": " + str(self.game.levelController.savedTimes[key] / 1000) + "s", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2 - 300 + (level % 3 * 300), int(level / 3) * 50 + 275))
                self.screen.blit(text, textRect)

            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -3): # Controls
            text = self.game.fontLarge.render("Controls", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, 40))
            self.screen.blit(text, textRect)

            controls = ["W A S D  -  Move", "", "Mouse  -  Aim", "", "Left click  -  Shoot", "", "Scrollwheel  -  Change weapons", "", "", "R  -  Restart level", "", "ESC  -  Go to main menu"]
            self.DrawParagraph(controls)
            text = self.game.fontMedium.render("Press any key to go back", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -2): # Title screen
            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 2))
            self.screen.blit(text, textRect)

        elif (self.game.menuPage == -1): # Main menu
            if (not self.menuInitialized):
                self.InitMainMenu()

            text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] / 3))
            self.screen.blit(text, textRect)

            mousePos = pygame.mouse.get_pos()

            for button in self.menuButtons.values():
                button.Draw(self.screen, button.IsMouseOver(mousePos))

        elif (self.game.menuPage >= CREDITS_PAGE):
            if (not self.creditsInitialized):
                self.InitCredits()

            if (13 * self.creditsSpace + self.menuScrollY > 0):
                text = self.game.fontTitle.render("Transgenesis", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, self.menuScrollY))
                self.screen.blit(text, textRect)

                text = self.creditsFont.render("Psycho - Developer, Software Architect", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 4 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFont.render("Seraphii - Developer, Assets Artist", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 5 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFont.render("Hypstersaurus - Developer, Texture Artist", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 6 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFont.render("Parazyte - Composer, Level Designer, Writer", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 7 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)
                text = self.creditsFont.render("Nemesis - Enemy Designer, Writer", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 8 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)

                text = self.creditsFontLarge.render("Thank you for playing!", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, 12 * self.creditsSpace + self.menuScrollY))
                self.screen.blit(text, textRect)

                self.menuScrollY -= 1
            else:
                text = self.game.fontMedium.render("Press any key", True, TEXT_COLOR)
                textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
                self.screen.blit(text, textRect)

        else: # Levels
            message = "Press Enter to start level " + str(self.game.currentLevel + 1) if (self.game.menuPage != CREDITS_PAGE - 1) else "Press Enter to continue"
            text = self.game.fontMedium.render(message, True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, self.screenSize[1] - 30))
            self.screen.blit(text, textRect)
            self.DrawParagraph(STORY[self.game.menuPage])

    def DrawParagraph(self, lines):
        for i in range(len(lines)):
            text = self.game.fontMedium.render(lines[i], True, TEXT_COLOR)
            textRect = text.get_rect(center = (self.screenSize[0] / 2, (self.screenSize[1] / 4) + (i * 30)))
            self.screen.blit(text, textRect)

class Button:
    def __init__(self, x, y, size, bgColor, textColor, hoverColor, font, text):
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.bgColor = bgColor
        self.textColor = textColor
        self.hoverColor = hoverColor
        self.font = font
        self.text = text

    def Draw(self, screen, mouseOver):
        pygame.draw.rect(screen, self.textColor, (self.x - 2 , self.y - 2 ,self.width + 4 ,self.height + 4), 0)

        if (mouseOver):
            pygame.draw.rect(screen, self.hoverColor, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(screen, self.bgColor, (self.x, self.y, self.width, self.height), 0)
        
        text = self.font.render(self.text, 1, self.textColor)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def IsMouseOver(self, mousePos):
        if mousePos[0] > self.x and mousePos[0] < self.x + self.width:
            if mousePos[1] > self.y and mousePos[1] < self.y + self.height:
                return True

        return False