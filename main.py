import pygame
import sys
import random
import math

WINDOW_SIZE = (600, 400)
GRID_SELECTOR = 5
BOOST_CHANCE = 1
MULTIPLIER_CHANCE = 1
BOOST_DURATION = 10000  # milliseconds (10 seconds)
MULTIPLIER_DURATION = 10000  # milliseconds (10 seconds)
GAME_NAME = "Snake of Chaos"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
APPLE = (255, 0, 0)
BOOST = (0, 0, 255)
MULTIPLIER = (255,255,0)

def get_all_common_divisors(width, height):
    mdc = math.gcd(width, height)
    divs = set()
    for i in range(1, int(math.sqrt(mdc)) + 1):
        if mdc % i == 0:
            divs.add(i)
            divs.add(mdc // i)
    return sorted(divs)

def generate_random_position():
    max_x = (WINDOW_SIZE[0] // grid_size) - 1
    max_y = (WINDOW_SIZE[1] // grid_size) - 1
    return [random.randint(0, max_x) * grid_size, random.randint(0, max_y) * grid_size]

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
        headpos[0] += moveDir[0] * grid_size
        headpos[1] += moveDir[1] * grid_size
        if headpos[0] < 0:
            headpos[0] = WINDOW_SIZE[0]-grid_size
        elif headpos[0] > WINDOW_SIZE[0]-grid_size:
            headpos[0] = 0
        elif headpos[1] < 0:
            headpos[1] = WINDOW_SIZE[1]-grid_size
        elif headpos[1] > WINDOW_SIZE[1]-grid_size:
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

def run_menu(screen):
    titlefont = pygame.font.Font('freesansbold.ttf', 50)
    titletext = titlefont.render(GAME_NAME, True, WHITE)
    titletext_rect = titletext.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 50))
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Press 'P' key to start", True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 20))
    screen.fill(BLACK)
    screen.blit(titletext, titletext_rect)
    screen.blit(text, text_rect)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting = False
    return "Play"

def run_game(screen):
    font = pygame.font.Font('freesansbold.ttf', 20)

    # Snake position
    init_snake_head = [2*grid_size, 3*grid_size]
    snake_body = [init_snake_head, [init_snake_head[0]-grid_size, init_snake_head[1]], [init_snake_head[0]-2*grid_size, init_snake_head[1]]]
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
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
            return "Menu"
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
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], grid_size, grid_size))
        pygame.draw.rect(screen, APPLE, pygame.Rect(apple_pos[0], apple_pos[1], grid_size, grid_size))
        if boost_pos is not None:
            pygame.draw.rect(screen, BOOST, pygame.Rect(boost_pos[0], boost_pos[1], grid_size, grid_size))
        if multiplier_pos is not None:
            pygame.draw.rect(screen, MULTIPLIER, pygame.Rect(multiplier_pos[0], multiplier_pos[1], grid_size, grid_size))
        
        #Score text
        text = font.render("Score: "+ str(score), True, WHITE)
        screen.blit(text,[0,0])
        if boost_time_remaining > 0:
            text = font.render("x"+str(current_speed)+" Boost time: "+ str(boost_time_remaining//1000), True, WHITE)
            screen.blit(text,[WINDOW_SIZE[0] - text.get_width(),0])
        if multiplier_time_remaining > 0:
            text = font.render("x"+str(current_multiplier)+" Multiplier time: "+ str(multiplier_time_remaining//1000), True, WHITE)
            screen.blit(text,[WINDOW_SIZE[0] - text.get_width(),text.get_height()])

        pygame.display.update()
        clock.tick(current_speed)

def main():
    divs = get_all_common_divisors(WINDOW_SIZE[0], WINDOW_SIZE[1])
    global grid_size
    grid_size = divs[GRID_SELECTOR]
    pygame.init()
    # Screen setup
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(GAME_NAME)
    state = "Menu"
    while True:
        pygame.display.update()
        if state == "Menu" or state == "Dead":
            state = run_menu(screen)
        elif state == "Play":
            state = run_game(screen)
main()