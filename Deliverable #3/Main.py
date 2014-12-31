from Utility import *
from Point import *
from Polygon import *
from Line import *
from MyButton import *
import cPickle as pickle
import tkFileDialog 

class MainInterface(object):
    def __init__(self,width,height):
        self.run(width,height)
    
    '''
Taken and modified from Kosbie's website
    
Animation: http://www.kosbie.net/cmu/fall-13/15-112/handouts/Animation.py
    
Non-resizeble: http://www.kosbie.net/cmu/fall-11/15-112/handouts/
misc-demos/src/resizableDemo.py

Mouse Motion:
http://www.kosbie.net/cmu/fall-11/15-112/handouts/misc-demos/src/
mouseMotionEventsDemo.py

Mouse Event:
http://www.kosbie.net/cmu/fall-11/15-112/handouts/misc-demos/src/
mouseEventsDemo.py

Key Event:
http://www.kosbie.net/cmu/fall-11/15-112/handouts/misc-demos/src/
keyEventsDemo.py
'''

    def run(self, width=800, height=600):
        # create the root and the canvas
        root = Tk()
        #Not resizable
        root.resizable(width=FALSE, height=FALSE)
        self.width,self.height = width,height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        #Create textboxes
        self.textBoxCreation(root)
        
        # set up timerFired events
        self.timerFiredDelay = 40 # milliseconds
        
        # set up events
        def redrawAllWrapper():
            self.canvas.delete(ALL)
            self.redrawAll()
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def keyPressedWrapper(event):
            self.keyPressed(event)
            redrawAllWrapper()
        def keyReleasedWrapper(event):
            self.keyReleased(event)
            redrawAllWrapper()
        def mouseReleasedWrapper(event):
            self.mouseReleased(event)
            redrawAllWrapper()
        def mouseMotion(event):
            self.mouseX = event.x
            self.mouseY = event.y    
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)

        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<ButtonRelease-1>", mouseReleasedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        root.bind("<KeyRelease>", keyReleasedWrapper)
        self.canvas.bind("<Motion>", mouseMotion)
        
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()
    
    '''
Entry textbox modified from: http://effbot.org/tkinterbook/entry.htm
'''
    
    def textBoxCreation(self,root):
        commonX,tWidth,bd = [30,120],10,2
        commonY = [420,455,490,525]
        self.textBoxList = []
        
        #Create textboxes
        self.vzTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)
        self.xTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)
        self.yTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)
        self.zTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)
        self.xyTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)
        self.yzTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)
        self.zxTextBox=Entry(root,width=tWidth,borderwidth=bd,justify=RIGHT)

        self.textBoxList = [self.vzTextBox,self.xTextBox,self.yTextBox,
                            self.zTextBox,self.xyTextBox,self.yzTextBox,
                            self.zxTextBox]
        #init for textboxes
        for i in self.textBoxList:
            i.pack()
            i.insert(0,0)
        
        #Position the textboxes
        self.vzTextBox.place(x=commonX[1],y=commonY[0])
        self.xTextBox.place( x=commonX[0],y=commonY[1])
        self.yTextBox.place( x=commonX[0],y=commonY[2])
        self.zTextBox.place( x=commonX[0],y=commonY[3])
        self.xyTextBox.place(x=commonX[1],y=commonY[1])
        self.yzTextBox.place(x=commonX[1],y=commonY[2])
        self.zxTextBox.place(x=commonX[1],y=commonY[3])
        
    def init(self):
        w,h = self.width,self.height
        #The vector in which points in the model are scaled to 
        self.scaleVector = [[100.0,0.0,0.0],
                            [0.0,100.0,0.0],
                            [0.0,0.0,100.0]]
        
        #Fixed vector of the screen
        self.fixedVector = [1.0*w/2,1.0*(h/2)-100,0.0]
        #Center vector of the screen
        self.centerVector = [1.0*w/2,1.0*(h/2)-100,0.0]
        
        self.initMouseVar()
        self.initHelpMsg()
        self.initLists()
        self.initKey()
        self.modeReset()
        self.initColor()
        self.initLoadSave()
        self.initInterface()
    
        #Tutorial Mode
        self.tutorialMode = False
        self.tutorialStep = 0
        self.tutorialInit()
        
    def initMouseVar(self):
        #Mouse variables and model vector
        self.mouseX,self.mouseY = 0,0
        self.newPoint = [0.0,0.0,0.0]
        self.oldPoint = None
        self.oldMX,self.oldMY = 0,0
        self.isMouse = False
    
    def initHelpMsg(self):
        #Help message for users
        self.msg=""
        self.helpmsg=""
        self.coodInfo = ""
    
    def initLists(self):
        #List of draw objects, hit objects, drag objects
        self.drawList = []
        self.hitList = []
        self.dragList = []
        self.selected = None
    
    def initKey(self):
        #If the key is pressed, store the names
        self.keyCPressed = False
        self.keyDeletePressed = False
        self.keyRPressed = False
        self.dirKey = []

    def modeReset(self):
        #If the polygon has done curve mode in the previous point
        self.prevPointCurve = False
        #If the drawing is complete
        self.drawComplete = 0
        #Store the list of temporary points
        self.tempStorage = []
        
        #Mode for delayed button
        self.isAddPoint = False
        self.isAddCurve = False
        self.isAddLine = False
        self.isAddPoly = False
        self.isDelete = False
        self.isChangeColor = False
    
    def initColor(self):
        #Color of the sliders and background color
        self.color = "#FFFFFF"
        self.bgcolor = "#000000"
        
    def initLoadSave(self):
        #Load and Save file name
        self.filename = ""
        self.tutorialSave = None
        
    def initInterface(self):
        #Radius of point
        self.pointRadius = 10
        
        #Transparency
        self.transparent = True
        
        #Interface Creation
        self.boundY = 400
        self.myOtherInterfaceCreation()
        self.myButtonCreation()
        
        #Limit of points and view:
        self.limitP = 100
        self.limitV = self.limitP*100
        self.limitZ = [100.0/32,100.0*32]
        self.moveSpeed = 5.0
        self.epsilon = 0.000001

        #Demo and temp objects    
        self.demoShape()
        #self.demoInsignia() #Only if you are interested to try
        self.tempObjects()
    
    def myOtherInterfaceCreation(self):
        panelW,panelH,panelX,panelY = self.width,200,0,self.boundY
        MyButton(panelW,panelH,panelX,panelY,self) #Panel
        
        msgW,msgH,msgX,msgY = 260,30,20,555
        MyButton(msgW,msgH,msgX,msgY,self,"MessageButton") #Message display
        
        msgW,msgH,msgX,msgY = 300,30,475,555
        MyButton(msgW,msgH,msgX,msgY,self,"MessageButton2") #Message display
        
        #Color Component
        commonX,commonY = [385,395,405],[420]
        r,sliderH,color = 5,128,["#FF0000","#00FF00","#0000FF"]
        MySlider(r,commonX[0],commonY[0],sliderH,
                 commonX[0],commonY[0],self,color[0])
        MySlider(r,commonX[1],commonY[0],sliderH,
                 commonX[1],commonY[0],self,color[1])
        MySlider(r,commonX[2],commonY[0],sliderH,
                 commonX[2],commonY[0],self,color[2])
        
        #Button for color button
        bW,bH,bX,bY = 30,30,380,555
        MyButton(bW,bH,bX,bY,self,"ColorButton")
        
        #Arrows
        aW,aH,commonX,commonY = 50,50,[525,575,525,475],[400,450,500,450]
        dirs = [1,2,3,4]
        MyArrow(aW,aH,commonX[0],commonY[0],dirs[0],self)
        MyArrow(aW,aH,commonX[1],commonY[1],dirs[1],self)
        MyArrow(aW,aH,commonX[2],commonY[2],dirs[2],self)
        MyArrow(aW,aH,commonX[3],commonY[3],dirs[3],self)
        
        #Sphere
        sR,sX,sY = 75,700,475
        Sphere(sR,sX,sY,self)
        
    def myButtonCreation(self):
        commonX = [340,420,210,250,290,385]
        commonY = [415,450,485,520,555]
        bW,bH = 30,30
        
        myButtonDict = {0:"AddPointButton",1:"AddLineButton",
                        2:"AddCurveButton",3:"AddPolyButton",
                        4:"DeleteButton", 5: "ZoomInButton",
                        6:"ZoomOutButton", 7:"LoadButton",
                        8:"SaveButton",9:"ClearScreenButton",
                        10:"AddButton", 11: "ShiftButton",
                        12:"MoveButton",13: "CopyShiftButton",
                        15:"RotateButton",16:"ResizeButton",
                        17:"ChangePointButton", 18: "TransparentButton",
                        20: "BGColorButton", 21: "ShiftViewButton",
                        22: "RotateViewButton",23: "StandardViewButton",
                        24: "HelpButton",14:"",19:""}
        
        #Create buttons using the values above
        rows,cols = 5,5
        for x in xrange(cols):
            for y in xrange(rows):
                if myButtonDict[x*rows+y]!="":
                    MyButton(bW,bH,commonX[x],commonY[y],
                             self,myButtonDict[x*rows+y])

    
        
    
    def tempObjects(self):
        #Create temporary objects while drawing
        self.tempPoint = tempPoint(0,0,0,"tempPoint","#FFFFFF",self)
        self.tempPoly = tempPolygon(self.tempStorage,
                                    "tempPoly",self.color,self)
        self.tempLine = tempLine(self.tempStorage,"tempLine",self.color,self)
    
    def deleteObjects(self):
        #Clean the screen
        Polygon.polyList = []
        Line.lineList = []
        Point.pointList = []
        #Reset counters
        Point.pointCount = 0
        Line.lineCount = 0
        Polygon.polyCount = 0
        self.msg = "Screen cleared."
        self.selected = None
    
    def timerFired(self):
        #Report coordinates of points inside the screen
        if self.mouseY<self.boundY:
            self.coodInfo="\tX: %0.2f Y: %0.2f Z: %0.2f" %(self.newPoint[0],
                        self.newPoint[1],self.newPoint[2])
            self.coodInfo+="\n mouseX: %d mouseY: %d mouseZ: %d"%(self.mouseX,
                            self.mouseY,int(self.vzTextBox.get()))
        else:
            self.coodInfo = ""
        
        #Report the name of the selected object
        if len(self.hitList)==0 and self.selected != None:
            i = self.selected
            if isinstance(i,Point)==True:
                self.msg = "<Point %s at X:%0.2f Y:%0.2f Z:%0.2f>"%(i.name,
                            i.x,i.y,i.z)
            elif isinstance(i,Polygon)==True:
                self.msg = "<Polygon: %s>" % (i.name)
            elif isinstance(i,Line)==True:
                self.msg = "<Line: %s>" % (i.name)
        
        #Tutorial Mode:
        if self.tutorialMode == True:return
            
        if self.isMouse == True:
            #Check for shifting arrows and sphere
            self.arrowShift()
            self.sphereRotate()
            
            if len(self.dragList)!=0:
                #If dragging is on
                self.XYtoModel()
                self.dragging()

        self.keyPressTime()
    
    def arrowShift(self):
        moveSpeed = self.moveSpeed
        degreeToRad = math.pi/180
        for i in MyArrow.getArrowList():
            if i.hitTest()==True:
                #shift around
                self.shift(moveSpeed*i.dirs[0],moveSpeed*i.dirs[1],0)

    def sphereRotate(self):
        moveSpeed = self.moveSpeed
        degreeToRad = math.pi/180
        for i in Sphere.getSphereList():
            if i.hitTest()==True:
                #The amount to rotate by distance from mouse and
                #center of Axis
                rotateX = moveSpeed*(self.mouseX - i.x0)/i.r
                rotateY = moveSpeed*(self.mouseY - i.y0)/i.r
                self.rotateZX(-rotateX*degreeToRad)
                self.rotateYZ(rotateY*degreeToRad)
    
    def XYtoModel(self,x=None,y=None,z=None):
        sV = self.scaleVector
        fV = self.fixedVector
        
        #Check for nasty input
        self.checkForNumber()
        
        #Get mouseZ
        default = True
        if x==None or y==None or z==None:
            sX,sY = self.mouseX,self.mouseY    
            try: sZ = float(self.vzTextBox.get())
            except: sZ = 0 #If text has a minus sign only
        else: default = False
            
        #AX = B, Matrix Gaussian Elimiation
        #A is the scale vector
        A = [[sV[0][0],sV[1][0],sV[2][0]],
             [sV[0][1],sV[1][1],sV[2][1]],
             [sV[0][2],sV[1][2],sV[2][2]]]
        
        #B is the screen coordinates minus fixed vector
        B = [sX-fV[0],
             sY-fV[1],
             sZ-fV[2]]
        
        #Decide if it return the point or set mouse event to the point
        if default == True:
            self.newPoint = matrixSolver(A,B)
        else: return B
    
    def dragging(self):        
        if len(self.dragList)==0:return
        
        #Slider dragging
        if isinstance(self.dragList[0],MySlider)==True:
            for i in self.dragList:
                i.y = self.mouseY
                if i.y<i.y0:
                    i.y = i.y0
                if i.y>(i.y0+i.size):
                    i.y = i.y0+i.size
                self.color = self.determineColor()
            return
        
        unMove = False    
        #If the point dragged is out of bound
        for i in self.dragList:
            i.x += self.newPoint[0]-self.oldPoint[0]
            i.y += self.newPoint[1]-self.oldPoint[1]
            i.z += self.newPoint[2]-self.oldPoint[2]
            
            if unMove == False:
                unMove = self.pointOutOfBound(i.x,i.y,i.z)
        
        #Then unmove it back
        if unMove == True:
            for i in self.dragList:
                i.x -= self.newPoint[0]-self.oldPoint[0]
                i.y -= self.newPoint[1]-self.oldPoint[1]
                i.z -= self.newPoint[2]-self.oldPoint[2]
        else:
            self.oldPoint = copy.deepcopy(self.newPoint)
    
    def keyPressTime(self):
        #Key on hold event
        degreeToRad = math.pi/180
        
        #Tutorial Mode:
        if self.tutorialMode == True:
            return
        
        #Delete objects when delete key is on hold
        moveSpeed = self.moveSpeed
        if self.keyDeletePressed == True:
            if len(self.hitList)>0:
                self.removeInstance(self.hitList[-1])
        
        #Decide if arrow keys cause rotation or shift by key R
        for dirs in self.dirKey:
            if self.keyRPressed == False:
                self.shift(moveSpeed*dirs[0],moveSpeed*dirs[1],0)
            else:
                self.rotateZX(-moveSpeed*dirs[0]*degreeToRad)
                self.rotateYZ(moveSpeed*dirs[1]*degreeToRad)
    
    def mousePressed(self,event):
        endOfTutorial = 27
        #Tutorial Mode:
        if self.tutorialMode == True:
            if self.tutorialStep < endOfTutorial:
                self.tutorialStep += 1
            else: self.tutorialEnd()
            return
        
        self.isMouse = True
        self.XYtoModel()
        self.dragList = []
        
        if self.mouseY <= self.boundY:
            #De-select objects
            if self.selected != None and self.selected.hitTest()==False:
                self.selected = None
            
            #Object events
            self.objectMousePressed()
        else:
            #Check for button pressed
            for i in MyButton.getButtonList():
                i.buttonPressed()
                
            #Check for slider
            for i in MySlider.getSliderList():
                if i.hitTest()==True:
                    self.dragList.append(i)
        
            #Delete objects and change colors to selected objects
            if self.isDelete == True: self.removeInstance()
            elif self.isChangeColor == True: self.changeColor()
                
    def objectMousePressed(self):
        if self.isAddPoint == True:
            self.addPoint() #Add Point
        elif self.isAddLine == True:
            self.addLine() #Add Line
        elif self.isAddCurve == True:    
            self.addCurve() #Add Curve
        elif self.isAddPoly == True:
            self.addPolygon() #Add Polygon
        elif len(self.hitList)!=0:
            #Find the last object that mouse over
            i = self.hitList[-1]
            
            #Copy the vector of mouse to a old point for point shifting
            self.oldPoint = copy.deepcopy(self.newPoint)
            
            #Get the selected object
            self.selected = i
            
            #Append only points to the draglist
            if isinstance(i,Point)==True:
                self.dragList.append(i)
            if isinstance(i,Polygon)==True or isinstance(i,Line)==True:
                for point in i.listP:
                    self.dragList.append(point[0])
                    
    def addPoint(self):
        #Get the new name for point
        name = "P"+str(Point.getPointCount()+1)
        
        if self.pointOutOfBound(*self.newPoint):
            return
        
        #Create new Point
        pt = self.newPoint
        p = Point(pt[0],pt[1],pt[2],name,self.color,self)
        self.isAddPoint = False
        self.selected = p
        return p
    
    def addLine(self):
        self.addLineObject(0)
        
    def addCurve(self):
        self.addLineObject(1)
    
    def getNewTempPoint(self):
        #Get the last point to be the point in the added line
        tempPoint = None
        for i in self.hitList:
            if isinstance(i,Point)==True:
                tempPoint = i
        
        #Or else create points        
        if tempPoint == None:
            tempPoint = self.addPoint()
        return tempPoint
    
    def addLineObject(self,lineType):
        #If the point is out of bound
        if self.pointOutOfBound(*self.newPoint):
            return
        
        #Get name for the line
        name = "L"+str(Line.getLineCount()+1)
        
        #Get the last point to be the point in the added line
        tempPoint = self.getNewTempPoint()
        self.tempStorage.append([tempPoint,lineType])

        #Draw complete after 2 points
        if self.drawComplete <= lineType:
            self.drawComplete += 1
        else:
            #Create new line
            l1 = Line(self.tempStorage,name,self.color,self)
            self.selected = l1
            self.isAddLine = False
            self.isAddCurve = False
            self.tempStorage = []
            self.drawComplete = 0

    def addPolygon(self,enterPressed=False):
        #If the point is out of bound
        if self.pointOutOfBound(*self.newPoint): return
        
        #Get name
        name = "Poly"+str(Polygon.getPolyCount()+1)
        
        #Get temporary point unless enter is pressed
        #In that case, get first point
        if enterPressed == True: tempPoint = self.tempStorage[0][0]
        else: tempPoint = self.getNewTempPoint()
        
        #Complete the draw if the last point is the original point    
        if (len(self.tempStorage)>0 and tempPoint == self.tempStorage[0][0]):
            self.drawComplete = 1
        else:
            #Curve mode vs non-curve mode
            if self.keyCPressed == False or self.prevPointCurve == True:
                if (len(self.tempStorage) == 0 or self.tempStorage[-1][0] != tempPoint): 
                    self.tempStorage.append([tempPoint,0])
                    self.prevPointCurve = False
            else:
                if (len(self.tempStorage) == 0 or self.tempStorage[-1][0] != tempPoint): 
                    self.tempStorage.append([tempPoint,1])
                    self.prevPointCurve = True
            
        if self.drawComplete == 1:        
            poly1 = Polygon(self.tempStorage,name,self.color,self)
            self.selected = poly1
            self.isAddPoly = False
            self.tempStorage = []
            self.drawComplete = 0
            self.keyCPressed = False

    def removeInstance(self,remLast=None):
        if remLast == None:remLast = self.selected
        
        if isinstance(remLast,Polygon)==True:    
            #Remove polygon
            idx = Polygon.polyList.index(remLast)
            Polygon.polyList = Polygon.polyList[:idx]+Polygon.polyList[idx+1:]
        elif isinstance(remLast,Line) == True:
            #Remove Line
            idx = Line.lineList.index(remLast)
            Line.lineList = Line.lineList[:idx]+Line.lineList[idx+1:]
        elif isinstance(remLast,Point) == True:
            
            #Remoe polygons and lines that has that point
            for i in Polygon.getPolyList():
                if ([remLast,0] in i.listP or [remLast,1] in i.listP):
                    self.removeInstance(i)
                    
            for i in Line.getLineList():
                if ([remLast,0] in i.listP or [remLast,1] in i.listP):
                    self.removeInstance(i)
                    
            idx = Point.pointList.index(remLast)
            Point.pointList = Point.pointList[:idx]+Point.pointList[idx+1:]
        
        if remLast == self.selected:
            remLast=None
            self.selected = None
            self.isDelete = False
       
    def changeColor(self):
        #Change color for selected objects
        if self.selected != None:
            self.selected.color = self.color
        self.isChangeColor = False
        
    def mouseReleased(self,event):
        self.isMouse = False
    
    def keyPressedTutorial(self,event):
        maxTutorialStep = 27
        
        #Quit    
        if event.char.lower() == "q":
            self.tutorialEnd()
        
        #Move up and down
        if self.tutorialStep > 0:
            if event.keysym == "Left" or event.keysym == "Up":
                self.tutorialStep -= 1
        if self.tutorialStep < maxTutorialStep:
            if event.keysym == "Right" or event.keysym == "Down":
                self.tutorialStep += 1
    
    def keyPressed(self, event):
        #Tutorial Mode:
        if self.tutorialMode == True:
            self.keyPressedTutorial(event)
            return
        
        #Change to curve mode for polygons
        if event.char.lower() == "c":
            self.keyCPressed = not self.keyCPressed
        
        #Rotation mode    
        if event.char.lower() == "r": self.keyRPressed = True
        
        #Delete instance
        if event.keysym == "Delete":
            self.keyDeletePressed = True
            self.removeInstance()
            
        #Complete polygon using Enter
        if event.keysym == "Return" and self.isAddPoly == True:
            self.addPolygon(True)
        
        dirs={"Left":[-1,0],"Right":[1,0],"Up":[0,-1], "Down":[0,1]}
            
        if (event.keysym == "Left" or event.keysym == "Right"
            or event.keysym == "Up" or event.keysym == "Down"):
            
            if dirs[event.keysym] not in self.dirKey:
                self.dirKey.append(dirs[event.keysym])
        
        #Zoom in and out
        if (event.char == "+"):self.zoom(2)
        elif (event.char == "_"):self.zoom(1.0/2)        
            
    def keyReleased(self, event):
        #Tutorial Mode:
        if self.tutorialMode == True and len(self.dirKey)==0:
            return
        
        #If delete and r is pressed
        if event.keysym == "Delete":
            self.keyDeletePressed = False
        if event.keysym == "r":
            self.keyRPressed = False
        
        #Shift using arrows to be released
        if event.keysym == "Left":
            idx = self.dirKey.index([-1,0])
            self.dirKey = self.dirKey[:idx]+self.dirKey[idx+1:]
        if event.keysym == "Right":
            idx = self.dirKey.index([1,0])
            self.dirKey = self.dirKey[:idx]+self.dirKey[idx+1:]
        if event.keysym == "Up":
            idx = self.dirKey.index([0,-1])
            self.dirKey = self.dirKey[:idx]+self.dirKey[idx+1:]
        if event.keysym == "Down":
            idx = self.dirKey.index([0,1])
            self.dirKey = self.dirKey[:idx]+self.dirKey[idx+1:]                
    
    def pointOutOfBound(self,x,y,z):
        limit = self.limitP
        #Out of bound points
        if abs(x) > limit or abs(y)>limit or abs(z)>limit:
            self.msg = "Points cannot be out of bound."
            self.msg += "\n<%s,%s> only" % (self.limitP,-self.limitP)
            self.selected = None
            return True
        else:
            return False
    
    def viewOutOfBound(self,x,y,z):
        limit = self.limitV
        #Out of bound view
        if abs(x) > limit or abs(y)>limit or abs(z)>limit:
            return True
        else:
            return False
    
    def determineColor(self):
        red,green,blue=0,0,0
        full = 255.0
        
        #Determine color using slider position
        for i in MySlider.getSliderList():
            if i.color == "#FF0000":
                red = int(full*(i.size-i.y+i.y0)/i.size)
            elif i.color == "#00FF00":
                green = int(full*(i.size-i.y+i.y0)/i.size)
            elif i.color == "#0000FF":
                blue = int(full*(i.size-i.y+i.y0)/i.size)
        return rgbString(red,green,blue)

    def redrawAll(self):
        #Draw background with background color
        self.canvas.create_rectangle(0,0,self.width,self.height,
                                     fill=self.bgcolor)
        self.drawObjects()
        self.drawInterface()
        
    def drawObjects(self):
        self.drawList = []
        self.hitList = []
        
        #Append the objects
        for i in Point.getPointList():
            i.modelToXYConversion()
            self.drawList.append(i)
        for i in Line.getLineList():
            self.drawList.append(i)
        for i in Polygon.getPolyList():
            self.drawList.append(i)
        
        #Sort them by depths
        self.drawList.sort(depthCmp)
        
        #Detect mouse over
        for i in self.drawList:
            if i.hitTest()==True and self.isAddPoint==False:
                if (isinstance(i,Point)==True or (self.isAddCurve == False
                    and self.isAddLine == False and self.isAddPoly == False)):
                    self.hitList.append(i)
        
        #Draw the objects
        for i in self.drawList:
            i.draw()

        self.tempPoly.draw()
        self.tempPoint.draw()
        self.tempLine.draw()
        
    def drawInterface(self):
        #draw buttons, shift arrow, slider and tutorial
        for i in MyButton.getButtonList():i.draw()
        for i in MyArrow.getArrowList():i.draw()
        for i in MySlider.getSliderList():i.draw()
        for i in MyTutorial.getTutorialList():i.draw()
        
        #Axis, text labels, help msg
        self.drawAxis()
        self.drawTextBoxLabels()
        self.drawHelpMessage()
    
    def drawHelpMessage(self):
        mX,mY,color = self.mouseX,self.mouseY,"#FFFF88"
        hRatio,wRatio = 15,7
        
        for i in MyButton.getButtonList():
            if i.hitTest() == True and len(i.helpMessage)>0:
                #Get the longest width of message and height of message
                subMessage = i.helpMessage.split("\n")
                width,height = 0,len(subMessage)*hRatio
                
                #Get the width of the message
                for subString in subMessage:
                    if width<len(subString)*wRatio:
                        width=len(subString)*wRatio
                
                #Create help box
                self.canvas.create_rectangle(mX,mY,mX+width,mY-height,
                                             fill=color)
                self.canvas.create_text(mX+2,mY,anchor="sw",
                                        text=i.helpMessage)
        
    def drawTextBoxLabels(self):
        commonX=[20, 110]
        commonY=[430,465,500,535]
        self.canvas.create_text(commonX[0],commonY[0],text="Mouse Z Position:",
                                anchor="w")
        self.canvas.create_text(commonX[0],commonY[1],text="X:")
        self.canvas.create_text(commonX[0],commonY[2],text="Y:")
        self.canvas.create_text(commonX[0],commonY[3],text="Z:")
        self.canvas.create_text(commonX[1],commonY[1],text="XY:")
        self.canvas.create_text(commonX[1],commonY[2],text="YZ:")
        self.canvas.create_text(commonX[1],commonY[3],text="ZX:")

    def drawAxis(self):
        sqrt = 0.5
        #Draw the sphere
        i = Sphere.getSphereList()[0]
        i.draw()
        
        sumOfSquares=dotProduct(self.scaleVector[0],self.scaleVector[0])**sqrt
        textList=['X','Y','Z']
        circleColor = ['#FF0000','#00FF00','#0000FF']
        
        #Sort the positions of the scale vector
        tempVector = []
        for idx in xrange(len(self.scaleVector)):
            tempList = self.scaleVector[idx]+[textList[idx]]+[circleColor[idx]]
            tempVector.append(tempList)
        tempVector = sorted(tempVector,depthCmp2)
        
        #Draw the axis vectors
        for point in tempVector:
            #Find the x and y position of the axis circles
            cx = (1.0*i.r*point[0]/sumOfSquares+i.x0)
            cy = (1.0*i.r*point[1]/sumOfSquares+i.y0)
            r = 5
            #Draw line from the circle
            self.canvas.create_line(i.x0,i.y0,cx,cy,width=3,fill=point[4])
            createCircle(self.canvas,cx,cy,r,point[4],r)
            self.canvas.create_text(cx,cy,text=point[3])
        
    def rotateXY(self,theta):
        #Rotate scale vector and fixed vector using center vector
        fV = self.fixedVector
        cV = self.centerVector
        diff = [fV[0]-cV[0],fV[1]-cV[1]]
        for iV in self.scaleVector:
            iV[0],iV[1] = rotate(iV[0],iV[1],theta)
        diff[0],diff[1] = rotate(diff[0],diff[1],theta)
        self.fixedVector[0],self.fixedVector[1] = diff[0]+cV[0],diff[1]+cV[1]
    
    def rotateYZ(self,theta):
        #Rotate scale vector and fixed vector using center vector
        fV = self.fixedVector
        cV = self.centerVector
        diff = [fV[1]-cV[1],fV[2]-cV[2]]
        for iV in self.scaleVector:
            iV[1],iV[2] = rotate(iV[1],iV[2],theta)
        diff[0],diff[1] = rotate(diff[0],diff[1],theta)
        self.fixedVector[1],self.fixedVector[2] = diff[0]+cV[1],diff[1]+cV[2]
    
    def rotateZX(self,theta):
        #Rotate scale vector and fixed vector using center vector
        fV = self.fixedVector
        cV = self.centerVector
        diff = [fV[2]-cV[2],fV[0]-cV[0]]
        for iV in self.scaleVector:
            iV[2],iV[0] = rotate(iV[2],iV[0],theta)
        diff[0],diff[1] = rotate(diff[0],diff[1],theta)
        self.fixedVector[2],self.fixedVector[0] = diff[0]+cV[2],diff[1]+cV[0]

    def shift(self,x,y,z):
        fV = self.fixedVector
        limit = self.limitV
        
        #Shift
        self.fixedVector[0] += x
        self.fixedVector[1] += y
        self.fixedVector[2] += z
        
        #Unshift if out of bounds
        if self.viewOutOfBound(x,y,z)==True:
            self.msg = "You cannot shift out of bounds."
            self.fixedVector[0] -= x
            self.fixedVector[1] -= y
            self.fixedVector[2] -= z

    def checkForNumber(self):
        for i in self.textBoxList:
            try:
                #Detect alphabets
                if i.get() != "-":float(i.get())
                
                #Detect spaces
                assert(i.get().find(" ")==-1)
                
                #Limit characters
                if len(i.get())>6:
                    self.msg = "Inputs must not exceed 6 characters."
                    i.delete(len(i.get())-1)
                
                #Remove leading zero
                if (len(i.get())>1 and
                    (i.get()[0:1]=="0" and i.get()[0:2]!="0.")):
                    i.delete(0)
            except:
                #If there are random things
                self.msg="Inputs must not contain \nany non-number component."
                i.delete(0,END)
                i.insert(0,0)
                
    def addPointByText(self):
        #Get coordinates
        name = "P"+str(Point.getPointCount()+1)
        x = float(self.xTextBox.get())
        y = float(self.yTextBox.get())
        z = float(self.zTextBox.get())
        
        if self.pointOutOfBound(x,y,z)==True:return
        
        #Create new point
        p = Point(x,y,z,name,self.color,self)
        self.selected = p
    
    def shiftPointByText(self):
        #Get coordinates
        x = float(self.xTextBox.get())
        y = float(self.yTextBox.get())
        z = float(self.zTextBox.get())

        if self.selected == None:return
        else:i = self.selected
                
        #Move and unmove if out of bound
        if isinstance(i,Point)==True:
            i.x,i.y,i.z = i.x+x,i.y+y,i.z+z
            if self.pointOutOfBound(i.x,i.y,i.z) == True:
                i.x,i.y,i.z = i.x-x,i.y-y,i.z-z
        else:
            unMove = False
            for [p,c] in i.listP:
                p.x,p.y,p.z = p.x+x,p.y+y,p.z+z
                if unMove == False:
                    unMove = self.pointOutOfBound(p.x,p.y,p.z)
        
            #Unmove when it is out of bound
            if unMove == True:
                for [p,c] in i.listP:
                    p.x,p.y,p.z = p.x-x,p.y-y,p.z-z
                        
    def movePointByText(self):
        #Get coordinates
        x = float(self.xTextBox.get())
        y = float(self.yTextBox.get())
        z = float(self.zTextBox.get())
        
        if self.selected == None:return
        else:i = self.selected
        
        if isinstance(i,Point)==True:
            #If the point is out of bound
            if self.pointOutOfBound(x,y,z)==False:i.x,i.y,i.z = x,y,z
            else:return
        else:
            #Get the amount to move for lines and polygons
            cx,cy,cz,lenP = 0,0,0,len(i.listP)
            for [p,c] in i.listP:
                cx += p.x/lenP
                cy += p.y/lenP
                cz += p.z/lenP
            dx,dy,dz = x-cx,y-cy,z-cz
            
            #Move and unmove if out of bound for points
            unMove = False
            for [p,c] in i.listP:
                p.x,p.y,p.z = p.x+dx,p.y+dy,p.z+dz
                if unMove == False: unMove = self.pointOutOfBound(p.x,p.y,p.z)
                    
            #Reverse the move
            if unMove == True:
                for [p,c] in i.listP:p.x,p.y,p.z = p.x-dx,p.y-dy,p.z-dz
                
    def copyPointByText(self):
        x = float(self.xTextBox.get())
        y = float(self.yTextBox.get())
        z = float(self.zTextBox.get())

        #If there is no selection
        if self.selected == None:return
        else:i = self.selected
        
        #Check for out of bound
        if isinstance(i,Point)==True:
            if self.pointOutOfBound(i.x+x,i.y+y,i.z+z)==True:return
        else:
            for [p,c] in i.listP:
                if self.pointOutOfBound(p.x+x,p.y+y,p.z+z)==True:return
        
        if isinstance(i,Point)==True:
            #Get name and add point
            name = "P"+str(Point.getPointCount()+1)
            self.selected = Point(i.x+x,i.y+y,i.z+z,name,i.color,self)
        else:
            #Get every point
            pointList = []
            for [p,c] in i.listP:
                n = "P"+str(Point.getPointCount()+1)
                pointList.append([Point(p.x+x,p.y+y,p.z+z,n,p.color,self),c])
                
            if isinstance(i,Polygon)==True:
                #Create new Shape
                name = "Poly"+str(Polygon.getPolyCount()+1)
                self.selected = Polygon(pointList,name,i.color,self)
            elif isinstance(i,Line)==True:
                #Create new line or curve
                name = "L"+str(Line.getLineCount()+1)
                self.selected = Line(pointList,name,i.color,self)
            
    def rotatePointByText(self):
        #Get coordinates
        xy = float(self.xyTextBox.get())*math.pi/180
        yz = float(self.yzTextBox.get())*math.pi/180
        zx = -float(self.zxTextBox.get())*math.pi/180
        
        #If there is no selection
        if self.selected == None:return
        else:i = self.selected
        
        if isinstance(i,Point)!=True:
            cx,cy,cz,lenP = 0,0,0,len(i.listP)
            for [p,c] in i.listP:
                cx += p.x/lenP
                cy += p.y/lenP
                cz += p.z/lenP
            
            unMove = False
            
            for [p,c] in i.listP:
                self.rotatePoints(p,xy,yz,zx,cx,cy,cz)
                if unMove == False:unMove = self.pointOutOfBound(p.x,p.y,p.z)
                    
            if unMove == True:
                #Unrotate
                xy,yz,zx = -xy,-yz,-zx
                for [p,c] in i.listP:
                    self.rotatePoints(p,xy,yz,zx,cx,cy,cz)
    
    def rotatePoints(self,p,xy,yz,zx,cx,cy,cz):
        #Rotate using the 3 angles, center points
        d1,d2 = p.x-cx,p.y-cy
        p.x,p.y = rotate(d1,d2,xy)[0]+cx,rotate(d1,d2,xy)[1]+cy
        d1,d2 = p.y-cy,p.z-cz
        p.y,p.z = rotate(d1,d2,yz)[0]+cy,rotate(d1,d2,yz)[1]+cz
        d1,d2 = p.z-cz,p.x-cx
        p.z,p.x = rotate(d1,d2,zx)[0]+cz,rotate(d1,d2,zx)[1]+cx
                
    def resizePointByText(self):
        #If there is no selection
        if self.selected == None:return
        else:i = self.selected
        
        #Get coordinates and fix them to be 1 if 0
        x = float(self.xTextBox.get())
        y = float(self.yTextBox.get())
        z = float(self.zTextBox.get())
        
        if abs(x) < self.epsilon: x = 1.0
        if abs(y) < self.epsilon: y = 1.0
        if abs(z) < self.epsilon: z = 1.0
    
        if isinstance(i,Point)!=True:
            #Get center Point
            cx,cy,cz,lenP = 0,0,0,len(i.listP)
            for [p,c] in i.listP:
                cx += p.x/lenP
                cy += p.y/lenP
                cz += p.z/lenP
            
            #Move
            unMove = False
            for [p,c] in i.listP:
                p.x = x*(p.x-cx)+cx
                p.y = y*(p.y-cy)+cy
                p.z = z*(p.z-cz)+cz
                if unMove == False:unMove = self.pointOutOfBound(p.x,p.y,p.z)
            
            #Unmove if out of bound
            if unMove == True:
                for [p,c] in i.listP:
                    p.x = 1.0/x*(p.x-cx)+cx
                    p.y = 1.0/y*(p.y-cy)+cy
                    p.z = 1.0/z*(p.z-cz)+cz
            
    def standardView(self):
        #Default view parameters
        w,h = self.width,self.height
        self.scaleVector = [[100.0,0.0,0.0],[0.0,100.0,0.0],[0.0,0.0,100.0]]
        self.fixedVector = [1.0*w/2,1.0*(h/2)-100,0.0]
        self.centerVector = [1.0*w/2,1.0*(h/2)-100,0.0]
    
    def shiftView(self):
        x = float(self.xTextBox.get())
        y = float(self.yTextBox.get())
        z = float(self.zTextBox.get())
        #Shift the view
        self.shift(x,y,z)
    
    def rotateView(self):
        xy = float(self.xyTextBox.get())*math.pi/180
        yz = float(self.yzTextBox.get())*math.pi/180
        zx = -float(self.zxTextBox.get())*math.pi/180
        #Rotate the view
        self.rotateXY(xy)
        self.rotateYZ(yz)
        self.rotateZX(zx)
        
    def bgColorChange(self):
        self.bgcolor = self.color

    def changePointSize(self):
        #Change the size of the points
        if self.pointRadius == 10:
            self.pointRadius = 1
        else:
            self.pointRadius = 10
            
    def changeTransparency(self):
        self.transparent = not self.transparent
        
    def zoom(self,zoomAmount):
        fV = self.fixedVector
        cV = self.centerVector
        sV = self.scaleVector
        
        sumOfSquares = dotProduct(sV[0],sV[0])**0.5
        
        #Zoom limits
        if zoomAmount > 1 and sumOfSquares > self.limitZ[1]:
            self.msg = "You cannot zoom in anymore."
            return
        if zoomAmount < 1 and sumOfSquares < self.limitZ[0]:
            self.msg = "You cannot zoom out anymore."
            return
        
        #Change the scale vector
        for point in self.scaleVector:
            point[0]*=zoomAmount
            point[1]*=zoomAmount
            point[2]*=zoomAmount
        
        #Change the fixed vector accordingly
        self.fixedVector[0]=zoomAmount*(fV[0]-cV[0])+cV[0]
        self.fixedVector[1]=zoomAmount*(fV[1]-cV[1])+cV[1]
    
    def tutorialInit(self):
        #Set up the tutorial and delete everything
        self.tutorialMode = True
        self.tutorialSave = self.saveString()
        self.deleteObjects()
        
        self.tutorialStep = 0
        
        #Set up the panel for tutorial
        panelW,panelH,panelX,panelY = self.width/2,200,self.width/4,100
        MyTutorial(panelW,panelH,panelX,panelY,self,"TutorialPanel") #Panel
        
    def tutorialEnd(self):
        #Restore it back to normal after tutorial
        self.tutorialStep = 0
        self.tutorialMode = False
        if self.tutorialSave != None:
            self.loadFromString(self.tutorialSave)
            self.tutorialSave = None
        MyTutorial.tutorialList = []
    
    '''
    Modified from:
    Load and Save: http://tkinter.unpythonic.net/wiki/tkFileDialog
    Pickle: http://docs.python.org/2/library/pickle.html
'''    
    def loadFile(self):
        #Save the values of the current screen
        saveValues = self.saveString()
        #Remove all objects on screen
        self.deleteObjects()
        
        try:
            #Load the menu of file dialog
            f = tkFileDialog.askopenfile(mode='rb',
                title='Choose a file',filetypes=[('Model','*.mdl')])
            contents = pickle.load(f)
            f.close()
            self.loadFromString(contents)
            self.msg = "Load successful"
        except:
            #If it failed, restore the current screen
            self.deleteObjects()
            self.loadFromString(saveValues)
            self.msg = "Please select a valid file to load!"
    
    def saveFile(self):
        #Get the filename
        self.filename = tkFileDialog.asksaveasfilename(title="Save",
                                    filetypes=[('Model','*.mdl')])
        if self.filename != "":
            self.filename += ".mdl"
            
            #Open the file and dump the values
            with open(self.filename,'wb') as f:
                saveValues = self.saveString()
                pickle.dump(saveValues, f)
            self.msg = "File saved."
        else:
            #If no file name is given
            self.msg = "File fail to save."
    
    def loadPoints(self,newSections):
        #Get the point variables
        newPointSection = newSections[0].split('|')[1:]
        
        #Split and create new point
        for point in newPointSection:
            pStats = point.split(',')
            name = pStats[0]
            color = pStats[4]
            x,y,z = float(pStats[1]),float(pStats[2]),float(pStats[3])
            Point(x,y,z,name,color,self)
    
    def loadLines(self,newSections):
        #Get line string codes
        newLineSection = newSections[1].split('|')[1:]
        for line in newLineSection:
            #Open up the line
            lineStat = line.split('[')
            #Get name and color of line before [
            lineName = lineStat[0].split(',')[0]
            lineColor = lineStat[0].split(',')[1]
            #Get the points separated by * before ]
            pointSection = lineStat[1].split(']')[0].split('*')[1:]
            listP = []
            #Get the points in the point Section
            for point in pointSection:
                pointStat = point.split(',')
                pointRef = None
                #Get the reference
                for i in Point.getPointList():
                    if i.name == pointStat[0]:
                        pointRef = i
                        break
                #Append it to the list
                listP.append([pointRef,int(pointStat[1])])
            #Create the line
            p = Line(listP,lineName,lineColor,self)
    
    def loadPoly(self,newSections):
        #Get poly string codes
        newPolySection = newSections[2].split('|')[1:]
        for poly in newPolySection:
            polyStat = poly.split('[')
            #Get name and color of poly before [
            polyName = polyStat[0].split(',')[0]
            polyColor = polyStat[0].split(',')[1]
            #Get the points separated by * before ]
            pointSection = polyStat[1].split(']')[0].split('*')[1:]
            listP = []
            #Get the points in the point Section
            for point in pointSection:
                pointStat = point.split(',')
                pointRef = None
                #Get the reference
                for i in Point.getPointList():
                    if i.name == pointStat[0]:
                        pointRef = i
                        break
                #Append it to the list    
                listP.append([pointRef,int(pointStat[1])])
            #Create the polygon
            p = Polygon(listP,polyName,polyColor,self)
    
    def loadRest(self,newSections):
        #Get the scale vector from section 3 which is 3x3 matrix
        i = 3
        newScaleVector = newSections[i].split('|')[1:]
        for idx in xrange(len(newScaleVector)):
            #Get the column values
            scaleStats = newScaleVector[idx].split(',')
            for idx2 in xrange(len(scaleStats)):
                self.scaleVector[idx][idx2] = float(scaleStats[idx2])
        i+=1
        #Get the fixed vector from section 4 which is 3x1 matrix
        newFixedVector = newSections[i].split('|')[1:]
        for idx in xrange(len(newFixedVector)):
            self.fixedVector[idx] =  float(newFixedVector[0].split(',')[idx])
        
        i+=1
        #Get rest of the global variables
        newCounts = newSections[i].split(',')
        Point.pointCount = int(newCounts[0])
        Line.lineCount = int(newCounts[1])
        Polygon.polyCount = int(newCounts[2])
        self.pointRadius = int(newCounts[3])
        
        if newCounts[4] == "True":
            self.transparent = True
        else:
            self.transparent = False
            
        self.bgcolor = newCounts[5]
        
    def loadFromString(self, newLoad):
        newPart = newLoad.split('@')

        if newPart[1] != str(hash(newPart[0])):
            assert(False)
        
        newSections = newPart[0].split('$')
        #Load points, lines, polygon and globals
        self.loadPoints(newSections)
        self.loadLines(newSections)
        self.loadPoly(newSections)
        self.loadRest(newSections)

    def saveObjects(self,newSave):
        
        #Encode points in string
        for i in Point.getPointList():
            newSave += "|"+i.name+","+str(i.x)+","+str(i.y)+","+str(i.z)
            newSave += ","+i.color
        
        #Encode lines in string
        newSave += "$"
        for i in Line.getLineList():
            newSave += "|"+i.name+","+i.color+"["
            for point in i.listP:
                newSave += "*"+point[0].name + "," + str(point[1]) 
            newSave += "]"    
        newSave += "$"
        
        #Encode polygons in string
        for i in Polygon.getPolyList():
            newSave += "|"+i.name+","+i.color+"["
            for point in i.listP:
                newSave += "*"+point[0].name + "," + str(point[1]) 
            newSave += "]"
        return newSave
    
    def saveGlobals(self,newSave):
        #Scale and fixed vector
        newSave += "$"
        for i in self.scaleVector:
            newSave += "|"+str(i[0])+","+str(i[1])+","+str(i[2])
        newSave += "$"
        i = self.fixedVector
        newSave += "|"+str(i[0])+","+str(i[1])+","+str(i[2])
        
        #Save the number of points, radius size, bg color and transparency
        newSave += "$"
        newSave += str(Point.getPointCount())
        newSave += ","+str(Line.getLineCount())+","+str(Polygon.getPolyCount())
        newSave += ","+str(self.pointRadius)+","+str(self.transparent)
        newSave += ","+self.bgcolor
        
        return newSave
    
    def saveString(self):
        newSave = ""
        newSave = self.saveObjects(newSave)
        newSave = self.saveGlobals(newSave)    
        
        #Hash the string to prevent corruption
        newSave += "@"+str(hash(newSave))
        return newSave

    def demoShape(self):
        
        #Create the points
        p1=Point(0,0,0,"P"+str(Point.pointCount),"#FFFFFF",self)
        p2=Point(1,0,0,"P"+str(Point.pointCount),"#000000",self)
        p3=Point(0,1,0,"P"+str(Point.pointCount),"#FF0000",self)
        p4=Point(1,1,0,"P"+str(Point.pointCount),"#FFFF00",self)
        p5=Point(0,0,1,"P"+str(Point.pointCount),"#00FF00",self)
        p6=Point(1,0,1,"P"+str(Point.pointCount),"#00FFFF",self)
        p7=Point(0,1,1,"P"+str(Point.pointCount),"#0000FF",self)
        p8=Point(1,1,1,"P"+str(Point.pointCount),"#FF00FF",self)

        #Create the polygon
        Polygon([[p1,1],[p2,0],[p4,0],[p3,0]],"Poly"+str(Polygon.polyCount),
                "#FF0000",self)
        #Create the polygon
        Polygon([[p5,1],[p6,0],[p8,0],[p7,0]],"Poly"+str(Polygon.polyCount),
                "#FFFF00",self)
        #Create the polygon
        Polygon([[p1,0],[p5,0],[p7,0],[p3,0]],"Poly"+str(Polygon.polyCount),
                "#00FF00",self)
        #Create the polygon
        Polygon([[p3,0],[p4,0],[p8,0],[p7,0]],"Poly"+str(Polygon.polyCount),
                "#FF00FF",self)
        #Create the polygon
        Polygon([[p1,1],[p2,0],[p4,0],[p8,1],[p6,0],[p5,0]],
                "Poly"+str(Polygon.polyCount),"#00FFFF",self)

        

    def demoInsignia(self):

        #My personal Insignia
        self.demoInner()
        self.demoOuter1()
        self.demoOuter2()
        self.demoSetup()

    def demoInner(self):
        maxRot = 10
        for rot in xrange(maxRot):
            cX,cY,cZ = [-0.2,1.8],[-1,0],[0,5]
            theta = (rot-1.0/5)*math.pi*2/maxRot

            #Create the points
            x,y = rotate(cX[0],cY[0],theta)
            p1=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p2=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)
            
            x,y = rotate(cX[0],cY[1],theta)
            p3=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p4=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            x,y = rotate(cX[1],cY[0],theta)
            p5=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p6=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            x,y = rotate(cX[1],cY[1],theta)
            p7=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p8=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            #Create the polygon
            poly1 = Polygon([[p1,0],[p2,0],[p4,0],[p3,0]],
                            "Poly"+str(Polygon.polyCount),"#FFFFFF",self)
            poly2 = Polygon([[p1,0],[p5,0],[p6,0],[p2,0]],
                            "Poly"+str(Polygon.polyCount),"#FF0000",self)
            poly3 = Polygon([[p5,0],[p6,0],[p8,0],[p7,0]],
                            "Poly"+str(Polygon.polyCount),"#FFFF00",self)

    def demoOuter1(self):
        maxRot = 5
        for rot in xrange(maxRot):
            cX,cY,cZ = [-1,1],[-2.00,-3.00],[0,5]
            theta = (rot+1.0/2)*math.pi*2/maxRot

            #Create the points
            x,y = rotate(cX[0],cY[0],theta)
            p1=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p2=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)
            
            x,y = rotate(cX[0],cY[1],theta)
            p3=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p4=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            x,y = rotate(cX[1],cY[0],theta)
            p5=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p6=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            x,y = rotate(cX[1],cY[1],theta)
            p7=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p8=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            #Create the polygon
            poly1 = Polygon([[p1,0],[p2,0],[p4,0],[p3,0]],
                            "Poly"+str(Polygon.polyCount),"#00FFFF",self)
            poly2 = Polygon([[p1,0],[p5,0],[p6,0],[p2,0]],
                            "Poly"+str(Polygon.polyCount),"#00FF00",self)
            poly3 = Polygon([[p5,0],[p6,0],[p8,0],[p7,0]],
                            "Poly"+str(Polygon.polyCount),"#00FFFF",self)

    def demoOuter2(self):
        maxRot = 5
        for rot in xrange(maxRot):
            cX,cY,cZ = [-1,1],[-3.10,-2.10],[0,5]
            theta = (rot)*math.pi*2/maxRot

            #Create the points
            x,y = rotate(cX[0],cY[0],theta)
            p1=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p2=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)
            
            x,y = rotate(cX[0],cY[1],theta)
            p3=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p4=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            x,y = rotate(cX[1],cY[0],theta)
            p5=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p6=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            x,y = rotate(cX[1],cY[1],theta)
            p7=Point(x,y,cZ[0],"P"+str(Point.pointCount),"#0000FF",self)
            p8=Point(x,y,cZ[1],"P"+str(Point.pointCount),"#0000FF",self)

            #Create the polygon
            poly1 = Polygon([[p1,0],[p2,0],[p4,0],[p3,0]],
                            "Poly"+str(Polygon.polyCount),"#00FFFF",self)
            poly2 = Polygon([[p1,0],[p5,0],[p6,0],[p2,0]],
                            "Poly"+str(Polygon.polyCount),"#0000FF",self)
            poly3 = Polygon([[p5,0],[p6,0],[p8,0],[p7,0]],
                            "Poly"+str(Polygon.polyCount),"#00FFFF",self)

    def demoSetup(self):
        self.pointRadius = 1
        angle = -60*math.pi/180
        self.rotateYZ(angle)
        dy = -150
        self.shift(0,dy,0)
        self.zoom(1.0/2)


m = MainInterface(800,600)





