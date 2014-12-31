from Utility import *

class Line(object):
    lineList = []
    lineCount = 0
    @classmethod
    def getLineList(cls):
        return Line.lineList
    
    @classmethod
    def getLineCount(cls):
        return int(Line.lineCount)
    
    def __init__(self,listP,name,color,mainInt,width=5):
        #List of Points and coodinates
        self.listP = listP
        self.listC = []
        
        self.name = name
        self.color = color
        self.width = width
        self.main = mainInt
        
        #Identify for curves
        if self.listP[0][1]==1: self.curve = True
        else: self.curve = False
        
        #Depth control
        self.sZ = 0
        Line.lineList.append(self)
        Line.lineCount += 1
    
    def step(self):
        listP = self.listP
        
        #Sum up the depth
        self.sZ,lenP = 0,len(self.listP)
        for point in self.listP:
            self.sZ += point[0].sZ/lenP

        #Get the coordinates
        x0,y0,z0=listP[0][0].sX,listP[0][0].sY,listP[0][0].sZ
        x1,y1,z1=listP[1][0].sX,listP[1][0].sY,listP[1][0].sZ
        
        #If it is curve
        if self.curve == True:
            x2,y2,z2=listP[2][0].sX,listP[2][0].sY,listP[2][0].sZ
            self.listC = beizerCurve(x0,y0,x1,y1,x2,y2)
        else:
            self.listC = [x0,y0,x1,y1]
            
    def draw(self):
        self.step()
        #Draw the line
        for i in xrange(0,len(self.listC)-2,2):
            x0,y0 = self.listC[i],self.listC[i+1]
            x1,y1 = self.listC[i+2],self.listC[i+3]
            
            #If not the top hit by mouse and not selected, then dun highlight
            if ([self]==self.main.hitList[-1:] or self==self.main.selected):
                self.main.canvas.create_line(x0,y0,x1,y1,
                                             fill="white",width=self.width+2)
                
                if self.main.mouseY<=self.main.boundY:
                    self.main.msg = "<Line: %s>" % (self.name)
            
            self.main.canvas.create_line(x0,y0,x1,y1,
                                             fill=self.color,width=self.width)

    def hitTest(self):
        if (hitTestLine(self.listC,(self.main.mouseX,
                                   self.main.mouseY),self.width)==True):
            return True
        else:
            return False

class tempLine(object):
    def __init__(self,listP,name,color,mainInt,width=1):
        self.listP = listP
        self.listC = []
        self.name = name
        self.main = mainInt
        self.color = color
        self.width = width
        self.sZ = 0
        
        #Contain the mouse point
        if self.main.isAddCurve == False:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,0]]
        else:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,1]]
        
        #Identify for curves
        if self.listP[0][1]==1: self.curve = True
        else: self.curve = False
            
    def step(self):
        #Get the average depth
        self.color = self.main.color
        
        #Add the mouse point to temp storage
        if self.main.isAddLine == True:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,0]]
            self.curve = False
        elif self.main.isAddCurve == True:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,1]]
            self.curve = True
        else:
            self.listP = [[self.main.tempPoint,1]]
            return
        
        if len(self.listP)<2:
            return
        
        listP = self.listP
        
        #Get the coordinates
        x0,y0,z0=listP[0][0].sX,listP[0][0].sY,listP[0][0].sZ
        x1,y1,z1=listP[1][0].sX,listP[1][0].sY,listP[1][0].sZ

        if self.curve == False or len(self.listP)<=2:
            #Draw basic line
            self.listC = [x0,y0,x1,y1]
        else:
            #Find parts
            x2,y2,z2=listP[2][0].sX,listP[2][0].sY,listP[2][0].sZ
            self.listC = beizerCurve(x0,y0,x1,y1,x2,y2)

    def draw(self):
        self.step()
        #Draw the line
        if (len(self.listP)>1 and (self.main.isAddLine == True
                                   or self.main.isAddCurve==True)):
            
            for i in xrange(0,len(self.listC)-2,2):
                x0,y0 = self.listC[i],self.listC[i+1]
                x1,y1 = self.listC[i+2],self.listC[i+3]
                self.main.canvas.create_line(x0,y0,x1,y1,
                                             fill=self.color,width=self.width)


    
