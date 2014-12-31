from Utility import *

       
class MyButton(object):

    buttonList = []
    listOfNames = ["MessageButton","MessageButton2",""]

    helpMessage = {"AddPointButton":"Add point \non screen",
                   "AddLineButton":"Add line \non screen",
                   "AddCurveButton":"Add curve \non screen",
                   "AddPolyButton":"Add polygon \non screen. \nPress c to alterate \nregular and curve mode",
                   "DeleteButton":"Delete instance \non screen",
                   "ColorButton":"Color instance \non screen",
                   "ZoomInButton":"Zoom in",
                   "ZoomOutButton":"Zoom out",
                   "LoadButton":"Load",
                   "SaveButton":"Save",
                   "ClearScreenButton":"Clear the \nwhole screen",
                   "AddButton":"Add point using \nx,y,z",
                   "ShiftButton":"Shift instance \nby x,y,z",
                   "MoveButton":"Move instance \nto x,y,z",
                   "CopyShiftButton":"Copy and shift instance \nby x,y,z",
                   "RotateButton":"Rotate instance by \nxy,yz,zx about its center",
                   "ResizeButton":"Resize instance by \nmultiplying the scale x,y,z",
                   "ChangePointButton":"Change point size",
                   "TransparentButton":"Toggle \nTransparency",
                   "BGColorButton":"Change background \ncolor",
                   "ShiftViewButton":"Shift the view on \nscreen using x,y,z",
                   "RotateViewButton":"Rotate the view on \nscreen using xy,yz,zx",
                   "StandardViewButton":"Change back to \ndefault view"}

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
        if self.name in MyButton.helpMessage:
            self.helpMessage = MyButton.helpMessage[self.name]
        else:
            self.helpMessage = ""
        MyButton.buttonList.append(self)

    def draw(self):
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        
        if self.hitTest()==True and self.name not in MyButton.listOfNames:
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
        elif self.name == "MessageButton2":
            self.main.canvas.create_text(x0+5,(y0+y1)/2,anchor="w",text=self.main.coodInfo)
        elif self.name == "AddButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Add",font="Ariel 5")
        elif self.name == "ShiftButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Shift",font="Ariel 5")
        elif self.name == "MoveButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Move\nTo",font="Ariel 5")
        elif self.name == "CopyShiftButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Copy\nShift",font="Ariel 5")
        elif self.name == "RotateButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Rotate",font="Ariel 5")
        elif self.name == "ResizeButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Resize",font="Ariel 5")
        elif self.name == "TransparentButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Trans.",font="Ariel 5")
        elif self.name == "ChangePointButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Change\nPoint",font="Ariel 5")
        elif self.name == "BGColorButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="BG\nColor",font="Ariel 5")
        elif self.name == "ShiftViewButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Shift\nView",font="Ariel 5")
        elif self.name == "RotateViewButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Rotate\nView",font="Ariel 5")
        elif self.name == "StandardViewButton":
            self.main.canvas.create_text((x0+x1)/2,(y0+y1)/2,text="Stand.\nView",font="Ariel 5")
            
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
                self.main.modeReset()
                self.main.isDelete = True
            elif self.name == "ColorButton":
                self.main.isChangeColor = True
            elif self.name == "ZoomInButton":
                self.main.zoom(2.0)
            elif self.name == "ZoomOutButton":
                self.main.zoom(0.5)
            elif self.name == "LoadButton":
                self.main.modeReset()
                self.main.loadFile()
            elif self.name == "SaveButton":
                self.main.modeReset()
                self.main.saveFile()
            elif self.name == "ClearScreenButton":
                self.main.modeReset()
                self.main.deleteObjects()
            elif self.name == "AddButton":
                self.main.modeReset()
                self.main.addPointByText()
            elif self.name == "ShiftButton":
                self.main.modeReset()
                self.main.shiftPointByText()
            elif self.name == "MoveButton":
                self.main.modeReset()
                self.main.movePointByText()
            elif self.name == "CopyShiftButton":
                self.main.modeReset()
                self.main.copyPointByText()
            elif self.name == "RotateButton":
                self.main.modeReset()
                self.main.rotatePointByText()
            elif self.name == "ResizeButton":
                self.main.modeReset()
                self.main.resizePointByText()
            elif self.name == "StandardViewButton":
                self.main.standardView()
            elif self.name == "RotateViewButton":
                self.main.rotateView()
            elif self.name == "ShiftViewButton":
                self.main.shiftView()
            elif self.name == "BGColorButton":
                self.main.bgColorChange()
            elif self.name == "ChangePointButton":
                self.main.changePointSize()
            elif self.name == "TransparentButton":
                self.main.changeTransparency()
                
    def hitTest(self):
        if rayCast(self.listC,(self.main.mouseX,self.main.mouseY)):
            return True
        else:
            return False

       
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
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        if self.hitTest()==True:
            if self.main.isMouse == False:
                color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            else:
                color1,color2,color3 = "#008800","#00CC00","#CCFFCC"
                
        x0,y0,x1,y1 = self.x0,self.y0,self.width+self.x0,self.height+self.y0
        self.listC = self.roundedArrowCood(x0,y0,x1,y1)
        self.main.canvas.create_polygon(self.listC,fill=color1)
        self.listC = self.roundedArrowCood(x0+2,y0+2,x1-2,y1-2)
        self.main.canvas.create_polygon(self.listC,fill=color3)
        self.listC = self.roundedArrowCood(x0+4,y0+4,x1-4,y1-4)
        self.main.canvas.create_polygon(self.listC,fill=color2)
        self.listC = self.roundedArrowCood(x0+6,y0+6,x1-6,y1-6)
        self.main.canvas.create_polygon(self.listC,fill=color3)
        self.listC = self.roundedArrowCood(x0,y0,x1,y1)
        
    def roundedArrowCood(self,x0,y0,x1,y1):
        self.listC = []
        if self.direction % 2 == 1:
            if self.direction == 3:
                y0,y1 = y1,y0
                
            self.listC.extend([x0,y1])
            self.listC.extend([(x0+x1)/2,y0])
            self.listC.extend([x1,y1])
        else:
            if self.direction == 2:
                x0,x1 = x1,x0
            
            self.listC.extend([x1,y0])
            self.listC.extend([x0,(y0+y1)/2])
            self.listC.extend([x1,y1])
                
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
    
    def draw(self):
        cx,cy,r = self.x0,self.y0,self.r
        
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        if self.hitTest()==True:
            if self.main.isMouse == False:
                color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            else:
                color1,color2,color3 = "#008800","#00CC00","#CCFFCC"
                
        self.main.canvas.create_oval(cx-r+0,cy-r+0,cx+r-0,cy+r-0,fill=color1,outline='')
        self.main.canvas.create_oval(cx-r+1,cy-r+1,cx+r-1,cy+r-1,fill=color3,outline='')
        self.main.canvas.create_oval(cx-r+2,cy-r+2,cx+r-2,cy+r-2,fill=color2,outline='')
        createCircle(self.main.canvas,cx,cy,r-4,"#DDDDFF",r)

    def hitTest(self):
        if hitTestCircle(self.x0,self.y0,self.r,(self.main.mouseX,self.main.mouseY))==True:
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
        if hitTestCircle(self.x,self.y,self.r,(self.main.mouseX,self.main.mouseY))==True:
            return True
        else:
            return False
