from Utility import *
    
class Polygon(object):
    polyList = []
    polyCount = 0    

    @classmethod
    def getPolyList(cls):
        return Polygon.polyList

    @classmethod
    def getPolyCount(cls):
        return int(Polygon.polyCount)
    
    def __init__(self,listP,name,color,mainInt,width=5):
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
        listP = self.listP
        self.listC = []
        
        #Sum up the depth
        self.sZ,lenP = 0,len(self.listP)
        for point in self.listP:
            self.sZ += point[0].sZ/lenP
        
        i = 0
        lenOfPoints = len(self.listP)
        while i < lenOfPoints:            
            #If it is not a curve
            if listP[i][1] == 0 or i+1==lenOfPoints:
                x0,y0,z0 = listP[i][0].sX,listP[i][0].sY,listP[i][0].sZ
                self.listC.extend([x0,y0])
                i+=1
            else:
                #For curves
                n0,n1,n2 = i,(i+1)%lenOfPoints,(i+2)%lenOfPoints

                x0,y0,z0 = listP[n0][0].sX,listP[n0][0].sY,listP[n0][0].sZ
                x1,y1,z1 = listP[n1][0].sX,listP[n1][0].sY,listP[n1][0].sZ
                x2,y2,z2 = listP[n2][0].sX,listP[n2][0].sY,listP[n2][0].sZ

                self.listC.extend(beizerCurve(x0,y0,x1,y1,x2,y2))
                i+=2
            
    def draw(self):
        self.step()

        
        if self.main.transparent == True:
            trans = "gray50"
        else:
            trans = ""
            

        #If not the top hit by mouse and not selected, then dun highlight
        if ([self]==self.main.hitList[-1:] or self==self.main.selected):
            self.main.canvas.create_polygon(self.listC,fill=self.color,outline="white",width=self.width,stipple=trans,activefill=self.color)
            if self.main.mouseY<=self.main.boundY:
                self.main.msg = "<Polygon: %s>" % (self.name)
        else:
            self.main.canvas.create_polygon(self.listC,fill=self.color,outline=self.color,stipple=trans)

    
    def hitTest(self):        
        if rayCast(self.listC,(self.main.mouseX,self.main.mouseY)):
            return True
        else:
            return False

        
class tempPolygon(object):
    
    def __init__(self,listP,name,color,mainInt,width=3):
        self.listC = []
        self.color = color
        self.canvas = mainInt.canvas
        self.width = width
        self.name = name
        self.main = mainInt
        if self.main.keyCPressed == False or self.main.polygonPressC == True:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,0]]
        else:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,1]]

        self.sZ = 0
    
    def step(self):
        #Get the average depth
        self.color = self.main.color
        if self.main.keyCPressed == False or self.main.prevPointCurve == True:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,0]]
        else:
            self.listP = self.main.tempStorage + [[self.main.tempPoint,1]]
        self.listC = []
        
        listP = self.listP
        
        i = 0
        lenOfPoints = len(self.listP)
        while i < lenOfPoints:            
            #If it is not a curve
            if listP[i][1] == 0 or i+1==lenOfPoints:
                x0,y0,z0 = listP[i][0].sX,listP[i][0].sY,listP[i][0].sZ
                self.listC.extend([x0,y0])
                i+=1
            else:
                #For curves
                n0,n1,n2 = i,(i+1)%lenOfPoints,(i+2)%lenOfPoints

                x0,y0,z0 = listP[n0][0].sX,listP[n0][0].sY,listP[n0][0].sZ
                x1,y1,z1 = listP[n1][0].sX,listP[n1][0].sY,listP[n1][0].sZ
                x2,y2,z2 = listP[n2][0].sX,listP[n2][0].sY,listP[n2][0].sZ

                self.listC.extend(beizerCurve(x0,y0,x1,y1,x2,y2))
                i+=2
            
    def draw(self):
        self.step()
        if len(self.listP)!=1 and self.main.isAddPoly == True:
            self.main.canvas.create_polygon(self.listC,fill=self.color,outline=self.color,stipple="gray50",activefill=self.color)


