# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:00:23 2016

@author: joaquin
"""
import pygame, sys, math
pygame.init()

black = 0,0,0
white = (255,255,255)
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
        self.pos_racket.y = infoObject.current_h/2 - self.pos_racket.width
        self.up_id = up_id
        self.down_id = down_id
    
    
    def key_detection(self):
        if event.type == pygame.KEYDOWN:
            if event.key == self.up_id:
                self.yspeed = -2
            elif event.key == self.down_id:
                self.yspeed = 2
        if event.type == pygame.KEYUP:
            if event.key == self.up_id or event.key == self.down_id:
                self.yspeed = 0    
        self.pos_racket.clamp_ip(screen_rect)                                    #Keeps the racket inside the window
                
    def update_position(self):
        self.pos_racket = self.pos_racket.move(0,self.yspeed)
        screen.blit(self.racket, self.pos_racket)
        
    def update(self):
        screen.blit(self.racket, self.pos_racket)

class Ballz:
    
    max_bounce_angle = 30                       #same for all objects
    
    def __init__(self, xspeed, yspeed, radius):
        self.radius = radius
        self.ball_surf = pygame.Surface((2*self.radius,2*self.radius))
        
        self.ball = pygame.draw.circle(self.ball_surf,white,(self.radius,self.radius),self.radius,0)
        
        self.ball_rect = self.ball_surf.get_rect()
        self.ball_rect.center = (infoObject.current_w/2, infoObject.current_h/2)
    
        self.xspeed = xspeed
        self.yspeed = yspeed
        
        self.intersectY = 0
        self.norm_intersectY = 0
        self.bounce_angle = 0                       #Initially set to horizontal bouncing
        
        self.x = self.ball_rect.x                   #Proxy variables to enable position floats
        self.y = self.ball_rect.y

    def moveBall(self):
        self.x += self.xspeed
        self.y += self.yspeed        
        
        self.ball_rect = self.ball_rect.move(self.x - self.ball_rect.x,self.y - self.ball_rect.y)
        screen.blit(self.ball_surf,self.ball_rect)
                 
            
    def bounce_check(self,racket_num):
        if self.ball_rect.colliderect(racket_num.pos_racket):    
            print('collision', racket_num)
#            self.xspeed = self.xspeed * -1
            self.intersectY = abs(((self.ball_rect.y + self.radius) - (racket_num.pos_racket.y + (racket_num.pos_racket.height)/2)))             #Find absolute value of point of intersection relative to origin
            self.norm_intersectY = self.intersectY/(racket_num.pos_racket.height/2)          #Normalize point of intersection
            self.bounce_angle = Ballz.max_bounce_angle * self.norm_intersectY                #Find the scaled bounce angle 
            print(self.intersectY)          
            print(self.bounce_angle)
         
            print(self.ball_rect.y)
            print(racket_num.pos_racket.y)
            print(racket_num.pos_racket.height)
            
            self.xspeed = .5*math.cos(math.radians(self.bounce_angle)) * -1
            self.yspeed = .5*math.sin(math.radians(self.bounce_angle))

            print(self.xspeed)
            print(self.yspeed)
            
        if self.y < 0 or self.y > infoObject.current_h:
            self.yspeed = self.yspeed * -1
#    def windowCollision(ball, ballDirX, ballDirY):
#        if ball.top == (lineThickness) or ball.bottom == (windowHeight - lineThickness):
#            ballDirY = ballDirY * -1
#            if ball.left == (lineThickness) or ball.right == (windowWidth - lineThickness):
#                ballDirX = ballDirX * -1
#                return ballDirX, ballDirY
#   
#    def paddleCollision(ball, PADDLE1, PADDLE2, ballDirX):
#        if ballDirX == -1 and PADDLE1.right == ball.left and PADDLE1.top < ball.top and PADDLE1.bottom > ball.bottom:
#            return -1
#        elif ballDirX == 1 and PADDLE2.left == ball.right and PADDLE2.top < ball.top and PADDLE2.bottom > ball.bottom:
#            return -1
#        else: return 1
        
ball1 = Ballz(.5,0,6)                  
           
#Initialize rackets
racket1 = Racket(0,pygame.K_w,pygame.K_s)
racket2 = Racket(infoObject.current_w - Racket.racket_p.get_width(),pygame.K_UP,pygame.K_DOWN)

pygame.key.set_repeat(2,2)

#Infinite loop to check for user input
while 1: 
   
    screen.fill(black)    
    
    for event in pygame.event.get():
        #Check if window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Check for keyboard input
        racket1.key_detection()
        racket2.key_detection()
        #Erase old images
        
    #Update position
    racket1.update_position()
    racket2.update_position()
    
    ball1.moveBall()
        
    #Update screen
    ball1.bounce_check(racket2)
    ball1.bounce_check(racket1)
    


    pygame.display.flip()































        