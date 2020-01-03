# 1 - Import library
import pygame
from pygame.locals import *
import math
import random
import time
# 2 - Initialize the game
pygame.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos=[100,100]



pygame.mixer.init()
clock = pygame.time.Clock()





# 3 - Load images
player = pygame.image.load("images/steve.png")
grass = pygame.image.load("images/sky.jpg")
arrow = pygame.image.load("images/arrow.png")
arrow = pygame.transform.scale(arrow,(70,50))
szkielet = pygame.image.load("images/szkielet.png")
menu = pygame.image.load("images/menu.png")
przycisk = pygame.image.load("images/przycisk.png")
przycisk = pygame.transform.smoothscale(przycisk,(336,50))

przycisk_hover = pygame.image.load("images/przycisk_hover.png")
przycisk_hover = pygame.transform.smoothscale(przycisk_hover,(336,50))

repeat = pygame.image.load("images/repeat.png")
repeat = pygame.transform.scale(repeat,(336,50))

repeat_hover = pygame.image.load("images/repeat_hover.png")
repeat_hover = pygame.transform.scale(repeat_hover,(336,50))

healthbar_full = pygame.image.load("images/health_bar/health.png")
healthbar_9 = pygame.image.load("images/health_bar/health1.png")
healthbar_8 = pygame.image.load("images/health_bar/health2.png")
healthbar_7 = pygame.image.load("images/health_bar/health3.png")
healthbar_6 = pygame.image.load("images/health_bar/health4.png")
healthbar_5 = pygame.image.load("images/health_bar/health5.png")
healthbar_4 = pygame.image.load("images/health_bar/health6.png")
healthbar_3 = pygame.image.load("images/health_bar/health7.png")
healthbar_2 = pygame.image.load("images/health_bar/health8.png")
healthbar_1 = pygame.image.load("images/health_bar/health9.png")
healthbar_dead = pygame.image.load("images/health_bar/health10_dead.png")
gameover = pygame.image.load("images/gameover_mc.png")
youwin = pygame.image.load("images/herobrine1.png")
youwin1 = pygame.image.load("images/herobrine2.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("audio/oof.wav")
enemy1 = pygame.mixer.Sound("audio/szkielet_oof1.wav")
enemy2 = pygame.mixer.Sound("audio/szkielet_oof2.wav")
enemy3 = pygame.mixer.Sound("audio/szkielet_oof3.wav")
enemy4 = pygame.mixer.Sound("audio/szkielet_oof4.wav")
shoot = pygame.mixer.Sound("audio/bow.wav")

cave1 = pygame.mixer.Sound("audio/menukoniec/cave1.wav")
cave2 = pygame.mixer.Sound("audio/menukoniec/cave2.wav")
click = pygame.mixer.Sound("audio/menukoniec/click.wav")
explode2 = pygame.mixer.Sound("audio/menukoniec/explode2.wav")
fallbig = pygame.mixer.Sound("audio/menukoniec/fallbig.wav")
fuse = pygame.mixer.Sound("audio/menukoniec/fuse.wav")
lose = pygame.mixer.Sound('audio/lose1.wav')

hit.set_volume(0.25)
enemy1.set_volume(0.25)
enemy2.set_volume(0.25)
enemy3.set_volume(0.25)
enemy4.set_volume(0.25)
shoot.set_volume(0.05)
lose.set_volume(0.02)
click.set_volume(0.05)
pygame.mixer.music.load('audio/tlo.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.75)
# 4 - keep looping through
running = 1
exitcode = 0



def game():
    global ticks,running, badtimer, player,szkielet, healthvalue, healthbar_full,healthbar_9,healthbar_8,healthbar_7,healthbar_6,healthbar_5,healthbar_4,healthbar_3,healthbar_2,healthbar_1,healthbar_dead, badtimer1
    running=1
    arrows=[]
    badtimer=100
    badtimer1=0
    healthvalue=10
    badguys=[[640,148]]
    keys = [False, False, False, False]
    acc = 0
    while running:
        badtimer-=1
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6 - draw the screen elements
        screen.blit(grass,(0,0))
            # 6.1 - Set player position and rotation
        player = pygame.transform.scale(player,( 150, 213))
        screen.blit(player, (50,148))

         # 6.2 - Draw arrows
        for bullet in arrows:
            index=0
            velx=math.cos(bullet[0])*10
            vely=math.sin(bullet[0])*10
            bullet[1]+=velx
            bullet[2]+=vely
            if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
                arrows.pop(index)
            index+=1
            for projectile in arrows:
                screen.blit(arrow, (projectile[1], projectile[2]))
          # 6.3 - Draw badgers
        if badtimer==0:
            badguys.append([640, 148])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=25
            else:
                badtimer1+=5
        index=0
        for badguy in badguys:
            if badguy[0]<-64:
                badguys.pop(index)
            badguy[0]-=5
             # 6.3.1 - Attack castle
            badrect=pygame.Rect(szkielet.get_rect())
            badrect.top=badguy[1]
            badrect.left=badguy[0]
            if badrect.left<64:
                hit.play()
                healthvalue -= 1
                badguys.pop(index)
                    #6.3.2 - Check for collisions
            index1=0
            for bullet in arrows:
                bullrect=pygame.Rect(arrow.get_rect())
                bullrect.left=bullet[1]
                bullrect.top=bullet[2]
                if badrect.colliderect(bullrect):
                    nr_soundu = random.randint(1,4)
                    if nr_soundu ==1:
                        enemy1.play()
                    elif nr_soundu ==2:
                        enemy2.play()
                    elif nr_soundu ==3:
                        enemy3.play()
                    elif nr_soundu ==4:
                        enemy4.play()
                    acc +=1
                    badguys.pop(index)
                    arrows.pop(index1)
                index1+=1
            # 6.3.3 - Next bad guy
            index+=1
        for badguy in badguys:
            szkielet = pygame.transform.scale(szkielet,( 140, 213))
            screen.blit(szkielet, badguy)
            # 6.5 - Draw health bar
        if healthvalue == 10:
            healthbar_full = pygame.transform.scale(healthbar_full,( 330, 76))
            screen.blit(healthbar_full, (5,5))
        elif healthvalue == 9:
            healthbar_9 = pygame.transform.scale(healthbar_9,( 330, 76))
            screen.blit(healthbar_9, (5,5))
        elif healthvalue == 8:
            healthbar_8 = pygame.transform.scale(healthbar_8,( 330, 76))
            screen.blit(healthbar_8, (5,5))
        elif healthvalue == 7:
            healthbar_7 = pygame.transform.scale(healthbar_7,( 330, 76))
            screen.blit(healthbar_7, (5,5))
        elif healthvalue == 6:
            healthbar_6 = pygame.transform.scale(healthbar_6,( 330, 76))
            screen.blit(healthbar_6, (5,5))
        elif healthvalue == 5:
            healthbar_5 = pygame.transform.scale(healthbar_5,( 330, 76))
            screen.blit(healthbar_5, (5,5))
        elif healthvalue == 4:
            healthbar_4 = pygame.transform.scale(healthbar_4,( 330, 76))
            screen.blit(healthbar_4, (5,5))
        elif healthvalue == 3:
            healthbar_3 = pygame.transform.scale(healthbar_3,( 330, 76))
            screen.blit(healthbar_3, (5,5))
        elif healthvalue == 2:
            healthbar_2 = pygame.transform.scale(healthbar_2,( 330, 76))
            screen.blit(healthbar_2, (5,5))
        elif healthvalue == 1:
            healthbar_1 = pygame.transform.scale(healthbar_1,( 330, 76))
            screen.blit(healthbar_1, (5,5))
        elif healthvalue == 0:
            healthbar_dead = pygame.transform.scale(healthbar_dead,( 330, 76))
            screen.blit(healthbar_dead, (5,5))

        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    keys[2]=True
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_SPACE:
                    keys[2]=False

         # 9 - Move player
            if keys[2]:
                 shoot.play()
                 arrows.append([0,playerpos[0]+90,playerpos[1]+90])
            #10 - Win/Lose check
        if acc >= 10:
            running=0
            exitcode=1
            game_outro(exitcode)
        if healthvalue<=0:
            running=0
            exitcode=0
            game_outro(exitcode)
# 11 - Win/lose display
game_intro()

pygame.display.flip()
