#import libraries 
import pygame
import random
import math
from pygame import mixer

#initializate pygame
pygame.init()

#window size
screen_with = 800
screen_height = 600

#size variable
size = (screen_with, screen_height)

#display window
screen = pygame.display.set_mode( size )

#backgroung image

background = pygame.image.load("fondo del juego.jpg")

#background music
mixer.music.load("disparo.wav")

#title
pygame.display.set_caption("Space Invaders")
mixer.music.play( -1 )

#icon
icon = pygame.image.load("enemigo_uno.png")
pygame.display.set_icon(icon)

#player
player_img = pygame.image.load("player.png")
player_x = 330
player_y = 520
player_x_change = 0

#enemy

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

#number of enemy
enemies = 10

for item in range (enemies):
    enemy_img. append (pygame.image.load("enemigo_uno.png"))
    enemy_x. append (random.randint (0, 765))
    enemy_y. append (random.randint (10, 120))
    enemy_x_change. append (0.6)
    enemy_y_change. append (16)


#bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 480 #the same player y
bullet_x_change = 0
bullet_y_change = 7
bullet_state = "ready"

#score
score = 0

#font variable
score_font = pygame.font.Font("Stocky.ttf", 32)

#text depotition
text_x = 10
text_y = 10

#game over font
go_font = pygame.font.Font("Stocky.ttf")
go_x = 200
go_y = 250

#game over funtion
def game_over(x, y):
    go_text = go_font.render("Game Over", True, (0,0,0))
    screen.blit(go_text, (x, y))

#score text funtion
def show_text( x,y ):
    score_text = score_font.render("Score " + str(score), True, (255,10,10))
    screen.blit(score_text, (x, y))

#player funtion
def player(x, y):
    screen.blit(player_img, (x, y))

#enemy funtion
def enemy(x, y, item):
    screen.blit(enemy_img[item], (x, y))

#fire funtion
def fire(x, y):
    global bullet_state
    bullet_state =("fire")
    screen.blit(bullet_img, (x + 21, y + 10))


#coalition funtion
def is_coalition(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2 )

    if distance < 26:
        return True
    else:
        return False
    

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
#revisa si la tecla es presionada
#verifica si la tecla es izquierda o derecha

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT :
                player_x_change -= 1.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("disparo.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                fire(player_x, bullet_y)
            
#revisa si la tecla fue levantada
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT :
                player_x_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_change += 1.4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_x_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x_change -= 1.4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_x_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player_x_change += 1.4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player_x_change = 0
        
    
    #color RGB: Red - Green - Blue
    rgb = (100, 100, 100)
    screen.fill(rgb)

    #show background image
    screen.blit(background, (0, 0))
    
    #enemy boderies
    #if enemy_x <= 0:
       #enemy_x = 0

    #elif enemy_x >= 765:
         #enemy_x = 765
    
    player_x += player_x_change
    player(player_x, player_y)
    #player x boderies left
    if player_x <= 0:
        player_x = 0


    #player x boderies right
    elif player_x >= 735:
        player_x = 735
   
    #enemy movement
    for item in range (enemies):

        #game over zone
        if enemy_y[item] > 476:
            for j in range (enemies):
                enemy_y [ j ] = 4000

            #call game over funtion
            game_over(go_x, go_y)

            break



        enemy_x[item] += enemy_x_change[item]
        
        if enemy_x[item] <= 0:
            enemy_x[item] <= 1
            enemy_x_change[item] = 0.7
            enemy_y[item] += enemy_y_change[item]
        
        elif enemy_x[item] >= 765:
            enemy_x[item] >= 764
            enemy_x_change[item] = -0.7
            enemy_y[item] += enemy_y_change[item]
        
        #Call coalition funtion
        coalition = is_coalition(enemy_x[item], enemy_y[item], bullet_x, bullet_y)
        if coalition == True:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            score += 40
            bullet_y = 480
            bullet_state = "ready"
            print (score)
            enemy_x[item] = random.randint(0, 765)
            enemy_y[item] = random.randint(10, 120)
        
        #call enemy funtion
        enemy(enemy_x[item], enemy_y[item], item)



    #bullet movement
    if bullet_y <= 0:
       bullet_y = 480
       bullet_state = "ready"

    if bullet_state == ("fire"):
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change


    


    #call text funtion
    show_text(text_x, text_y)

    
    #Update the window
    pygame.display.update()
  