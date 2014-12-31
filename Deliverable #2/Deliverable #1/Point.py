from Tkinter import *
import math
import copy
class Point(object):
    pointList = []
    pointCount = 0
    @classmethod
    def getPointList(cls):
        return Point.pointList
    
    @classmethod
    def getPointCount(cls):
        return int(Point.pointCount)
    
    def __init__(self,x,y,z,name,color,mainInt):
        #X,Y,Z in vectors
        self.x,self.y,self.z = x,y,z
        self.color = color
        self.name = name
        self.main = mainInt
        
        #Radius of the circle
        self.r = 10

        #Actual screen X,Y,Z
        self.sX,self.sY,self.sZ = x,y,z

        Point.pointList.append(self)
        Point.pointCount+=1
        
    def modelToXYConversion(self):
        sV = self.main.scaleVector
        fV = self.main.fixedVector
        
        self.sX = (self.x*sV[0][0]+self.y*sV[1][0]+self.z*sV[2][0])+fV[0]
        self.sY = (self.x*sV[0][1]+self.y*sV[1][1]+self.z*sV[2][1])+fV[1]
        self.sZ = (self.x*sV[0][2]+self.y*sV[1][2]+self.z*sV[2][2])+fV[2]
        return self.sX,self.sY,self.sZ
    
    def draw(self):
        self.modelToXYConversion()
        r = self.r

        if (len(self.main.hitList)==0 or self != self.main.hitList[len(self.main.hitList)-1]) and self!=self.main.selected:
            self.createCircle(self.sX,self.sY,r)
            listCood = [self.sX,self.sY-r,self.sX-r,self.sY-r/2,self.sX,self.sY,self.sX+r,self.sY-r/2]
        else:
            self.createCircle(self.sX,self.sY,r)
            self.main.canvas.create_oval(self.sX-r,self.sY-r,self.sX+r,self.sY+r, fill='',outline="white",width=3)
            listCood = [self.sX,self.sY-r,self.sX-r,self.sY-r/2,self.sX,self.sY,self.sX+r,self.sY-r/2]
            self.main.msg = "<Point %s at X:%0.2f Y:%0.2f Z:%0.2f>" % (self.name,self.x,self.y,self.z)

    def rgbString(self, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)
    
    def createCircle(self,cx,cy,r):
        if r<1:
            return
        else:
            redNumber = int(self.color[1:],16)/(2**16)
            greenNumber = (int(self.color[1:],16)/(2**8))%(2**8)
            blueNumber = int(self.color[1:],16)%(2**8)

            red = int(1.0*(self.r-r)/self.r*(255-redNumber)+redNumber)
            green = int(1.0*(self.r-r)/self.r*(255-greenNumber)+greenNumber)
            blue = int(1.0*(self.r-r)/self.r*(255-blueNumber)+blueNumber)
            
            color = self.rgbString(red,green,blue)
            self.main.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)
            self.createCircle(cx,cy-1,r-2)
        
    def hitTest(self):
        if (self.r**2>=((self.main.mouseX-self.sX)**2+(self.main.mouseY-self.sY)**2)):
            return True
        else:
            return False
