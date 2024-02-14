import pygame
import random

pygame.init()

screen_x = 500
screen_y = 800

platform_width = 70
platform_height = 18

player_width = 50
player_height = 49

screen = pygame.display.set_mode([screen_x, screen_y]) 
pygame.display.set_caption("Doodle jump")
framerate = 144

done = False

# Set up classes for sprites
class Platform(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, platform_type, platform_data):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.platform_data = platform_data
        self.direction = 1
        self.visible = False
        self.platform_free_to_move = False

        # Used for when platform is off screen
        self.old_x = x
        
        if platform_type == "static":
            # Normal platform type
            platform_image = pygame.image.load("img/platform_static.png")
        elif platform_type == "broken":
            # Platform that breaks when you stand on it
            platform_image = pygame.image.load("img/platform_broken.png")
        elif platform_type == "horizontal":
            # Platform that moves horizontally
            platform_image = pygame.image.load("img/platform_horizontal.png")
        elif platform_type == "vertical":
            # Platform that moves vertically
            platform_image = pygame.image.load("img/platform_vertical.png")
        elif platform_type == "vanishing":
            # Platform that vanishes when you step on it
            platform_image = pygame.image.load("img/platform_vanishing.png")
        elif platform_type == "explosive":
            # Platform that explodeds over a timer
            platform_image = pygame.image.load("img/platform_explosive_stage0.png")

        (width, height) = platform_image.get_size()
        self.image = pygame.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))
        
        self.image.blit(platform_image, (0,0))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y

    def GetPosition(self):
        position = []
        position.append(self.rect.top)
        position.append(self.rect.left)
        position.append(self.rect.bottom)
        position.append(self.rect.right)
        position.append(self.rect.centerx)
        position.append(self.rect.centery)

        return position

    def MovePlatform(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def Draw(self):
        if self.visible:
            self.screen.blit(self.image, self.rect)

    def GetData(self):
        return self.platform_data

    def GetDirection(self):
        return self.direction

    def SetDirection(self, direction):
        self.direction = direction

    def SetVisibility(self, visibility):
        self.visible = visibility

        if not self.visible:
            self.rect.centerx = -200
        elif not self.platform_free_to_move:
             # This shows that the platform is free to move
            self.platform_free_to_move = True
            self.rect.centerx = self.old_x

    def GetVisibility(self):
        return self.visible

        

class PlatformGenerator:
    def __init__(self):
        
        self.difficulty = 1
        self.platform_list = []
        self.difficulty_levels = 3
        self.biomes_per_difficulty = 20
        self.last_platform_y = 0

    def Generate(self):
        for i in range(self.difficulty_levels):
            for x in range(self.biomes_per_difficulty):

                # Now generate a large set of 'biomes' and return the array of platforms
                static_chance = ["static_biome"]*5
                horizontal_chance = ["horizontal_biome"]*1

                biome_types = static_chance
                biome_types.extend(horizontal_chance)
                
                biome_to_add = random.choice(biome_types)

                if biome_to_add == "static_biome":
                    biome_data = self.static_biome(random.randint(20, 100))
                elif biome_to_add == "horizontal_biome":
                    biome_data = self.horizontal_biome(random.randint(10, 15))

                self.platform_list.extend(biome_data)

                self.platform_list.append({"x": random.randint(0, screen_x-platform_width), "y": self.last_platform_y, "type": "vertical", "horizontal_velocity": 0 })

            self.difficulty += 1


        return self.platform_list

    def static_biome(self, biome_length):
        # Define chances of platforms being added to the list
        static_chance = ["static"]*20
        broken_chance = ["broken"]*3
        horizontal_chance = ["horizontal"]*2

        platform_types = static_chance
        platform_types.extend(broken_chance)
        platform_types.extend(horizontal_chance)

        biome_data = []
        for i in range(biome_length):
            # Store the y coordinate of the last platform
            self.last_platform_y += platform_height*4*self.difficulty

            h_velocity = 0

            # Choose platform to add
            platform_to_add = random.choice(platform_types)
            if platform_to_add == "horizontal": 
                h_velocity = self.difficulty
            # Make broken platforms move at random
            if platform_to_add == "broken": 
                h_velocity = random.randint(0, self.difficulty)

            platform_data = {
                "x": random.randint(0, screen_x-platform_width),
                "y": self.last_platform_y,
                "type": platform_to_add,
                "horizontal_velocity": h_velocity
            }

            biome_data.append(platform_data)

        return biome_data

    def horizontal_biome(self, biome_length):
        biome_data = []
        for i in range(biome_length):
            # Store the y coordinate of the last platform
            self.last_platform_y += platform_height*4*self.difficulty

            platform_data = {
                "x": random.randint(0, screen_x-platform_width),
                "y": self.last_platform_y,
                "type": "horizontal",
                "horizontal_velocity": self.difficulty
            }

            biome_data.append(platform_data)
        return biome_data

    def explosive_biome(self, biome_length):
        pass



        


# Player class used for the doodle jump sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        self.screen = screen

        self.direction = "facing_left"
        
        pygame.sprite.Sprite.__init__(self)
        self.player_image = pygame.image.load("img/player_default.png")

        (width, height) = self.player_image.get_size()
        self.image = pygame.Surface([width, height])
        self.image.set_colorkey((0, 0, 0))
        pygame.transform.scale(self.image, (100, 100))
        
        self.image.blit(self.player_image, (0, 0))
        self.rect = self.image.get_rect()
        
        
        self.rect.x = x
        self.rect.y = y

    # Setter function to change position based on change in x / y
    def MovePlayer(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # Getter function to retrieve the position in pixels of the player sprite
    def GetPosition(self):
        position = []
        position.append(self.rect.top)
        position.append(self.rect.left)
        position.append(self.rect.bottom)
        position.append(self.rect.right)
        position.append(self.rect.centerx)
        position.append(self.rect.centery)

        return position

    def SetPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def Draw(self):
        if self.direction == "facing_left":
            self.screen.blit(self.player_image, self.rect)
        elif self.direction == "facing_right":
            self.screen.blit(pygame.transform.flip(self.player_image, True, False), self.rect)

    def ChangeDirection(self, sprite):
        self.direction = sprite

    def GetDirection(self):
        return self.direction
            

# Initialise sounds that will be used in the game
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
# fall_sound = pygame.mixer.Sound("sounds/fall_sound.wav")
break_sound = pygame.mixer.Sound("sounds/break_sound.wav")

# Apply the backgroud to the pygame window
background = pygame.image.load("img/background.png").convert()

# Instanciate player class
player = Player(100, screen_y-200, screen)

# Instanciate and create platform sprites
# Create base platforms
platform_list = []
platforms_active = []
# Now, using the generator class create a level
generator = PlatformGenerator()
platform_data = generator.Generate()

for i in platform_data:
    # Create an list of platforms
    plt = Platform(screen, i["x"], screen_y-i["y"], i["type"], i)
    platform_list.append(plt)

    # Every platform is invisible to start with
    #platform_list[-1].SetVisibility(False)



# Fall variable to show if the sprite is falling or not
fall_velocity = 0
gravity_value = 0.5
time_falling  = 0
jump_velocity = 0
fall_velocity = 0
previous_y_coord = 0
falling = 0

# Store the current score (y position of the lowest platform)
score = abs(platform_list[0].GetPosition()[5])

# Stop drawing all platfroms out of range
for i in platform_list:
    y_value = i.GetData()["y"]
    if y_value > score+screen_y:
            i.SetVisibility(False)
            # Preform a linear search to remove the platforms not on screen from the active platforms
            try:
                platforms_active.remove(i)
            except ValueError:
                pass

while not done:
    player_pos = player.GetPosition()
    player_direction = player.GetDirection()

    # This is used to determine if the player is falling or not
    if previous_y_coord < player_pos[5]:
        falling = 1
    else:
        falling = 0
    previous_y_coord = player_pos[5]

    # Nested loop for hit detection, in terms of this game we only need
    # two types of detection, top of the platform and if the player and sprites touch anywhere
    for platforms in platforms_active:
        platform = platforms.GetPosition()

        # Now check for block below the sprite and if there is none, apply gravity            
        if platform[4]-(platform_width/2)-(player_width/3) <= player_pos[4] <= platform[4]+(platform_width/2)+(player_width/3) and platform[5]-(platform_height/2)-(player_height/2) <= player_pos[5] <= platform[5] and falling:

            # Check if the player should fall through the platform (Stepped on broken platform)
            if platforms.GetData()["type"] == "broken":
                platforms_active.remove(platforms)
                break_sound.play()
            else:
                jump_sound.play()
                fall_velocity = 0
                jump_velocity = 5
    

    # This section is for special platforms
    # Move horizontal platforms
    for platform in platforms_active:
        data = platform.GetData()
        pos = platform.GetPosition()
        if data["horizontal_velocity"]:
            direction = platform.GetDirection()
            platform.MovePlatform(direction*data["horizontal_velocity"], 0)
            if pos[4] > screen_x-platform_width/2:
                platform.SetDirection(-1)
            elif pos[4] < platform_width/2:
                platform.SetDirection(1)



    # Loop to detect window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Loop to move the sprite on key press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.MovePlayer(-5, 0)
        player.ChangeDirection("facing_left")
    if keys[pygame.K_d]:
        player.MovePlayer(5, 0)
        player.ChangeDirection("facing_right")

    # Move sprite according to gravity
    player.MovePlayer(0, fall_velocity-jump_velocity)

    if time_falling%(framerate/9) == 0:
        fall_velocity += gravity_value
        if jump_velocity:
            jump_velocity -= gravity_value
        
    if fall_velocity or jump_velocity:
        time_falling += 1


    # Move platforms so that player is always in the middle of the screen
    if player_pos[5] < (screen_y/8)*5:
        player.MovePlayer(0, 2)
        for i in platform_list:
            i.MovePlatform(0, 2)
        score += 2

    for i in platform_list:
        # Check if platform if off screen or coming onto screen, then add to array or remove where appropriate
        y_value = i.GetData()["y"]
        window_y_value = i.GetPosition()[5]

        # Remove all platforms below the screen
        if window_y_value > screen_y+platform_height:
            
            i.SetVisibility(False)



        else:
            # Draw all incoming platforms
            if y_value >= 0 and y_value < score+platform_height*5:
                if not i.GetVisibility():
                    i.SetVisibility(True)

                    # Now add to the platforms_active list
                    platforms_active.append(i)

    

    # Check for deaths
    if player_pos[5] > screen_y+100:
        #fall_sound.play()
        pass

    # If sprite moves too far to the right place them on the left and from right to left
    if player_pos[4] > screen_x and player_direction == "facing_right":
        player.SetPosition(0, player_pos[5])
    elif player_pos[4] < 0 and player_direction == "facing_left":
        player.SetPosition(screen_x, player_pos[5])
    
    # Draw all objects to screen
    screen.blit(background, [0,0])
    player.Draw()
    player.update()
    for i in platforms_active:
        i.Draw()

    pygame.display.flip()
    pygame.time.Clock().tick(framerate)

pygame.quit()
