from config import *

rarity_colors = {
    'common': (200,200,200),
    'uncommon': (150,255,150),
    'rare': (150,150,255),
    'epic': (255,150,150),
    'legendary': (255,150,255),
    'impossible': (0,0,0)
}

class BaseCard(pyg.sprite.Sprite):
    name = 'Base Card'
    effect = "nothing"
    type = 'card'
    rarity = 'impossible'

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pyg.Surface((128,230))
        self.color = rarity_colors[self.rarity]
        
        pme.draw_rect((0,0),self.image.get_size(),(64,64,64),3,self.image)

        pme.draw_text((0,0), self.name, 2, (255,255,255),self.color, True,self.image)
        self.draw_description()
    
    def draw_description(self):
        if len(self.effect.split(' ')) > 5:
            lines = limit_line_length(self.effect, 20)
                    
            ypos = 30
            for line in lines:
                print(line)
                pme.draw_text((3, ypos), line, 3, (255,255,255),antialias=True,screen=self.image)
                ypos += 16
        else:
            pme.draw_text((3, 30), self.effect, 3, (255,255,255),antialias=True,screen=self.image)

    def draw(self,xpos):
        SCREEN.blit(self.image, (xpos, SCREEN.get_size()[1]-275))
    
    def action(self,player):
        pass
class MoreDamage1(BaseCard):
    name = 'More Damage'
    effect = 'Add 0.5% of damage.'
    rarity = 'common'

    def action(self,player):
        player.damage += player.damage*0.005

class MoreHealth1(BaseCard):
    name = 'More Health'
    effect = 'Add 0.5% of health.'
    rarity = 'common'
    def action(self,player):
        old_max = player.maxhealth
        player.maxhealth += player.maxhealth*0.005

        player.health *= old_max/player.maxhealth

class MoreProjectSpeed(BaseCard):
    name = 'More Project speed'
    effect = 'Add 0.5% of speed of the projectiles.'
    rarity = 'uncommon'
    def action(self, player):
        player.attack_speed += player.attack_speed*0.005

class MoreDamage2(BaseCard):
    name = 'More Damage 2'
    effect = 'Add 2% of damage.'
    rarity = 'uncommon'
    def action(self, player):
        player.damage += player.damage*0.02

class MoreDamage3(BaseCard):
    name = 'More Damage 3'
    effect = 'Add 12% of damage.'
    rarity = 'rare'
    def action(self, player):
        player.damage += player.damage*0.12

class MoreHealth2(BaseCard):
    name = 'More Health 2'
    effect = 'Add 2% of health.'
    rarity = 'uncommon'
    def action(self, player):
        old_max = player.maxhealth
        player.maxhealth += player.maxhealth*0.02

        player.health *= old_max/player.maxhealth

class MoreSpeed(BaseCard):
    name = 'More Speed'
    effect = 'Add 1.5% of speed of the projectiles.'
    rarity = 'rare'
    def action(self, player):
        player.speed += player.speed*0.015

class MoreSpeed(BaseCard):
    name = 'More Speed'
    effect = 'Add 1.5% of speed of the projectiles.'
    rarity = 'rare'
    def action(self, player):
        player.speed += player.speed*0.015

class MoreAttackSpeed(BaseCard):
    name = 'More Attack Speed'
    effect = 'Reduce 0.5% of attack delay.'
    rarity = 'epic'
    def action(self, player):
        player.attack_delay_s -= player.attack_delay_s*0.005

Cards = [MoreDamage1, MoreHealth1, MoreProjectSpeed, MoreDamage2, MoreDamage3, MoreHealth2, MoreSpeed]