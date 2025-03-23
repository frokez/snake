import pygame
from sys import exit
import numpy as np
from random import randint

SNAKE_TEXTURE_PATH = 'resources/snake.png'
APPLE_TEXTURE_PATH = 'resources/apple.png'

class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(SNAKE_TEXTURE_PATH).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(APPLE_TEXTURE_PATH).convert_alpha()
        self.rect = self.image.get_rect(topleft = (900,0))
    
    def gen_apple(self):
        global grid

        x,y = self.rect.topleft
        grid[y // 100, x // 100] = 0
        while True:
            applex = randint(0,9)
            appley = randint(0,9)
            # row = y column = x
            if grid[appley,applex] == 0: # check if grid spot is taken by player or apple
                grid[appley,applex] = 2  # replace said place if its emptya
                #convert grid pos to pixel pos
                self.rect.topleft = (applex * 100, appley * 100)  # update sprite position
                break
    
    def update(self):
        self.gen_apple()

def collision_sprite():
    global applecount
    head = list(player.sprites())[0]
    if pygame.sprite.spritecollide(head,apple_group,False):
        apple_group.sprite.update()  # regenerate the apple
        applecount +=1
        grow_snake() # add new segment to snake
        

def grow_snake():
    # Get the last segment of the snake
    last_segment = list(player.sprites())[-1]
    # Determine where the new segment should be placed
    new_x = last_segment.rect.x
    new_y = last_segment.rect.y

    # Create a new segment and add it to the player group
    new_segment =SnakeSegment(new_x,new_y)
    player.add(new_segment)

def update_snake():
    global grid 
    grid.fill(0) #clear grid
    segments = list(player.sprites())

    # update position of last segment to the segment before, e.g. segment 5 : (100,900) segment 6: (100,1000) after update segment 5 : (100,800) segment 6: (100,900)
    for i in range(len(segments) - 1, 0, -1):
        segments[i].rect.topleft = segments[i - 1].rect.topleft
        #update grid for each segment
        grid[segments[i].rect.y // 100, segments[i].rect.x // 100] = 1
    
    head = segments[0]
    if direction == 'left':
        head.rect.x -= 100
    elif direction == 'right':
        head.rect.x += 100
    elif direction == 'up':
        head.rect.y -= 100
    else:
        head.rect.y += 100


def check_self_collision():
    segments = list(player.sprites())
    head = segments[0]  # head
    body = segments[1:]  # rest of the snake

    # Check if the head collides with any segment of the body
    if pygame.sprite.spritecollide(head, body, False):
        pygame.quit()
        exit()

def check_out_of_bounds():
    head = list(player.sprites())[0]
    if head.rect.x < 0 or head.rect.x >= 1000 or head.rect.y < 0 or head.rect.y >= 1000:
        pygame.quit() 
        exit()

 
    



# 0 empty space
# 1 player
# 2 apple




pygame.init()    


size = (10,10)
grid = np.zeros(size)


GRID_SIZE = 1000
CELL_SIZE = 100
screen = pygame.display.set_mode((GRID_SIZE,GRID_SIZE))
clock = pygame.time.Clock()
direction = 'right'
applecount = 0


player = pygame.sprite.Group()
player.add(SnakeSegment(0,0))

apple_group = pygame.sprite.GroupSingle()
apple_group.add(Apple())

TICKRATE = 40
GAME_FRAMERATE = 5

frameCounter = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()


    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] or keys[pygame.K_UP]) and direction != 'down':
        direction = 'up'
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and direction != 'left':
        direction = 'right'
    elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and direction != 'right':
        direction = 'left'
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and direction != 'up':
        direction = 'down'

    if (frameCounter == TICKRATE/GAME_FRAMERATE):
        frameCounter = 0
        screen.fill((0,0,0))

        #update player
        update_snake()
        check_out_of_bounds()
        check_self_collision()
        collision_sprite()

        player.draw(screen)

        apple_group.draw(screen)
    else:
        frameCounter += 1
    


    
    

    # print(applecount)
    print(grid)
    pygame.display.update()   
    clock.tick(TICKRATE) 




    