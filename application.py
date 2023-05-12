import pygame, sys, random, pyautogui, keyboard
from settings import *
from damgui.damgui import damgui
from damgui.constants import settings
from pynput.mouse import Controller, Button

class Application:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZES)
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(pygame.image.load("winicon.png").convert_alpha())
        self.clock = pygame.time.Clock()
        
        self.toggle_key = None
        self.toggle_name = None
        self.cps = 10
        self.cooldown = 0
        self.next_cps = self.cps
        self.listening_key = False
        self.enabled = False
        self.running = False
        self.was_pressing = False
        self.last_press = pygame.time.get_ticks()
        self.isdown = False
        self.mouse_controller = Controller()
        
    def damgui(self):
        # window
        settings.OUTLINE_COL = settings.WINDOW_BG_COL
        damgui.begin("main_win","Clicky Autoclicker",(0,0),SIZES,False)
        # close btn
        settings.OUTLINE_COL = settings.ELEMENT_BG_COL
        damgui.custom_pos((W-30-settings.Y_MARGIN,settings.Y_MARGIN))
        if damgui.button("close_btn","X",(30,28)): self.quit()
        settings.reset()
        # fps
        settings.FONT = settings.FONT_XS
        damgui.label("fps_l",f"FPS: {self.clock.get_fps():.2f}")
        settings.reset()
        
        settings.FONT = settings.FONT_L
        # cps, + -
        damgui.label("cps_l",f"CPS: {self.cps}",(110,0),"midleft")
        if damgui.place_side().button("decrease_btn","-"): self.cps -= 1
        if damgui.place_side().button("decrease_btn2","-10"): self.cps -= 10
        if damgui.place_side().button("increase_btn2","+10"): self.cps += 10
        if damgui.place_side().button("increase_btn","+"): self.cps += 1
        # toggle key
        damgui.label("toggle_l",f"Toggle Key",(0,0),"midleft")
        if damgui.place_side().button("toggle_btn",self.toggle_name,(150,30)):
            self.toggle_name = "Press a key"
            self.listening_key = True
        # enabled
        damgui.label("active_l",f"Enabled")
        if damgui.place_side().checkbox("active_cb",(33,33)): self.enabled = True
        else: self.enabled = False; self.running = False
        # start stop
        if not self.running and self.enabled:
            settings.ELEMENT_BG_COL = (0,120,0)
            settings.ELEMENT_HOVER_COL = (0,150,0)
        if damgui.button("start_btn","Start") and self.enabled:
            self.running = True
        settings.ELEMENT_BG_COL = settings.defaults["ELEMENT_BG_COL"]
        settings.ELEMENT_HOVER_COL = settings.defaults["ELEMENT_HOVER_COL"]
        if self.running:
            settings.ELEMENT_BG_COL = (120,0,0)
            settings.ELEMENT_HOVER_COL = (150,0,0)
        if damgui.place_side().button("stop_btn","Stop"):
            self.running = False
        
        settings.reset()
        settings.FONT = settings.FONT_S
        damgui.label("damus_l","By Damus666")
        
        damgui.end()
        damgui.frame_end(self.screen)
    
    def update(self):
        
        self.cooldown = 1000/self.cps
        if not self.listening_key:
            try:
                if (now_pressed:=keyboard.is_pressed(self.toggle_name)) and not self.was_pressing:
                    self.running = not self.running
                self.was_pressing = now_pressed
            except: pass
            
            if self.running:
                if pygame.time.get_ticks()-self.last_press >= self.cooldown:
                    self.last_press = pygame.time.get_ticks()
                    self.mouse_controller.click(Button.left)
                    if self.isdown:
                        #pyautogui.mouseUp()
                        
                        self.isdown = False
                    else:
                        #pyautogui.mouseDown()
                        self.isdown = True
                    
        
        damgui.frame_start()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    damgui.element_data("active_cb")["selected"] = False
                    self.running = False; self.enabled = False
                if self.listening_key:
                    self.toggle_name = pygame.key.name(event.key)
                    self.toggle_key = event.key
                    self.listening_key = False
            damgui.register_event(event)
        self.screen.fill(settings.WINDOW_BG_COL)
        
    def awake(self):
        ...
        
    def quit(self):
        pygame.quit()
        sys.exit()
        
    def run(self):
        while True:
            self.update()
            self.damgui()
            self.clock.tick(FPS)
            pygame.display.update()