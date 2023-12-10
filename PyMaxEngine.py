# Imports
import pygame as pyg # PyGame Dependecies
from pygame.locals import * # PyGame Dependecies
import os # ?
from sys import exit # PyGame quit
from datetime import datetime # Screenshots
from requests import get # Load Version
from json import loads # Load Version
from colorama import Fore # Color for terminal

"""
Requires:
pygame;
requests;
"""
# Exceptions
class OutdatedExc(Exception):
    def __init__(self,message="Can't run Engine because: Version is outdated."):
        """Excpetion for version"""
        self.message =message + "\n> Download a updated version here: https://mrjuaumbr.github.io"
        super().__init__(self.message)
# Notes
"""
Fix bugs, implement some features, new name(Old: PooPEngine2 > New: PyMaxEngine), don't crash if already exists a same font, warn if not updated and color for terminal in some cases
 - 0.3;
"""

# Variables
strftime = "%d.%m.%Y_%H%M%S"
colors = {}


# Main
class PyMaxEngine():
    """PyMaxEngine"""
    TEXTINPUT_BLACKLIST = [K_KP_ENTER,K_END,K_DELETE,K_END,K_PAGEDOWN,K_PAGEUP,K_INSERT,K_BACKSPACE]
    def __init__(self,screen:pyg.surface=None) -> None:
        """A simple Engine for complement pygame and make it easier"""
        self.Name = "PyMaxEngine"
        self.ver = self.version()
        self.fonts = []
        self.screen = screen
        self.colors = colors
        # Check if Updated
        self.check_update()
                    
        self.screenshot_path = 'screenshot_'
        self.requirements = ["pygame>=2.5.0","requests>=2.31.0"] # Requirements
        self.set_colors()
        pyg.init()

    def set_colors(self):
        """Set colors"""
        c = self.get_colors()
        for color in c:
            self.colors[str(color)] = c[color]
            self.colors[str(color).upper()] = c[color]
            self.colors[str(color).lower()] = c[color]
    def get_colors(self):
        """Get Colors source"""
        r = get('https://mrjuaumbr.github.io/data/colors.json')
        r = loads(r.text)
        return r
    
    def check_update(self):
        """"Check if it is updated"""
        pass

    def requirements_gen(self):
        """Generate a requirements.txt for pip install"""
        with open('requirements.txt','w+') as f:
            f.writelines(self.requirements)

    def version(self):
        """Get version place"""
        return f"{self.v()} - {self.Name}: https://mrjuaumbr.github.io"
    
    def v(self):
        """Get version number"""
        return "0.3"
    def set_icon(self, icon:pyg.surface):
        """Set icon"""
        pyg.display.set_icon(icon)

    def create_screen(self,size:tuple or list,**kwargs):
        """Create a screen and return, TIP: Don't use Fullscreen windows or use Scaled(auto)"""
        if not self.screen:
            if kwargs.get('flags'): # Scale if fullscreen and not Scaled
                if str(kwargs.get('flags')) == str(-2147483648):
                    kwargs.update(flags=-2147483136)
                    print(f"[PyMaxEngine] {Fore.GREEN}Fullscreen withou scale, scaled!{Fore.RESET}")
            os.environ['SDL_VIDEO_CENTERED'] = '1'
            if kwargs:
                self.screen = pyg.display.set_mode(size,**kwargs)
            else:
                self.screen =pyg.display.set_mode(size)
            print(f'[PyMaxEngine] {Fore.GREEN}Screen created!{Fore.RESET}')
            return self.screen
        else:
            print(f"[PyMaxEngine] {Fore.RED}You already have a screen!{Fore.RESET}")

    def while_key_hold(self,key):
        keys = pyg.key.get_pressed()
        if keys[key]:
            return True
        else:
            return False
        
    def create_sysFont(self,name:str,size:int,bold=False,italic=False) -> pyg.font:
        """Create a font and return"""
        r = pyg.font.SysFont(name, size, bold, italic)
        
        if r in self.fonts:
            print(f"[PyMaxEngine] {Fore.RED}Font already exists in index: {self.fonts.index(r)}{Fore.RESET}")
        else:
            self.fonts.append(r)
            print(f"[PyMaxEngine] {Fore.GREEN}Font created in index: {self.fonts.index(r)}{Fore.RESET}")
        return r
    
    def create_font(self,font_file="", font_size = 16) -> pyg.font:
        """
        Create a font with your file
        font_path = the path of ttf file
        font_size = Size inf pixel of font
        """
        f = pyg.font.Font(font_file, font_size)
        if f in self.fonts:
            raise(f"This font already exists in fonts list. font don't created, you can acess this in index: {self.fonts.index(f)}")
        else:
            self.fonts.append(f)
        return (self.fonts.index(f), f)

    def draw_circle(self,Position:tuple or list,color:tuple, radius:int) -> pyg.Rect:
        """Draw a circle"""
        o = pyg.draw.circle(self.screen,color,Position,radius)
        return o
    
    def load_image(self,path) ->pyg.surface:
        """Load a image"""
        i = pyg.image.load(path)
        return i
    
    def insert_on(self, surface:pyg.surface, position:tuple or list) -> pyg.surface:
        """Insert a SURFACE on a surface"""
        self.screen.blit(surface, position)

    def draw_textbox(self, Position:tuple or list,font:int,colors=[tuple,tuple,tuple],active=False, text='',character_limit=100,otherBlackList=[]) -> [bool, str]:
        if type(font) == int:
            font = self.fonts[font]
        size = pyg.font.Font.size(font,str(text))

        blacklist = self.TEXTINPUT_BLACKLIST
        for b in otherBlackList:
            if not b in blacklist:
                blacklist.append(b)

        
        if size[0]+Position[0] >= self.screen.get_size()[0]:
            X = Position[0] - ((size[0]+Position[0])-self.screen.get_size()[0])
        else:
            X = Position[0]
        if active:
            curColor = colors[1]
        elif not active:
            curColor = colors[2]
        if len(str(text)) < 1:
            ctext = "    "
        else:
            ctext = text
        box = self.draw_text((X,Position[1]),str(ctext),font,colors[0],curColor)
        if pyg.mouse.get_pressed(3)[0]:
            if box.collidepoint(pyg.mouse.get_pos()):
                active = True
            else:
                active = False
        else:
            if not active:
                active = False
        
        if active:
            if len(str(text)) < character_limit:
                if not size[0] >= (self.screen.get_size()[0]*2):
                    if self.while_key_hold(K_BACKSPACE):
                        if not len(str(text)) < 1:
                            text = text[:-1]
                            pyg.time.delay(50)

                    for ev in pyg.event.get():
                        if ev.type == pyg.KEYDOWN:
                            if not ev.key in blacklist:
                                text += ev.unicode

        return (active, text)

    def draw_image(self,image:str or pyg.image,Position: tuple or list) -> pyg.surface:
        """Draw a image"""
        if type(image) == str:
            image = self.load_image(image)
        r = image.get_rect()
        r.topleft = Position
        self.screen.blit(image,r)
        return image

    def resize_surface(self,surface:pyg.surface,size:tuple or list) -> pyg.surface:
        """Resize a surface by scale"""
        i = pyg.transform.scale(surface,size)
        return i

    def flip_surface(self,surface:pyg.surface,flip_x=False,flip_y=False) -> pyg.surface:
        """Flip a surface"""
        i = pyg.transform.flip(surface,flip_x,flip_y)
        return i

    def rotate_surface(self,surface:pyg.surface,angle:float) -> pyg.surface:
        """Rotate a surface"""
        i = pyg.transform.rotate(surface,angle)
        return i

    def draw_rect(self,Position:tuple or list,Size:tuple or list, color:tuple,border:int=0,screen:pyg.surface=None) -> pyg.Rect:
        """Draw a rect, it can have Alpha: (R,G,B,A)"""
        if len(color) == 4:
            o = pyg.Surface(Size,SRCALPHA)
            o.fill((color[0],color[1],color[2]))
            o.set_alpha(color[3])
            r = o.get_rect(topleft=Position)
            if screen:
                screen.blit(o,r)
            else:
                self.screen.blit(o,r)
            o = r
        elif len(color) == 3:
            if screen:
                o = pyg.draw.rect(screen,color,Rect(Position[0],Position[1],Size[0],Size[1]),border)
            else:
                o = pyg.draw.rect(self.screen,color,Rect(Position[0],Position[1],Size[0],Size[1]),border)
        return o

    def draw_rect2(self,Position:tuple or list,Size:tuple or list, color:tuple,border:int=0) -> pyg.Rect:
        """Draw a rect, it can have Alpha: (R,G,B,A)"""
        self.draw_rect(Position,Size,color,0)
        if border > 0:
            self.draw_rect(Position,Size,color,border)

    def draw_slider(self,Position:tuple or list,Width:int,CurX:int,colors=((0,0,0),(200,200,200))):
        """Draw a slider control return current ball X and float between 0 - 1"""
        MaxX = Position[0] + Width
        self.draw_rect(Position,(Width,20),colors[0])
        b = self.draw_circle((CurX,Position[1]+10),colors[1],25)
        if b.collidepoint(pyg.mouse.get_pos()):
            if pyg.mouse.get_pressed(3)[0]:
                CurX = pyg.mouse.get_pos()[0]
                if CurX > MaxX:
                    CurX = MaxX
                elif CurX < Position[0]:
                    CurX = Position[0]
        Value = CurX/MaxX
        if Value > 1:
            Value = 1
        elif Value<0:
            Value = 0

        return CurX, Value

    def draw_bar(self,Position: tuple or list, Size: tuple or list,CurValue:int,maxValue:int,colors=((0,0,0),(200,10,10),(0,0,0)),text="",textfont=0, screen:pyg.Surface=None):
        """Draw a bar, with max value, can be used as health bar."""
        tryDiv = lambda CurValue, maxValue: CurValue/maxValue if CurValue > 0 else 0
        X = tryDiv(CurValue,maxValue)
        self.draw_rect(Position,(Size[0]*X,Size[1]),colors[1],screen=screen)
        self.draw_rect(Position,Size,colors[0],3,screen=screen)
        if text != "":
            if len(self.fonts) < 1:
                myf = self.create_sysFont("arial",int(Size[1]*0.8),False,False)
            else:
                myf = self.fonts[textfont]
            self.draw_text((Position[0]+4,Position[1]),text,myf,(200,200,200),screen=screen)

    def draw_text(self,Position: tuple or list,text:str,font: pyg.font or int, color:tuple or list,bgcolor=None, antialias=False, screen:pyg.Surface=None) -> pyg.rect:
        """Draw a text based into your font."""
        if type(font) == int:
            font = self.fonts[font]
        if bgcolor:
            r = font.render(str(text),antialias,color,bgcolor)
        else:
            r = font.render(str(text),antialias,color)
        r_rect = r.get_rect()
        r_rect.topleft = Position
        if screen:
            screen.blit(r,r_rect)
        else:
            self.screen.blit(r,r_rect)
        return r_rect

    def draw_button(self,Position:tuple or list,text:str,font:pyg.font or int, color:tuple or list,bgcolor=None, waitMouseUp=False, Tip=None) -> bool:
        """Draw a button, return True it is pressed"""
        if self.draw_text(Position,text,font,color,bgcolor).collidepoint(pyg.mouse.get_pos()):
            if Tip:
                Tip.HoveRing(True)
            if pyg.mouse.get_pressed(3)[0]:
                if waitMouseUp:
                    pyg.time.delay(250)
                    return True
                return True
            else:
                return False
        else:
            if Tip:
                Tip.HoveRing(False)
            return False
        
    def draw_button2(self, Position:tuple or list, text:str, font:pyg.font.Font or int, Colors:tuple or list=[tuple,tuple,tuple], waitMouseUp=False, Tip=None) -> bool:
        """Draw a button, return True it is pressed"""
        if type(font) == int:
            font:pyg.font.Font = self.fonts[font]
        else:
            font:pyg.font.Font = font
        
        render_size = font.size(text)
        bg = self.draw_rect((Position[0],Position[1]),(render_size[0],render_size[1]),Colors[1])
        if len(Colors) == 3:
            self.draw_rect((Position[0]-2,Position[1]-2),(render_size[0]+4,render_size[1]+4),Colors[2],2)
        text = self.draw_text(Position,text,font,Colors[0],antialias=True)
        if bg.collidepoint(pyg.mouse.get_pos()) or text.collidepoint(pyg.mouse.get_pos()):
            if Tip:
                Tip.HoveRing(True)
            if pyg.mouse.get_pressed(3)[0]:
                if waitMouseUp:
                    pyg.time.delay(250)
                    return True
                return True
            else:
                return False
        else:
            if Tip:
                Tip.HoveRing(False)
            return False

    def draw_select(self,Position: tuple or list,items:list or tuple,cur_index:int,font:int or pyg.font,colors=((0,0,0),(200,200,100))):
        """Draw a select object, based in items list"""
        if type(font) == int:
            font = self.fonts[font]
        if len(str(items[cur_index])) <= 1:
            fix = font.size(str(items[cur_index]))[0] * 1.2
        else:
            fix = font.size(str(items[cur_index]))[0]
        self.draw_text((Position[0]-fix/4,Position[1]),items[cur_index],font,colors[0],colors[1])
        bback = self.draw_button((Position[0]-fix,Position[1]),"<",font,colors[0],colors[1],True)
        bnext = self.draw_button((Position[0]+fix,Position[1]),">",font,colors[0],colors[1],True)
        if bback:
            pyg.time.delay(90)
            if cur_index-1<0:
                cur_index=len(items)-1
            else:
                cur_index -=1
        elif bnext:
            pyg.time.delay(90)
            if cur_index +1>len(items)-1:
                cur_index = 0
            else:
                cur_index+=1
        return cur_index

    def draw_switch(self,Position: tuple or list,font:pyg.font or int,curState:bool,colors=((0,0,0),(200,100,100),(100,100,200))) -> bool:
        """Draw a switch object: On & Off"""
        tx = ""
        if curState:
            tx = "On"
            C = colors[2]
        else:
            tx = "Off"
            C = colors[1]
        if self.draw_button(Position,tx,font,colors[0],C):
            curState = not curState
            pyg.time.delay(150)
        return curState

    def hex_to_rgb(self,hex):
        """Convert Hexadecimal to RGB"""
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        
        return tuple(rgb)
    
    def rgb_to_hex(self,r, g, b) -> str:
        """Convert RGB to Hexadecimal"""
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def quit(self):
        """Pygame.quit() event with sys.exit()"""
        pyg.quit()
        exit()

    def save_surface(self,surface: pyg.surface):
        """Save a screenshot of the passed surface"""
        pyg.image.save(surface,f'{self.screenshot_path}{datetime.now().strftime(strftime)}.png')

    def key_pressed(self,Key:int) -> bool:
        """Return True while the key pressed"""
        keys = pyg.key.get_pressed()
        if keys[Key]:
            return True
        else:
            return False

    def events(self):
        """Get Pygame Events"""
        return pyg.event.get()

    def get_scale_ratio(self,map=[[]],tile_size=64) -> float:
        """Math to get a scale ratio based on tile map and tile_size"""
        SCREEN_SIZE = self.screen.get_size()
        if tile_size <= 0:
            tile_size = 1
        X_ROWS = len(map[0])
        Y_ROWS = len(map)
        X_RATIO = X_ROWS/SCREEN_SIZE[0]
        Y_RATIO = Y_ROWS/SCREEN_SIZE[1]
        TILES_FORX = SCREEN_SIZE[0]/tile_size
        TILES_FORY = SCREEN_SIZE[1]/tile_size
        ratio = ((TILES_FORX+TILES_FORY)/2)*((X_RATIO+Y_RATIO)/2)
        return ratio

    def update(self):
        """Update screen"""
        pyg.display.update()


# Extras
class Tip():
    """Tip"""
    def __init__(self,Tip:str,pme:PyMaxEngine,FR_Color:tuple or list=(0,0,0),BG_Color:tuple or list=(255,255,255),font:pyg.font or int=None) -> None:
        """Tip"""
        self.Tip = Tip
        self.Active = False
        if type(font) == int:
            self.Font:pyg.font.Font = pme.fonts[font]
        else:
            self.Font:pyg.font.Font = font
        self.Colors = FR_Color, BG_Color
        self.pme = pme
    
    def Draw(self,mouse_pos:tuple):
        """Draw"""
        if self.Active:
            if self.Tip.find('\n') == -1:
                t = []
            else:
                t = self.Tip.split('\n')
            s_posy:int = mouse_pos[1]-16
            size_rect = [0,0]
            if len(t) > 0:
                line_form = []
                for line in t:
                    size = self.Font.size(line)
                    size_rect[1] += size[1]
                    size_rect[0] = size[0]
                    pos:int = s_posy
                    line_form.append((line, pos))
                    s_posy += size[1]+2

                self.pme.draw_rect((mouse_pos[0]+16,mouse_pos[1]-16),(size_rect[0]+2,size_rect[1]+2),self.Colors[1])
                Border = lambda: self.Colors[2] if len(self.Colors) >= 3 else (255,255,255)
                self.pme.draw_rect((mouse_pos[0]+14,mouse_pos[1]-18),(size_rect[0]+4,size_rect[1]+4),Border(),2)
                for t in line_form:
                    #self.pme.draw_text((mouse_pos[0]+16,mouse_pos[1]-16),self.Tip,self.Font,self.Colors[0],self.Colors[1],True)
                    self.pme.draw_text((mouse_pos[0]+16,t[1]),t[0],self.Font,self.Colors[0],antialias=True)
            else:
                size = self.Font.size(self.Tip)
                size_rect[1] = size[1]
                size_rect[0] = size[0]
                self.pme.draw_rect((mouse_pos[0]+16,mouse_pos[1]-16),(size_rect[0]+2,size_rect[1]+2),self.Colors[1])
                Border = lambda: self.Colors[2] if len(self.Colors) >= 3 else (255,255,255)
                self.pme.draw_rect((mouse_pos[0]+14,mouse_pos[1]-18),(size_rect[0]+4,size_rect[1]+4),Border(),2)
                self.pme.draw_text((mouse_pos[0]+16,mouse_pos[1]-16),self.Tip,self.Font,self.Colors[0],antialias=True)

    def HoveRing(self,state:bool):
        m = pyg.mouse.get_pos()
        self.Active = state
        self.Draw(m)


# Test Engine
if __name__ == "__main__": #Test Engine
    pme = PyMaxEngine()
    pme.create_screen((125,125),flags=FULLSCREEN|SCALED)
    