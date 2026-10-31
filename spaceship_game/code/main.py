import pygame
from random import randint, uniform
from os.path import join


# ============================================================
# PLAYER SPRITE
# ============================================================

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # Load the player image.
        # convert_alpha() preserves transparency.
        self.image = pygame.image.load(
            "../resources/images/player.png"
        ).convert_alpha()

        # Position the player at the center of the window.
        self.rect = self.image.get_frect(
            center=(win_width // 2, win_height // 2)
        )

        # Vector2 stores movement along the X and Y axes.
        self.direction = pygame.Vector2()

        # Movement speed in pixels per second.
        self.speed = 300

        # Shooting cooldown variables.
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400  # Milliseconds

        # ----------------------------------------------------
        # TRANSFORM
        # Space reserved for experimenting with transformations.
        # Examples: scaling, rotation, and flipping.
        # ----------------------------------------------------

        # A mask represents the opaque pixels of the player.
        # It can be used for pixel-perfect collision detection.
        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self):
        # Only check the timer when shooting is on cooldown.
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()

            # get_ticks() returns elapsed milliseconds since
            # pygame.init() was called.
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        # Check which keys are currently being held.
        keys = pygame.key.get_pressed()

        # Calculate movement direction.
        # Right = +1, Left = -1.
        self.direction.x = (
            int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        )

        # Down = +1, Up = -1.
        self.direction.y = (
            int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        )

        # Normalize the direction to prevent faster diagonal movement.
        # A normalized vector has a length of 1.
        self.direction = (
            self.direction.normalize()
            if self.direction
            else self.direction
        )

        # Move according to direction, speed, and elapsed time.
        # dt makes movement independent of the frame rate.
        self.rect.center += self.direction * self.speed * dt

        # Check for keys pressed during the current frame.
        recent_keys = pygame.key.get_just_pressed()

        # Fire a laser when Space is pressed.
        if recent_keys[pygame.K_SPACE]:
            Laser(
                laser_surf,
                self.rect.midtop,
                (all_sprites, laser_sprites)
            )

            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

            # Play the laser sound effect.
            laser_sound.play()

        # Update the shooting cooldown.
        self.laser_timer()


# ============================================================
# STAR SPRITE
# ============================================================

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, Surf):
        super().__init__(groups)

        self.image = Surf

        # Place each star at a random position in the window.
        self.rect = self.image.get_frect(
            center=(
                randint(0, win_width),
                randint(0, win_height)
            )
        )


# ============================================================
# LASER SPRITE
# ============================================================

class Laser(pygame.sprite.Sprite):
    def __init__(self, Surf, pos, groups):
        super().__init__(groups)

        self.image = Surf

        # Place the laser so its bottom-center aligns with pos.
        # This makes it appear directly above the player's ship.
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, dt):
        # Move the laser upward at 400 pixels per second.
        self.rect.centery -= 400 * dt

        # Remove the laser once it leaves the top of the window.
        if self.rect.bottom < 0:
            self.kill()


# ============================================================
# METEOR SPRITE
# ============================================================

class Meteor(pygame.sprite.Sprite):
    def __init__(self, Surf, pos, groups):
        super().__init__(groups)

        # Keep the original image so rotations don't repeatedly
        # transform an already-rotated image.
        self.original_Surf = Surf
        self.image = Surf

        # Set the meteor's initial position.
        self.rect = self.image.get_frect(center=pos)

        # Track how long the meteor has existed.
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000  # Milliseconds

        # Give the meteor a direction with a random horizontal
        # component and a downward vertical component.
        self.direction = pygame.Vector2(
            uniform(-0.5, 0.5), 1
        )

        # Randomize the meteor's movement speed.
        self.speed = randint(400, 500)

        # Rotation settings.
        self.rotation_speed = randint(40, 80)
        self.rotation = 0

    def update(self, dt):
        # Move the meteor using its direction and speed.
        self.rect.center += self.direction * self.speed * dt

        # Remove the meteor after its lifetime expires.
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()

        # Continuously rotate the meteor.
        self.rotation += self.rotation_speed * dt

        # Rotate the original image by the current angle.
        self.image = pygame.transform.rotozoom(
            self.original_Surf,
            self.rotation,
            1
        )

        # Rotation can change an image's dimensions.
        # Recreate the rectangle while keeping the meteor centered.
        self.rect = self.image.get_frect(center=self.rect.center)


# ============================================================
# ANIMATED EXPLOSION SPRITE
# ============================================================

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)

        # Store all images used in the explosion animation.
        self.frames = frames

        # Start at the first frame.
        self.frames_index = 0

        self.image = self.frames[self.frames_index]

        # Position the explosion at the specified coordinates.
        self.rect = self.image.get_frect(center=pos)

        # Play the explosion sound when the animation is created.
        explosion_sound.play()

    def update(self, dt):
        # Advance through the animation at 20 frames per second.
        # Using dt keeps the animation speed independent of FPS.
        self.frames_index += 20 * dt

        # Display the current animation frame.
        if self.frames_index < len(self.frames):
            self.image = self.frames[int(self.frames_index)]

        else:
            # Remove the explosion after the last frame.
            self.kill()


# ============================================================
# COLLISION DETECTION
# ============================================================

def collisions():
    global running

    # Check whether the player collides with a meteor.
    # collide_mask checks opaque pixels instead of just rectangles.
    #
    # The True argument removes collided meteor sprites.
    collision_sprites = pygame.sprite.spritecollide(
        player,
        meteor_sprites,
        True,
        pygame.sprite.collide_mask
    )

    # End the game if the player hits a meteor.
    if collision_sprites:
        running = False

    # Check each laser against the meteor group.
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(
            laser,
            meteor_sprites,
            True
        )

        # If a laser hits a meteor, remove the laser and
        # create an explosion at the laser's position.
        if collided_sprites:
            laser.kill()

            AnimatedExplosion(
                explosion_frames,
                laser.rect.midtop,
                all_sprites
            )


# ============================================================
# SCORE DISPLAY
# ============================================================

def display_score():
    # Convert elapsed milliseconds into a score-like counter.
    current_time = pygame.time.get_ticks() // 100

    # Render the number as a text surface.
    text_surf = font.render(
        str(current_time),
        True,
        "#76e5c6"
    )

    # Position the text near the bottom-center of the window.
    text_rect = text_surf.get_frect(
        midbottom=(win_width / 2, win_height - 50)
    )

    # Draw the score.
    display_window.blit(text_surf, text_rect)

    # Draw a border around the score.
    # inflate() expands the rectangle.
    # move() shifts the rectangle.
    pygame.draw.rect(
        display_window,
        (240, 230, 230),
        text_rect.inflate(20, 10).move(0, -8),
        5,
        10
    )


# ============================================================
# GENERAL GAME SETUP
# ============================================================

pygame.init()

win_width, win_height = 1280, 720

# Create the game window.
display_window = pygame.display.set_mode(
    (win_width, win_height)
)

pygame.display.set_caption("Space Shooter ")

running = True

# Clock tracks time between frames.
clock = pygame.time.Clock()


# ============================================================
# LOAD GAME ASSETS
# ============================================================

# Load images.
star_surf = pygame.image.load(
    "../resources/images/star.png"
).convert_alpha()

meteor_surf = pygame.image.load(
    "../resources/images/meteor.png"
).convert_alpha()

laser_surf = pygame.image.load(
    "../resources/images/laser.png"
).convert_alpha()

# Load the font used for the score.
font = pygame.font.Font(
    "../resources/images/Oxanium-Bold.ttf",
    40
)

# Load the 21 images used for the explosion animation.
# join() combines path components using the correct separator.
explosion_frames = [
    pygame.image.load(
        join("..", "resources", "images", "explosion", f"{i}.png")
    ).convert_alpha()
    for i in range(21)
]


# ============================================================
# LOAD AUDIO
# ============================================================

laser_sound = pygame.mixer.Sound(
    "../resources/audio/laser.wav"
)
laser_sound.set_volume(0.5)

explosion_sound = pygame.mixer.Sound(
    "../resources/audio/explosion.wav"
)
explosion_sound.set_volume(0.5)

# Example of loading another sound effect.
# damage_sound = pygame.mixer.Sound("../resources/audio/damage.ogg")

# Background music.
game_music = pygame.mixer.Sound(
    "../resources/audio/game_music.wav"
)
game_music.set_volume(0.5)

# loops=-1 means the music repeats indefinitely.
game_music.play(loops=-1)


# ============================================================
# CREATE SPRITE GROUPS
# ============================================================

# all_sprites contains the sprites that should be updated and drawn.
all_sprites = pygame.sprite.Group()

# These groups allow us to handle specific sprite types separately.
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

# Create 20 stars and add them to all_sprites.
for i in range(20):
    Star(all_sprites, star_surf)

# Create the player.
player = Player(all_sprites)


# ============================================================
# CUSTOM METEOR SPAWNING EVENT
# ============================================================

# Create a custom event that pygame can trigger.
meteor_event = pygame.event.custom_type()

# Trigger the event every 500 milliseconds.
pygame.time.set_timer(meteor_event, 500)


# ============================================================
# MAIN GAME LOOP
# ============================================================

while running:

    # Get the time elapsed since the previous frame.
    # tick() returns milliseconds; divide by 1000 for seconds.
    dt = clock.tick() / 1000

    # --------------------------------------------------------
    # EVENT HANDLING
    # --------------------------------------------------------

    for event in pygame.event.get():

        # Handle the window's close button.
        if event.type == pygame.QUIT:
            running = False

        # Spawn a meteor whenever the custom event occurs.
        if event.type == meteor_event:

            # Random horizontal position.
            # Negative Y places the meteor above the window.
            x, y = (
                randint(0, win_width),
                randint(-200, -100)
            )

            # Add the meteor to both groups.
            Meteor(
                meteor_surf,
                (x, y),
                (all_sprites, meteor_sprites)
            )

    # --------------------------------------------------------
    # UPDATE SPRITES AND CHECK COLLISIONS
    # --------------------------------------------------------

    # Calls update(dt) on every sprite in all_sprites.
    all_sprites.update(dt)

    # Check player-meteor and laser-meteor collisions.
    collisions()

    # --------------------------------------------------------
    # DRAW THE FRAME
    # --------------------------------------------------------

    # Clear the previous frame.
    display_window.fill("#3a2e3f")

    # Draw the score.
    display_score()

    # Draw every sprite in all_sprites.
    all_sprites.draw(display_window)

    # Present the completed frame.
    pygame.display.update()

# Exit pygame after the main loop ends.
pygame.quit()


# ============================================================
# LEARNING NOTES: PYGAME CONCEPTS AND EXPERIMENTS
# ============================================================
#
# These examples are commented out intentionally.
# Uncomment an example when you want to experiment with it.
#
# IMPORTANT:
# Some examples below are alternatives to the implementation
# above. Don't uncomment all of them at once.
#
# ============================================================
# 1. RECTANGLES AND POSITIONING
# ============================================================
#
# get_frect() creates a floating-point rectangle.
# Floating-point coordinates allow smoother movement.
#
# meteor_rect = meteor_surf.get_frect(
#     center=(win_width // 2, win_height // 2)
# )
#
# laser_rect = laser_surf.get_frect(
#     bottomleft=(20, win_height - 20)
# )
#
# Common rectangle anchors:
# rect.center      -> center of the rectangle
# rect.topleft     -> top-left corner
# rect.midtop      -> middle of the top edge
# rect.midbottom   -> middle of the bottom edge
# rect.bottomleft  -> bottom-left corner
#
# The anchor passed to get_frect() determines which part of
# the image is placed at the supplied coordinates.


# ============================================================
# 2. CREATING AND FILLING A SURFACE
# ============================================================
#
# A Surface is an image-like area that can be drawn onto.
# You can create one without loading an image from a file.
#
# surf = pygame.Surface((100, 200))
# surf.fill("aquamarine")
#
# x = 100
#
# To display the surface:
#
# display_window.blit(surf, (100, 100))
#
# blit() draws one surface onto another surface.


# ============================================================
# 3. LOADING AND DISPLAYING IMAGES
# ============================================================
#
# Load an image from a file:
#
# player_surf = pygame.image.load(
#     "../resources/images/player.png"
# ).convert_alpha()
#
# convert_alpha() preserves transparency.
#
# Create a rectangle for positioning:
#
# player_rect = player_surf.get_frect(
#     center=(win_width // 2, win_height // 2)
# )
#
# Draw the image:
#
# display_window.blit(player_surf, player_rect)
#
# Alternative:
#
# display_window.blit(player_surf, player_rect.topleft)
#
# A sprite's image and rectangle belong to the sprite instance.
# For example, player.image and player.rect refer to the actual
# player sprite's image and position.


# ============================================================
# 4. DISPLAYING MULTIPLE STARS USING RANDOM POSITIONS
# ============================================================
#
# Load the star image:
#
# star = pygame.image.load(
#     "../resources/images/star.png"
# ).convert_alpha()
#
# Generate 20 random positions:
#
# star_positions = [
#     (randint(0, win_width), randint(0, win_height))
#     for i in range(20)
# ]
#
# Draw every star:
#
# for pos in star_positions:
#     display_window.blit(star, pos)
#
# This approach uses positions and blit().
# The Star class in the main implementation uses sprites instead.


# ============================================================
# 5. MOVING AN OBJECT WITH A VECTOR
# ============================================================
#
# Create a movement vector:
#
# player_direction = pygame.Vector2()
# player_speed = 300
#
# Check the keyboard:
#
# keys = pygame.key.get_pressed()
#
# player_direction.x = (
#     int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
# )
#
# player_direction.y = (
#     int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
# )
#
# Normalize the vector to prevent faster diagonal movement:
#
# player_direction = (
#     player_direction.normalize()
#     if player_direction
#     else player_direction
# )
#
# Apply movement:
#
# player_rect.center += player_direction * player_speed * dt
#
# Vector2 stores X and Y together.
# This is why rect.center can be updated using a Vector2,
# while rect.centery must be updated using a single number.


# ============================================================
# 6. CHECKING KEY PRESSES
# ============================================================
#
# Check whether a key is currently held:
#
# keys = pygame.key.get_pressed()
#
# if keys[pygame.K_RIGHT]:
#     print("Right key is being held")
#
# Check whether a key was pressed during the current frame:
#
# recent_keys = pygame.key.get_just_pressed()
#
# if recent_keys[pygame.K_SPACE]:
#     print("Space was pressed")
#
# Difference:
# get_pressed() checks the current held state.
# get_just_pressed() detects a new press during the current frame.
#
# These functions belong in the main update logic, not inside
# the event loop if you need to check input continuously.


# ============================================================
# 7. HANDLING KEYBOARD AND MOUSE EVENTS
# ============================================================
#
# Inside the event loop, you can respond to individual events.
#
# for event in pygame.event.get():
#
#     if event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_1:
#             print("The 1 key was pressed")
#
#     if event.type == pygame.MOUSEMOTION:
#         player_rect.center = event.pos
#
# KEYDOWN detects a key-press event.
# MOUSEMOTION detects mouse movement.
# event.pos contains the mouse coordinates for that event.


# ============================================================
# 8. READING RELATIVE MOUSE MOVEMENT
# ============================================================
#
# pygame.mouse.get_rel() returns the mouse's relative movement
# since the previous call.
#
# print(pygame.mouse.get_rel())
#
# The result is a pair of values: (movement_x, movement_y).
# Unlike the mouse position, these values describe movement
# rather than absolute screen coordinates.


# ============================================================
# 9. MOVING A RECTANGLE DIRECTLY
# ============================================================
#
# This is NOT valid when player_direction is a Vector2:
#
# player_rect.x += player_direction * 0.4
#
# rect.x is a single number, but player_direction contains
# both X and Y components.
#
# To update one axis, use the corresponding vector component:
#
# player_rect.x += player_direction.x * player_speed * dt
# player_rect.y += player_direction.y * player_speed * dt
#
# Alternatively, update both axes together:
#
# player_rect.center += player_direction * player_speed * dt


# ============================================================
# 10. BOUNCING AN OBJECT OFF THE WINDOW EDGES
# ============================================================
#
# Reverse the horizontal direction when the object hits
# either the left or right edge:
#
# if player_rect.right > win_width or player_rect.left < 0:
#     player_direction.x *= -1
#
# Reverse the vertical direction when the object hits
# either the top or bottom edge:
#
# if player_rect.bottom > win_height or player_rect.top < 0:
#     player_direction.y *= -1
#
# This creates a simple bouncing effect.
# It is an alternative movement experiment, not part of
# the current player movement implementation.


# ============================================================
# 11. CREATING A SPRITE AND ADDING IT TO A GROUP
# ============================================================
#
# Example:
#
# class ExampleSprite(pygame.sprite.Sprite):
#     def __init__(self, groups):
#         super().__init__(groups)
#
# When you instantiate this class:
#
# example = ExampleSprite(all_sprites)
#
# super().__init__(groups) registers the sprite in the group.
# You do not need to add the class itself:
#
# all_sprites.add(ExampleSprite)  # Incorrect
#
# Groups contain sprite instances, not sprite classes.
#
# The group can then call update() on its sprites and draw
# their images using their rectangles.


# ============================================================
# 12. DRAWING A SPRITE
# ============================================================
#
# A sprite group can draw every sprite it contains:
#
# all_sprites.draw(display_window)
#
# This uses each sprite's image and rect.
#
# You can also draw an individual sprite manually:
#
# display_window.blit(player.image, player.rect)
#
# Here, player is the Player instance.
# Player.image and Player.rect would refer to class attributes
# instead, which is not how this sprite stores its data.


# ============================================================
# 13. CUSTOM EVENTS AND TIMERS
# ============================================================
#
# Create a custom event:
#
# meteor_event = pygame.event.custom_type()
#
# Trigger it every 500 milliseconds:
#
# pygame.time.set_timer(meteor_event, 500)
#
# Handle it in the event loop:
#
# if event.type == meteor_event:
#     print("Spawn a meteor")
#
# This lets pygame schedule repeated events without requiring
# you to manually count frames.
#
# To stop the timer:
#
# pygame.time.set_timer(meteor_event, 0)


# ============================================================
# 14. FRAME-RATE-INDEPENDENT MOVEMENT
# ============================================================
#
# Get elapsed time in seconds:
#
# dt = clock.tick() / 1000
#
# Move an object:
#
# rect.centerx += speed * dt
#
# If speed is 300 pixels per second and dt is 0.016 seconds,
# the object moves approximately 4.8 pixels during that frame.
#
# Using dt helps keep movement consistent across frame rates.
#
# clock.tick(60) can be used instead to limit the game to
# approximately 60 frames per second.


# ============================================================
# 15. SPRITE COLLISION DETECTION
# ============================================================
#
# Rectangle-based collision:
#
# collided_sprites = pygame.sprite.spritecollide(
#     laser,
#     meteor_sprites,
#     True
# )
#
# This checks rectangle overlap.
# The True argument removes collided sprites from the group.
#
# Pixel-mask collision:
#
# collided_sprites = pygame.sprite.spritecollide(
#     player,
#     meteor_sprites,
#     True,
#     pygame.sprite.collide_mask
# )
#
# Mask collision checks the opaque pixels of the sprites.
# It can be more precise than rectangle-based collision.
#
# A sprite's mask can be created using:
#
# self.mask = pygame.mask.from_surface(self.image)


# ============================================================
# 16. ROTATING AN IMAGE
# ============================================================
#
# Rotate a surface:
#
# rotated_image = pygame.transform.rotate(original_image, angle)
#
# Rotate and scale a surface:
#
# transformed_image = pygame.transform.rotozoom(
#     original_image,
#     angle,
#     scale
# )
#
# Example:
#
# rotated_image = pygame.transform.rotozoom(
#     meteor_surf,
#     45,
#     1
# )
#
# The final argument is the scale factor.
# A value of 1 keeps the original scale.
#
# Keep the original surface when rotating repeatedly to avoid
# accumulating transformations on an already-transformed image.
#
# Rotation may change the surface dimensions, so update the
# rectangle while preserving its center:
#
# rect = rotated_image.get_frect(center=rect.center)


# ============================================================
# 17. ANIMATING WITH A LIST OF IMAGES
# ============================================================
#
# Load animation frames:
#
# frames = [
#     pygame.image.load(
#         join("..", "resources", "images", "explosion", f"{i}.png")
#     ).convert_alpha()
#     for i in range(21)
# ]
#
# Track the current frame:
#
# frame_index = 0
#
# Advance the animation:
#
# frame_index += 20 * dt
#
# Display the current frame:
#
# image = frames[int(frame_index)]
#
# Stop the animation when the index reaches the number of frames:
#
# if frame_index >= len(frames):
#     print("Animation finished")
#
# This is the basic principle behind AnimatedExplosion.
```