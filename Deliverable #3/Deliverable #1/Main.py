from Tkinter import *
import math
import copy
import string

from Point import Point
from Polygon import Polygon
from Line import Line
from MyButton import MyButton
from MyButton import MyArrow
from MyButton import Sphere
from MyButton import MySlider

def depthCmp(obj1,obj2):
    return int(obj2.sZ - obj1.sZ)

def depthCmp2(obj1,obj2):
    return int(obj2[2] - obj1[2])

def matrixSolver(A,B):
    rows,cols = len(A),len(B)
    i,j = 0,0
    while (i<rows):
        #If there is a zero in that place
        while A[i][j]==0:
            i+=1
        temp = A[i][j]
        
        #Check for the zero case
        if i!=j:
            for col in xrange(cols):
                A[j][col] += A[i][col]/temp
            B[j] += B[i]/temp
        else:
            for col in xrange(cols):
                A[j][col] /= temp
            B[j] /= temp
        
        #Make other rows zero
        for row in xrange(rows):
            if row != j:
                temp = A[row][j]
                for col in xrange(cols):
                    A[row][col] = A[row][col] - A[j][col]*temp
                B[row]-=B[j]*temp
        j += 1
        i = j
    return B
        
class MainInterface(object):
    def __init__(self,w,h):
        self.scaleVector = [[100.0,0.0,0.0],[0.0,100.0,0.0],[0.0,0.0,100.0]]
        self.fixedVector = [1.0*w/2,1.0*(h/2)-100,0.0]
        self.centerVector = [1.0*w/2,1.0*(h/2)-100,0.0]
        self.mouseX,self.mouseY = 0,0
        self.run(w,h)

    # Call app.run(width,height) to get your app started
    def run(self, width=800, height=600):
        # create the root and the canvas
        root = Tk()
        self.width = width
        self.height = height
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
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
        def mousePressedWrapper(event):
            self.mousePressed(event)
            redrawAllWrapper()
        def mouseReleasedWrapper(event):
            self.mouseReleased(event)
            redrawAllWrapper()
        def mouseMotion(event):
            self.mouseX = event.x
            self.mouseY = event.y

        root.bind("<Button-1>", mousePressedWrapper)
        root.bind("<ButtonRelease-1>", mouseReleasedWrapper)
        root.bind("<Key>", keyPressedWrapper)
        self.canvas.bind("<Motion>", mouseMotion)

        # set up timerFired events
        self.timerFiredDelay = 10 # milliseconds
        def timerFiredWrapper():
            self.timerFired()
            redrawAllWrapper()
            # pause, then call timerFired again
            self.canvas.after(self.timerFiredDelay, timerFiredWrapper)
        # init and get timerFired running
        self.init()
        timerFiredWrapper()
        # and launch the app
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
    
    def modeReset(self):
        self.polygonPressC = False
        self.testLine = 0
        self.tempStorage = []
        self.isAddPoint = False
        self.isAddCurve = False
        self.isAddLine = False
        self.isAddPoly = False
        self.isDelete = False
        self.isChangeColor = False
    
    def deleteAll(self):
        MyButton.buttonList = []
        MySlider.sliderList = []
        MyArrow.arrowList = []
        Sphere.sphereList = []
        self.deleteObjects()
        
    def deleteObjects(self):
        
        Polygon.polyList = []
        Line.lineList = []
        Point.pointList = []
        
        Point.pointCount = 0
        Line.lineCount = 0
        Polygon.polyCount = 0
        
        self.scaleVector = [[100.0,0.0,0.0],[0.0,100.0,0.0],[0.0,0.0,100.0]]
        w,h = self.width,self.height
        self.fixedVector = [1.0*w/2,1.0*(h/2)-100,0.0]
              
    def init(self):
        self.deleteAll()
        self.msg = ""
        self.newPoint = [0.0,0.0,0.0]
        self.drawList = []
        self.hitList = []
        self.dragList = []
        self.oldMX,self.oldMY = 0,0
        self.event = None
        self.keyCPressed = False
        self.selected = None
        self.isMouse = False
        self.modeReset()
        self.color = "#FFFFFF"
        self.filename = "save.txt"
        
        MyButton(self.width,200,0,400,self)
        MyButton(30,30,20,415,self,"AddPointButton")
        MyButton(30,30,20,450,self,"AddLineButton")
        MyButton(30,30,20,485,self,"AddCurveButton")
        MyButton(30,30,20,520,self,"AddPolyButton")
        MyButton(30,30,20,555,self,"DeleteButton")
        MyButton(30,30,65,555,self,"ColorButton")

        MyButton(30,30,110,415,self,"ZoomInButton")
        MyButton(30,30,110,450,self,"ZoomOutButton")
        MyButton(30,30,110,485,self,"LoadButton")
        MyButton(30,30,110,520,self,"SaveButton")
        MyButton(30,30,110,555,self,"ClearScreenButton")

        MyButton(300,30,150,555,self,"MessageButton")
        
        MyArrow(50,50,525,425,1,self)
        MyArrow(50,50,575,475,2,self)
        MyArrow(50,50,525,525,3,self)
        MyArrow(50,50,475,475,4,self)
        
        Sphere(75,725,500,self)

        MySlider(5,70,420,128,70,420,self,"#FF0000")
        MySlider(5,80,420,128,80,420,self,"#00FF00")
        MySlider(5,90,420,128,90,420,self,"#0000FF")
        
        '''
        p1=Point(0,0,0,"p1","#FF0000",self)
        p2=Point(0,0,1,"p2","#FFFF00",self)
        p3=Point(0,1,0,"p3","#00FF00",self)
        p4=Point(0,1,1,"p4","#00FFFF",self)
        p5=Point(1,0,0,"p5","#0000FF",self)
        p6=Point(1,0,1,"p6","#FF00FF",self)
        p7=Point(1,1,0,"p7","#FFFFFF",self)
        p8=Point(1,1,1,"p8","#000000",self)

        Polygon([[p1,0],[p2,0],[p4,0],[p3,0]],"poly1","#FF0000",self,3)
        Polygon([[p1,0],[p5,0],[p7,0],[p3,0]],"poly2","#FFFF00",self,3)
        Polygon([[p5,0],[p6,0],[p8,0],[p7,0]],"poly2","#00FF00",self,3)
        Polygon([[p6,0],[p2,0],[p4,0],[p8,0]],"poly2","#00FFFF",self,3)
        Polygon([[p1,0],[p2,0],[p6,0],[p5,0]],"poly2","#0000FF",self,3)
        Polygon([[p3,0],[p7,0],[p8,0],[p4,0]],"poly2","#FF00FF",self,3)
        '''
        
    def timerFired(self):
        canvas = self.canvas
        canvas.delete(ALL)
        moveSpeed = 5.0
        if self.isMouse == True:
            for i in MyArrow.getArrowList():
                if i.hitTest()==True:
                    if i.motion == 0:
                        self.shift(moveSpeed*i.dirs[0],moveSpeed*i.dirs[1],0)
                    else:
                        self.rotateZX(i.dirs[0]*math.pi/180)
                        self.rotateYZ(i.dirs[1]*math.pi/180)
                        
            for i in Sphere.getSphereList():
                if i.hitTest()==True:
                    rotateX = moveSpeed*(self.mouseX - i.x0)/i.r
                    rotateY = moveSpeed*(self.mouseY - i.y0)/i.r
                    
                    self.rotateZX(-rotateX*math.pi/180)
                    self.rotateYZ(rotateY*math.pi/180)
            
            if len(self.dragList)!=0:
                self.XYtoModel()
                for i in self.dragList:
                    if isinstance(i,Point)==True:
                        i.x += self.newPoint[0]-self.oldPoint[0]
                        i.y += self.newPoint[1]-self.oldPoint[1]
                        i.z += self.newPoint[2]-self.oldPoint[2]
                    else:
                        i.y = self.mouseY
                        if i.y<i.y0:
                            i.y = i.y0
                        if i.y>(i.y0+i.size):
                            i.y = i.y0+i.size
                        self.color = self.determineColor()
                    
                self.oldPoint = copy.deepcopy(self.newPoint)
    
    def loadFile(self):
        self.deleteObjects()
        try:
            with open(self.filename, "r") as f:
                contents = f.read()
            self.loadFromString(contents)
        except:
            pass
        
    def loadFromString(self, newLoad):
        newSections = newLoad.split('$')
        
        newPointSection = newSections[0].split('|')[1:]
        for point in newPointSection:
            pStats = point.split(',')
            Point(float(pStats[1]),float(pStats[2]),float(pStats[3]),pStats[0],pStats[4],self)
        
        newLineSection = newSections[1].split('|')[1:]
        for line in newLineSection:
            lineStat = line.split('[')
            lineName = lineStat[0].split(',')[0]
            lineColor = lineStat[0].split(',')[1]
            pointSection = lineStat[1].split(']')[0].split('*')[1:]
            listP = []
            for point in pointSection:
                pointStat = point.split(',')
                pointRef = None
                for i in Point.getPointList():
                    if i.name == pointStat[0]:
                        pointRef = i
                        break
                listP.append([pointRef,int(pointStat[1])])
            p = Line(listP,lineName,lineColor,self,3)
        
        newPolySection = newSections[2].split('|')[1:]
        for poly in newPolySection:
            polyStat = poly.split('[')
            polyName = polyStat[0].split(',')[0]
            polyColor = polyStat[0].split(',')[1]
            pointSection = polyStat[1].split(']')[0].split('*')[1:]
            listP = []
            for point in pointSection:
                pointStat = point.split(',')
                pointRef = None
                for i in Point.getPointList():
                    if i.name == pointStat[0]:
                        pointRef = i
                        break
                listP.append([pointRef,int(pointStat[1])])
            p = Polygon(listP,polyName,polyColor,self,3)
        
        newScaleVector = newSections[3].split('|')[1:]
        for idx in xrange(len(newScaleVector)):
            scaleStats = newScaleVector[idx].split(',')
            for idx2 in xrange(len(scaleStats)):
                self.scaleVector[idx][idx2] = float(scaleStats[idx2])
                
        newFixedVector = newSections[4].split('|')[1:]
        for idx in xrange(len(newFixedVector)):
            self.fixedVector[idx] =  float(newFixedVector[0].split(',')[idx])
        
        newCounts = newSections[5].split(',')
        Point.pointCount = float(newCounts[0])
        Line.lineCount = float(newCounts[1])
        Polygon.polyCount = float(newCounts[2])
            
    def saveFile(self):
        with open(self.filename, "w") as f:
            saveValues = self.saveString()
            f.write(saveValues)
                
    def saveString(self):
        newSave = ""
        for i in Point.getPointList():
            newSave += "|"+i.name+","+str(i.x)+","+str(i.y)+","+str(i.z)+","+i.color
        
        newSave += "$"
        for i in Line.getLineList():
            newSave += "|"+i.name+","+i.color+"["
            for point in i.listP:
                newSave += "*"+point[0].name + "," + str(point[1]) 
            newSave += "]"    
        newSave += "$"
        for i in Polygon.getPolyList():
            newSave += "|"+i.name+","+i.color+"["
            for point in i.listP:
                newSave += "*"+point[0].name + "," + str(point[1]) 
            newSave += "]"
        newSave += "$"
        for i in self.scaleVector:
            newSave += "|"+str(i[0])+","+str(i[1])+","+str(i[2])
        newSave += "$"
        i = self.fixedVector
        newSave += "|"+str(i[0])+","+str(i[1])+","+str(i[2])
        
        newSave += "$"
        newSave += str(Point.getPointCount())+","+str(Line.getLineCount())+","+str(Polygon.getPolyCount())
        return newSave
    
    def determineColor(self):
        red,green,blue=0,0,0
        for i in MySlider.getSliderList():
            if i.color == "#FF0000":
                red = int(255.0*(i.size-i.y+i.y0)/i.size)
            elif i.color == "#00FF00":
                green = int(255.0*(i.size-i.y+i.y0)/i.size)
            elif i.color == "#0000FF":
                blue = int(255.0*(i.size-i.y+i.y0)/i.size)
        return self.rgbString(red,green,blue)

    def mousePressed(self,event):
        self.isMouse = True
        self.XYtoModel()
        
        self.dragList = []
        
        if self.mouseY <= 400:
            if self.selected != None and self.selected.hitTest()==False:
                self.selected = None
            if self.isAddPoint == True:
                self.addPoint()
            elif self.isAddLine == True:
                self.addLine()
            elif self.isAddCurve == True:    
                self.addCurve()
            elif self.isAddPoly == True:
                self.addPolygon()
            elif len(self.hitList)!=0:
                last = len(self.hitList)-1
                i = self.hitList[last]
                self.oldPoint = copy.deepcopy(self.newPoint)
                self.selected = i
                if isinstance(i,Point)==True:
                    self.dragList.append(i)
                if isinstance(i,Polygon)==True or isinstance(i,Line)==True:
                    for point in i.listP:
                        self.dragList.append(point[0])

        for i in MyButton.getButtonList():
            i.buttonPressed()

        for i in MySlider.getSliderList():
            if i.hitTest()==True:
                self.dragList.append(i)

        if self.isDelete == True:
            self.removeInstance()
        elif self.isChangeColor == True:
            self.changeColor()
        self.redrawAll()   

    def changeColor(self):
        if self.selected != None:
            self.selected.color = self.color
        self.isChangeColor = False
    
    def mouseReleased(self,event):
        self.isMouse = False
        
    def keyPressed(self, event):
        if event.char == "c":
            self.keyCPressed = not self.keyCPressed
        if event.keysym == "Delete":
            self.removeInstance()

        if event.keysym == "Return" and self.isAddPoly == True:
            self.addPolygon(True)
        
    #Rotate functions 
    def rotate(self,x,y,theta): 
        radius = (x**2+y**2)**0.5
        angle = math.atan2(y,x)
        newX = radius*math.cos(angle+theta)
        newY = radius*math.sin(angle+theta)
        return newX,newY

    def redrawAll(self):
        self.canvas.create_rectangle(0,0,self.width,self.height,fill="black")
        self.drawList = []
        self.hitList = []
        for i in Point.getPointList():
            self.drawList.append(i)
        for i in Line.getLineList():
            self.drawList.append(i)
        for i in Polygon.getPolyList():
            self.drawList.append(i)
    
        self.drawList.sort(depthCmp)
        for i in self.drawList:
            if i.hitTest()==True:
                self.hitList.append(i)

        for i in self.drawList:
            i.draw()

        for i in MyButton.getButtonList():
            i.draw()
            
        for i in MyArrow.getArrowList():
            i.draw()

        for i in MySlider.getSliderList():
            i.draw()

        for i in Sphere.getSphereList():
            i.draw()
            sumOfSquares = (self.scaleVector[0][0]**2+self.scaleVector[0][1]**2+self.scaleVector[0][2]**2)**0.5
            textList = ['X','Y','Z']
            circleColor = ['#FF0000','#00FF00','#0000FF']
            count = 0

            tempVector = []

            for idx in xrange(len(self.scaleVector)):
                tempList = self.scaleVector[idx] + [textList[idx]] + [circleColor[idx]]
                tempVector.append(tempList)
                
            tempVector = sorted(tempVector,depthCmp2)
            
            for point in tempVector:
                cx = (1.0*i.r*point[0]/sumOfSquares+i.x0)
                cy = (1.0*i.r*point[1]/sumOfSquares+i.y0)
                r = 5
                self.canvas.create_line(i.x0,i.y0,cx,cy,width=3,fill=point[4])
                self.createCircle(cx,cy,r,point[4])
                self.canvas.create_text(cx,cy,text =point[3])
                count += 1

    def rgbString(self, red, green, blue):
        return "#%02x%02x%02x" % (red, green, blue)
    
    def createCircle(self,cx,cy,r,color):
        smallr = 10
        if r<1:
            return
        else:
            redNumber = int(color[1:],16)/(2**16)
            greenNumber = (int(color[1:],16)/(2**8))%(2**8)
            blueNumber = int(color[1:],16)%(2**8)

            red = int(1.0*(smallr-r)/smallr*(255-redNumber)+redNumber)
            green = int(1.0*(smallr-r)/smallr*(255-greenNumber)+greenNumber)
            blue = int(1.0*(smallr-r)/smallr*(255-blueNumber)+blueNumber)
            
            color = self.rgbString(red,green,blue)
            self.canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)
            self.createCircle(cx,cy-1,r-2,color)        

    #3 directions of rotations
    def rotateXY(self,theta):
        diff = [self.fixedVector[0]-self.centerVector[0],self.fixedVector[1]-self.centerVector[1]]
        for iV in self.scaleVector:
            iV[0],iV[1] = self.rotate(iV[0],iV[1],theta)
        diff[0],diff[1] = self.rotate(diff[0],diff[1],theta)
        self.fixedVector[0],self.fixedVector[1] = diff[0]+self.centerVector[0],diff[1]+self.centerVector[1]
    
    def rotateYZ(self,theta):
        diff = [self.fixedVector[1]-self.centerVector[1],self.fixedVector[2]-self.centerVector[2]]
        for iV in self.scaleVector:
            iV[1],iV[2] = self.rotate(iV[1],iV[2],theta)
        diff[0],diff[1] = self.rotate(diff[0],diff[1],theta)
        self.fixedVector[1],self.fixedVector[2] = diff[0]+self.centerVector[1],diff[1]+self.centerVector[2]
    
    def rotateZX(self,theta):
        diff = [self.fixedVector[2]-self.centerVector[2],self.fixedVector[0]-self.centerVector[0]]
        for iV in self.scaleVector:
            iV[2],iV[0] = self.rotate(iV[2],iV[0],theta)
        diff[0],diff[1] = self.rotate(diff[0],diff[1],theta)
        self.fixedVector[2],self.fixedVector[0] = diff[0]+self.centerVector[2],diff[1]+self.centerVector[0]

    def shift(self,x,y,z):
        self.fixedVector[0] += x
        self.fixedVector[1] += y
        self.fixedVector[2] += z

    def addPoint(self):
        name = "P"+str(Point.getPointCount()+1)
        p = Point(self.newPoint[0],self.newPoint[1],self.newPoint[2],name,self.color,self)
        self.isAddPoint = False
        return p

    def addLine(self):
        tempPoint = None
        name = "L"+str(Line.getLineCount()+1)
        for i in self.hitList:
            if isinstance(i,Point)==True:
                tempPoint = i
            
        if tempPoint == None:        
            self.tempStorage.append([self.addPoint(),0])
        else:
            self.tempStorage.append([tempPoint,0])
        
        if self.testLine == 0:
            self.testLine = 1
        else:
            l1 = Line(self.tempStorage,name,self.color,self,5)
            self.isAddLine = False
            self.tempStorage = []
            self.testLine = 0

    def addCurve(self):
        name = "L"+str(Line.getLineCount()+1)
        tempPoint = None
        for i in self.hitList:
            if isinstance(i,Point)==True:
                tempPoint = i
            
        if tempPoint == None:        
            self.tempStorage.append([self.addPoint(),1])
        else:
            self.tempStorage.append([tempPoint,1])
        
        if self.testLine <= 1:
            self.testLine +=1
        else:        
            l1 = Line(self.tempStorage,name,self.color,self,5)
            self.isAddCurve = False
            self.tempStorage = []
            self.testLine = 0
    
    def addPolygon(self,enterPressed=False):
        name = "Poly"+str(Polygon.getPolyCount()+1)
        tempPoint = None

        if enterPressed == True:
            tempPoint = self.tempStorage[0][0]
        else:
            for i in self.hitList:
                if isinstance(i,Point) == True:
                    tempPoint = i
            
            if tempPoint == None:
                tempPoint = self.addPoint()
            
        if (len(self.tempStorage)>0 and tempPoint == self.tempStorage[0][0]):
            self.testLine = 1
        else:    
            if self.keyCPressed == False or self.polygonPressC == True:
                self.tempStorage.append([tempPoint,0])
                self.polygonPressC = False
            else:
                self.tempStorage.append([tempPoint,1])
                self.polygonPressC = True
            
        if self.testLine == 1:        
            poly1 = Polygon(self.tempStorage,name,self.color,self,5)
            self.isAddPoly = False
            self.tempStorage = []
            self.testLine = 0
            self.keyCPressed = False

    def removeInstance(self):
        remLast = self.selected
        if isinstance(remLast,Polygon)==True:
            i = Polygon.polyList.index(remLast)
            Polygon.polyList = Polygon.polyList[:i]+Polygon.polyList[i+1:]
        elif isinstance(remLast,Line) == True:
            i = Line.lineList.index(remLast)
            Line.lineList = Line.lineList[:i]+Line.lineList[i+1:]
        elif isinstance(remLast,Point) == True:
            for i in self.drawList:
                if (isinstance(i,Point)==False and i!=None and
                    ([remLast,0] in i.listP or [remLast,1] in i.listP)):
                    if isinstance(i,Polygon)==True:
                        idx = Polygon.polyList.index(i)
                        Polygon.polyList = Polygon.polyList[:idx]+Polygon.polyList[idx+1:]
                    elif isinstance(i,Line) == True:
                        idx = Line.lineList.index(i)
                        Line.lineList = Line.lineList[:idx]+Line.lineList[idx+1:]   
            idx = Point.pointList.index(remLast)
            Point.pointList = Point.pointList[:idx]+Point.pointList[idx+1:]
            
        remLast=None
        self.selected = None
        self.isDelete = False
        
    def XYtoModel(self):
        sV = self.scaleVector
        fV = self.fixedVector
        
        sX,sY,sZ = self.mouseX,self.mouseY,0
        
        #AX = B
        A = [[sV[0][0],sV[1][0],sV[2][0]],
             [sV[0][1],sV[1][1],sV[2][1]],
             [sV[0][2],sV[1][2],sV[2][2]]]
  
        B = [sX-fV[0],
             sY-fV[1],
             sZ-fV[2]]
        
        self.newPoint = matrixSolver(A,B)
    
m = MainInterface(800,600)




