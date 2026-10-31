import pygame
from random import randint

#general setup guide 
pygame.init()
win_width , win_height = 1280,720
display_window = pygame.display.set_mode((win_width , win_height))
pygame.display.set_caption("Space Shooter ")
running = True
clock = pygame.time.Clock()

#plain surface
surf = pygame.Surface((100,200))
surf.fill("aquamarine")
x = 100

#importing image
player_surf = pygame.image.load("../resources/images/player.png").convert_alpha()
player_rect = player_surf.get_frect(center = (win_width // 2, win_height // 2))
player_direction = pygame.math.Vector2(1,0)
player_speed = 300


star = pygame.image.load("../resources/images/star.png").convert_alpha()
star_positions = [(randint(0,win_width),randint(0,win_height)) for i in range(20)]

meteor_surf = pygame.image.load("../resources/images/meteor.png").convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (win_width // 2, win_height // 2))

laser_surf = pygame.image.load("../resources/images/laser.png").convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, win_height - 20 ))


while running:
    dt = clock.tick(10)/1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game 
    display_window.fill("gray")
    for pos in star_positions: 
        display_window.blit(star, pos )
    display_window.blit(meteor_surf, meteor_rect)
    display_window.blit(laser_surf, laser_rect)

    # player movement
    # player_rect.x += player_direction * 0.4
    # if player_rect.right > win_width or player_rect.left < 0 :
    #     player_direction *= -1
    player_rect.center += player_direction * player_speed * dt
    display_window.blit(player_surf, player_rect.topleft)

    pygame.display.update()
pygame.quit()
