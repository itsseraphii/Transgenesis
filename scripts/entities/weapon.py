import pygame
import math
from gameworld import TILE_SIZE
import sys

try: # Path for files when app is built by PyInstaller
    BASE_PATH = sys._MEIPASS
except:
    BASE_PATH = "."

SWING_SOUND_FILE = BASE_PATH + "/sounds/swing.mp3"
GUNSHOT_SOUND_FILE = BASE_PATH + "/sounds/gunshot.mp3"
BULLET_IMAGE = BASE_PATH + "/res/bullet.png"
BULLET_SPEED = 20
BULLET_SIZE = 3

MELEE_OFFSET_XY = -(TILE_SIZE / 2)
MELEE_SIZE = [TILE_SIZE * 2] * 2

class Weapon:
    def __init__(self, player, gameworld):
        self.player = player
        self.gameworld = gameworld
        self.playerSize = self.player.GetSize()
        self.screenSize = pygame.display.get_window_size()
        self.bulletImage = pygame.image.load(BULLET_IMAGE)
        self.bullets = []

        self.swingSound = pygame.mixer.Sound(SWING_SOUND_FILE)
        self.gunshotSound = pygame.mixer.Sound(GUNSHOT_SOUND_FILE)

        self.CreateWeapons()
        self.lastAttackTime = 0

    def CreateWeapons(self):
        self.weapons = {}
        # key: name   value: [isRanged, damage, weaponCooldown]
        self.weapons.update({"Crowbar": [False, 2, 750]})
        self.weapons.update({"Revolver": [True, 3, 800]})
        self.weapons.update({"Assault Rifle": [True, 1, 115]})
        self.weapons.update({"Sniper": [True, 8, 2000]})

    def Attack(self, equippedWeapon, ammo): # playerPos required for melee
        currentTime = pygame.time.get_ticks()

        if (currentTime >= self.lastAttackTime + self.weapons[equippedWeapon][2]): # Attack if cooldown has passed
            self.lastAttackTime = currentTime

            if (self.weapons[equippedWeapon][0] and ammo > 0): # Ranged weapon with ammo
                playerPos = self.player.GetPos()
                angle = -math.radians(self.player.GetAngle())

                # [posX, posY, angle, damage]
                self.bullets.append([self.playerSize[0] / 2 + playerPos[0], self.playerSize[1] + playerPos[1], angle, self.weapons[equippedWeapon][1]])

                self.gunshotSound.play()

                return True # Decrement ammo

            elif (not self.weapons[equippedWeapon][0]): # Melee Weapon
                playerPos = self.player.GetPos()
                meleeRect = pygame.Rect((playerPos[0] + MELEE_OFFSET_XY, playerPos[1] + MELEE_OFFSET_XY), MELEE_SIZE)

                self.swingSound.play()

                for key in list(self.gameworld.monsters): # Check collisions with multiple monsters
                    if (pygame.Rect(self.gameworld.monsters[key].posX, self.gameworld.monsters[key].posY, self.gameworld.monsters[key].monster_size[0], self.gameworld.monsters[key].monster_size[1]).colliderect(meleeRect)):
                        self.gameworld.monsters[key].Stun(self.weapons[equippedWeapon][1] * 200) # More stun than ranged weapons
                        self.gameworld.monsters[key].Damage(self.weapons[equippedWeapon][1])

        return False

    def ComputeNewBulletPos(self, oldX, oldY, angle):
        newX = oldX + (BULLET_SPEED * math.cos(angle))
        newY = oldY + (BULLET_SPEED * math.sin(angle))
        return [newX, newY]

    def UpdateBullets(self):
        playerPos = self.player.GetPos()

        for i in range(len(self.bullets) - 1, -1, -1): # Check bullet out of screen
            if (self.bullets[i][0] > self.screenSize[0] / 2 + playerPos[0] or self.bullets[i][0] < -self.screenSize[0] / 2 + playerPos[0] or self.bullets[i][1] > self.screenSize[1] / 2 + playerPos[1] or self.bullets[i][1] < -self.screenSize[1] + playerPos[1]):
                self.bullets.pop(i)
            else:
                newPos = self.ComputeNewBulletPos(self.bullets[i][0], self.bullets[i][1], self.bullets[i][2])
                bulletRect = pygame.Rect(newPos[0], newPos[1], BULLET_SIZE, BULLET_SIZE)
                hasHit = False

                for monster in self.gameworld.monsters.values(): # Check collisions with monsters
                    if (pygame.Rect(monster.posX, monster.posY, monster.monster_size[0], monster.monster_size[1]).colliderect(bulletRect)):
                        monster.Stun(self.bullets[i][3] * 150)
                        monster.Damage(self.bullets[i][3])
                        self.bullets.pop(i) # Delete bullet
                        hasHit = True
                        break
                
                if (not hasHit): # Continue moving bullet
                    self.bullets[i][0] = newPos[0]
                    self.bullets[i][1] = newPos[1]
    
    def Draw(self, screen):
        self.UpdateBullets()

        for bullet in self.bullets:
            screen.blit(self.bulletImage, (bullet[0], bullet[1]))