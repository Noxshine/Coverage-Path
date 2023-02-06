
import math
import numpy as np

from constants import *


Ndir = [-1,0]
Sdir = [1,0]
Wdir = [0,-1]
Edir = [0,1]

NEdir = [-1,1]
NWdir = [-1,-1]
SEdir = [1,1]
SWdir = [1,-1]

directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,1),(-1,-1),(1,-1),(1,1)]

class Rb() :
    def __init__(self):
        self.posX = 19
        self.posY = 0
        self.Bmove = True
        self.Pmove = False
        self.path = [(19,0)]
        self.backTrackList = [] # diem dac biet

        self.posChoose = ()


        self.oldPos = ()
        self.move = ()

        self.mark1 = False # do a boustrophedon first to decomposition
        self.mark2 = False # color path

        self.ApathList = [] # A* path list
        self.sptList = []
        self.pathLeng = 0

        #self.dir = 
    def BoustrophedonMove(self, board_state):
        x = self.posX
        y = self.posY        

        N_cell = [x + Ndir[0], y + Ndir[1]]
        S_cell = [x + Sdir[0], y + Sdir[1]]
        E_cell = [x + Edir[0], y + Edir[1]]
        W_cell = [x + Wdir[0], y + Wdir[1]]

        if self.CheckAvailableCell(board_state, N_cell[0], N_cell[1]):
            move = Ndir
        elif self.CheckAvailableCell(board_state, S_cell[0], S_cell[1]):
            move = Sdir
        elif self.CheckAvailableCell(board_state, E_cell[0], E_cell[1]):
            move = Edir
        elif self.CheckAvailableCell(board_state, W_cell[0], W_cell[1]):
            move = Wdir
        else :
            move = [0,0]
            self.Bmove = False

        oldPos = (self.posX,self.posY)

        self.posX += move[0]
        self.posY += move[1]  

        self.pathLeng += self.sqrtEucDis(self.TwoPointDis(oldPos,(self.posX,self.posY)) )
        self.path.append((self.posX,self.posY))
    

    def CheckAvailableCell(self, board_state, x, y):
        if 0 <= x <= 19 and 0 <= y <= 19 :
            if board_state.board[x][y] == '0':
                return True
            else :
                return False

        return False

    def getBackTrackingList(self, board_state):
        for pos in self.path :
            if self.evaluatePathPos(board_state, pos[0], pos[1]) >=1 :
                self.backTrackList.append(pos)

    def evaluatePathPos(self, board_state, x, y):
        
        c1 = [x + Edir[0], y + Edir[1]]
        c2 = [x + NEdir[0], y + NEdir[1]]
        c3 = [x + Ndir[0], y + Ndir[1]]
        c4 = [x + NWdir[0], y + NWdir[1]]
        c5 = [x + Wdir[0], y + Wdir[1]]
        c6 = [x + SWdir[0], y + SWdir[1]]
        c7 = [x + Sdir[0], y + Sdir[1]]
        c8 = [x + SEdir[0], y + SEdir[1]]

        return self.fB(board_state,c1,c8) + self.fB(board_state,c1,c2) + self.fB(board_state,c5,c6) + self.fB(board_state,c5,c4) + self.fB(board_state,c7,c6) + self.fB(board_state,c7,c8)

    # caculate function b(si, sj)
    def fB(self, board_state, cel1, cel2):

        if 0<= cel1[0]<=19 and 0<=cel1[1] <=19 and board_state.board[cel1[0]][cel1[1]] == '0':
            
            if not (0<= cel2[0]<=19 and 0<=cel2[1] <=19) or board_state.board[cel2[0]][cel2[1]] == '1' :
                return 1
            else: 
                 return 0
        else :
            return 0
    

    def euclideDistance(self, choosePos):
        x = choosePos[0]
        y = choosePos[1]

        a = x - self.posX
        b = y - self.posY

        return a**2 + b**2

    def TwoPointDis(self, posA, posB):
        x1 = posA[0]
        y1 = posA[1]

        x2 = posB[0]
        y2 = posB[1]

        d1 = x1 - x2 
        d2 = y1 - y2

        return d1**2 + d2**2

    def sqrtEucDis(seld, temp):
        return round(math.sqrt(temp),2)

    # find path by A*
    def findPathA_star(self, board_state, choosePos):
        curPos = (self.posX,self.posY)

        openArr = []
        openArr.append([0,curPos[0],curPos[1]])

        closeArr = np.random.choice([False], p=[1], size=20 * 20)
        closeArr = closeArr.reshape(20, 20)

        list = []
        for i in range(20*20):
            c = cell()
            list.append(c)

        arr = np.array(list)
        celldetail = arr.reshape(20, 20)

        celldetail[curPos[0]][curPos[1]].f = 0
        celldetail[curPos[0]][curPos[1]].g = 0
        celldetail[curPos[0]][curPos[1]].h = 0
        celldetail[curPos[0]][curPos[1]].parent_x = curPos[0]
        celldetail[curPos[0]][curPos[1]].parent_y = curPos[1]


        while openArr.__len__() != 0 :
            openArr.sort()
            p = openArr[0]
            openArr.pop(0)

            x = p[1]
            y = p[2]

            closeArr[x , y] = True

            for d in directions :
                x1 = x + d[0]
                y1 = y + d[1]

                if (x1,y1) == choosePos :
                    celldetail[x1][y1].parent_x = x
                    celldetail[x1][y1].parent_y = y
                    return self.A_star_path(celldetail, curPos, choosePos)
                    
                elif 0<= x1 < 20 and 0<= y1 <20  and board_state.board[x1][y1] == '2' :
                    gnew = celldetail[x][y].g + self.TwoPointDis((x,y),(x1,y1))
                    hnew = self.TwoPointDis((x1,y1), choosePos)
                    fnew = gnew + hnew
                    if (celldetail[x1][y1].f > fnew and closeArr[x1 , y1] == False):
                        openArr.append([fnew, x1, y1])
                        celldetail[x1][y1].f = fnew
                        celldetail[x1][y1].g = gnew
                        celldetail[x1][y1].h = hnew
                        celldetail[x1][y1].parent_x = x
                        celldetail[x1][y1].parent_y = y
            
        
    def A_star_path(self,celldetail,curPos,choosePos):
        pathList = []
        pathList.append(choosePos)
        p = choosePos
        while not p == curPos :
            par_pos = (celldetail[p[0]][p[1]].parent_x,celldetail[p[0]][p[1]].parent_y)
            pathList.append(par_pos)
            p = par_pos
        return pathList
    
    def A_star_SPT(self):
        pass
        #Apath = self.pathList
#
        #Apath.reverse()
        #leng = Apath.__len__()
#
        #rootPos = Apath[0]
        #desPos = Apath[leng-1]
        
# check if there are obstacle between line of 2 pos        
    def checkObstacle2Pos (self, bs, pos1, pos2):
        x1 = pos1[0]
        y2 = pos1[1]

        x2 = pos2[0]
        y2 = pos2[1]

        tan_goc = abs(x1-x2)/abs(y1-y2)


# find the shortest position in backtracking list 
    def getShortestPos(self,bs):
        if not self.backTrackList == [] :
            disMIN = MAX
            pos = 0
            for i in range(len(self.backTrackList)) :
                dis = self.euclideDistance(self.backTrackList[i])
                if dis < disMIN:
                    disMIN = dis
                    pos = i
                                            
            self.posChoose = self.backTrackList[pos]
            print(self.posChoose)
            #robot.backTrackList.remove(robot.backTrackList[pos]) 
            
            # find path from current pos to next position
            self.ApathList = self.findPathA_star(bs, self.posChoose)
            self.Pmove = True
            print(self.ApathList)

    # theta*
    def checkLineOfSign(self, pos1, pos2, bs) :
        x0 = pos1[0]
        y0 = pos1[1]

        x1 = pos2[0]
        y1 = pos2[1]

        dy = y1 - y0
        dx = x1 - x0

        f = 0
        if dy < 0 :
            dy = -dy
            s_y = -1
        else :
            s_y = 1
        
        if dx < 0 :
            dx = -dx
            s_x = -1
        else :
            s_x = 1
        
        if dx > dy :
            while not x0 == x1 :
                f = f + dy
                if f > dx :
                    if bs.board[x0 + (s_x-1)//2][y0+ (s_y-1)//2] == '1' :
                        return False
                    y0 = y0 + s_y
                    f = f - dx
                if not f == 0 and bs.board[x0 + (s_x-1)//2][y0+ (s_y-1)//2] == '1' :
                    return False
                if dy == 0 and bs.board[x0 + (s_x-1)//2][y0] == '1' and bs.board[x0 + (s_x-1)//2][y0-1] == '1' :
                    return False
                x0 = x0 + s_x
        else :
            while not y0 == y1 :
                f = f + dx
                if f > dy :
                    if bs.board[x0 + (s_x-1)//2][y0+ (s_y-1)//2] == '1' :
                        return False
                    x0 = x0 + s_x
                    f = f - dy
                if not f == 0 and bs.board[x0 + (s_x-1)//2][y0+ (s_y-1)//2] == '1' :
                    return False
                if dx == 0 and bs.board[x0][y0 + (s_y-1)//2] == '1' and bs.board[x0 - 1][y0 + (s_y-1)//2] == '1' :
                    return False
                y0 = y0 + s_y
    
        return True


    # do the whole thing
    # logic 
    def play(self,bs):
        if self.mark1:
            if self.Bmove == True :
                self.BoustrophedonMove(bs)
                bs.updatePath(self)
            else :
                self.mark1 = False
                self.mark2 = True
                self.getBackTrackingList(bs)
                print(self.backTrackList)

        if self.mark2 :
            if self.posChoose == ():
                self.getShortestPos(bs)
                # already have shortestPos 
                # A* Apathlist
                # Pmove = True

                # A* SPT algorithm
                curpos = self.ApathList.pop()
                prepos = ()
                chosepos = curpos
                goal = self.ApathList[0]
                self.sptList.append(curpos)

                while not curpos == goal :
                    
                    if self.checkLineOfSign(chosepos, curpos, bs) :
                        prepos = curpos
                        curpos = self.ApathList.pop()
                        continue
                    else :
                        chosepos = prepos
                        self.sptList.append(chosepos)

                self.sptList.append(goal)
                self.sptList.reverse()

            elif self.Pmove : 
                if self.sptList == []:
                    self.Pmove = False
                    self.Bmove = True  
                else :
                    self.oldPos = (self.posX, self.posY)
                    oldPos = (self.posX, self.posY)
                    self.move = self.sptList.pop()
                    self.posX = self.move[0]
                    self.posY = self.move[1]                
                    self.path.append((self.move[0],self.move[1]))

                    self.pathLeng += self.sqrtEucDis(self.TwoPointDis(oldPos,(self.posX,self.posY)) )


                bs.updatePath(self)

            else :
                if self.Bmove == True :
                    self.BoustrophedonMove(bs)

                    bs.updatePath(self)
                else :
                    self.posChoose = ()
                    self.backTrackList = []
                    self.getBackTrackingList(bs)


class cell:
    def __init__(self):
        self.parent_x = -1
        self.parent_y = -1
        self.f = np.inf
        self.g = np.inf
        self.h = np.inf