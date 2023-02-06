
import pygame as pg


fps = 10

import BoardEngine
import Robot
from constants import *

def main():
    pg.init()
    screen = pg.display.set_mode((400,420))

    ingame = True
    clock = pg.time.Clock()

    bs = BoardEngine.Board_State()
    robot = Robot.Rb()

    bgrcolor = pg.Color(("white"))

    while ingame :
        for event in pg.event.get() :
            if event.type == pg.QUIT:  
                robot.mark1 = True
            if event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                x = int(location[1]//BLOCK)
                y = int(location[0]//BLOCK)
                
                bs.changeObstacle(x, y)

        screen.fill(bgrcolor)
        robot.play(bs)
    
        repaintBoard(screen, bs, robot)        
        clock.tick(fps)      
        pg.display.flip()

    
def repaintBoard(screen, bs, robot):
    bs.drawObstacle(screen)
    bs.drawPath(screen)
    bs.drawCurrentPos(screen, robot)

    if robot.Pmove and not robot.oldPos == () and not robot.move == ():
        bs.drawLine(screen,robot.oldPos,robot.move)
    # DRAW LAST
    bs.drawStart(screen)
    bs.drawOutline(screen)
    bs.drawPathLength(screen, robot)

main()



            





    



