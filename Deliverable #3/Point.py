from Utility import *

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
        self.draw()
        Point.pointList.append(self)
        Point.pointCount+=1
        
    def modelToXYConversion(self):
        #Use the scale and fixed vector to plot the screen X,Y,Z
        sV = self.main.scaleVector
        fV = self.main.fixedVector
        
        #Matrix Cross Product to find the screen coordinates
        self.sX = (self.x*sV[0][0]+self.y*sV[1][0]+self.z*sV[2][0])+fV[0]
        self.sY = (self.x*sV[0][1]+self.y*sV[1][1]+self.z*sV[2][1])+fV[1]
        self.sZ = (self.x*sV[0][2]+self.y*sV[1][2]+self.z*sV[2][2])+fV[2]
        return self.sX,self.sY,self.sZ
    
    def draw(self):
        self.modelToXYConversion()
        self.r = self.main.pointRadius
        
        #Get the variables from instance
        sX,sY,sZ = self.sX,self.sY,self.sZ
        x,y,z,color,r,n = self.x,self.y,self.z,self.color,self.r,self.name
        
        #if out of bound, do not draw
        if (self.sX>self.main.width+r or self.sY>self.main.boundY+r or
            self.sX<-r or self.sY<-r):
            return
        
        #If not the top hit by mouse and not selected, then dun highlight
        if ([self]==self.main.hitList[-1:] or self==self.main.selected):
            #Outline of 5
            self.main.canvas.create_oval(sX-r,sY-r,sX+r,sY+r,fill='',
                                         outline="white",width=5)
            
            if (self.main.mouseY<=self.main.boundY and
                [self]==self.main.hitList[-1:]):
                self.main.msg="<Point %s at X:%0.2f Y:%0.2f Z:%0.2f>"%(n,x,y,z)
        
        #Create the circle for the point        
        createCircle(self.main.canvas,sX,sY,r,color,r)    
            
    def hitTest(self):
        #if mouse in the circle
        mouse = (self.main.mouseX,self.main.mouseY)
        if hitTestCircle(self.sX,self.sY,self.r,mouse)==True:
            return True
        else:
            return False

class tempPoint(object):
    def __init__(self,x,y,z,name,color,mainInt):
        #X,Y,Z in vectors
        self.x,self.y,self.z = x,y,z
        self.color = color
        self.name = name
        self.main = mainInt

        #Actual screen X,Y,Z
        self.sX,self.sY,self.sZ = x,y,z
        
    def modelToXYConversion(self):
        #Use the scale and fixed vector to plot the screen X,Y,Z
        sV = self.main.scaleVector
        fV = self.main.fixedVector
        
        #Matrix Cross Product to find the screen coordinates
        self.sX = (self.x*sV[0][0]+self.y*sV[1][0]+self.z*sV[2][0])+fV[0]
        self.sY = (self.x*sV[0][1]+self.y*sV[1][1]+self.z*sV[2][1])+fV[1]
        self.sZ = (self.x*sV[0][2]+self.y*sV[1][2]+self.z*sV[2][2])+fV[2]
        return self.sX,self.sY,self.sZ
    
    def draw(self):
        #Update the location of this invisible point
        self.modelToXYConversion()
        self.main.XYtoModel()
        [self.x,self.y,self.z] = self.main.newPoint


