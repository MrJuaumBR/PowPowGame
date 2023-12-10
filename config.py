from PyMaxEngine import *

pme = PyMaxEngine()

SCREEN = pme.create_screen((800, 600))
pyg.display.set_caption('PowPow Game')

FPS = 60

# Fonts
pme.create_sysFont('arial',32,True,False)
pme.create_sysFont('arial',28,True,False)
pme.create_sysFont('arial',16,True,False)
pme.create_sysFont('arial',12,True,False)

RClock = pyg.time.Clock()

WAVE = 1
def SetWave(w):
    WAVE = w

def Clock(time):
    r = FPS*time
    return r

def limit_line_length(text, limit):
    lines = []
    current_line = ""
    
    for word in text.split():
        if len(current_line) + len(word) <= limit:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    lines.append(current_line.strip())
    
    return lines