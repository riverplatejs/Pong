# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:48:03 2016

@author: joaquin
"""

import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 225)

display_width = 1250
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Pong")

Block_Size = 20
FPS = 15

direction = "right"

smallfont = pygame.font.SysFont("monospace", 25)
medfont = pygame.font.SysFont("monospace", 50)
largefont = pygame.font.SysFont("monospace", 80)
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)

    
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False #change to function of game >> run()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to Pong", blue, -100, size="large")
        message_to_screen("Are you the best Pong player in EK128?", black, -30)
        message_to_screen("Press C to play or Q to quit.", black, 180)
        pygame.display.update()
game_intro()       