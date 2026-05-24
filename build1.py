import pygame
from pygame.locals import *

pygame.init()

screen_width = 500
screen_height = 500

#this function creates the game window 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lizz Levels") 

tile_size = 100
#load images
#sun_img = pygame.image.load('img/sun.pgn')
background_img = pygame.image.load('img/sky.jpg')
background_img = pygame.transform.scale(background_img, (1000, 1000))


def draw_grid():
    for line in range(0,6):
        pygame.draw.line(screen, (255,255, 255), (0, line * tile_size), (screen_width, line* tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size,0), (line * tile_size, screen_height))
        

class World():
    def __init__(self,data):
        self.tile_list =[]
        
        #load images
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')

        row_count = 0 
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1: #where the world data has a 1 there will be a dirt image/tile 
                    img =pygame.transform.scale(dirt_img,(tile_size, tile_size)) 
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size #since x coord increases with col count then 
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)   
                    self.tile_list.append(tile)
                if tile == 2: #where the world data has a 2 there will be a dirt image/tile 
                    img =pygame.transform.scale(grass_img,(tile_size, tile_size)) 
                    img_rect = img.get_rect()
                    img_rect.x = col_count*tile_size #since x coord increases with col count then 
                    img_rect.y = row_count*tile_size
                    tile = (img, img_rect)   
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
                

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
        


#world_data = [
#[1,1,1,1,1],
#[1,0,0,0,1],
#[1,0,0,0,1],
#[1,2,2,2,1],
#]

world_data = [
    [1, 1, 1, 1, 1],  # Row 0
    [1, 0, 0, 0, 1],  # Row 1
    [1, 0, 0, 0, 1],  # Row 2
    [1, 0, 0, 0, 1],  # Row 3
    [1, 2, 2, 2, 1]   # Row 4 - added this to complete the grid
]
world = World(world_data)
#the loop which the game runs in
run = True
while run:
    screen.blit(background_img,(0,0))
    #screen.blit(sun_img, (50,70))
    draw_grid()
    world.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #closes the game
            run = False 

    pygame.display.update()

pygame.quit()#closes the innit 


