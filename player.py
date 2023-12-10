from typing import Any, List, Optional

from pygame.rect import Rect
from pygame.surface import Surface
from config import *
import random
import math

class Bullets(pyg.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)

    def update(self, player,*args: Any, **kwargs: Any) -> None:
        for sprite in self.sprites():
            sprite.update(player)

    def draw(self, surface: Surface):
        for sprite in self.sprites():
            sprite.draw(surface)

class Bullet(pyg.sprite.Sprite):
    lifeTime = Clock(4)
    type = 'bullet'
    def __init__(self, position, direction, player, *groups: pyg.sprite.Group):
        super().__init__(*groups)
        self.image = pyg.Surface((10, 10))  # Replace with your bullet image
        self.image.fill((200,200,200))
        self.rect = self.image.get_rect(center=position)
        self.speed = 7  # Adjust bullet speed as needed
        self.direction = direction

        self.player = player
        
        self.damage = self.player.damage
        self.speed = self.player.attack_speed * self.speed
    
    def CheckScreenLimits(self):
        size = SCREEN.get_size()
        if self.rect.right > size[0]:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.bottom > size[1]:
            self.kill()
        if self.rect.top < 0:
            self.kill()

    def LifeTimeCounter(self):
        if self.lifeTime > 0:
            self.lifeTime -= 1
        if self.lifeTime <= 0:
            self.kill()

    def checkCollision(self):
        sprites = self.player.groups()[0].sprites()
        for sprite in sprites:
            if sprite.type == 'bullet':
                return
            if self.rect.colliderect(sprite.rect):
                if sprite.type == 'enemy':
                    if sprite.health > 0:
                        sprite.takeDamage(self.damage * random.choice([.8,1,1.2]))
                        self.kill()

    def update(self, player):
        # Move the bullet in the direction of the vector
        self.rect.move_ip(self.direction * self.speed)

        self.checkCollision()
        self.LifeTimeCounter()
        self.CheckScreenLimits()
        

    def draw(self,screen):
        SCREEN.blit(self.image, self.rect)

class player(pyg.sprite.Sprite):
    type = 'player'
    
    attack_delay_s = 1.5
    heal_delay = 5

    AutoCountHeal = Clock(heal_delay)
    attack_delay = Clock(attack_delay_s)

    damage = 5
    attack_speed = 1
    _locked = False
    Bullets = Bullets()

    level = 1
    experience = 0
    speed = 2.5
    def __init__(self, *groups: pyg.sprite.Group) -> None:
        super().__init__(*groups)
        self.rect = Rect(400, 300, 32,32)
        self.image = pyg.Surface((32,32))
        self.move = pyg.math.Vector2(0,0)

        self.image.fill((200,170,200))

        self.maxhealth = 100
        self.health = self.maxhealth

        self.LeveledUp = False

    def addExp(self,exp:int):
        self.experience += exp
        if self.experience >= self.level*10:
            self.experience -= self.level*10
            self.level += 1
            self.LeveledUp = True
    
    def takeDamage(self,damage):
        if self.health > 0:
            self.health -= damage
            self.AutoCountHeal += Clock(self.heal_delay/5)

    def heal(self, value):
        if self.health > 0:
            self.health += value

    def autoHeal(self):
        if self.AutoCountHeal > 0:
            self.AutoCountHeal -= 1
        elif self.AutoCountHeal <= 0:
            self.AutoCountHeal = Clock(.1)
            if self.health < self.maxhealth:
                self.heal(((self.health/self.maxhealth)/10) * self.maxhealth)
            else:
                self.AutoCountHeal = Clock(5)

        if self.health <= 0:
            self._locked = True

    def attack(self):
        player_pos = self.rect.center
        direction = pyg.math.Vector2(pyg.mouse.get_pos()) - player_pos
        
        # Normalize the direction vector
        direction = direction.normalize()

        Bullet(player_pos, direction, self, [self.Bullets, self.groups()[0]])

    def input(self):
        if (pme.while_key_hold(K_w) or pme.while_key_hold(K_UP)):
            self.move.y = -1
        elif (pme.while_key_hold(K_s) or pme.while_key_hold(K_DOWN)):
            self.move.y = 1
        if (pme.while_key_hold(K_a) or pme.while_key_hold(K_LEFT)):
            self.move.x = -1
        elif (pme.while_key_hold(K_d) or pme.while_key_hold(K_RIGHT)):
            self.move.x = 1

        if self.attack_delay > 0:
            self.attack_delay -= 1

        if pyg.mouse.get_pressed(3)[0]:
            if self.attack_delay <= 0:
                self.attack()
                self.attack_delay = Clock(self.attack_delay_s)
                


    def mov(self):
        if not self._locked:
            self.rect.x += self.move.x * self.speed
            self.rect.y += self.move.y * self.speed

            self.move.x *= 0.01
            self.move.y *= 0.01

    def draw_info(self):
        pos = (self.rect.centerx,self.rect.bottom)
        pme.draw_text((pos[0]-22,pos[1]+8),'Player',2,(0,0,0),(255,255,0),True)
        if self.health < self.maxhealth:
            pme.draw_bar((pos[0]-32,pos[1]-48),(64,10),self.health, self.maxhealth, text=f'{int(self.health)} / {int(self.maxhealth)}', textfont=3)

    def update(self, *args, **kwargs) -> None:
        self.input()
        self.mov()
        self.autoHeal()
        self.Bullets.update(self)
        return super().update(*args, **kwargs)

    def draw(self):
        SCREEN.blit(self.image, self.rect)

    def getd(self,name:str) -> any:
        try:
            return self.__dict__[name]
        except:
            return 0

class Sprites(pyg.sprite.Group):
    def __init__(self, *sprites) -> None:
        super().__init__(*sprites)

    def getNumOfEnemys(self) -> int:
        n = 0
        for sprite in self.sprites():
            if sprite.type == 'enemy':
                n += 1
        return n

    def update(self, player) -> None:
        for sprite in self.sprites():
            if sprite.type == 'bullet':
                return
            sprite.update(player)
            
    def draw_info(self):
        for sprite in self.sprites():
            try:
                sprite.draw_info()
            except:
                pass

class ExpShard(pyg.sprite.Sprite):
    type = 'exp'
    def __init__(self, color:tuple, exp_value:int,pos,*groups) -> None:
        super().__init__(*groups)
        self.color = color
        self.size = (16,16)
        self.image = pyg.Surface(self.size, SRCALPHA)
        self.image = pyg.transform.rotate(self.image, 45)
        self.image.fill(self.color)
        self.image.set_alpha(150)

        self.exp = exp_value * random.choice([0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 2])

        self.rect = Rect(pos[0],pos[1],self.size[0],self.size[1])

    def CheckCollide(self,player):
        if player.rect.colliderect(self.rect):
            player.addExp(self.exp)
            self.kill()

    def update(self,player, *args: Any, **kwargs: Any) -> None:
        self.CheckCollide(player)

class EnemyBlue(pyg.sprite.Sprite):
    type = 'enemy'

    color = (100,100,200)
    speed = 2 * WAVE
    move_delay = Clock(.1)
    attack_delay = Clock(1)
    damage = 3 * WAVE

    delete_clock = 0

    _died = False

    maxhealth = 10 * WAVE
    health = maxhealth

    level = 1
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        x = random.choice([64, 256, 448, 648, 700])
        y = random.choice([64, 256, 458])
        self.rect =Rect(x,y,32,32)
        self.image = pyg.Surface((32,32),SRCALPHA)

        self.image.fill(self.color)

        self.move = pyg.math.Vector2(0,0)

    def takeDamage(self, damage):
        if self.health > 0:
            self.health -= damage

    def mov(self):
        if self.health > 0:
            self.rect.x += self.move.x * 2.5
            self.rect.y += self.move.y * 2.5

            self.move.x *= 0.01
            self.move.y *= 0.01

    def follow_player(self, player_position):
        if self.move_delay <= 0:
            try:
                # Calculate the direction vector from enemy to player
                p = pyg.math.Vector2(player_position)
                direction = p - self.rect.center
                
                # Normalize the direction vector
                direction = direction / math.sqrt(direction[0]**2 + direction[1]**2)
                
                # Calculate the new position of the enemy
                new_position = self.rect.center + direction * (self.speed*random.choice([0.8,1,1.2]))
                
                if self.health > 0:
                    self.rect.center = new_position
                    self.move_delay = Clock(.1)
            except:
                pass
        else:
            self.move_delay -= 1

    def draw_info(self):
        pos = (self.rect.centerx, self.rect.bottom)
        if self.health < self.maxhealth and not (self.health <= 0):
            pme.draw_bar((pos[0]-32,pos[1]-48),(64,10),self.health, self.maxhealth, text=f'{int(self.health)} / {int(self.maxhealth)}', textfont=3)

    def died(self):
        if self.health <= 0 and not (self._died):
            self.delete_clock = Clock(2.5)
            self.health = 0
            self.image.set_alpha(100)
            self.image = pyg.transform.scale(self.image,(24,24))
            self._died = True
            self.reward()


        if self._died:
            if self.delete_clock > 0:
                self.delete_clock -= 1
                if self.delete_clock <= 0:
                    if self.health <= 0:
                        self.Spawn()
                        self.kill()

    def reward(self):
        r = random.randint(1,9) + random.randint(0,1)
        if r in [1, 3, 4]:
            self.groups()[0].add(ExpShard((255,190,255,),self.level+15, self.rect.center))
        elif r in [2,5,6]:
            self.groups()[0].add(ExpShard((190,255,190,),self.level+6, self.rect.center))
        elif r in [7,8,9]:
            self.groups()[0].add(ExpShard((255,190,190,),self.level+8, self.rect.center))
        else:
            self.groups()[0].add(ExpShard((190,190,255,),self.level+4, self.rect.center))

    def Spawn(self):
        if random.randint(1,5) == 3:
            self.groups()[0].add(EnemyGreen())
        elif random.randint(1,10) == 2:
            self.groups()[0].add(EnemyBlue())
            self.groups()[0].add(EnemyBlue())
        else:
            self.groups()[0].add(EnemyBlue())

    def collision(self, player:player):
        if self.health > 0:
            if self.rect.colliderect(player.rect):
                if self.attack_delay <= 0:
                    player.takeDamage(self.damage)
                    self.attack_delay = Clock(1)
        
        if self.attack_delay > 0:
            self.attack_delay -= 1

    def update(self, player,*args, **kwargs) -> None:
        self.follow_player(player.rect.center)
        self.collision(player)
        self.died()
        return super().update(*args, **kwargs)

class EnemyGreen(EnemyBlue):
    color = (100,200,100)

    type = 'enemy'

    speed = 4 * WAVE
    move_delay = Clock(.1)
    attack_delay = Clock(1)
    damage = 5 * WAVE

    maxhealth = 20 * WAVE
    health = maxhealth

    level = 2
    def Spawn(self):
        if random.randint(1,5) == 3:
            self.groups()[0].add(EnemyRed())
        elif random.randint(1,10) == 2:
            self.groups()[0].add(EnemyGreen())
            self.groups()[0].add(EnemyGreen())
        else:
            self.groups()[0].add(EnemyGreen())

class EnemyRed(EnemyBlue):
    color = (200,100,100)

    type = 'enemy'

    speed = 5 * WAVE
    move_delay = Clock(.1)
    attack_delay = Clock(1)
    damage = 6 * WAVE

    maxhealth = 25 * WAVE
    health = maxhealth

    level = 3
    def Spawn(self):
        if random.randint(1,5) == 3:
            self.groups()[0].add(EnemyPurple())
        elif random.randint(1,10) == 2:
            self.groups()[0].add(EnemyRed())
            self.groups()[0].add(EnemyRed())
        else:
            self.groups()[0].add(EnemyRed())

class EnemyPurple(EnemyBlue):
    color = (200,100,200)

    type = 'enemy'

    speed = 6 * WAVE
    move_delay = Clock(.1)
    attack_delay = Clock(1)
    damage = 7 * WAVE

    maxhealth = 30 * WAVE
    health = maxhealth

    level = 4
    def Spawn(self):
        if random.randint(1,10) == 3:
            self.groups()[0].add(EnemyBlue())
        else:
            self.groups()[0].add(EnemyPurple())