from Utility import *

       
class MyButton(object):

    buttonList = []
    listOfNames = ["MessageButton","MessageButton2","","TutorialPanel"]

    helpMessage = {
"AddPointButton":"Add point \non screen",
"AddLineButton":"Add line \non screen",
"AddCurveButton":"Add curve \non screen",
"AddPolyButton":"""Add polygon on screen.
Press <c> to alterate \nregular and curve mode
Press <Enter> to end""",
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
"StandardViewButton":"Change back to \ndefault view",
"HelpButton":"Replay Tutorial"}

    @classmethod
    def getButtonList(cls):
        return MyButton.buttonList
    
    def __init__(self,w,h,x0,y0,main,name=""):
        #Button attributes
        self.width = w
        self.height = h
        self.x0 = x0
        self.y0 = y0
        self.main = main
        self.listC = []
        self.name = name
        #Obtain Help messages from the class dictionary
        if self.name in MyButton.helpMessage:
            self.helpMessage = MyButton.helpMessage[self.name]
        else:
            self.helpMessage = ""
        
        #Only add to the list if it is true button
        if type(self)==MyButton:
            MyButton.buttonList.append(self)

    def draw(self):
        #Color for button UI
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        
        #Buttons must be pressable
        if self.hitTest()==True and self.name not in MyButton.listOfNames:
            #If mouse down is true
            if self.main.isMouse == False:
                color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            else:
                color1,color2,color3 = "#008800","#00CC00","#CCFFCC"
        
        #Create the buttons    
        x0,y0,x1,y1 = self.x0,self.y0,self.width+self.x0,self.height+self.y0
        self.listC = self.roundedButtonCood(x0,y0,x1,y1)
        self.main.canvas.create_polygon(self.listC,fill=color1,width=1)
        self.listC = self.roundedButtonCood(x0+1,y0+1,x1-1,y1-1)
        self.main.canvas.create_polygon(self.listC,fill=color3,width=1)
        self.listC = self.roundedButtonCood(x0+2,y0+2,x1-2,y1-2)
        self.main.canvas.create_polygon(self.listC,fill=color2,width=1)
        self.listC = self.roundedButtonCood(x0+3,y0+3,x1-3,y1-3)
        
        #If the button is called color button, change customerisation
        if self.name == "ColorButton":
            color3 = self.main.color
        elif self.name == "ClearScreenButton":
            color3 = "#000000"
        self.main.canvas.create_polygon(self.listC,fill=color3,width=1)
        
        self.listC = self.roundedButtonCood(x0,y0,x1,y1)
        
        #Draw specific button
        self.drawIndButtons(x0,y0,x1,y1)
        
    def drawIndButtons(self,x0,y0,x1,y1):
        cx,cy = (x0+x1)/2,(y0+y1)/2
        canvas = self.main.canvas
        textFont = "Ariel 5"
        
        #The drawing for various buttons
        if self.name == "AddPointButton":
            r = (x1-x0)*0.1
            #draw a point
            canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="blue")
        elif self.name == "AddLineButton":
            r = (x1-x0)*0.2
            #Draw a line
            canvas.create_line(cx-r,cy+r,cx+r,cy-r,fill="blue",width=3)           
        elif self.name == "AddCurveButton":
            r = (x1-x0)*0.7
            #Draw an arc
            canvas.create_arc(x0,y1,x0+r,y1-r,outline="blue",
                              fill="",width=3,style=ARC)
        elif self.name == "AddPolyButton":
            if self.main.keyCPressed == False:
                r = (x1-x0)*0.2
                #Draw a triangle
                canvas.create_polygon(cx,y0+r,x0+r,y1-r,x1-r,
                                      y1-r,fill="blue",width=3)
            else:
                r = (x1-x0)*0.7
                #Draw a quarter
                canvas.create_arc(x0,y1,x0+r,y1-r,
                                  outline="blue",fill="blue",width=3)                
        elif self.name == "DeleteButton" or self.name=="ClearScreenButton":
            r = (x1-x0)*0.2
            #Draw cross(X)
            canvas.create_line(cx-r,cy+r,cx+r,cy-r,fill="red",width=3)
            canvas.create_line(cx-r,cy-r,cx+r,cy+r,fill="red",width=3)            
        elif self.name == "ZoomInButton" or self.name=="ZoomOutButton":
            r = (x1-x0)*0.4
            #Draw magnifying glass
            canvas.create_oval(cx-r,cy-r,cx,cy,fill="white",width=1)
            #Draw + or -
            if self.name == "ZoomInButton":
                canvas.create_text(cx+r/2,cy-r/2,text="+")
            else:
                canvas.create_text(cx+r/2,cy-r/2,text="-")
            r = (x1-x0)*0.3
            #Draw the handle for the magnifying glass
            canvas.create_line(cx,cy,cx+r,cy+r,fill="blue",width=3)          
        elif self.name == "LoadButton":
            diffX = x1-x0
            diffY = y1-y0
            #load folder right polygon
            tempListP = [x0+0.4*diffX,y0+0.3*diffX,x0+0.3*diffX,y0+0.75*diffX,
                         x0+0.7*diffX,y0+0.75*diffX,x0+0.8*diffX,y0+0.3*diffX]
            canvas.create_polygon(tempListP,fill="yellow",
                                  width=1,outline='black')
            
            #Load folder left polygon
            tempListP = [x0+0.2*diffX,y0+0.4*diffX,x0+0.3*diffX,y0+0.75*diffX,
                         x0+0.7*diffX,y0+0.75*diffX,x0+0.6*diffX,y0+0.4*diffX]
            canvas.create_polygon(tempListP,fill="yellow",
                                  width=1,outline='black') 
        elif self.name == "SaveButton":
            diffX = x1-x0
            diffY = y1-y0
            
            #The whole disk
            tempListP = [x0+0.2*diffX,y0+0.2*diffX,x0+0.8*diffX,y0+0.2*diffX,
                         x0+0.8*diffX,y0+0.8*diffX,x0+0.2*diffX,y0+0.8*diffX]
            canvas.create_polygon(tempListP,fill="white",
                                  width=1,outline='black')
            
            #The disk center
            tempListP = [x0+0.3*diffX,y0+0.5*diffX,x0+0.7*diffX,y0+0.5*diffX,
                         x0+0.7*diffX,y0+0.8*diffX,x0+0.3*diffX,y0+0.8*diffX]
            canvas.create_polygon(tempListP,fill="white",
                                  width=1,outline='black')
            
            #The top of the disk
            tempListP = [x0+0.2*diffX,y0+0.2*diffX,x0+0.8*diffX,y0+0.2*diffX,
                         x0+0.8*diffX,y0+0.4*diffX,x0+0.2*diffX,y0+0.4*diffX]
            canvas.create_polygon(tempListP,fill="blue",
                                  width=1,outline='black')
            
            #The metal part of the floppy disk
            tempListP = [x0+0.35*diffX,y0+0.2*diffX,x0+0.65*diffX,y0+0.2*diffX,
                         x0+0.65*diffX,y0+0.4*diffX,x0+0.35*diffX,y0+0.4*diffX]
            canvas.create_polygon(tempListP,fill="gray",
                                  width=1,outline='black')
        elif self.name == "MessageButton":
            #Normal help message
            canvas.create_text(x0+5,(y0+y1)/2,anchor="w",text=self.main.msg)
        elif self.name == "MessageButton2":
            #Coordinate of mouse message
            canvas.create_text(x0+5,(y0+y1)/2,anchor="w",
                               text=self.main.coodInfo)
        elif self.name == "AddButton":
            canvas.create_text(cx,cy,text="Add",font=textFont)
        elif self.name == "ShiftButton":
            canvas.create_text(cx,cy,text="Shift",font=textFont)
        elif self.name == "MoveButton":
            canvas.create_text(cx,cy,text="Move\nTo",font=textFont)
        elif self.name == "CopyShiftButton":
            canvas.create_text(cx,cy,text="Copy\nShift",font=textFont)
        elif self.name == "RotateButton":
            canvas.create_text(cx,cy,text="Rotate",font=textFont)
        elif self.name == "ResizeButton":
            canvas.create_text(cx,cy,text="Resize",font=textFont)
        elif self.name == "TransparentButton":
            canvas.create_text(cx,cy,text="Trans.",font=textFont)
        elif self.name == "ChangePointButton":
            canvas.create_text(cx,cy,text="Change\nPoint",font=textFont)
        elif self.name == "BGColorButton":
            canvas.create_text(cx,cy,text="BG\nColor",font=textFont)
        elif self.name == "ShiftViewButton":
            canvas.create_text(cx,cy,text="Shift\nView",font=textFont)
        elif self.name == "RotateViewButton":
            canvas.create_text(cx,cy,text="Rotate\nView",font=textFont)
        elif self.name == "StandardViewButton":
            canvas.create_text(cx,cy,text="Stand.\nView",font=textFont)
        elif self.name == "HelpButton":
            canvas.create_text(cx,cy,text="Help",font=textFont)
            
    def roundedButtonCood(self,x0,y0,x1,y1):
        r = 5
        self.listC = []
        
        #The top left rounded corner
        self.listC.extend([x0,y0+r])
        self.listC.extend([x0+r/2,y0+r/2])
        self.listC.extend([x0+r,y0])
        
        #The top right rounded corner
        self.listC.extend([x1-r,y0])
        self.listC.extend([x1-r/2,y0+r/2])
        self.listC.extend([x1,y0+r])
        
        #The botton left
        self.listC.extend([x1,y1-r])
        self.listC.extend([x1-r/2,y1-r/2])
        self.listC.extend([x1-r,y1])
        
        #Bottom right
        self.listC.extend([x0+r,y1])
        self.listC.extend([x0+r/2,y1-r/2])
        self.listC.extend([x0,y1-r])
        return self.listC
    
    def buttonPressed(self):
        #All the button events
        if self.hitTest()==True:
            if self.name == "ColorButton":self.main.isChangeColor = True
            elif self.name == "ZoomInButton":self.main.zoom(2.0)
            elif self.name == "ZoomOutButton":self.main.zoom(0.5)
            elif self.name == "StandardViewButton":self.main.standardView()
            elif self.name == "RotateViewButton":self.main.rotateView()
            elif self.name == "ShiftViewButton":self.main.shiftView()
            elif self.name == "BGColorButton":self.main.bgColorChange()
            elif self.name == "ChangePointButton":self.main.changePointSize()
            elif self.name =="TransparentButton":self.main.changeTransparency()
            else:
                self.main.modeReset()
                if self.name == "AddPointButton":self.main.isAddPoint = True
                elif self.name == "AddLineButton":self.main.isAddLine = True
                elif self.name == "AddCurveButton":self.main.isAddCurve = True
                elif self.name == "AddPolyButton":self.main.isAddPoly = True
                elif self.name == "DeleteButton":self.main.isDelete = True
                elif self.name == "LoadButton":self.main.loadFile()
                elif self.name == "SaveButton":self.main.saveFile()
                elif self.name == "ClearScreenButton":self.main.deleteObjects()
                elif self.name == "AddButton":self.main.addPointByText()
                elif self.name == "ShiftButton":self.main.shiftPointByText()
                elif self.name == "MoveButton":self.main.movePointByText()
                elif self.name == "CopyShiftButton":self.main.copyPointByText()
                elif self.name == "RotateButton":self.main.rotatePointByText()
                elif self.name == "ResizeButton":self.main.resizePointByText()
                elif self.name == "HelpButton":self.main.tutorialInit()
                    
    def hitTest(self):
        #If the button gets mouse over
        if rayCast(self.listC,(self.main.mouseX,self.main.mouseY)):
            return True
        else:
            return False

class MyTutorial(MyButton):
    allText = {
0: """Welcome to\n 3D Mini-Modelling!""",
1: """Click on this button to add a point to screen.
The point is generated using mouse and Mouse Z textbox""",
2: """Click on this button to add a line to screen
by linking 2 existing points or adding new ones.""",
3: """Click on this button to add a curve to screen
by linking 3 existing points or adding new ones.

The 2nd point is the control point.""",
4: """Click on this button to add a polygon to screen
by linking n existing points or adding new ones.

You can change between curved polygon
and regular one by pressing <C> on keyboard.""",
5: """To complete the drawing of the polygon,
press <Enter> on the keyboard
or click on the first point in the polygon.
Incomplete lines, curves and polygons will not be drawn.""",
6: """Click on this button to delete a selected object.

Alternatively, you can also hold
<DELETE> on the keyboard for multiple deletion.""",
7: """Click on this button to change color
for a selected object""",
8: """Click on this button to zoom in.

Alternatively, you can press <+> on the keyboard.""",
9: """Click on this button to zoom out

Alternatively, you can press <_> on the keyboard.

Take note both zoom in and zoom out has a limit""",
10: """Click on this button to load a .mdl file""",
11: """Click on this button to save a .mdl file""",
12: """Click on this button to remove
all the objects on screen""",
13: """Click on this button to add a point on X,Y,Z
using the 3 textboxes X,Y,Z.

Take note that text inputs cannot
contain non-number elements
and there is a limit on the length of input.""",
14: """Click on this button to shift a point by X,Y,Z
using the 3 textboxes X,Y,Z.""",
15: """Click on this button to move an object to X,Y,Z
using the 3 textboxes X,Y,Z.""",
16: """Click on this button to copy and shift an object
by X,Y,Z using the 3 textboxes X,Y,Z.""",
17: """Click on this button to rotate a non-point object
about its center by XY,YZ,ZX
using the 3 textboxes XY,YZ,ZX.""",
18: """Click on this button to resize a non-point object
about its center by X,Y,Z using the 3 textboxes X,Y,Z.

The default resize scale is 1.

Input 0 is taken to be 1 in this case.""",
19: """Click on this button to
change the size of the point
from big to small and vice versa.

Useful for viewing and editing points""",
20: """Click on this button to
change the transparency of polygons.""",
21: """Click on this button to change
the background color.""",
22: """Click on this button to shift the view
by X, Y, Z using the 3 textboxes X,Y,Z.

There is a limit on the view.""",
23: """Alternatively, you can click
on the triangular buttons to shift around.

Another way is to hold the arrow keys to move around.""",
24: """Click on this button to rotate the view
by XY, YZ, ZX using the 3 textboxes XY,YZ,ZX.""",
25: """Alternatively, you can click on the rotation sphere
on the right to rotate the view.

Another way is to hold <R> on the keyboard and
the arrow keys to move around.""",
26: """Click on this button to change the view
back to default view.""",
27: """End of Tutorial"""
}
        
    allButtons = {
1: "AddPointButton",
2: "AddLineButton",
3: "AddCurveButton",
4: "AddPolyButton",
5: "AddPolyButton",
6: "DeleteButton",
7: "ColorButton",
8: "ZoomInButton",
9: "ZoomOutButton",
10: "LoadButton",
11: "SaveButton",
12: "ClearScreenButton",
13: "AddButton",
14: "ShiftButton",
15: "MoveButton",
16: "CopyShiftButton",
17: "RotateButton",
18: "ResizeButton",
19: "ChangePointButton",
20: "TransparentButton",
21: "BGColorButton",
22: "ShiftViewButton",
23: "ShiftViewButton",
24: "RotateViewButton",
25: "RotateViewButton",
26: "StandardViewButton"
    }    

    endText = """Click anywhere to continue.
Press <Q> to quit. Press arrow keys to move forward and backward.
Application is frozen during tutorial."""    
    
    tutorialList = []
    @classmethod
    def getTutorialList(cls):
        return MyTutorial.tutorialList
    
    def __init__(self,w,h,x0,y0,main,name=""):
        #Tutorial attributes
        self.width = w
        self.height = h
        self.x0 = x0
        self.y0 = y0
        self.main = main
        self.listC = []
        self.name = name
        
        #Load the super class
        super(MyTutorial,self).__init__(w,h,x0,y0,main)
        MyTutorial.tutorialList.append(self)
        
    def draw(self):
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        f1, f2, f3, f4 = "Ariel 24","Ariel 12","Ariel 12 bold","Ariel 8"
        
        maxTutorial = 27
        canvas = self.main.canvas
        
        #Draw rounded tutorial interface   
        x0,y0,x1,y1 = self.x0,self.y0,self.width+self.x0,self.height+self.y0
        self.listC = self.roundedButtonCood(x0,y0,x1,y1)
        canvas.create_polygon(self.listC,fill=color1,width=1)
        self.listC = self.roundedButtonCood(x0+1,y0+1,x1-1,y1-1)
        canvas.create_polygon(self.listC,fill=color3,width=1)
        self.listC = self.roundedButtonCood(x0+2,y0+2,x1-2,y1-2)
        canvas.create_polygon(self.listC,fill=color2,width=1)
        self.listC = self.roundedButtonCood(x0+3,y0+3,x1-3,y1-3)
        canvas.create_polygon(self.listC,fill=color3,width=1)
        self.listC = self.roundedButtonCood(x0,y0,x1,y1)
        
        cx,cy = (x0+x1)/2,(y0+y1)/2
        
        tutTxt = MyTutorial.allText[self.main.tutorialStep]
        if self.main.tutorialStep==0 or self.main.tutorialStep==maxTutorial:
            #The start and the end use bolder letters
            canvas.create_text(cx,cy,text=tutTxt,font=f1,justify="center")
        else:
            #Page number
            stepTxt = "Page %d out of 26" % (self.main.tutorialStep)
            canvas.create_text(cx,y0,text=stepTxt,font=f3,
                               justify="center",anchor='n')
            
            #information in tutorial
            canvas.create_text(cx,cy,text=tutTxt,font=f2,justify="center")
            
            #Draw a red arrow pointing to the 
            self.drawArrow(MyTutorial.allButtons[self.main.tutorialStep])
            
            #Draw red box
            self.drawBox()

        #Ending text
        endT = MyTutorial.endText
        if self.main.tutorialStep==maxTutorial:
            endT += "\nDemos are available in MDL folder"
        elif self.main.tutorialStep==0:
            endT += "\nFor first timer, please read through the tutorial."
        canvas.create_text(cx,y1,text=endT,font=f4,justify="center",anchor="s")
        
    def drawArrow(self,buttonName):
        x,y=0,0
        lenOfArrow = 20
        widthOfArrow = 10
        
        exceptSteps=[23,25]
        
        #Get the button's x and y
        for i in MyButton.getButtonList():
            if i.name == buttonName:
                x,y = i.x0,i.y0
        
        #Only for these 2 steps, the x and y are different
        if self.main.tutorialStep == exceptSteps[0]:
            x,y = 500,450
        elif self.main.tutorialStep == exceptSteps[1]:
            x,y = 650,420
        
        #Draw an red arrow    
        self.main.canvas.create_line(x,y,x-lenOfArrow,y-lenOfArrow,
                                     width=10,fill="red",arrow="first")

    def drawBox(self):
        #Draw bounding boxes for tutorial
        if self.main.tutorialStep in [1]:
            self.main.canvas.create_rectangle(10,410,200,450,fill=""
                                              ,width=5,outline="red")
        elif self.main.tutorialStep in [13,14,15,16,18,22]:
            self.main.canvas.create_rectangle(10,450,100,550,fill="",
                                              width=5,outline="red")
        elif self.main.tutorialStep in [17,24]:
            self.main.canvas.create_rectangle(100,450,200,550,fill="",
                                              width=5,outline="red")
        elif self.main.tutorialStep in [21]:
            self.main.canvas.create_rectangle(375,410,415,590,fill="",
                                              width=5,outline="red") 
    
class MyArrow(MyButton):
    arrowList = []
    @classmethod
    def getArrowList(cls):
        return MyArrow.arrowList
    
    def __init__(self,w,h,x0,y0,direction,main):
        #Arrow attributes
        self.width = w
        self.height = h
        self.x0 = x0
        self.y0 = y0
        self.main = main
        self.direction = direction
        self.listC = []
        
        dirs = [[0,-1],[1,0],[0,1],[-1,0]]
        self.dirs = dirs[direction-1]
        MyArrow.arrowList.append(self)

    def draw(self):
        #Color selection
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        if self.hitTest()==True:
            if self.main.isMouse == False:
                color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            else:
                color1,color2,color3 = "#008800","#00CC00","#CCFFCC"
        
        #Draw fancy triangle button
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
        #Get the coordinates by direction
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
        #Sphere attributes
        self.r = r
        self.x0 = x0
        self.y0 = y0
        self.main = main
        Sphere.sphereList.append(self)
    
    def draw(self):
        cx,cy,r = self.x0,self.y0,self.r
        canvas = self.main.canvas
        
        #Color selection
        color1,color2,color3 = "#888888","#CCCCCC","#FFFFFF"
        if self.hitTest()==True:
            if self.main.isMouse == False:
                color1,color2,color3 = "#008800","#00CC00","#FFFFFF"
            else:
                color1,color2,color3 = "#008800","#00CC00","#CCFFCC"
                
        canvas.create_oval(cx-r+0,cy-r+0,cx+r-0,cy+r-0,fill=color1,outline='')
        canvas.create_oval(cx-r+1,cy-r+1,cx+r-1,cy+r-1,fill=color3,outline='')
        canvas.create_oval(cx-r+2,cy-r+2,cx+r-2,cy+r-2,fill=color2,outline='')
        
        #Draw the circle
        createCircle(self.main.canvas,cx,cy,r-4,"#DDDDFF",r)

    def hitTest(self):
        mouse = (self.main.mouseX,self.main.mouseY)
        #Test for mouse over
        if hitTestCircle(self.x0,self.y0,self.r,mouse)==True:
            return True
        else:
            return False

class MySlider(object):
    sliderList = []
    @classmethod
    def getSliderList(cls):
        return MySlider.sliderList
    
    def __init__(self,r,x,y,size,x0,y0,main,color):
        #Slider attributes, the line and the circle
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
        
        #Line drawing
        self.main.canvas.create_line(x0,y0,x0,y0+size,fill=color1,width=5)
        self.main.canvas.create_line(x0,y0,x0,y0+size,fill=color2,width=1)

        #Color selection
        color1,color2,color3 = "#888888","#CCCCCC",self.color
        
        if self.hitTest()==True:
            if self.main.isMouse == False:
                color1,color2,color3 = "#CCCCCC","#FFFFFF",self.color
            else:
                color1,color2,color3 = "#777777","#AAAAAA",self.color
            
        #Nice circle drawing
        self.listC = [x-r,y-r,x+r,y+r]
        self.main.canvas.create_oval(self.listC,fill=color1,width=0)
        self.listC = [x-r+1,y-r+1,x+r-1,y+r-1]
        self.main.canvas.create_oval(self.listC,fill=color3,width=0)
        self.listC = [x-r+2,y-r+2,x+r-2,y+r-2]
        self.main.canvas.create_oval(self.listC,fill=color2,width=0)
        self.listC = [x-r+3,y-r+3,x+r-3,y+r-3]
        self.main.canvas.create_oval(self.listC,fill=color3,width=0)


    def hitTest(self):
        #Slider mouseover
        mouse = (self.main.mouseX,self.main.mouseY)
        if hitTestCircle(self.x,self.y,self.r,mouse)==True:
            return True
        else:
            return False
