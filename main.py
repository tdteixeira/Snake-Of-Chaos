import pygame
import sys
import random

WINDOW_SIZE = (600, 400)
GRID_SIZE = 20
BOOST_CHANCE = 1
MULTIPLIER_CHANCE = 1
BOOST_DURATION = 10000  # milliseconds (10 seconds)
MULTIPLIER_DURATION = 10000  # milliseconds (10 seconds)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
APPLE = (255, 0, 0)
BOOST = (0, 0, 255)
MULTIPLIER = (255,255,0)

def generate_random_position():
    max_x = (WINDOW_SIZE[0] // GRID_SIZE) - 1
    max_y = (WINDOW_SIZE[1] // GRID_SIZE) - 1
    return [random.randint(0, max_x) * GRID_SIZE, random.randint(0, max_y) * GRID_SIZE]

def get_moveDir(event,moveDir):
    movDir=moveDir
    if moveDir != [0, 1] and (event.key == pygame.K_UP or event.key == pygame.K_w):
        movDir = [0,-1]
    elif moveDir != [0, -1] and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
        movDir = [0,1]
    elif moveDir != [1, 0] and (event.key == pygame.K_LEFT or event.key == pygame.K_a):
        movDir = [-1,0]
    elif moveDir != [-1, 0] and (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
        movDir = [1,0] 
    return movDir  

def move_snake(snake_body, moveDir):
    if moveDir != [0,0]:
        headpos=snake_body[0].copy()
        headpos[0] += moveDir[0] * GRID_SIZE
        headpos[1] += moveDir[1] * GRID_SIZE
        if headpos[0] < 0:
            headpos[0] = WINDOW_SIZE[0]-GRID_SIZE
        elif headpos[0] > WINDOW_SIZE[0]-GRID_SIZE:
            headpos[0] = 0
        elif headpos[1] < 0:
            headpos[1] = WINDOW_SIZE[1]-GRID_SIZE
        elif headpos[1] > WINDOW_SIZE[1]-GRID_SIZE:
            headpos[1] = 0
        for i in range(len(snake_body)-1,0,-1):
            snake_body[i]=snake_body[i-1]
        snake_body[0] = headpos
        return headpos
    return None

def check_item_collision(headpos, item_pos):
    if headpos == item_pos:
        return None, True
    return item_pos, False

def check_for_death(headpos, snake_body):
    return headpos in snake_body[1:]

def main():
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Snake of Chaos") 
    font = pygame.font.Font('freesansbold.ttf', 20)

    # Snake position
    init_snake_head = [2*GRID_SIZE, 3*GRID_SIZE]
    snake_body = [init_snake_head, [init_snake_head[0]-GRID_SIZE, init_snake_head[1]], [init_snake_head[0]-2*GRID_SIZE, init_snake_head[1]]]
    #Movement related
    pending_moveDir = [0,1]
    moveDir = [0,1]
    base_speed = 10
    current_speed = base_speed
    #Boost related
    boost = 2
    boost_pos = None
    boost_time_remaining = 0 
    #Multiplier related
    multiplier_base = 1
    current_multiplier = 2
    multiplier_pos = None
    multiplier_time_remaining = 0
    #General
    died = False
    score = 0
    apple_pos = generate_random_position()
    clock = pygame.time.Clock()


    while True:
        if died == True:
            text = font.render("Game Over", True, (255,255,255))
            text_rect = text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Check For KeyPressEvents
            if event.type == pygame.KEYDOWN:
                pending_moveDir = get_moveDir(event,moveDir)
        
        moveDir = pending_moveDir
        
        #Logic
        if (boost_pos is None and random.randint(1,100) <= BOOST_CHANCE):
            boost_pos = generate_random_position()
            print("Boost appeared at", boost_pos)
        if (multiplier_pos is None and random.randint(1,100) <= MULTIPLIER_CHANCE):
            multiplier_pos = generate_random_position()
            print("Multiplier appeared at", multiplier_pos)
        headpos = move_snake(snake_body,moveDir)
        if headpos is not None:
            died = check_for_death(headpos, snake_body)
            apple_pos, apple_collected = check_item_collision(headpos, apple_pos)
            if apple_collected:
                apple_pos = generate_random_position()
                print("Apple appeared at", apple_pos)
                score=score+current_multiplier
                for _ in range(current_multiplier):
                    snake_body.append(snake_body[-1].copy())
            if boost_pos is not None:
                boost_pos, boost_collected = check_item_collision(headpos, boost_pos)
                if boost_collected:
                    boost_time_remaining = BOOST_DURATION
                    current_speed = current_speed * boost
            if multiplier_pos is not None:
                multiplier_pos, multiplier_collected = check_item_collision(headpos, multiplier_pos)
                if multiplier_collected:
                    multiplier_time_remaining = MULTIPLIER_DURATION
                    current_multiplier = current_multiplier * 2
        
        # Handle boost timer using delta time
        if boost_time_remaining > 0:
            dt = clock.get_time()  # milliseconds since last tick
            boost_time_remaining -= dt
        else:
            current_speed = base_speed
        if multiplier_time_remaining > 0:
            dt = clock.get_time()  # milliseconds since last tick
            multiplier_time_remaining -= dt
        else:
            current_multiplier = multiplier_base
            
        #Visuals
        screen.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, APPLE, pygame.Rect(apple_pos[0], apple_pos[1], GRID_SIZE, GRID_SIZE))
        if boost_pos is not None:
            pygame.draw.rect(screen, BOOST, pygame.Rect(boost_pos[0], boost_pos[1], GRID_SIZE, GRID_SIZE))
        if multiplier_pos is not None:
            pygame.draw.rect(screen, MULTIPLIER, pygame.Rect(multiplier_pos[0], multiplier_pos[1], GRID_SIZE, GRID_SIZE))
        
        #Score text
        text = font.render("Score: "+ str(score), True, (255,255,255))
        screen.blit(text,[0,0])
        if boost_time_remaining > 0:
            text = font.render("x"+str(current_speed)+" Boost time: "+ str(boost_time_remaining//1000), True, (255,255,255))
            screen.blit(text,[WINDOW_SIZE[0] - text.get_width(),0])
        if multiplier_time_remaining > 0:
            text = font.render("x"+str(current_multiplier)+" Multiplier time: "+ str(multiplier_time_remaining//1000), True, (255,255,255))
            screen.blit(text,[WINDOW_SIZE[0] - text.get_width(),text.get_height()])

        pygame.display.update()
        clock.tick(current_speed)

main()