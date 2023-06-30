# encoding: utf-8
import os, sys, random
import time
import pygame 
from pygame.locals import *
from drew import *

# 顏色.
color_block         = (0,0,0)
color_white         = (255, 255, 255)
color_red           = (255, 0, 0)
color_gray          = (107,130,114)
color_gray_block    = (20,31,23)
color_gray_green    = (0, 255, 0)

# 定義方塊.
brick_dict = {
    "10": ( 4, 8, 9,13), "11": ( 9,10,12,13),   # N1.
    "20": ( 5, 8, 9,12), "21": ( 8, 9,13,14),   # N2.
    "30": ( 8,12,13,14), "31": ( 4, 5, 8,12), "32": (8,  9, 10, 14), "33": (5,  9, 12, 13), # L1.
    "40": (10,12,13,14), "41": ( 4, 8,12,13), "42": (8,  9, 10, 12), "43": (4,  5,  9, 13), # L2.
    "50": ( 9,12,13,14), "51": ( 4, 8, 9,12), "52": (8,  9, 10, 13), "53": (5,  8,  9, 13), # T.
    "60": ( 8, 9,12,13),    # O.
    "70": (12,13,14,15), "71": ( 1, 5, 9,13)    #I.
}
class test2:
    fin = False
    def __init__ (self,BRICK_DROP_RAPIDLY,BRICK_DOWN_SPEED_MAX,Font,Canvas,Clock,Posx):
        self.clear = False
        self.initPosx = Posx
        self.canvas = Canvas
        self.font = Font
        self.BRICK_DROP_RAPIDLY = BRICK_DROP_RAPIDLY
        self.BRICK_DOWN_SPEED_MAX = BRICK_DOWN_SPEED_MAX
        self.time_temp = time.time()
        self.time_now = 0
        # 時脈.
        self.clock = Clock

        # 方塊陣列(10x20).
        self.bricks_array = []
        # 方塊陣列(4x4).
        self.bricks = []
        # 下一個方塊陣列(4x4).
        self.bricks_next = []
        # 下一個方塊圖形陣列(4x4).
        self.bricks_next_object = []
        # 方塊數量串列.
        self.bricks_list = []
        # 懲罰方塊圖形陣列(1X20).
        self.punish_bricks_object = []
        # 懲罰方塊數量.
        self.punishbrick = 0
        # hold方塊陣列(4x4).
        self.hold_bricks = []
        # hold方塊圖形陣列(4x4).
        self.hold_bricks_object = []
        # hold方塊編號(1~7).
        self.hold_brick_id = 0
        # hold方塊狀態(0~3).
        self.hold_brick_state = 0
        #hold了1次
        self.ishold = False

        # 方塊在容器的位置.
        # (-2~6)(  為6的時候不能旋轉方塊).
        self.container_x = 3
        # (-3~16)(-3表示在上邊界外慢慢往下掉).
        self.container_y =-4

        # 除錯訊息.
        self.debug_message = False
        # 判斷遊戲結束.
        self.game_over = False

        # 方塊下降速度.
        self.brick_down_speed = BRICK_DOWN_SPEED_MAX

        # 方塊編號(1~7).
        self.brick_id = 1
        # 方塊狀態(0~3).
        self.brick_state = 0

        # 下一個方塊編號(1~7).
        self.brick_next_id = 1

        # 最大連線數.
        self.lines_number_max = 0
        # 本場連線數.
        self.lines_number = 0
        # 連線數.
        self.punish_lines_number = 0

        # 遊戲狀態.
        # 0:遊戲進行中.
        # 1:清除方塊.
        self.game_mode = 0
        # 方塊陣列(10x20).
        for i in range(10):
            self.bricks_array.append([0]*20)
        # 方塊陣列(4x4).
        for i in range(4):
            self.bricks.append([0]*4)
        # 下一個方塊陣列(4x4).
        for i in range(4):
            self.bricks_next.append([0]*4)
        # 下一個方塊圖形陣列(4x4).
        for i in range(4):
            self.bricks_next_object.append([0]*4)    
        # 方塊數量串列.
        for i in range(10):
            self.bricks_list.append([0]*20)
        # 懲罰方塊圖形陣列.
        for i in range(20):
            self.punish_bricks_object.append([0])
        # hold方塊陣列(4x4).
        for i in range(4):
            self.hold_bricks.append([0]*4)
        # hold方塊圖形陣列(4x4).
        for i in range(4):
            self.hold_bricks_object.append([0]*4)
            
        # 方塊下降速度.
        self.brick_down_speed = self.BRICK_DOWN_SPEED_MAX

        # 將繪圖方塊放入陣列.
        for y in range(20):
            for x in range(10):
                self.bricks_list[x][y] = self.Box(pygame, self.canvas, "brick_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block)

        # 將繪圖方塊放入陣列.
        for y in range(4):
            for x in range(4):
                self.bricks_next_object[x][y] = self.Box(pygame, self.canvas, "brick_next_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block)

        # 將繪圖方塊放入陣列.
        for y in range(20):
            self.punish_bricks_object[y] = self.Box(pygame, self.canvas, "punish_brick_x_" + str(0) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block)
        
        # 將繪圖方塊放入陣列.
        for y in range(4):
            for x in range(4):
                self.hold_bricks_object[x][y] = self.Box(pygame, self.canvas, "punish_brick_x_" + str(x) + "_y_" + str(y), [ 0, 0, 26, 26], color_gray_block)

        # 背景區塊.
        self.background = self.Box(pygame, self.canvas, "_background", [ self.initPosx+100, 18, 282, 562], color_gray)

        # 背景區塊.
        self.background_bricks_next = self.Box(pygame, self.canvas, "_background_bricks_next", [ self.initPosx+412, 50, 114, 114], color_gray)

        # 懲罰背景區塊.
        self.punish_background = self.Box(pygame, self.canvas, "_punish_background", [ self.initPosx+50, 18, 30, 562], color_gray)

        # hold背景區塊.
        self.hold_background = self.Box(pygame, self.canvas, "_hold_background", [ self.initPosx+412, 300, 114, 114], color_gray)

        # 方塊編號(1~7).
        self.brick_next_id = random.randint( 1, 7)

        # 產生新方塊.
        self.brickNew()

        self.fin = False

    #-------------------------------------------------------------------------
    # 函數:秀字.
    # 傳入:
    #   text    : 字串.
    #   x, y    : 坐標.
    #   color   : 顏色.
    #-------------------------------------------------------------------------
    def showFont( self, text, x, y, color):
        text = self.font.render(text, True, color) 
        self.canvas.blit( text, (x,y))

    #-------------------------------------------------------------------------
    # 函數:取得方塊索引陣列.
    # 傳入:
    #   brickId : 方塊編號(1~7).
    #   state   : 方塊狀態(0~3).
    #-------------------------------------------------------------------------
    def getBrickIndex( self, brickId, state):
        # 組合字串.
        brickKey = str(brickId)+str(state)
        # 回傳方塊陣列.
        return brick_dict[brickKey]

    #-------------------------------------------------------------------------
    # 轉換定義方塊到方塊陣列.
    # 傳入:
    #   brickId : 方塊編號(1~7).
    #   state   : 方塊狀態(0~3).
    #-------------------------------------------------------------------------
    def transformToBricks( self, brickId, state):
        # 清除方塊陣列.
        for x in range(4):
            for y in range(4):
                self.bricks[x][y] = 0
        
        # 取得方塊索引陣列.
        p_brick = self.getBrickIndex(brickId, state)
        
        # 轉換方塊到方塊陣列.
        for i in range(4):        
            bx = int(p_brick[i] % 4)
            by = int(p_brick[i] / 4)
            self.bricks[bx][by] = brickId

        """
        # 印出訊息.
        for y in range(4): 
            s = ""
            for x in range(4): 
                s = s + str(bricks[x][y]) + ","       
            print(s)
        """

    #-------------------------------------------------------------------------
    # 判斷是否可以複製到容器內.
    # 傳出:
    #   true    : 可以.
    #   false   : 不可以.
    #-------------------------------------------------------------------------
    def ifCopyToBricksArray(self):
        posX = 0
        posY = 0
        for x in range(4):
            for y in range(4):
                if (self.bricks[x][y] != 0):
                        posX = self.container_x + x
                        posY = self.container_y + y
                        if (posX >= 0 and posY >= 0):
                            try:
                                if (self.bricks_array[posX][posY] != 0):
                                    return False
                            except:
                                return False
        return True

    #-------------------------------------------------------------------------
    # 複製方塊到容器內.
    #-------------------------------------------------------------------------
    def copyToBricksArray(self):
        posX = 0
        posY = 0
        for x in range(4):
            for y in range(4):
                if (self.bricks[x][y] != 0):
                    posX = self.container_x + x
                    posY = self.container_y + y
                    if (posX >= 0 and posY >= 0):
                        self.bricks_array[posX][posY] = self.bricks[x][y]
        
    #-------------------------------------------------------------------------
    # 初始遊戲.
    #-------------------------------------------------------------------------
    def resetGame(self):
        self.container_y =-4
        # 清除方塊陣列.
        for x in range(10):
            for y in range(20):
                self.bricks_array[x][y] = 0
                
        # 清除方塊陣列.
        for x in range(4):
            for y in range(4):
                self.bricks[x][y] = 0

        # 初始方塊下降速度.
        self.brick_down_speed = self.BRICK_DOWN_SPEED_MAX

        # 最大連線數.
        if(self.lines_number > self.lines_number_max):
            self.lines_number_max = self.lines_number
        # 連線數.
        self.lines_number = 0
        self.game_mode = 0
        self.punishbrick = 0
        self.ishold = False
        self.hold_brick_id = 0
        # 清除方塊陣列.
        for y in range(4):
            for x in range(4):
                self.hold_bricks[x][y] = 0

    #---------------------------------------------------------------------------
    # 判斷與設定要清除的方塊.
    # 傳出:
    #   連線數
    #---------------------------------------------------------------------------
    def ifClearBrick(self):
        pointNum = 0
        lineNum = 0
        for y in range(20):
            for x in range(10):
                if (self.bricks_array[x][y] > 0):
                    pointNum = pointNum + 1
                if (pointNum == 10):
                    for i in range(10):
                        lineNum = lineNum + 1
                        self.bricks_array[i][y] = 9
            pointNum = 0
        return lineNum

    #-------------------------------------------------------------------------
    # 更新下一個方塊.
    #-------------------------------------------------------------------------
    def updateNextBricks(self, brickId):
        # 清除方塊陣列.
        for y in range(4):
            for x in range(4):
                self.bricks_next[x][y] = 0

        # 取得方塊索引陣列.
        pBrick = self.getBrickIndex(brickId, 0)

        # 轉換方塊到方塊陣列.
        for i in range(4):
            bx = int(pBrick[i] % 4)
            by = int(pBrick[i] / 4)
            self.bricks_next[bx][by] = brickId

        # 更新背景區塊.
        self.background_bricks_next.update()

        # 更新方塊圖.
        pos_y = 52
        for y in range(4):
            pos_x = self.initPosx+414
            for x in range(4):
                if(self.bricks_next[x][y] != 0):
                    self.bricks_next_object[x][y].rect[0] = pos_x
                    self.bricks_next_object[x][y].rect[1] = pos_y
                    self.bricks_next_object[x][y].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28

    #-------------------------------------------------------------------------
    # 更新hold方塊.
    #-------------------------------------------------------------------------
    def updateHoldBricks(self):
        # 更新背景區塊.
        self.hold_background.update()

        # 更新方塊圖.
        pos_y = 302
        for y in range(4):
            pos_x = self.initPosx+414
            for x in range(4):
                if(self.hold_bricks[x][y] != 0):
                    self.hold_bricks_object[x][y].rect[0] = pos_x
                    self.hold_bricks_object[x][y].rect[1] = pos_y
                    self.hold_bricks_object[x][y].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28

    #-------------------------------------------------------------------------
    # 計算hold方塊.
    #-------------------------------------------------------------------------
    def calHoldBricks(self):
        if self.ishold == True:
            return
        if self.hold_brick_id == 0:
            self.hold_brick_id = self.brick_id
            self.hold_brick_state = 0
            #產生新塊.
            # 初始方塊位置.
            self.container_x = 3
            self.container_y =-4

            # 現在出現方塊.
            self.brick_id = self.brick_next_id

            # 下個出現方塊.
            # 方塊編號(1~7).
            self.brick_next_id = random.randint( 1, 7)
            
            # 初始方塊狀態.
            self.brick_state = 0
            # 轉換定義方塊到方塊陣列(bricks).
            self.transformToBricks( self.brick_id, self.brick_state)

        else:
            bid = self.brick_id
            self.brick_id = self.hold_brick_id
            self.hold_brick_id = bid
            self.hold_brick_state = 0
            #產生新塊.
            # 初始方塊位置.
            self.container_x = 3
            self.container_y =-4
            # 初始方塊狀態.
            self.brick_state = 0
            # 轉換定義方塊到方塊陣列(bricks).
            self.transformToBricks( self.brick_id, self.brick_state)
        
        self.ishold = True

        # 清除方塊陣列.
        for y in range(4):
            for x in range(4):
                self.hold_bricks[x][y] = 0

        # 取得方塊索引陣列.
        p_brick = self.getBrickIndex(self.hold_brick_id, self.hold_brick_state)
        
        # 轉換方塊到方塊陣列.
        for i in range(4):        
            bx = int(p_brick[i] % 4)
            by = int(p_brick[i] / 4)
            self.hold_bricks[bx][by] = self.hold_brick_id
    #-------------------------------------------------------------------------
    # 更新懲罰方塊.
    #-------------------------------------------------------------------------
    def updatePunishBricks(self, Punishbrick):
        self.punish_background.update()
        self.punishbrick += Punishbrick
        pos_x = self.initPosx+52
        pos_y = 20
        for y in range(20):
            if y + self.punishbrick >= 20:
                self.punish_bricks_object[y].rect[0] = pos_x
                self.punish_bricks_object[y].rect[1] = pos_y
                self.punish_bricks_object[y].update()
            pos_y = pos_y + 28

    #-------------------------------------------------------------------------
    # 清除懲罰方塊.
    #-------------------------------------------------------------------------
    def clearPunishBricks(self):
        Bricks_array = self.bricks_array
        i = random.randint(0,9)
        for y in range(self.punishbrick,20):
            for x in range(10):
                self.bricks_array[x][y-self.punishbrick] = Bricks_array[x][y]
        for y in range(20-self.punishbrick,20):
            for x in range(10):
                if x == i:
                    self.bricks_array[x][y] = 0
                    continue
                else:
                    self.bricks_array[x][y] = 1
        self.punishbrick = 0

    def fall(self):
        # 往下降.
        while True :
            self.container_y = self.container_y + 1; 
            # 碰到方塊.
            if (not self.ifCopyToBricksArray()):
                self.ishold = False
                #產生新塊.
                self.brickNew()
                #清除懲罰方塊   
                self.clearPunishBricks()
                # 轉換定義方塊到方塊陣列(bricks).
                self.transformToBricks( self.brick_id, self.brick_state)
                # 清除時脈.
                self.time_now = 0
                break
    #-------------------------------------------------------------------------
    # 產生新方塊.
    #-------------------------------------------------------------------------
    def brickNew(self):
        # 判斷遊戲結束.
        self.game_over = False
        if (self.container_y < -1):
            self.game_over = True

        # 複製方塊到容器內.
        self.container_y = self.container_y - 1
        self.copyToBricksArray()  
        
        #------------------------------------------------    
        # 判斷與設定要清除的方塊.
        lines = self.ifClearBrick() / 10;        
        if (lines > 0):
            # 消除連線數量累加.
            self.lines_number =  self.lines_number + lines
            # 修改連線數量.
            #modifyLabel(linesNumber, fontLinesNumber)
            self.punish_lines_number = lines
            # 1:清除方塊.
            self.game_mode = 1

        # 初始方塊位置.
        self.container_x = 3
        self.container_y =-4

        # 現在出現方塊.
        self.brick_id = self.brick_next_id

        # 下個出現方塊.
        # 方塊編號(1~7).
        self.brick_next_id = random.randint( 1, 7)
        
        # 初始方塊狀態.
        self.brick_state = 0

        # GameOver.
        if (self.game_over):
            # 重新開始遊戲.
            #self.resetGame()
            self.fin = True
        
    #-------------------------------------------------------------------------
    # 清除的方塊.
    #-------------------------------------------------------------------------
    def clearBrick(self):
        # 一列一列判斷清除方塊.
        temp = 0    
        for x in range(10):
            for i in range(19):
                for y in range(20):
                    if (self.bricks_array[x][y] == 9):
                        if (y > 0):
                            temp = self.bricks_array[x][y - 1]
                            self.bricks_array[x][y - 1] = self.bricks_array[x][y]
                            self.bricks_array[x][y] = temp
                            y = y - 1
                self.bricks_array[x][0] = 0
    #-----------------------------------------------------------------
    # 變換方塊-上.
    def UP(self):
        if self.game_mode == 0:
            # 在右邊界不能旋轉.
            if (self.container_x == 8):
                return
            # 判斷方塊N1、N2、I.
            if (self.brick_id == 1 or self.brick_id == 2 or self.brick_id == 7):
                # 長條方塊旋轉例外處理.
                if (self.brick_id == 7):
                    if (self.container_x < 0 or self.container_x == 7):
                        return
                # 旋轉方塊.
                self.brick_state = self.brick_state + 1
                if (self.brick_state > 1):
                    self.brick_state = 0                    
                # 轉換定義方塊到方塊陣列.
                self.transformToBricks(self.brick_id, self.brick_state)
                # 碰到方塊.
                if (not self.ifCopyToBricksArray()):
                    self.brick_state = self.brick_state - 1
                    if (self.brick_state < 0):
                        self.brick_state = 1
                    self.transformToBricks(self.brick_id, self.brick_state)
            # 判斷磚跨L1、L2、T.                                
            elif (self.brick_id == 3 or self.brick_id == 4 or self.brick_id == 5):
                # 旋轉方塊.
                self.brick_state = self.brick_state + 1
                if (self.brick_state > 3):
                    self.brick_state = 0                    
                # 轉換定義方塊到方塊陣列.
                self.transformToBricks(self.brick_id, self.brick_state)
                # 碰到方塊.
                if (not self.ifCopyToBricksArray()):
                    self.brick_state = self.brick_state - 1
                    if (self.brick_state < 0):
                        self.brick_state = 3
                    self.transformToBricks(self.brick_id, self.brick_state)
    
    def DOWN(self):
        if self.game_mode == 0:
            # 方塊快速下降.
            self.brick_down_speed = self.BRICK_DROP_RAPIDLY
    
    def LEFT(self):
        if self.game_mode == 0:
            self.container_x = self.container_x - 1
            if (self.container_x < 0):
                if (self.container_x == -1):
                    if (self.bricks[0][0] != 0 or self.bricks[0][1] != 0 or self.bricks[0][2] != 0 or self.bricks[0][3] != 0):
                        self.container_x = self.container_x + 1
                elif (self.container_x == -2): 
                    if (self.bricks[1][0] != 0 or self.bricks[1][1] != 0 or self.bricks[1][2] != 0 or self.bricks[1][3] != 0):
                        self.container_x = self.container_x + 1
                else:
                    self.container_x = self.container_x + 1
            # 碰到方塊.
            if (not self.ifCopyToBricksArray()):
                self.container_x = self.container_x + 1

    def RIGHT(self):
        if self.game_mode == 0:
            self.container_x = self.container_x + 1
            if (self.container_x > 6):
                if (self.container_x == 7):
                    if (self.bricks[3][0] != 0 or self.bricks[3][1] != 0 or self.bricks[3][2] != 0 or self.bricks[3][3] != 0):
                        self.container_x = self.container_x - 1;                        
                elif (self.container_x == 8):
                    if (self.bricks[2][0] != 0 or self.bricks[2][1] != 0 or self.bricks[2][2] != 0 or self.bricks[2][3] != 0):
                        self.container_x = self.container_x - 1                        
                else:
                    self.container_x = self.container_x - 1
            # 碰到方塊.
            if (not self.ifCopyToBricksArray()):
                self.container_x = self.container_x - 1   

    def RDOWN(self):
        # 恢復正常下降速度.
        self.brick_down_speed = self.BRICK_DOWN_SPEED_MAX

    def DeBug(self):
        self.debug_message = not self.debug_message
    
    #-------------------------------------------------------------------------
    # 畫Box.
    #-------------------------------------------------------------------------
    class Box(object):
        #-------------------------------------------------------------------------
        # 建構式.
        #   pygame    : pygame.
        #   canvas    : 畫佈.
        #   name    : 物件名稱.
        #   rect      : 位置、大小.
        #   color     : 顏色.
        #-------------------------------------------------------------------------
        def __init__( self, pygame, canvas, name, rect, color):
            self.pygame = pygame
            self.canvas = canvas
            self.name = name
            self.rect = rect
            self.color = color

            self.visivle = True
            
        #-------------------------------------------------------------------------
        # 更新.
        #-------------------------------------------------------------------------
        def update(self):
            if(self.visivle):
                self.pygame.draw.rect( self.canvas, self.color, self.rect)
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------    
    # 主迴圈.
    #-------------------------------------------------------------------------
    
    def runningGame(self):
        # 計算時脈.
        self.time_now = self.time_now + (time.time() - self.time_temp)
        self.time_temp = time.time()
        # 遊戲中.
        if (self.game_mode == 0):
            # 處理方塊下降.
            if(self.time_now >= self.brick_down_speed):
                # 往下降.
                self.container_y = self.container_y + 1; 
                # 碰到方塊.
                if (not self.ifCopyToBricksArray()):
                    self.ishold = False
                    #產生新塊.
                    self.brickNew()
                    #清除懲罰方塊   
                    self.clearPunishBricks()
                # 轉換定義方塊到方塊陣列(bricks).
                self.transformToBricks( self.brick_id, self.brick_state)
                # 清除時脈.
                self.time_now = 0
        # 清除方塊.
        elif (self.game_mode == 1):
            
            self.clear = True
            # 清除的方塊.
            self.clearBrick()
            # 遊戲中.
            self.game_mode = 0
            # 轉換定義方塊到方塊陣列.
            self.transformToBricks(self.brick_id, self.brick_state)
            
        #---------------------------------------------------------------------    
        # 更新下一個方塊圖形.
        self.updateNextBricks(self.brick_next_id)
        # 更新繪圖.
        pos_y = 20
        # 更新背景區塊.
        self.background.update()
        self.updateHoldBricks()
        for y in range(20):
            pos_x = self.initPosx+100
            for x in range(10):
                if(self.bricks_array[x][y] != 0):
                    self.bricks_list[x][y].rect[0] = pos_x
                    self.bricks_list[x][y].rect[1] = pos_y
                    self.bricks_list[x][y].update()
                pos_x = pos_x + 28        
            pos_y = pos_y + 28    
        # 更新方塊
        for y in range(4):
            for x in range(4):            
                if (self.bricks[x][y] != 0):
                    posX = self.container_x + x
                    posY = self.container_y + y
                    if (posX >= 0 and posY >= 0):
                        self.bricks_list[posX][posY].rect[0] = (posX * 28) + self.initPosx+100
                        self.bricks_list[posX][posY].rect[1] = (posY * 28) + 20
                        self.bricks_list[posX][posY].update()
        #---------------------------------------------------------------------    
        # 除錯訊息.
        if(self.debug_message):
            self.font = pygame.font.SysFont("consolas", 24)
            # 更新容器.
            str_x = ""
            pos_x = self.initPosx+15
            pos_y = 20
            for y in range(20):
                str_x = ""
                for x in range(10):
                    str_x = str_x + str(self.bricks_array[x][y]) + " "
                self.showFont( str_x, pos_x, pos_y, color_red)
                pos_y = pos_y + 28
                
            # 更新方塊
            posX = self.initPosx+0
            posY = 0    
            for y in range(4):
                str_x = ""
                for x in range(4):            
                    if (self.bricks[x][y] != 0):
                        posX = self.container_x + x
                        posY = self.container_y + y
                        if (posX >= 0 and posY >= 0):
                            str_x = str_x + str(self.bricks[x][y]) + " "
                    else:
                        str_x = str_x + "  "
                pos_x = self.initPosx+15 + (self.container_x * 26)
                pos_y = 20 + (posY * 28)
                self.showFont( str_x, pos_x, pos_y, color_white)
            self.font = pygame.font.Font("msjh.ttf", 24)

        # 顯示訊息.
        self.showFont( u"下次出現方塊", self.initPosx+412, 16, color_gray)

        #showFont( u"最大連線數", 588, 190, color_gray)
        #showFont( str(int(lines_number_max)), 588, 220, color_gray)

        self.showFont( u"消除行數", self.initPosx+412, 190, color_gray)
        self.showFont( str(int(self.lines_number)), self.initPosx+412, 220, color_gray)
        self.showFont( u"HOLD", self.initPosx+412, 265, color_gray)

        # 顯示FPS.
        # 除錯訊息.
        if(self.debug_message):    
            self.showFont( u"FPS:" + str(self.clock.get_fps()), 6, 0, color_gray_green)  