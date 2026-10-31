import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("../resources/images/player.png").convert_alpha()
        self.rect = self.image.get_frect(center = (win_width // 2, win_height // 2))
        self.direction = pygame.Vector2()
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print('fire')


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, Surf):
        super().__init__(groups)
        self.image = Surf
        self.rect = self.image.get_frect(center = (randint(0,win_width),randint(0,win_height)))


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

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load("../resources/images/star.png").convert_alpha() 
for i in range(20):
    Star(all_sprites, star_surf)
Player = Player(all_sprites)


 
meteor_surf = pygame.image.load("../resources/images/meteor.png").convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (win_width // 2, win_height // 2))

laser_surf = pygame.image.load("../resources/images/laser.png").convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20, win_height - 20 ))


while running:
    dt = clock.tick()/1000
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
   
     # updates 
    all_sprites.update(dt)



    #draw the game 
    display_window.fill("gray")
   
    all_sprites.draw(display_window)



    pygame.display.update()
pygame.quit()





















































    # for pos in star_positions: 
    #     display_window.blit(star, pos )

# star = pygame.image.load("../resources/images/star.png").convert_alpha()
# star_positions = [(randint(0,win_width),randint(0,win_height)) for i in range(20)]

    # display_window.blit(meteor_surf, meteor_rect)
    # display_window.blit(laser_surf, laser_rect)

 # player movement
    # display_window.blit(player_surf, player_rect.topleft)
    # display_window.blit(Player.image, Player.rect)  bad way to display a sprite


   # input  
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # player_direction = player_direction.normalize() if player_direction else player_direction
    # player_rect.center += player_direction * player_speed * dt

    # recent_keys = pygame.key.get_just_pressed()
    # if recent_keys[pygame.K_SPACE]:
    #     print('fire')


# all_sprites.add(Player) not needed cause we used the when we initialized the class with group
#importing image
# player_surf = pygame.image.load("../resources/images/player.png").convert_alpha()
# player_rect = player_surf.get_frect(center = (win_width // 2, win_height // 2))
# player_direction = pygame.math.Vector2()
# player_speed = 300


 # adding key controls practice for learning purpose  
        # if  event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

        #input
        # print(pygame.mouse.get_rel())

# player_rect.x += player_direction * 0.4
    # if player_rect.right > win_width or player_rect.left < 0 :
    #     player_direction *= -1
    # dvd movement (for fun)
    # if player_rect.bottom > win_height or player_rect.top < 0 :
    #     player_direction.y *= -1
    # if player_rect.right > win_width or player_rect.left < 0:
    #         player_direction.x *= -1