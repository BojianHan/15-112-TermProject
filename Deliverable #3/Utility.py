from Tkinter import *
import math
import copy
import string
import random

def createCircle(canvas,cx,cy,r,color,oriR,oriC=None):
    #oriC is the original color from the first fn call
    if oriC == None:
        oriC = color
    else:
        color = oriC
    full = 255.0
    
    #If radius is smaller than 1
    if r<1:
        return
    else:
        byteLen = 8
        #Get the color of individual components
        redNumber = int(color[1:],2*byteLen)/(2**(2*byteLen))
        greenNumber = (int(color[1:],2*byteLen)/(2**byteLen))%(2**byteLen)
        blueNumber = int(color[1:],2*byteLen)%(2**byteLen)
        
        #Shift in color
        red = int(1.0*(oriR-r)/oriR*(full-redNumber)+redNumber)
        green = int(1.0*(oriR-r)/oriR*(full-greenNumber)+greenNumber)
        blue = int(1.0*(oriR-r)/oriR*(full-blueNumber)+blueNumber)
        
        #New color
        color = rgbString(red,green,blue)
        
        #Create smaller circles
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)
        createCircle(canvas,cx,cy-1,r-2,color,oriR,oriC)

#Depth comparison for objects
def depthCmp(obj1,obj2):
    #Compare objects depth
    if obj2.sZ > obj1.sZ: return 1
    else: return -1

#Depth comparison for lists
def depthCmp2(cood1,cood2):
    #Compare coordinate depth
    if cood2[2] > cood1[2]: return 1
    else: return -1

#By Gaussian Elimination (Only for solvable ones)
#Programmed myself!!!
def matrixSolver(A,B):
    rows,cols,i,j = len(A),len(B),0,0
    A,B = copy.deepcopy(A),copy.deepcopy(B)
    while (i<rows):
        #If there is a zero in that place
        #Continue until there is no zero in that column
        while A[i][j]==0:i+=1
        temp = 1.0*A[i][j]
        
        if i!=j:
            #If there is a zero in the j,j position
            #Then add the values from the temp row
            #So that the zero in the j,j position disappear
            for col in xrange(cols):A[j][col] += 1.0*A[i][col]/temp
            B[j] += 1.0*B[i]/temp
        else:
            #Divide the values such that the value in j,j position
            #is 1.
            for col in xrange(cols):A[j][col] /= 1.0*temp
            B[j] /= 1.0*temp
        
        #Make other rows zero using the j,j row
        for row in xrange(rows):
            if row != j:
                #This temp is the value in the j column for the
                #row,j position
                temp = 1.0*A[row][j]
                for col in xrange(cols):
                    A[row][col] = 1.0*A[row][col] - 1.0*A[j][col]*temp
                B[row]-= 1.0*B[j]*temp
        i,j = j+1,j+1
    return B

def dotProduct(A,B):
    total = 0
    #Add the products together
    for idx in xrange(len(A)):
        total += A[idx]*B[idx]
    return total
            
#Rotate functions 
def rotate(x,y,theta):
    #Get the radius and angle
    radius = (x**2+y**2)**0.5
    angle = math.atan2(y,x)
    
    #Shift the angle and compute new X and new Y
    newX = radius*math.cos(angle+theta)
    newY = radius*math.sin(angle+theta)
    return newX,newY

'''rgbString Taken from http://www.cs.cmu.edu/~112/'''            
def rgbString(red, green, blue):
    #Return color
    return "#%02x%02x%02x" % (red, green, blue)

'''
Bezier curve equation taken and modified from
http://stackoverflow.com/questions/6711707/
draw-a-quadratic-bezier-curve-through-three-given-points
'''

def beizerCurve(x0,y0,x1,y1,x2,y2):
    #Find parts
    parts = int((abs(x2-x0)+abs(y2-y0))/10)+1
    listC = []

    #Get the bezier curve coordinates
    for part in xrange(parts+1):
        t = 1.0*part/parts
        B = [0,0]
        B[0] = x0*(1-t)**2+2*(1-t)*t*x1+x2*t**2
        B[1] = y0*(1-t)**2+2*(1-t)*t*y1+y2*t**2
        listC.extend(B)
        
    return listC

#Calculas textbook to find scalar projection
def hitTestLine(point,mouse,r):

    if boundBox(point,mouse,r)==False:
        return False

    sqrt = 0.5
    for i in xrange(0,len(point)-2,2):
        #Check between 2 points
        p1,p2 = i,i+2
        P1 = [1.0*point[p1%len(point)],1.0*point[(p1+1)%len(point)]]
        P2 = [1.0*point[p2%len(point)],1.0*point[(p2+1)%len(point)]]

        vectA = [P2[0]-P1[0],P2[1]-P1[1]]
        vectB = [mouse[0]-P1[0],mouse[1]-P1[1]]

        if dotProduct(vectA,vectA)!=0:
            #Distance to line
            compAB=dotProduct(vectA,vectB)/(dotProduct(vectA,vectA)**sqrt)
            distMouse = dotProduct(vectB,vectB)**sqrt
            
            distToLine = abs(distMouse**2 - compAB**2)**sqrt
            
            if distToLine <= r:
                return True
        
    return False

def hitTestCircle(x0,y0,r,mouse):
    #Bounding circle
    if (r**2>=((mouse[0]-x0)**2+(mouse[1]-y0)**2)):
        return True
    else:
        return False
    
def boundBox(listC,mouse,r=0):
    if len(listC) == 0:
        return False
    
    #Check for the min and max x and y
    xList = [listC[i] for i in xrange(len(listC)) if i%2==0]
    yList = [listC[i] for i in xrange(len(listC)) if i%2==1]

    if (min(xList)-r<=mouse[0]<=max(xList)+r and
        min(yList)-r<=mouse[1]<=max(yList)+r):
        return True
    else:
        return False
 
    
'''
Ray-casting algorithm learnt from:
http://rosettacode.org/wiki/Ray-casting_algorithm
'''
def rayCast(point,mouse,r=0):
    newX = []

    if boundBox(point,mouse,r)==False:
        return False

    for i in xrange(0,len(point),2):
        #Check between 2 points
        p1,p2 = i,i+2
        P1 = [1.0*point[p1%len(point)],1.0*point[(p1+1)%len(point)]]
        P2 = [1.0*point[p2%len(point)],1.0*point[(p2+1)%len(point)]]

        #If P1's x is bigger than P2's x
        if P1[0]>P2[0]:
            P1,P2 = P2,P1

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

    #Polygon face converted to a line
    if len(newX) == 1:
        return hitTestLine(point,mouse,r)

    check = 0
    for i in xrange(len(newX)):
        if newX[i]<mouse[0]:
            check += 1

    #Check raycast for even and odd
    if check%2 == 1: return True
    else: return False

def testDepthCmp():
    class Struct: pass
    a = Struct()
    a.sZ = 1
    b = Struct()
    b.sZ = 0
    c = Struct()
    c.sZ = -1
    
    assert(depthCmp(a,b)==-1)
    assert(depthCmp(c,b)==1)
    assert(depthCmp(a,c)==-1)
    
    print "depthCmp passed"

def testDepthCmp2():
    a = [1,1,1]
    b = [1,1,0]
    c = [1,1,-1]
    
    assert(depthCmp2(a,b)==-1)
    assert(depthCmp2(c,b)==1)
    assert(depthCmp2(a,c)==-1)
    
    print "depthCmp2 passed"

def testMatrixSolver():
    A = [[1,1,1],
         [1,2,3],
         [2,3,5]]
    B = [1,2,3]
    assert(matrixSolver(A,B)==[0,1,0])
    B = [2,4,6]
    assert(matrixSolver(A,B)==[0,2,0])
    A = [[1,2,1],
         [1,2,4],
         [2,3,5]]
    B = [1,4,6]
    assert(matrixSolver(A,B)==[2,-1,1])
    print "matrixSolver works"

def testDotProduct():
    A = [1,2,3]
    assert(dotProduct(A,A)==14)
    B = [1,2,4]
    assert(dotProduct(A,B)==17)
    assert(dotProduct(B,B)==21)
    print "dotProduct works"

def testRotate():
    assert (rotate(1,1,math.pi)==(-1.0000000000000002, -1.0))
    assert (rotate(2,1,math.pi/2)==(-1.0, 2.0))
    assert (rotate(1,0,math.pi/4)==(0.7071067811865476, 0.7071067811865475))
    print "rotate works"

def testRGB():
    assert (rgbString(255,255,255)=="#ffffff")
    assert (rgbString(255,0,255)=="#ff00ff")
    assert (rgbString(0,0,255)=="#0000ff")
    print "rgbString works"

def testBeizerCurve():
    assert (beizerCurve(0,0,1,1,0,4)==[0.0, 0.0, 0.0, 4.0])
    assert (beizerCurve(1,1,2,2,3,3)==[1.0, 1.0, 3.0, 3.0])
    assert (beizerCurve(20,20,30,30,20,20)==[20.0, 20.0, 20.0, 20.0])
    print "beizerCurve works"

def testHitTestLine():
    assert (hitTestLine([15,15,20,20],(15,15),5))
    assert (hitTestLine([15,15,20,20],(10,10),1)==False)
    assert (hitTestLine([10,10,20,20],(10,10),0))
    print "hitTestLine works"

def testHitTestCircle():
    assert (hitTestCircle(10,10,10,(5,5)))
    assert (hitTestCircle(10,10,10,(0,0))==False)
    assert (hitTestCircle(10,10,10,(7,7)))
    print "hitTestCircle passed"

def testBoundBox():
    assert (boundBox([0,0,10,10],(10,10)))
    assert (boundBox([0,0,10,10],(10,11))==False)
    assert (boundBox([0,0,10,10],(11,10))==False)
    print "boundBox works"

def testRayCast():
    assert (rayCast([0,0,0,10,10,10],(5,5))==True)
    assert (rayCast([0,0,0,10,10,10],(10,1))==False)
    assert (rayCast([0,0,0,10,10,10],(1,10))==True)
    
    print "rayCast works"

'''
testDepthCmp()
testDepthCmp2()
testMatrixSolver()
testDotProduct()
testRotate()
testRGB()
testBeizerCurve()
testHitTestLine()
testHitTestCircle()
testBoundBox()
testRayCast()
'''
