import math
import copy
from Tkinter import *
import math


#point = [[0,400],[0,100],[300,100],[100,300],[300,300],[300,100],[400,100],[400,400]]

oriPoint = [[0,400],[0,100],[300,100],[100,300],[300,300],[300,100],[400,100],[400,400]]


point = [[100,100],[100,300],[300,300],[300,100]]
newPoint = []

parts = 10

for i in xrange(0,len(point),2):
    for part in xrange(parts):
        n0 = i%len(point)
        n1 = (i+1)%len(point)
        n2 = (i+2)%len(point)
        t = 1.0*part/parts
        B = [0,0]
        B[0] = point[n0][0]*(1-t)**2+2*(1-t)*t*point[n1][0]+point[n2][0]*t**2
        B[1] = point[n0][1]*(1-t)**2+2*(1-t)*t*point[n1][1]+point[n2][1]*t**2
        newPoint.append(B)

#newPoint.append(point[len(point)-1])

point = copy.deepcopy(newPoint)


#point = [[100.0,100.0],[200.0,0.0],[400.0,100.0],[300.0,300.0]]
#point = [[0,400],[0,100],[300,100],[100,300],[300,300],[300,100],[400,100],[400,400]]
#point = [[0,0],[300,0],[300,100],[100,100],[100,300],[300,300],[300,400],[0,400]]
mouse = [0,0]

def snakemousePressed(canvas,event):
    global mouse
    mouse[0],mouse[1]=event.x,event.y
    redrawAll(rayCast())

for i in xrange(len(point)):
    point[i][0] += 0.0
    point[i][1] += 0.0 

def rayCast():
    newX = []
    for i in xrange(len(point)):
        P1 = point[i%len(point)]
        P2 = point[(i+1)%len(point)]

        if P1[0]>P2[0]:
            P1,P2 = copy.copy(P2),copy.copy(P1)
            
        if P1[1]<=mouse[1]<=P2[1] or P1[1]>=mouse[1]>=P2[1]:
            x0 = P2[0]-P1[0]
            y0 = P2[1]-P1[1]
            y1 = mouse[1]-P1[1]

            if y1 == y0 == 0:
                x1 = x0
            else:
                x1 = y1/y0*x0
            
            newX.append(x1+P1[0])

    newX.sort()
    check = 0
    for i in xrange(len(newX)):
        if newX[i]<mouse[0]:
            check += 1
        else:
            break

    if check%2 == 1:
        return True
    else:
        return False

from Tkinter import *
root = Tk()
root.bind("<Button-1>", lambda event:snakemousePressed(canvas,event))
canvas = Canvas(root, width=400, height=400)
canvas.pack()
canvas.create_polygon(point, fill="red",outline="black")

def redrawAll(found):
    canvas.delete(ALL)
    #canvas.create_polygon(oriPoint, fill="gray",outline="black")
    canvas.create_polygon(point, fill="red",outline="black")

    if found == False:
        canvas.create_text(mouse[0],mouse[1],text=mouse)
    else:
        canvas.create_text(mouse[0],mouse[1],text="YES")
    
root.mainloop()


