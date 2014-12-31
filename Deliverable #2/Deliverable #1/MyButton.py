from Tkinter import *
import math
import copy
import random

class MyButton(object):

    buttonList = []
    listOfNames = ["AddPointButton","AddLineButton","AddCurveButton","AddPolyButton",
                   "DeleteButton","ZoomInButton","ZoomOutButton","LoadButton","SaveButton",
                   "ClearScreenButton","ColorButton"]

    @classmethod
    def getButtonList(cls):
        return MyButton.buttonList
    
    def __init__(self,w,h,x0,y0,main,name=""):    
        self.width = w
        self.height = h
        self.x0 = x0
        self.y0 = y0
        self.main = main
        self.listC = []
        self.name = name
        MyButton.buttonList.append(self)

    def draw(self):
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        
        if self.hitTest()==True and self.name in MyButton.listOfNames:
            if self.main.isMouse == False:
                color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            else:
                color1,color2,color3 = "#008800","#00CC00","#CCFFCC"
            
        x0,y0,x1,y1 = self.x0,self.y0,self.width+self.x0,self.height+self.y0
        self.listC = self.roundedButtonCood(x0,y0,x1,y1)
        self.main.canvas.create_polygon(self.listC,fill=color1,width=1)
        self.listC = self.roundedButtonCood(x0+1,y0+1,x1-1,y1-1)
        self.main.canvas.create_polygon(self.listC,fill=color3,width=1)
        self.listC = self.roundedButtonCood(x0+2,y0+2,x1-2,y1-2)
        self.main.canvas.create_polygon(self.listC,fill=color2,width=1)
        self.listC = self.roundedButtonCood(x0+3,y0+3,x1-3,y1-3)

        if self.name == "ColorButton":
            color3 = self.main.color
        elif self.name == "ClearScreenButton":
            color3 = "#000000"
        self.main.canvas.create_polygon(self.listC,fill=color3,width=1)
        
        self.listC = self.roundedButtonCood(x0,y0,x1,y1)
        
        cx,cy = (x0+x1)/2,(y0+y1)/2
        if self.name == "AddPointButton":
            r = (x1-x0)*0.1
            self.main.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="blue")
        elif self.name == "AddLineButton":
            r = (x1-x0)*0.2
            self.main.canvas.create_line(cx-r,cy+r,cx+r,cy-r,fill="blue",width = 3)
        elif self.name == "AddCurveButton":
            r = (x1-x0)*0.7
            self.main.canvas.create_arc(x0,y1,x0+r,y1-r,outline="blue",fill="",width = 3,style=ARC)
        elif self.name == "AddPolyButton":
            if self.main.keyCPressed == False:
                r = (x1-x0)*0.2
                self.main.canvas.create_polygon(cx,y0+r,x0+r,y1-r,x1-r,y1-r,fill="blue",width = 3)
            else:
                r = (x1-x0)*0.7
                self.main.canvas.create_arc(x0,y1,x0+r,y1-r,outline="blue",fill="blue",width = 3)
        elif self.name == "DeleteButton" or self.name=="ClearScreenButton":
            r = (x1-x0)*0.2
            self.main.canvas.create_line(cx-r,cy+r,cx+r,cy-r,fill="red",width = 3)
            self.main.canvas.create_line(cx-r,cy-r,cx+r,cy+r,fill="red",width = 3)
        elif self.name == "ZoomInButton" or self.name=="ZoomOutButton":
            r = (x1-x0)*0.4
            self.main.canvas.create_oval(cx-r,cy-r,cx,cy,fill="white",width=1)
            if self.name == "ZoomInButton":
                self.main.canvas.create_text(cx+r/2,cy-r/2,text="+")
            else:
                self.main.canvas.create_text(cx+r/2,cy-r/2,text="-")
            r = (x1-x0)*0.3
            self.main.canvas.create_line(cx,cy,cx+r,cy+r,fill="blue",width=3)
        elif self.name == "LoadButton":
            diffX = x1-x0
            diffY = y1-y0
            tempListP = [x0+0.4*diffX,y0+0.3*diffX,x0+0.3*diffX,y0+0.75*diffX,
                         x0+0.7*diffX,y0+0.75*diffX,x0+0.8*diffX,y0+0.3*diffX]
            self.main.canvas.create_polygon(tempListP,fill="yellow",width=1,outline='black')
            tempListP = [x0+0.2*diffX,y0+0.4*diffX,x0+0.3*diffX,y0+0.75*diffX,
                         x0+0.7*diffX,y0+0.75*diffX,x0+0.6*diffX,y0+0.4*diffX]
            self.main.canvas.create_polygon(tempListP,fill="yellow",width=1,outline='black')
        elif self.name == "SaveButton":
            diffX = x1-x0
            diffY = y1-y0
            tempListP = [x0+0.2*diffX,y0+0.2*diffX,x0+0.8*diffX,y0+0.2*diffX,
                         x0+0.8*diffX,y0+0.8*diffX,x0+0.2*diffX,y0+0.8*diffX]
            self.main.canvas.create_polygon(tempListP,fill="white",width=1,outline='black')
            tempListP = [x0+0.3*diffX,y0+0.5*diffX,x0+0.7*diffX,y0+0.5*diffX,
                         x0+0.7*diffX,y0+0.8*diffX,x0+0.3*diffX,y0+0.8*diffX]
            self.main.canvas.create_polygon(tempListP,fill="white",width=1,outline='black')
            tempListP = [x0+0.2*diffX,y0+0.2*diffX,x0+0.8*diffX,y0+0.2*diffX,
                         x0+0.8*diffX,y0+0.4*diffX,x0+0.2*diffX,y0+0.4*diffX]
            self.main.canvas.create_polygon(tempListP,fill="blue",width=1,outline='black')
            tempListP = [x0+0.35*diffX,y0+0.2*diffX,x0+0.65*diffX,y0+0.2*diffX,
                         x0+0.65*diffX,y0+0.4*diffX,x0+0.35*diffX,y0+0.4*diffX]
            self.main.canvas.create_polygon(tempListP,fill="gray",width=1,outline='black')
        elif self.name == "MessageButton":
            self.main.canvas.create_text(x0+5,(y0+y1)/2,anchor="w",text=self.main.msg)
            

    def roundedButtonCood(self,x0,y0,x1,y1):
        r = 5
        self.listC = []
        
        self.listC.extend([x0,y0+r])
        self.listC.extend([x0+r/2,y0+r/2])
        self.listC.extend([x0+r,y0])

        self.listC.extend([x1-r,y0])
        self.listC.extend([x1-r/2,y0+r/2])
        self.listC.extend([x1,y0+r])

        self.listC.extend([x1,y1-r])
        self.listC.extend([x1-r/2,y1-r/2])
        self.listC.extend([x1-r,y1])

        self.listC.extend([x0+r,y1])
        self.listC.extend([x0+r/2,y1-r/2])
        self.listC.extend([x0,y1-r])
        return self.listC
    
    def buttonPressed(self):
        if self.hitTest()==True:
            
            if self.name == "AddPointButton":
                self.main.modeReset()
                self.main.isAddPoint = True
            elif self.name == "AddLineButton":
                self.main.modeReset()
                self.main.isAddLine = True
            elif self.name == "AddCurveButton":
                self.main.modeReset()
                self.main.isAddCurve = True
            elif self.name == "AddPolyButton":
                self.main.modeReset()
                self.main.isAddPoly = True
            elif self.name == "DeleteButton":
                self.main.isDelete = True
            elif self.name == "ColorButton":
                self.main.isChangeColor = True
            elif self.name == "ZoomInButton":
                for point in self.main.scaleVector:
                    point[0]*=2
                    point[1]*=2
                    point[2]*=2
            elif self.name == "ZoomOutButton":
                self.main.modeReset()
                for point in self.main.scaleVector:
                    point[0]/=2
                    point[1]/=2
                    point[2]/=2
            elif self.name == "LoadButton":
                self.main.modeReset()
                self.main.loadFile()
            elif self.name == "SaveButton":
                self.main.modeReset()
                self.main.saveFile()
            elif self.name == "ClearScreenButton":
                self.main.modeReset()
                self.main.deleteObjects()
        
            
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
                P1,P2 = copy.copy(P2), copy.copy(P1)

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
       
class MyArrow(MyButton):
    arrowList = []
    @classmethod
    def getArrowList(cls):
        return MyArrow.arrowList
    
    def __init__(self,w,h,x0,y0,direction,main,motion=0):    
        self.width = w
        self.height = h
        self.x0 = x0
        self.y0 = y0
        self.main = main
        self.direction = direction
        self.motion = motion
        self.listC = []
        
        dirs = [[0,-1],[1,0],[0,1],[-1,0]]
        self.dirs = dirs[direction-1]
        MyArrow.arrowList.append(self)

    def draw(self):
        color1,color2,color3 = "#888888","#CCCCCC","#DDDDDD"
        if self.hitTest()==True:
            color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            
        x0,y0,x1,y1 = self.x0,self.y0,self.width+self.x0,self.height+self.y0
        self.listC = self.roundedArrowCood(x0,y0,x1,y1)
        self.main.canvas.create_polygon(self.listC,fill=color1,width=1,outline=color2)
        self.listC = self.roundedArrowCood(x0+2,y0+2,x1-2,y1-2)
        self.main.canvas.create_polygon(self.listC,fill=color3,width=1,outline=color2)
        self.listC = self.roundedArrowCood(x0+5,y0+5,x1-5,y1-5)
        self.main.canvas.create_polygon(self.listC,fill=color2,width=1,outline=color2)
        self.listC = self.roundedArrowCood(x0+7,y0+7,x1-7,y1-7)
        self.main.canvas.create_polygon(self.listC,fill=color3,width=1,outline=color2)
        self.listC = self.roundedArrowCood(x0,y0,x1,y1)
        
    def roundedArrowCood(self,x0,y0,x1,y1):
        self.listC = []
        if self.direction % 2 == 1:
            if self.direction == 3:
                y0,y1 = y1,y0
                
            self.listC.extend([x0,(y0+y1)/2])
            self.listC.extend([(x0+x1)/2,y0])
            self.listC.extend([x1,(y0+y1)/2])
                
            tempX = x0+(x1-x0)*0.75
            self.listC.extend([tempX,(y0+y1)/2])
            self.listC.extend([tempX,y1])
                
            tempX = x0+(x1-x0)*0.25
            self.listC.extend([tempX,y1])
            self.listC.extend([tempX,(y0+y1)/2])
        else:
            if self.direction == 2:
                x0,x1 = x1,x0
            
            self.listC.extend([(x0+x1)/2,y0])
            self.listC.extend([x0,(y0+y1)/2])
            self.listC.extend([(x0+x1)/2,y1])
                
            tempY = y0+(y1-y0)*0.75
            self.listC.extend([(x0+x1)/2,tempY])
            self.listC.extend([x1,tempY])
                
            tempY = y0+(y1-y0)*0.25
            self.listC.extend([x1,tempY])
            self.listC.extend([(x0+x1)/2,tempY])

        return self.listC
    

class Sphere(object):
    sphereList = []
    @classmethod
    def getSphereList(cls):
        return Sphere.sphereList
    
    def __init__(self,r,x0,y0,main):
        self.r = r
        self.x0 = x0
        self.y0 = y0
        self.main = main
        Sphere.sphereList.append(self)
        
    def rgbString(self, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)
    
    def draw(self):
        cx,cy,r = self.x0,self.y0,self.r
        self.createCircle(cx,cy,r)

    def createCircle(self,cx,cy,r):
        if r<5:
            return
        elif self.r!=r:
            red = int(1.0*(self.r-r)/self.r*255)
            green = int(1.0*(self.r-r)/self.r*255)
            color = self.rgbString(red,green,255)
            self.main.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)
            self.createCircle(cx,cy-1,r-2)
        else:
            red = int(1.0*(self.r-r)/self.r*255)
            green = int(1.0*(self.r-r)/self.r*255)
            color = self.rgbString(red,green,255)

            if self.hitTest()==True:
                color1 = "#00CC00"
            else:
                color1 = "#CCCCCC"
            
            self.main.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=3,outline=color1)
            self.createCircle(cx,cy-1,r-2)

    def hitTest(self):
        if ((self.main.mouseX-self.x0)**2+(self.main.mouseY-self.y0)**2)<self.r**2:
            return True
        else:
            return False


class MySlider(object):
    sliderList = []
    @classmethod
    def getSliderList(cls):
        return MySlider.sliderList
    
    def __init__(self,r,x,y,size,x0,y0,main,color):
        self.r = r
        self.x = x
        self.y = y
        self.x0 = x0
        self.y0 = y0
        self.size = size
        self.main = main
        self.color = color
        MySlider.sliderList.append(self)

    def draw(self):
        r,size=self.r,self.size
        x,y = self.x,self.y
        x0,y0 = self.x0,self.y0
        color1,color2 = "#CCCCCC",self.color
        self.main.canvas.create_line(x0,y0,x0,y0+size,fill=color1,width=5)
        self.main.canvas.create_line(x0,y0,x0,y0+size,fill=color2,width=1)


        color1,color2,color3 = "#888888","#CCCCCC",self.color
        
        if self.hitTest()==True:
            if self.main.isMouse == False:
                color1,color2,color3 = "#CCCCCC","#FFFFFF",self.color
            else:
                color1,color2,color3 = "#777777","#AAAAAA",self.color
            
        
        self.listC = [x-r,y-r,x+r,y+r]
        self.main.canvas.create_oval(self.listC,fill=color1,width=0)
        self.listC = [x-r+1,y-r+1,x+r-1,y+r-1]
        self.main.canvas.create_oval(self.listC,fill=color3,width=0)
        self.listC = [x-r+2,y-r+2,x+r-2,y+r-2]
        self.main.canvas.create_oval(self.listC,fill=color2,width=0)
        self.listC = [x-r+3,y-r+3,x+r-3,y+r-3]
        self.main.canvas.create_oval(self.listC,fill=color3,width=0)


    def hitTest(self):
        if ((self.main.mouseX-self.x)**2+(self.main.mouseY-self.y)**2)<self.r**2:
            return True
        else:
            return False
