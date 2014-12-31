from Tkinter import *
import math
import copy

class Line(object):
    lineList = []
    lineCount = 0
    @classmethod
    def getLineList(cls):
        return Line.lineList
    
    @classmethod
    def getLineCount(cls):
        return int(Line.lineCount)
    
    def __init__(self,listP,name,color,mainInt,width=1):
        #List of Points
        self.listP = listP

        #List of Coordinates
        self.listC = []
        self.name = name
        
        #Identify for curves
        if self.listP[0][1]==1: self.curve = True
        else: self.curve = False
            
        self.color = color
        self.width = width
        self.main = mainInt
        
        #Depth control
        self.sZ = 0
        Line.lineList.append(self)
        Line.lineCount += 1
    
    def step(self):
        sumDepth = 0
        
        #Sum up the depth
        for point in self.listP:
            sumDepth += point[0].sZ
        self.sZ = sumDepth/len(self.listP)

        
        #Get the coordinates
        x0,y0,z0=self.listP[0][0].sX,self.listP[0][0].sY,self.listP[0][0].sZ
        x1,y1,z1=self.listP[1][0].sX,self.listP[1][0].sY,self.listP[1][0].sZ
        
        if self.listP[0][1] == 1:
            x2,y2,z2=self.listP[2][0].sX,self.listP[2][0].sY,self.listP[2][0].sZ

        if self.curve == False:
            #Draw basic line
            self.listC = [x0,y0,x1,y1]
        else:
            #Find parts
            parts = int((abs(x2-x0)+abs(y2-y0)+abs(z2-z0))/10)+1
            self.listC = []

            #Get the bezier curve coordinates
            for part in xrange(parts+1):
                t = 1.0*part/parts
                B = [0,0]
                B[0] = x0*(1-t)**2+2*(1-t)*t*x1+x2*t**2
                B[1] = y0*(1-t)**2+2*(1-t)*t*y1+y2*t**2
                self.listC.extend(B)

    def draw(self):
        self.step()
        #Draw the line
        for i in xrange(0,len(self.listC)-2,2):
            x0,y0 = self.listC[i],self.listC[i+1]
            x1,y1 = self.listC[i+2],self.listC[i+3]

            if (len(self.main.hitList)==0 or self != self.main.hitList[len(self.main.hitList)-1]) and self!=self.main.selected:
                self.main.canvas.create_line(x0,y0,x1,y1,fill=self.color,width=self.width)
            else:
                self.main.canvas.create_line(x0,y0,x1,y1,fill="white",width=self.width+2)
                self.main.canvas.create_line(x0,y0,x1,y1,fill=self.color,width=self.width)
                self.main.msg = "<Line: %s>" % (self.name)

    def hitTest(self):
        newX = []
        point = self.listC
        mouse = (self.main.mouseX,self.main.mouseY)
        r = self.width
        
        for i in xrange(0,len(point)-2,2):
            #Check between 2 points
            p1,p2 = i,i+2
            P1 = [1.0*point[p1%len(point)],1.0*point[(p1+1)%len(point)]]
            P2 = [1.0*point[p2%len(point)],1.0*point[(p2+1)%len(point)]]

            #If P1's x is bigger than P2's x, swap them
            if P1[0]>P2[0]:
                P1,P2 = copy.copy(P2),copy.copy(P1)

            #If the mouse y is within the bound
            if P1[1]-r<=mouse[1]<=P2[1]+r or P1[1]+r>=mouse[1]>=P2[1]-r:
                #Difference in x and y between P1 and P2
                x0 = P2[0]-P1[0]
                y0 = P2[1]-P1[1]

                #the distance between mouse and P1
                y1 = mouse[1]-P1[1]

                #If on a straight line
                if y0 == 0: x1 = x0
                else: x1 = y1/y0*x0
                
                if abs(mouse[0] - x1-P1[0])<=r:
                    return True
        return False
    
