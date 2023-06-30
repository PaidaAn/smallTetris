# encoding: utf-8
import os, sys, random
import time
import pygame 
from pygame.locals import *
from drew import *

import serial

from TetrisClass import test2

try:
    ser = serial.Serial('COM5', 9600)
    isXmiddle = True
    timer = 0
    isYmiddle = True
    isfall = False
    isDown = False
except:
    print("no COM")

mode = 0

# 常數-方塊快速下降速度.
BRICK_DROP_RAPIDLY   = 0.03
# 常數-方塊正常下降速度.
BRICK_DOWN_SPEED_MAX = 0.5

# 視窗大小.
canvas_width = 1400
canvas_height = 600

# 顏色.
color_block         = (0,0,0)
color_white         = (255, 255, 255)
color_red           = (255, 0, 0)
color_gray          = (107,130,114)
color_gray_block    = (20,31,23)
color_gray_green    = (0, 255, 0)

#-------------------------------------------------------------------------
# 函數:秀字.
# 傳入:
#   text    : 字串.
#   x, y    : 坐標.
#   color   : 顏色.
#-------------------------------------------------------------------------
def showFont( text, x, y, color):
    global canvas
    text = font.render(text, True, color) 
    canvas.blit( text, (x,y))

# 初始.
pygame.init()
# 顯示Title.
pygame.display.set_caption(u"俄羅斯方塊遊戲")
# 建立畫佈大小.
# 全螢幕模式.
#canvas = pygame.display.set_mode((canvas_width, canvas_height), pygame.DOUBLEBUF and pygame.FULLSCREEN )
# 視窗模式.
canvas = pygame.display.set_mode((canvas_width, canvas_height))

#print(pygame.font.get_fonts())
# 設定字型-黑體.
font = pygame.font.Font("msjh.ttf", 24)

# 時脈.
clock = pygame.time.Clock()

#初始化gameZone
GZ1 = test2(BRICK_DROP_RAPIDLY,BRICK_DOWN_SPEED_MAX,font,canvas,clock,000)
GZ2 = test2(BRICK_DROP_RAPIDLY,BRICK_DOWN_SPEED_MAX,font,canvas,clock,800)


#-------------------------------------------------------------------------
running = True
#-------------------------------------------------------------------------
#音樂設置
#-------------------------------------------------------------------------
#pygame.mixer.music.load("TetrisMusic.wav")
#pygame.mixer.music.set_volume(0.02)
fall_sound = pygame.mixer.Sound("down.wav")
fall_sound.set_volume(0.04)
clear_sound = pygame.mixer.Sound("clear.wav")
clear_sound.set_volume(0.04)
#-------------------------------------------------------------------------
# 主迴圈.
#-------------------------------------------------------------------------
while running:
    try:
        line = ser.readline().decode()
        if (line != None):
            data = [int(val) for val in line.split(',')]
            print(data)
    except:
        pass
    if (GZ1.fin == True or GZ2.fin == True):
        if mode == 1:
            mode = 3
        elif mode == 2:
            mode = 4
    #---------------------------------------------------------------------
    # 判斷輸入.
    #---------------------------------------------------------------------
    # 搖桿
    if (mode == 1):
        try:
            if (len(data) == 4 and (mode == 1 or mode == 2)):
                timer+=1
                if (data[1] < 480 and isXmiddle):
                    GZ1.LEFT()
                    isXmiddle = False
                elif (data[1] > 520 and isXmiddle):
                    GZ1.RIGHT()
                    isXmiddle = False
                elif (data[1] >= 480 and data[1] <= 520):
                    isXmiddle = True
                if (data[0] < 480 and isYmiddle):
                    GZ1.UP()
                    isYmiddle = False
                elif (data[0] >= 480 and data[0] <= 520 ):
                    if (isDown):
                        GZ1.RDOWN()
                    isYmiddle = True
                    isDown = False
                elif (data[0] > 520):
                    GZ1.DOWN()
                    isDown = True
                if (data[2] == 1):
                    GZ1.calHoldBricks()
                if (data[3] == 0 and not isfall):
                    fall_sound.play()
                    GZ1.fall()
                    isfall = True
                elif (data[3] == 1):
                    isfall = False
                if (timer >= 15):
                    isXmiddle = True
                    timer = 0
        except:
            pass
    

    #---------------------------------------------------------------------
    # 鍵盤
    for event in pygame.event.get():
        # 離開遊戲.
        if event.type == pygame.QUIT:
            running = False        
        if(mode == 1 or mode == 2):
            # GZ1判斷按下按鈕
            if event.type == pygame.KEYDOWN:
                #-----------------------------------------------------------------
                # 判斷按下ESC按鈕
                if event.key == pygame.K_ESCAPE:
                    running = False
                #-----------------------------------------------------------------
                # 除錯訊息開關.
                elif event.key == pygame.K_b:
                    GZ1.DeBug()                
                #-----------------------------------------------------------------
                # 變換方塊-上. 
                elif event.key == pygame.K_w:
                    GZ1.UP()
                #-----------------------------------------------------------------
                # 快速下降-下.
                elif event.key == pygame.K_s:
                    GZ1.DOWN()
                #-----------------------------------------------------------------
                # 移動方塊-左.
                elif event.key == pygame.K_a:
                    GZ1.LEFT()
                #-----------------------------------------------------------------
                # 移動方塊-右.
                elif event.key == pygame.K_d:
                    GZ1.RIGHT()             
                #-----------------------------------------------------------------
                # HOLD.
                elif event.key == pygame.K_m:
                    GZ1.calHoldBricks()
                #-----------------------------------------------------------------
                # fall.
                elif event.key == pygame.K_SPACE:
                    GZ1.fall()
                    #音效
                    fall_sound.play()

            #-----------------------------------------------------------------
            # 判斷放開按鈕
            if event.type == pygame.KEYUP:
                # 快速下降-下.
                if event.key == pygame.K_s:
                    GZ1.RDOWN()
            
            # GZ2判斷按下按鈕
            if event.type == pygame.KEYDOWN and mode == 2:
                #-----------------------------------------------------------------
                # 判斷按下ESC按鈕
                if event.key == pygame.K_ESCAPE:
                    running = False
                #-----------------------------------------------------------------
                # 除錯訊息開關.
                elif event.key == pygame.K_b:
                    GZ2.DeBug()                
                #-----------------------------------------------------------------
                # 變換方塊-上.
                elif event.key == pygame.K_UP:
                    GZ2.UP()
                #-----------------------------------------------------------------
                # 快速下降-下.
                elif event.key == pygame.K_DOWN:
                    GZ2.DOWN()
                #-----------------------------------------------------------------
                # 移動方塊-左.
                elif event.key == pygame.K_LEFT:
                    GZ2.LEFT()
                #-----------------------------------------------------------------
                # 移動方塊-右.
                elif event.key == pygame.K_RIGHT:
                    GZ2.RIGHT()               
                #-----------------------------------------------------------------
                # HOLD.
                elif event.key == pygame.K_KP3:
                    GZ2.calHoldBricks()
                #-----------------------------------------------------------------
                # fall.
                elif event.key == pygame.K_KP_0:
                    GZ2.fall()
                    #音效
                    fall_sound.play()
                    
            #-----------------------------------------------------------------
            # 判斷放開按鈕
            if event.type == pygame.KEYUP and mode == 2:
                # 快速下降-下.
                if event.key == pygame.K_DOWN:
                    GZ2.RDOWN()
    if (mode == 0):
        pygame.draw.rect(surface=canvas, rect=[ 0, 0, 800, 600], color=color_block)
        showFont( u"案1單人", 600, 250, color_white)
        showFont( u"案2雙人", 600, 300, color_white)
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                #pygame.mixer.music.play(-1)
                mode = 1
            elif event.key == pygame.K_2:
                #pygame.mixer.music.play(-1)
                mode = 2
        continue
    #---------------------------------------------------------------------    
    if (mode == 3):
        #pygame.mixer.music.play(-1)
        font = pygame.font.Font("msjh.ttf", 24)
        showFont( u"案1單人", 600, 250, color_white)
        showFont( u"案2雙人", 600, 300, color_white)
        font = pygame.font.Font("msjh.ttf", 48)
        showFont( u"FAIL", 200, 300, color_red)
        font = pygame.font.Font("msjh.ttf", 24)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
                    GZ2.punish_lines_number = 0
                    GZ2.resetGame()
                GZ1.fin = False
                GZ1.punish_lines_number = 0
                GZ1.resetGame()
    elif (mode == 4):
        #pygame.mixer.music.play(-1)
        font = pygame.font.Font("msjh.ttf", 24)
        showFont( u"案1單人", 600, 250, color_white)
        showFont( u"案2雙人", 600, 300, color_white)
        font = pygame.font.Font("msjh.ttf", 48)
        if GZ1.fin == True:
            showFont( u"FAIL", 200, 300, color_red)
            showFont( u"WIN", 1000, 300, color_red)
        elif GZ2.fin == True:
            showFont( u"WIN", 200, 300, color_red)
            showFont( u"FAIL", 1000, 300, color_red)
        font = pygame.font.Font("msjh.ttf", 24)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                elif event.key == pygame.K_2:
                    mode = 2
                GZ1.fin = False
                GZ2.fin = False
                GZ1.resetGame()
                GZ2.resetGame()
    else:
        if GZ1.clear == True or GZ2.clear == True:
            #音效
            clear_sound.play()
            GZ1.clear = False
            GZ2.clear = False
        # 清除畫面.
        canvas.fill(color_block)
        if mode == 1:
            GZ1.updatePunishBricks(0)
            GZ1.runningGame()
        if mode == 2:
            if GZ1.punish_lines_number > 0:
                GZ2.updatePunishBricks(int(GZ1.punish_lines_number))
                GZ1.punish_lines_number = 0
            elif GZ2.punish_lines_number > 0:
                GZ1.updatePunishBricks(int(GZ2.punish_lines_number))
                GZ2.punish_lines_number = 0
            else:
                GZ1.updatePunishBricks(0)
                GZ2.updatePunishBricks(0)
            GZ1.runningGame()
            GZ2.runningGame()
    # 更新畫面.
    pygame.display.update()
    clock.tick(60)

# 離開遊戲.
pygame.quit()
quit()