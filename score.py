# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:09:05 2016

@author: ryanlukomski
"""

score1 = 0
score2 = 0

def scoreboard(score):
    font = pygame.font.Font(None, 36)
        
    scoreDisplay = "Player 1: "+str(score)
    score_surf = font.render(scoreDisplay, 1, white)
    score_pos = (0, 0)
    screen.blit(score_surf, score_pos)

    scoreDisplay2 = "Player 2: "+str(score)
    score_surf2 = font.render(scoreDisplay2, 1, white)
    score_pos2 = (1155, 0)
    screen.blit(score_surf2, score_pos2)

        
    pygame.display.flip()
    
scoreboard(score1)
scoreboard(score2)