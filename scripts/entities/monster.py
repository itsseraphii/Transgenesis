from enum import Enum

from pygame.rect import Rect
from spriteUtils import getFrames
import random
import math
import pygame

TURN_ANGLE = 2

class MonsterType(Enum):
    FATBOI = 105
    ZOMBIE = 110

class Monster:
    def __init__(self, id, monster_type, spawn_location, gameworld):
        self.gameworld = gameworld
        self.id = id
        self.posX = spawn_location[0]
        self.posY = spawn_location[1]
        self.lastHitTime = 0
        self.angle = 0

        if (MonsterType(monster_type) == MonsterType.FATBOI) :
            self.monster_type = MonsterType.FATBOI
            self.speed = 1
            self.image_source = "monster_n1.png"
            self.animation_speed = 150
            self.accuracy = 2
            self.target_cooldown = 1750 #ms
            self.monster_size = [64, 64]
            self.health = 9

            # Hitbox Info
            self.hitBoxOffestX = 15
            self.hitBoxOffestY = 15
            self.hitBoxWidth = 40
            self.hitBoxLength = 40
        else:
            self.monster_type = MonsterType.ZOMBIE
            self.speed = 1.5
            self.image_source = "zombie1.png"
            self.animation_speed = 84
            self.accuracy = 3 # Range of target, lower is better
            self.target_cooldown = 1250 #ms
            self.monster_size = [32, 32]
            self.health = 6

            # Hitbox Info
            self.hitBoxWidth = 20
            self.hitBoxLength = 20
            self.hitBoxOffestX = self.hitBoxWidth/2
            self.hitBoxOffestY = self.hitBoxLength/2

        self.animation = getFrames(self.image_source, self.monster_size)
        self.lastFrameTime = 0
        self.lastTargetUpdate = 0
        self.target = gameworld.player.GetPos()
        self.frame_counter = 0
        self.NextFrame()

    def Draw(self, screen):
        screen.blit(self.image, (self.posX, self.posY))
        # Hitboxes
        # pygame.draw.rect(screen, (255,0,0), Rect(self.posX + self.hitBoxOffestX, self.posY + self.hitBoxOffestY, self.hitBoxWidth, self.hitBoxLength), 2)

    def Damage(self, damage):
        self.health -= damage

        if (self.health <= 0):
            # TODO death anim (currently just deleting)
            self.gameworld.monsters.pop(self.id)

    def Stun(self, timeMS):
        self.lastHitTime = pygame.time.get_ticks() + timeMS

    def Move(self):
        currentTime = pygame.time.get_ticks()

        if currentTime > self.lastTargetUpdate + self.target_cooldown :
            self.lastTargetUpdate = currentTime
            playerLocation = self.gameworld.player.GetPos()

            # Faraway
            if abs(playerLocation[0]) - abs(self.posX) > 100 or abs(playerLocation[1]) - abs(self.posY) > 100 :
                # Draws a zone around the player, choosing a random angle to select a target
                targetAngle = math.degrees(random.uniform(0, 6.29))
                self.target[0] = playerLocation[0] + (self.accuracy * self.gameworld.tile_size) * math.sin(targetAngle)
                self.target[1] = playerLocation[1] + (self.accuracy * self.gameworld.tile_size) * math.cos(targetAngle)
            else: # straight to the player
                self.target = playerLocation

        if (self.lastHitTime < pygame.time.get_ticks()):
            if (currentTime >= self.lastFrameTime + self.animation_speed ):
                self.lastFrameTime = currentTime
                self.NextFrame()

            if self.target[0] > self.posX :
                self.posX += self.speed
                if (self.angle > 90 and self.angle <= 270): 
                    self.angle -= TURN_ANGLE
                elif (self.angle < 90 or self.angle > 270): 
                    self.angle += TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxLength
                    ))):
                    self.posX -= self.speed
            elif self.target[0] < self.posX :
                self.posX -= self.speed
                if (self.angle > 270 or self.angle <= 90): 
                    self.angle -= TURN_ANGLE

                elif (self.angle < 270 and self.angle > 90): 
                    self.angle += TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxLength
                    ))):
                    self.posX += self.speed
            
            if self.target[1] > self.posY :
                self.posY += self.speed
                if (self.angle > 180): 
                    self.angle += TURN_ANGLE
                elif (self.angle <= 180): 
                    self.angle -= TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxLength
                    ))):
                    self.posY -= self.speed
            elif self.target[1] < self.posY :
                self.posY -= self.speed
                if (self.angle < 180): 
                    self.angle += TURN_ANGLE
                elif (self.angle >= 180): 
                    self.angle -= TURN_ANGLE
                if(self.gameworld.player.CheckCollisionWithObstacles( 
                Rect(
                    self.posX + self.hitBoxOffestX, 
                    self.posY + self.hitBoxOffestY,
                    self.hitBoxWidth, self.hitBoxLength
                    ))):
                    self.posY += self.speed

    def NextFrame(self):
        self.frame_counter += 1

        if (self.frame_counter >= len(self.animation)) :
            self.frame_counter = 0

        # update l'angle s'il va plus que 360 ou moins que 0 après calculs
        if self.angle < 0: self.angle = 360 + self.angle
        else: self.angle %= 360
        self.image = pygame.transform.rotate(self.animation[self.frame_counter], int(self.angle))

