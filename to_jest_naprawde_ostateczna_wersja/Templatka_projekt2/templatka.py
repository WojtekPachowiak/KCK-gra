# -*- coding: utf-8 -*-

import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
#from pyOpenBCI import OpenBCIGanglion


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -9000)
        if brt.new_blink:
            if brt.blinks_num == 1:

                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = True
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

    import pygame
    import math

    import random
    import time


    pygame.init()
    width, height = 640, 480
    screen=pygame.display.set_mode((width, height))
    keys = [False, False, False, False]
    playerpos=[100,100]



    pygame.mixer.init()
    clock = pygame.time.Clock()






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
    fuse.set_volume(0.25)
    explode2.set_volume(0.25)
    pygame.mixer.music.load('audio/tlo.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.75)

    running = 1
    exitcode = 0

    def game_intro():
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.MOUSEBUTTONUP:
                    keys[1]= False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    keys[1]= True


            screen.fill(0)
            screen.blit(menu,(0,0))
            mouse_pos = pygame.mouse.get_pos()
            rect = przycisk.get_rect ()
            rect.center = (((width/2),(height/2)))
            screen.blit(przycisk,rect)
            if rect.collidepoint(mouse_pos):
                screen.blit(przycisk_hover,rect)
                if keys[1]== True:
                    click.play()
                    intro=False
                    game()
            pygame.display.update()


    def game_outro(exitcode):
        outro = True
        game_over_screen = True
        start_ticks=pygame.time.get_ticks()
        while outro:
            ms=(pygame.time.get_ticks()-start_ticks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.MOUSEBUTTONUP:
                    keys[3]= False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    keys[3]= True

            if exitcode==0:
                lose.play()
                pygame.mixer.music.stop()
                pygame.display.update()
                if game_over_screen == True:
                    screen.blit(gameover,(0,0))
                    game_over_screen = False
                mouse_pos = pygame.mouse.get_pos()
                rect = repeat.get_rect ()
                rect.center = (((width/2),(height/2)))
                screen.blit(repeat,rect)
                if rect.collidepoint(mouse_pos):
                        screen.blit(repeat_hover,rect)
                        if keys[3]== True:
                            lose.stop()
                            click.play()
                            outro = False
                            game()



            else:
                if ms == 0:
                    pygame.mixer.music.stop()
                    cave1.play()
                    screen.blit(youwin, (0,0))
                    pygame.display.flip()
                    print(ms)


                elif ms == 4000:

                    cave2.play()
                    screen.blit(youwin1, (0,0))
                    pygame.display.flip()



                elif ms == 5000:
                    fuse.play()
                    pygame.display.flip()


                elif ms == 7000:
                    explode2.play()
                    pygame.display.flip()


                elif ms == 7300:
                    screen.fill((0,0,0))
                    pygame.display.flip()



                elif ms == 9300:
                    fallbig.play()
                    

                elif ms == 10300:

                    outro=False
                    pygame.quit()
                    quit()




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

            screen.fill(0)

            screen.blit(grass,(0,0))

            player = pygame.transform.scale(player,( 150, 213))
            screen.blit(player, (50,148))


            for bullet in arrows:
                index=0
                velx=math.cos(bullet[0])*7
                vely=math.sin(bullet[0])*7
                bullet[1]+=velx
                bullet[2]+=vely
                if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
                    arrows.pop(index)
                index+=1
                for projectile in arrows:
                    screen.blit(arrow, (projectile[1], projectile[2]))

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
                badguy[0]-=3

                badrect=pygame.Rect(szkielet.get_rect())
                badrect.top=badguy[1]
                badrect.left=badguy[0]
                if badrect.left<64:
                    hit.play()
                    healthvalue -= 1
                    badguys.pop(index)

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

                index+=1
            for badguy in badguys:
                szkielet = pygame.transform.scale(szkielet,( 140, 213))
                screen.blit(szkielet, badguy)

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


            pygame.display.flip()
            if blink.value == 1:
                print('BLINK!')
                blink.value = 0
                keys[2]=True

            if keys[2]:
                 shoot.play()
                 arrows.append([0,playerpos[0]+90,playerpos[1]+90])
                 keys[2]=False

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit(0)

            if acc == 10:
                running=0
                exitcode=1
                game_outro(exitcode)
            if healthvalue==0:
                running=0
                exitcode=0
                game_outro(exitcode)

    game_intro()

    pygame.display.flip()
    clock.tick(10)




# Zakończenie podprocesów
    proc_blink_det.join()
