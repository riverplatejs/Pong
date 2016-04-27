# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:00:23 2016

@author: joaquin
"""
import pygame, sys, math, time, random, pygame.mixer
pygame.init()

black = 0,0,0
white = (255,255,255)
#Initialize Display
infoObject = pygame.display.Info()
y = infoObject.current_h/2      #Starts in the middle of the screen (same
x = infoObject.current_w - 21 
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_rect = screen.get_rect()
###Score_board###
score1 = 0
score2 = 0
#Sounds
bounce = pygame.mixer.Sound('bounce.wav')
point = pygame.mixer.Sound('point.wav')
win = pygame.mixer.Sound('win.wav')

def scoreboard(score1, score2):
    font = pygame.font.Font(None, 36)
        
    scoreDisplay = "Player 1: "+str(score1)
    score_surf = font.render(scoreDisplay, 1, white)
    score_pos = (0, 0)
    screen.blit(score_surf, score_pos)

    scoreDisplay2 = "Player 2: "+str(score2)
    score_surf2 = font.render(scoreDisplay2, 1, white)
    score_pos2 = (1155, 0)
    screen.blit(score_surf2, score_pos2)

#Racket class
class Racket:
    
    racket_p = pygame.image.load('racket.png')    
    
    def __init__(self,x_start,up_id,down_id):
        self.x_start = x_start
        self.racket = pygame.image.load('racket.png')
        self.pos_racket = self.racket.get_rect()
        self.yspeed = 0
        self.pos_racket.x = self.x_start
        self.pos_racket.y = infoObject.current_h/2 - self.pos_racket.width/2
        self.up_id = up_id
        self.down_id = down_id
    
    
    def key_detection(self):
        if event.type == pygame.KEYDOWN:
            if event.key == self.up_id:
                self.yspeed = -1
                print('keydown')
            elif event.key == self.down_id:
                self.yspeed = 1
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
        self.speed = ((self.xspeed)**2 + (self.yspeed)**2)**(1/2)
        
        self.intersectY = 0
        self.norm_intersectY = 0
        self.bounce_angle = 0                       #Initially set to horizontal bouncing
        
        self.x = self.ball_rect.x                   #Proxy variables to enable position floats
        self.y = self.ball_rect.y
        
        self.last_time1 = 0
        self.diff_time1 = 0
        
        self.last_time2 = 0
        self.diff_time2 = 0
        
        self.bounced = False
        
    def moveBall(self):
        self.x += self.xspeed
        self.y += self.yspeed        
        
        self.ball_rect = self.ball_rect.move(self.x - self.ball_rect.x,self.y - self.ball_rect.y)
        screen.blit(self.ball_surf,self.ball_rect)
                 
            
    def bounce_check(self,racket_num):
        
        #Bouncing against rackets
        self.diff_time1 = int(round(time.time() * 1000)) - self.last_time1 
        if self.ball_rect.colliderect(racket_num.pos_racket) and self.diff_time1 > 1000:  
            
            self.intersectY = ((self.ball_rect.y + self.radius) - (racket_num.pos_racket.y + (racket_num.pos_racket.height)/2))           #Find absolute value of point of intersection relative to origin
            self.norm_intersectY = self.intersectY/(racket_num.pos_racket.height/2)          #Normalize point of intersection
            self.bounce_angle = Ballz.max_bounce_angle * self.norm_intersectY                #Find the scaled bounce angle 
            self.xspeed = math.copysign(self.speed,-1*self.xspeed)*math.cos(abs(math.radians(self.bounce_angle)))
            self.yspeed = math.copysign(self.speed,-self.norm_intersectY)*math.sin(abs(math.radians(self.bounce_angle)))
            self.bounced = True
            self.last_time1 = int(round(time.time() * 1000))
            bounce.play()
            
        #Bouncing against vertical wall sides    
        self.diff_time2 = int(round(time.time() * 1000)) - self.last_time2        
        if (self.y < 0 or self.y + self.ball_rect.height > infoObject.current_h) and self.diff_time2 > 1000:
            
            self.yspeed = self.yspeed * -1
            self.bounced = True
            self.last_time2 = int(round(time.time() * 1000)) 
        
    def check_bounds(self):
        global score1
        global score2        
        
        if self.ball_rect.x < 0:
            self.new_ball()
            score2 += 1
            point.play()
           
        if self.ball_rect.x > infoObject.current_w:
            self.new_ball()
            score1 += 1
            point.play()
            
    def new_ball(self):
        self.x, self.y = infoObject.current_w/2, infoObject.current_h/2
        self.xspeed, self.yspeed = random.choice([1,-1])*random.uniform(1.7,2.0), random.choice([1,-1])*random.uniform(0,1)
        self.speed = ((self.xspeed)**2 + (self.yspeed)**2)**(1/2)


ball1 = Ballz(1.2,0,6)                  
           
#Initialize rackets
racket1 = Racket(0,pygame.K_w,pygame.K_s)
racket2 = Racket(infoObject.current_w - Racket.racket_p.get_width(),pygame.K_UP,pygame.K_DOWN)

pygame.key.set_repeat(7,7)

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
    ball1.check_bounds()
        
    #Update screen
    ball1.bounce_check(racket1)
    ball1.bounce_check(racket2)
    
    scoreboard(score1, score2)
       
    pygame.display.flip()































        