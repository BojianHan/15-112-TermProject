from Tkinter import *
import math
import copy
import string
import random

#Depth comparison for objects
def depthCmp(obj1,obj2):
    if obj2.sZ > obj1.sZ: return 1
    else: return -1

#Depth comparison for lists
def depthCmp2(cood1,cood2):
    if cood2[2] > cood1[2]: return 1
    else: return -1

#By Gaussian Elimination
def matrixSolver(A,B):
    rows,cols,i,j = len(A),len(B),0,0
    while (i<rows):
        #If there is a zero in that place
        #Continue until there is no zero in that column
        while A[i][j]==0:
            i+=1
        temp = A[i][j]
        
        if i!=j:
            #If there is a zero in the j,j position
            #Then add the values from the temp row
            #So that the zero in the j,j position disappear
            for col in xrange(cols):
                A[j][col] += A[i][col]/temp
            B[j] += B[i]/temp
        else:
            #Divide the values such that the value in j,j position
            #is 1.
            for col in xrange(cols):
                A[j][col] /= temp
            B[j] /= temp
        
        #Make other rows zero using the j,j row
        for row in xrange(rows):
            if row != j:
                #This temp is the value in the j column for the
                #row,j position
                temp = A[row][j]
                for col in xrange(cols):
                    A[row][col] = A[row][col] - A[j][col]*temp
                B[row]-=B[j]*temp
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
    radius = (x**2+y**2)**0.5
    angle = math.atan2(y,x)
    newX = radius*math.cos(angle+theta)
    newY = radius*math.sin(angle+theta)
    return newX,newY
            
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def createCircle(canvas,cx,cy,r,color,oriR,oriC=None):
    if oriC == None:
        oriC = color
    else:
        color = oriC
    full = 255.0
    if r<1:
        return
    else:
        redNumber = int(color[1:],16)/(2**16)
        greenNumber = (int(color[1:],16)/(2**8))%(2**8)
        blueNumber = int(color[1:],16)%(2**8)
        red = int(1.0*(oriR-r)/oriR*(full-redNumber)+redNumber)
        green = int(1.0*(oriR-r)/oriR*(full-greenNumber)+greenNumber)
        blue = int(1.0*(oriR-r)/oriR*(full-blueNumber)+blueNumber)
        
        color = rgbString(red,green,blue)
        
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)
        createCircle(canvas,cx,cy-1,r-2,color,oriR,oriC)

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

def hitTestLine(point,mouse,r):   
    for i in xrange(0,len(point)-2,2):
        #Check between 2 points
        p1,p2 = i,i+2
        P1 = [1.0*point[p1%len(point)],1.0*point[(p1+1)%len(point)]]
        P2 = [1.0*point[p2%len(point)],1.0*point[(p2+1)%len(point)]]

        #If P1's x is bigger than P2's x, swap them
        if P1[0]>P2[0]:
            P1,P2 = P2,P1

        #If the mouse y is within the bound of the line and r
        if (P1[1]-r<=mouse[1]<=P2[1]+r or
            P1[1]+r>=mouse[1]>=P2[1]-r):
            
            #Difference in x and y between P1 and P2
            x0 = P2[0]-P1[0]
            y0 = P2[1]-P1[1]

            #the y distance between mouse and P1
            y1 = mouse[1]-P1[1]

            #the x distance between mouse and P1
            if y0 == 0: x1 = x0
            else: x1 = y1/y0*x0
            
            if abs(mouse[0]-(x1+P1[0]))<=r:
                return True
    return False

def hitTestCircle(x0,y0,r,mouse):
    if (r**2>=((mouse[0]-x0)**2+(mouse[1]-y0)**2)):
        return True
    else:
        return False
    
def boundBox(listC,mouse):
    if len(listC) == 0:
        return False
    
    xList = [listC[i] for i in xrange(len(listC)) if i%2==0]
    yList = [listC[i] for i in xrange(len(listC)) if i%2==1]

    if (min(xList)<=mouse[0] <=max(xList) and
        min(yList)<=mouse[1] <=max(yList)):
        return True
    else:
        return False
        
def rayCast(point,mouse):
    newX = []

    if boundBox(point,mouse)==False:
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

    check = 0
    for i in xrange(len(newX)):
        if newX[i]<mouse[0]:
            check += 1

    #Check raycast for even and odd
    if check%2 == 1: return True
    else: return False
