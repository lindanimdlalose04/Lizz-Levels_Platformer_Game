import pygame
from pygame.locals import *

pygame.init()

screen_width = 880
screen_height = 650

#this function creates the game window 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lizz Levels") 

#load images
sun_img = pygame.image.load('img/sun.pgn')
backgroung_img = pygame.image.load('img/sky.png')


#the loop which the game runs in
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #closes the game
            run = False  

pygame.quit()#closes the innit 


