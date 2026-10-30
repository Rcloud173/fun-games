import pygame
from random import randint

#general setup guide 
pygame.init()
win_width , win_height = 1280,720
display_window = pygame.display.set_mode((win_width , win_height))
pygame.display.set_caption("Space Shooter ")
running = True

#plain surface
surf = pygame.Surface((100,200))
surf.fill("aquamarine")
x = 100

#importing image
player_surf = pygame.image.load("../resources/images/player.png").convert_alpha()
player_rect = player_surf.get_frect(center = (win_width // 2, win_height // 2))

star = pygame.image.load("../resources/images/star.png").convert_alpha()
star_positions = [(randint(0,win_width),randint(0,win_height)) for i in range(20)]

meteor_surf = pygame.image.load("../resources/images/meteor.png").convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (win_width // 2, win_height // 2))


while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game 
    display_window.fill("gray")
    for pos in star_positions:
        display_window.blit(star, pos )
    if player_rect.right < win_width:
        player_rect.left += 0.2
    display_window.blit(player_surf, player_rect)
    display_window.blit(meteor_surf, meteor_rect)
    pygame.display.update()
pygame.quit()
