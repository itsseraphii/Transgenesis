import os
import json
from cryptography.fernet import Fernet
from utils.constants import SAVE_KEY, SAVE_PATH
from game import Game

class LevelController:
    def __init__(self, screen):
        gameState = [0, 0, -2] # [-1: exit  0: restart level  1: next level, currentLevel, menuPage]
        self.savedProgress = self.LoadData()
        game = Game()

        while (gameState[0] != -1):
            gameState = game.Init(self, screen, gameState[0] + gameState[1], gameState[0] + gameState[2])

        self.SaveData(gameState)

    def VerifyLevelTime(self, level, newTime):
        key = str(level)
        
        if (key in self.savedTimes):
            if (newTime < int(self.savedTimes[key])):
                self.savedTimes[key] = newTime
        else:
            self.savedTimes[key] = newTime

    def HasSavedProgress(self):
        return self.savedProgress is not None and self.savedProgress[1] >= 0

    def Progressed(self, gameState): # True if no progress is saved or if there has been progress
        return not self.HasSavedProgress() or gameState[1] > self.savedProgress[0] or gameState[2] > self.savedProgress[1]

    def UpdateProgress(self, gameState):
        if (self.Progressed(gameState)):
            self.savedProgress = [gameState[1], gameState[2]]

    def SaveData(self, gameState):
        self.UpdateProgress(gameState)

        saveData = {
            "level": self.savedProgress[0],
            "menu": self.savedProgress[1],
            "deaths": self.savedDeaths,
            "kills": self.savedKills,
            "roundsFired": self.savedRoundsFired,
            "roundsHit": self.savedRoundsHit,
            "pickups": self.savedPickups,
            "completions": self.savedCompletions, 
            "times": self.savedTimes
        }

        saveData = json.dumps(saveData)
        saveData = Fernet(SAVE_KEY).encrypt(saveData.encode()).decode()

        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

        with open(SAVE_PATH, "w") as file:
            file.write(saveData)

    def LoadData(self):
        self.savedKills = 0
        self.savedDeaths = 0
        self.savedRoundsFired = 0
        self.savedRoundsHit = 0
        self.savedPickups = 0
        self.savedCompletions = 0
        self.savedTimes = {}

        try:
            with open(SAVE_PATH, "r") as file:
                saveData = file.read()

            saveData = Fernet(SAVE_KEY).decrypt(saveData.encode()).decode()
            saveData = json.loads(saveData)

            self.savedKills = saveData["kills"]
            self.savedDeaths = saveData["deaths"]
            self.savedRoundsFired = saveData["roundsFired"]
            self.savedRoundsHit = saveData["roundsHit"]
            self.savedPickups = saveData["pickups"]
            self.savedCompletions = saveData["completions"]
            self.savedTimes = saveData["times"]

            return [int(saveData["level"]), int(saveData["menu"])]

        except:
            return None

    def ResetStats(self):
        self.savedKills = 0
        self.savedDeaths = 0
        self.savedRoundsFired = 0
        self.savedRoundsHit = 0
        self.savedPickups = 0
        self.savedCompletions = 0
        self.savedTimes = {}