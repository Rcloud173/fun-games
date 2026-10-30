import pygame

#general setup guide 
pygame.init()
win_height , win_width = 800,600
display_window = pygame.display.set_mode((win_height, win_width))
running = True

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    #draw the game

pygame.quit()
