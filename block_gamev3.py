# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:00:23 2016

@author: joaquin
"""
import pygame, sys
pygame.init()

black = 0,0,0
#Initialize Display
infoObject = pygame.display.Info()
y = infoObject.current_h/2      #Starts in the middle of the screen (same
x = infoObject.current_w - 21 
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_rect = screen.get_rect()

#Racket class
class Racket:
    
    racket_p = pygame.image.load('racket.png')    
    
    def __init__(self,x_start,up_id,down_id):
        self.x_start = x_start
        self.racket = pygame.image.load('racket.png')
        self.pos_racket = self.racket.get_rect()
        self.yspeed = 0
        self.pos_racket.x = self.x_start
        self.pos_racket.y = y
        self.up_id = up_id
        self.down_id = down_id
    
    def key_detection(self):
        if event.type == pygame.KEYDOWN:
            if event.key == self.up_id:
                self.yspeed = -6
            elif event.key == self.down_id:
                self.yspeed = 6
        if event.type == pygame.KEYUP:
            if event.key == self.up_id or event.key == self.down_id:
                self.yspeed = 0    
        self.pos_racket.clamp_ip(screen_rect)                                    #Keeps the racket inside the window
                
    def update_position(self):
        self.pos_racket = self.pos_racket.move(0,self.yspeed)
        screen.blit(self.racket, self.pos_racket)
        
           
           
#Initialize rackets
racket1 = Racket(0,pygame.K_w,pygame.K_s)
racket2 = Racket(infoObject.current_w - Racket.racket_p.get_width(),pygame.K_UP,pygame.K_DOWN)

pygame.key.set_repeat(10,10)

#Infinite loop to check for user input
while 1: 
    for event in pygame.event.get():
        #Check if window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Check for keyboard input
        racket1.key_detection()
        racket2.key_detection()
        #Erase old images
        screen.fill(black)
        #Update position
        racket1.update_position()
        racket2.update_position()
        #Update screen
        pygame.display.flip() 

























        