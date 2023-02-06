
import numpy as np
import pygame as pg

from constants import *


class Board_State():
    def __init__(self):
        self.board = np.loadtxt("Scenario/test2.txt",dtype = "str")
        # board piority 
        # self.bPiority 
    def printBoard(self):
        print(self.board)

    def changeObstacle(self,x,y):
        if self.board[x][y] == '0':
            self.board[x][y] = '1'
        else :
            self.board[x][y] = '0'

    def updatePath(self, robot):
        i = robot.posX
        j = robot.posY

        if self.board[i][j]== '0':
            self.board[i][j] = '2'




    # RENDER
    def drawOutline(self, screen):
        for i in range(WIDTH) :
            for j in range(HEIGHT) :
                pg.draw.rect(screen, BLACK, pg.Rect(i*BLOCK,j*BLOCK , BLOCK, BLOCK),1)

    # draw obstacle
    def drawObstacle(self, screen):
        for i in range(WIDTH) :
            for j in range(HEIGHT) :
                if self.board[i][j]=='1':
                    pg.draw.rect(screen, GREEN, pg.Rect(j*BLOCK,i*BLOCK , BLOCK, BLOCK))

    def drawCurrentPos(self, screen, robot):
        x = robot.posX
        y = robot.posY
        pg.draw.rect(screen, BLUE , pg.Rect(y*BLOCK,x*BLOCK , BLOCK, BLOCK))

    def drawLine(self, screen, pos1, pos2):
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        pg.draw.line(screen, BLACK , (y1*BLOCK+10, x1*BLOCK+10) , (y2*BLOCK+10, x2*BLOCK+10),5 )


    # draw path - update by boardstate
    def drawPath(self, screen):
        for i in range(WIDTH) :
            for j in range(HEIGHT) :
                if self.board[i][j]=='2':
                    pg.draw.rect(screen, YELLOW, pg.Rect(j*BLOCK,i*BLOCK , BLOCK, BLOCK))

    def drawStart(self, screen):
        color = pg.Color(("red"))
        pg.draw.rect(screen, RED, pg.Rect(0,380 , BLOCK, BLOCK))

    def drawPathLength(self, screen, robot):
        font = pg.font.SysFont('Calibre', 30, bold=True)
        screen.blit(font.render("PATH : " + str(robot.pathLeng) ,True,pg.Color("red")),(0,400))
