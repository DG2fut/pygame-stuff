import pygame #2d graphics library
import os #to import the assets 
pygame.font.init()
pygame.mixer.init()

#making a new surface/window of certain width and height
WIDTH, HEIGHT = 900 , 500
SW, SH = 55, 40
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("turi ip ip ip")

#event of getting hit
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#colors 
#color range - R,G,B(0-255) 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#border
BORDER = pygame.Rect(WIDTH//2 -5,0,10,HEIGHT) 

#sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Pygame-1\Assets','Gun+Silencer.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Pygame-1\Assets','Gun+Silencer.mp3'))

#font used to display health
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#frame rate update rate
FPS = 60 
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3


YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Pygame-1\Assets','spaceship_yellow.png'))
#rotating and resizing
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SW,SH)), 90) 


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Pygame-1\Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        RED_SPACESHIP_IMAGE, (SW,SH)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Pygame-1\Assets','space.png')),(WIDTH,HEIGHT))

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    #filling the screen with a bg
    WIN.blit(SPACE, (0,0))
    
    #border
    pygame.draw.rect(WIN,BLACK,BORDER)

    #displaying text for health
    red_health_text = HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10,10))
    
    #displaying the spaceship images
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) 
    
    #drawing the bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW, bullet)
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left key
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right key
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up key
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10: #down key
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left key
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right key
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 : #up key
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10: #down key
        red.y += VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # if yellow bullet collides
            #event (red gets hit) happens
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL    
        if yellow.colliderect(bullet): #if red bullet collides
            #event (yellow gets hit) happens
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2
    ,HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
   #player red
    red = pygame.Rect(700,300,SW,SH)
    #x,y,width,height
    #player yellow
    yellow = pygame.Rect(100,300,SW,SH)
    #for drawing the spaceships at any position

    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() #for controlling the fps rate of the loop

    #event loop
    run = True
    while run:
        clock.tick(FPS)
        #event QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            #to fire bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width - 5, yellow.y + yellow.height//2 - 2, 10, 5)
                    #shape and position of the bullet
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x + 5, red.y + red.height//2 - 2, 10, 5)
                    #shape and position of the bullet
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            
            if event.type == RED_HIT:
                red_health -= 1 #red loses health
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1 #yellow loses health
                BULLET_HIT_SOUND.play()
        
        winner_text= ""
        if red_health <= 0:
            winner_text = "Yellow wins!"
        
        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        
        #to tell what keys are being pressed at a given moment
        keys_pressed = pygame.key.get_pressed()        
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        #if bullets hit
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()

