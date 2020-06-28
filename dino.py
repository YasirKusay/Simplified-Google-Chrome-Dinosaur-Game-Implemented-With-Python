import pygame 
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (173, 216, 230)
yellow = (255, 255, 0)
dark_green = (0, 100, 0)

DISPLAY_LENGTH = 600
DISPLAY_WIDTH = 800

jump_up = False
jump_down = False
is_duck = False

curr_player_pos_x = 100
curr_player_pos_y = 350

SCORE = 0

gameOver = False
gameExit = False

smallfont = pygame.font.SysFont("comicsansms", 25) # second parameter is font size

# checks that the numbers of num1 are somewhere in between the numbers of num2
def check_two_inbetweens(num1_low, num1_high, num2_low, num2_high):
    for i in range(num1_low, num1_high):
        if i >= num2_low and i <= num2_high: 
            return True
    return False

def score():
    text = smallfont.render(str(SCORE), True, black)
    gameDisplay.blit(text, [400, 50])

def text_objects(text, colour):
    textSurface = smallfont.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, colour):
    textSurf, textRect = text_objects(msg, colour) # textsurf refers to the surface of the message, textrect
    textRect.center = (DISPLAY_WIDTH/2), (DISPLAY_LENGTH/2)
    gameDisplay.blit(textSurf, textRect)

# we are assuming that there can be at most 3 obstacles on the screen

trap_1_x = None
trap_1_y = None
trap_1_length = None
trap_1_height = None

trap_2_x = None
trap_2_y = None
trap_2_length = None
trap_2_height = None

trap_3_x = None
trap_3_y = None
trap_3_length = None
trap_3_height = None

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_LENGTH))
pygame.display.set_caption('Tank')
gameDisplay.fill(white)
# pygame.display.update()
clock = pygame.time.Clock()
'''
pix = pygame.PixelArray(gameDisplay) # gives us the array of our display
# we can now manipulate it as below, specifically for pixel drawing stuff

def draw_basic_background():
    global pix
    for i in range(0, DISPLAY_WIDTH):
        for j in range(450, DISPLAY_LENGTH):
            pix[i][j] = green
'''
# person = pygame.image.load('megadeth.jpeg')
# pygame.display.update()

def jumpUp():
    global curr_player_pos_y
    global jump_up
    global jump_down
    if curr_player_pos_y > 250:
        curr_player_pos_y -= 10
        # print(curr_player_pos_y)
        #pygame.draw.rect(gameDisplay, black, [100, curr_player_pos_y, 10, 100])
    if curr_player_pos_y <= 250: 
        jump_up = False
        jump_down = True
        # print(curr_player_pos_y)
        return
        #print(curr_player_pos_y)
        #pygame.draw.rect(gameDisplay, black, [100, curr_player_pos_y, 10, 100])

def jumpDown():
    global curr_player_pos_y
    global jump_up
    global jump_down
    if curr_player_pos_y < 350:
        curr_player_pos_y += 10
        # pygame.draw.rect(gameDisplay, black, [100, curr_player_pos_y, 10, 100])
    if curr_player_pos_y >= 350: 
        jump_down = False
        return
        # pygame.draw.rect(gameDisplay, black, [100, curr_player_pos_y, 10, 100])

def determine_enemy():
    num = random.randint(1, 5)
    if num == 1:
        return "tall, thin"
    elif num == 2:
        return "short, wide"
    elif num == 3:
        return "short, thin"
    elif num == 4:
        return "tall, wide"
    else:
        return "bird"

def determine_size():
    obstacle = determine_enemy()
    x = None
    y = None
    length = None
    height = None

    if obstacle == "tall, thin":
        x = 900
        y = 380
        length = 10
        height = 70
    elif obstacle == "short, wide":
        x = 900
        y = 410
        length = 50
        height = 40
    elif obstacle == "short, thin":
        x = 900
        y = 410
        length = 10
        height = 40
    elif obstacle == "tall, wide":
        x = 900
        y = 400
        length = 35
        height = 50 # shortened because impossible to scale
    else: # placeholder for bird
        x = 900
        y = 440
        length = 10
        height = 10

    return x, y, length, height

def spawn_obstacle():

    global trap_1_x
    global trap_1_y
    global trap_1_length
    global trap_1_height

    global trap_2_x
    global trap_2_y
    global trap_2_length
    global trap_2_height

    global trap_3_x
    global trap_3_y
    global trap_3_length
    global trap_3_height

    distance_between_obstacles = round(random.randint(200, 800))

    if trap_1_x == None and trap_2_x == None and trap_3_x == None:
        trap_1_x, trap_1_y, trap_1_length, trap_1_height = determine_size()
        
        trap_2_x, trap_2_y, trap_2_length, trap_2_height = determine_size()
        trap_2_x = distance_between_obstacles + trap_1_x

        distance_between_obstacles = round(random.randint(200, 400))
        trap_3_x, trap_3_y, trap_3_length, trap_3_height = determine_size()
        trap_3_x = distance_between_obstacles + trap_2_x

        return

    if trap_2_x == None and trap_1_x != None:
        trap_2_x, trap_2_y, trap_2_length, trap_2_height = determine_size()
        trap_2_x = distance_between_obstacles + trap_1_x
        return

    if trap_3_x == None and trap_1_x != None:
        trap_3_x, trap_3_y, trap_3_length, trap_3_height = determine_size()
        trap_3_x = distance_between_obstacles + trap_2_x
        return

    if trap_1_x == None and trap_3_x != None:
        trap_1_x, trap_1_y, trap_1_length, trap_1_height = determine_size()
        trap_1_x = distance_between_obstacles + trap_3_x
        return
    

"""
def old_spawn_obstacles():
    global trap_1_x
    global trap_1_y
    global trap_1_length
    global trap_1_height

    if trap_1_x == None:
        trap_1_x, trap_1_y, trap_1_length, trap_1_height = determine_size()
        return
"""
def gameLoop():

    global jump_up
    global jump_down
    global is_duck

    global curr_player_pos_x
    global curr_player_pos_y 

    curr_player_pos_x = 100
    curr_player_pos_y = 350
    jump_down = False
    jump_up = False
    is_duck = False

    global SCORE

    global gameOver
    global gameExit

    gameExit = False
    gameOver = False

    global trap_1_x
    global trap_1_y
    global trap_1_length
    global trap_1_height

    trap_1_x = None
    trap_1_y = None

    global trap_2_x
    global trap_2_y
    global trap_2_length
    global trap_2_height

    trap_2_x = None
    trap_2_y = None

    global trap_3_x
    global trap_3_y
    global trap_3_length
    global trap_3_height

    trap_3_x = None
    trap_3_y = None

    # need to reset the map somehow

    while gameExit == False:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen(f"Your score is {SCORE}", green)
                
            pygame.display.update()

            gameDisplay.fill(white)
            message_to_screen("Game over, press C to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        SCORE = 0
                        gameLoop() # calling game loop within game loop
                    if event.type == pygame.QUIT: # has to be referenced by timegame
                        gameExit = True
                        return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if curr_player_pos_x == 100 and curr_player_pos_y == 350:
                        jump_up = True
                
                if event.key == pygame.K_DOWN:
                    if curr_player_pos_x == 100 and curr_player_pos_y == 350:
                        #curr_player_pos_y = 330
                        is_duck = True
                else:
                    #curr_player_pos_y = 350
                    is_duck = False

        gameDisplay.fill(white)
        # draw_basic_background()
        pygame.draw.circle(gameDisplay, yellow, [70, 70], 50)
        pygame.draw.rect(gameDisplay, green, [0, 450 , 800, 250])

        spawn_obstacle()

        # pygame.draw.rect(gameDisplay, black, [100, 350, 10, 100])
        if jump_up == True:
            jumpUp()
        elif jump_down == True:
            jumpDown()
        #else:
        if is_duck == False:
            pygame.draw.rect(gameDisplay, black, [100, curr_player_pos_y, 10, 100])
        else:
            pygame.draw.rect(gameDisplay, black, [100, 420, 10, 30]) # remember, location on display refers to top block       
            pygame.draw.rect(gameDisplay, black, [100, 420, 70, 10])

        trap_1_x -= 10
        trap_2_x -= 10
        trap_3_x -= 10
    
        if trap_1_x != None:
            print("trap_1")
            pygame.draw.rect(gameDisplay, dark_green, [trap_1_x, trap_1_y, trap_1_length, trap_1_height])
            if trap_1_x < 0 - trap_1_length:
                trap_1_x = None
                trap_1_y = None
                trap_1_length = None 
                trap_1_y = None

        if trap_2_x != None:
            print("trap_2")
            pygame.draw.rect(gameDisplay, dark_green, [trap_2_x, trap_2_y, trap_2_length, trap_2_height])
            if trap_2_x < 0 - trap_2_length:
                trap_2_x = None
                trap_2_y = None
                trap_2_length = None 
                trap_2_y = None
        
        if trap_3_x != None:
            print("trap_3")
            pygame.draw.rect(gameDisplay, dark_green, [trap_3_x, trap_3_y, trap_3_length, trap_3_height])
            if trap_3_x < 0 - trap_3_length:
                trap_3_x = None
                trap_3_y = None
                trap_3_length = None 
                trap_3_y = None

        '''
        if jump_up == False and jump_down == False: 
            if curr_player_pos_x + 10 == trap_1_x or curr_player_pos_x + 10 == trap_2_x or curr_player_pos_x + 10 == trap_3_x:
                pygame.quit()
                quit()
        '''
        if trap_1_x != None and trap_1_y != None:
            if check_two_inbetweens(curr_player_pos_x, curr_player_pos_x + 10, trap_1_x, trap_1_x + trap_1_length) == True:
                if check_two_inbetweens(curr_player_pos_y, curr_player_pos_y + 100, trap_1_y, trap_1_y + trap_1_height) == True:
                    gameOver = True

        if trap_2_x != None and trap_2_y != None:
            if check_two_inbetweens(curr_player_pos_x, curr_player_pos_x + 10, trap_2_x, trap_2_x + trap_2_length) == True:
                if check_two_inbetweens(curr_player_pos_y, curr_player_pos_y + 100, trap_2_y, trap_2_y + trap_2_height) == True:
                    gameOver = True

        if trap_3_x != None and trap_3_y != None:
            if check_two_inbetweens(curr_player_pos_x, curr_player_pos_x + 10, trap_3_x, trap_3_x + trap_3_length) == True:
                if check_two_inbetweens(curr_player_pos_y, curr_player_pos_y + 100, trap_3_y, trap_3_y + trap_3_height) == True:
                    gameOver = True
        
        SCORE += 1
        score()
        pygame.display.update()
        clock.tick(100)

gameLoop()
pygame.quit()
quit()
