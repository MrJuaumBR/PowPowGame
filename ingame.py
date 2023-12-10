from config import *
from player import player, Sprites, EnemyBlue
from Cards import *
import random

def game_run():
    run = True
    All = Sprites()
    plr = player(All)
    SetWave(1)

    for i in range(random.randint(10,13)):
        All.add(EnemyBlue())
    
    Pause = False

    TheRnDCards = []

    while run:
        pme.draw_text((400,25), f'Enemys: {All.getNumOfEnemys()}', 2, (255,255,255),antialias=True)
        for ev in pme.events():
            if ev.type == QUIT:
                run = False
                pme.quit()
            elif ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    Pause = not Pause

        if plr.LeveledUp:
            Pause = True

        pme.update()
        if plr.health > 0 and not Pause:
            All.update(plr)
            SCREEN.fill((150,200,175))
            All.draw(SCREEN)
            All.draw_info()
            plr.Bullets.draw(SCREEN)
            pme.draw_text((15,60),f'Level: {plr.level}',2,(255,255,255),antialias=True)
            pme.draw_bar((15,15),(250,25),plr.experience,plr.level*10,text=f'{int(plr.experience)} / {plr.level * 10}',colors=((0,0,0),(100,100,200),(0,0,0)),textfont=2)
            pme.draw_bar((15,35),(250,25),plr.health,plr.getd("maxhealth"),text=f'{int(plr.health)} / {int(plr.getd("maxhealth"))}',colors=((0,0,0),(200,100,100),(0,0,0)),textfont=2)
            # Info
            pme.draw_text((15,75),f'Damage: {int(plr.getd("damage"))}', 3, (255,255,255),antialias=True)
            pme.draw_text((15,87),f'Speed: {int(plr.getd("speed"))}', 3, (255,255,255),antialias=True)
        else:
            if Pause:
                if not plr.LeveledUp:
                    SCREEN.fill((150,200,175))
                    All.draw(SCREEN)
                    plr.Bullets.draw(SCREEN)
                    pme.draw_text((0,0),'PAUSED', 0, (255,255,255), (0,0,0), True)

                    if pme.draw_button((15, 50),'Resume', 1, (255,255,255), (50,175,75), True):
                        Pause = False
                    if pme.draw_button((15, 100),'Suicide', 1, (255, 255, 255), (175, 50, 75), True):
                        plr.health = 0
                        Pause = False
                    if pme.draw_button((15, 150),'Quit', 1, (255, 255, 255),(175, 50, 75),True):
                        run = False
                else:
                    pme.draw_rect2((0,325),(800,275),(170,150,90,200),3)
                    pme.draw_text((350,100),'Leveled Up!',0,(255,255,255),antialias=True)

                    if len(TheRnDCards) == 0:
                        def RndCard():
                            TheRnDCards.clear()
                            for i in range(3):
                                c = random.choice(Cards)
                                if not c in TheRnDCards:
                                    TheRnDCards.append(c())
                                else:
                                    RndCard()
                        RndCard()

                    xpos = [128, 306, 484]
                    btns = []
                    for i in range(3):
                        TheRnDCards[i].draw(xpos[i])
                        sl =pme.draw_button((xpos[i],SCREEN.get_size()[1]-40),f'Select({i+1})', 1, (255,255,255), (50,50,50), True)
                        btns.append((i,sl))
                    for btn in btns:
                        if btn[1]:
                            TheRnDCards[btn[0]].action(plr)
                            TheRnDCards.clear()
                            plr.LeveledUp = False
                            Pause = False
            else:
                SCREEN.fill((200,100,105))
                pme.draw_text((0,0),'GAME OVER', 0, (255,255,255), (0,0,0), True)
                if pme.draw_button((15, 65),'Restart', 1, (255,255,255), (50,175,75), True):
                    game_run()
                    run = False
                if pme.draw_button((15, 115),'Quit', 1, (255, 255, 255),(175, 50, 75),True):
                    run = False

        RClock.tick(FPS)