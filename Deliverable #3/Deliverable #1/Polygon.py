from Tkinter import *
import math
import copy
    
class Polygon(object):
    polyList = []
    polyCount = 0    

    @classmethod
    def getPolyList(cls):
        return Polygon.polyList

    @classmethod
    def getPolyCount(cls):
        return int(Polygon.polyCount)
    
    def __init__(self,listP,name,color,mainInt,width=3):
        self.listP = listP
        self.listC = []
        self.color = color
        self.canvas = mainInt.canvas
        self.width = width
        self.name = name
        self.main = mainInt
        self.sZ = 0
        Polygon.polyList.append(self)
        Polygon.polyCount += 1
    
    def step(self):
        #Get the average depth
        sumDepth = 0
        for point in self.listP:
            sumDepth += point[0].sZ    
        self.sZ = sumDepth/len(self.listP)
        
        self.listC = []

        i = 0
        lenOfPoints = len(self.listP)
        
        while i < lenOfPoints:            
            #If it is not a curve
            
            if self.listP[i][1] == 0 or i+1==lenOfPoints:
                x0,y0,z0 = self.listP[i][0].sX,self.listP[i][0].sY,self.listP[i][0].sZ
                self.listC.extend([x0,y0])
                i+=1
            else:
                #For curves
                n0,n1,n2 = i,(i+1)%lenOfPoints,(i+2)%lenOfPoints

                x0,y0,z0 = self.listP[n0][0].sX,self.listP[n0][0].sY,self.listP[n0][0].sZ
                x1,y1,z1 = self.listP[n1][0].sX,self.listP[n1][0].sY,self.listP[n1][0].sZ
                x2,y2,z2 = self.listP[n2][0].sX,self.listP[n2][0].sY,self.listP[n2][0].sZ

                #Find parts
                parts = int((abs(x2-x0)+abs(y2-y0)+abs(z2-z0))/10)+1

                #Get the bezier curve coordinates
                for part in xrange(parts):
                    t = 1.0*part/parts
                    B = [0,0]
                    B[0] = x0*(1-t)**2+2*(1-t)*t*x1+x2*t**2
                    B[1] = y0*(1-t)**2+2*(1-t)*t*y1+y2*t**2
                    self.listC.extend([B[0],B[1]])
                i+=2
            
    def draw(self):
        self.step()
        if (len(self.main.hitList)==0 or self != self.main.hitList[len(self.main.hitList)-1]) and self!=self.main.selected:
            self.main.canvas.create_polygon(self.listC,fill=self.color,outline=self.color,stipple="gray50")
        else:
            self.main.canvas.create_polygon(self.listC,fill=self.color,outline="white",width=self.width,stipple="gray50")
            self.main.msg = "<Polygon: %s>" % (self.name)

    def boundBox(self):
        if len(self.listC) == 0:
            return False
        
        xList = [self.listC[i] for i in xrange(len(self.listC)) if i%2==0]
        yList = [self.listC[i] for i in xrange(len(self.listC)) if i%2==1]

        if (min(xList)<=self.main.mouseX <=max(xList) and
            min(yList)<=self.main.mouseY <=max(yList)):
            return True
        else:
            return False
    
    def hitTest(self):
        newX = []
        point = self.listC
        mouse = (self.main.mouseX,self.main.mouseY)

        if self.boundBox()==False:
            return False

        for i in xrange(0,len(point),2):
            #Check between 2 points
            p1,p2 = i,i+2
            P1 = [1.0*point[p1%len(point)],1.0*point[(p1+1)%len(point)]]
            P2 = [1.0*point[p2%len(point)],1.0*point[(p2+1)%len(point)]]

            #If P1's x is bigger than P2's x
            if P1[0]>P2[0]:
                P1,P2 = copy.copy(P2),copy.copy(P1)

            #If the mouse y is within the bound
            if P1[1]<=mouse[1]<=P2[1] or P1[1]>=mouse[1]>=P2[1]:
                #Difference in x and y between P1 and P2
                x0 = P2[0]-P1[0]
                y0 = P2[1]-P1[1]

                #the distance between mouse and P1
                y1 = mouse[1]-P1[1]

                #If on a straight line
                if y0 == 0: x1 = x0
                else: x1 = y1/y0*x0

                #Get the x of the line at the mouse y
                newX.append(x1+P1[0])

        #Remove potential duplicates
        newX = list(set(newX))

        check = 0
        for i in xrange(len(newX)):
            if newX[i]<mouse[0]:
                check += 1

        #Check raycast for even and odd
        if check%2 == 1: return True
        else: return False
        
