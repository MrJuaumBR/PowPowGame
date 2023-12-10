from config import *
from ingame import game_run

def game():
    while True:
        pme.draw_text((275,100),'Pow Pow Game',0,(0,0,0),(255,255,0),True)

        if pme.draw_button((200,155),'Play',1,(0,0,0),(100,255,190),True):
            game_run()

        for ev in pme.events():
            if ev.type == QUIT:
                pme.quit()

        pme.update()
        SCREEN.fill((255, 255, 255))

if __name__ == '__main__':
    game()