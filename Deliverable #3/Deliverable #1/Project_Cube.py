import math
from Tkinter import *

Trial = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],[1,0,0],[1,0,1],[1,1,0],[1,1,1]]
Link = [[0,1],[0,2],[0,4],[1,3],[1,5],[2,6],[2,3],[3,7],[4,5],[4,6],[5,7],[6,7]]
Face = [[0,1,3,2,0,0],[0,1,5,4,0,1],[4,5,7,6,0,2],[2,3,7,6,0,3],[0,4,6,2,0,4],[1,5,7,3,0,5]]

#Trial = [[0,0,0],[1,0,0],[0,1,0]]
#Face = [[0,1,2,0,0,0]]
#Link = [[0,1],[1,2],[0,2]]

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def Fun3D():
    global Trial
    global Link
    global Face
    scale = 100
    
    Trial = RotateXY(Trial)
    Trial = RotateYZ(Trial)
    Trial = RotateZX(Trial)

    for FaceC in xrange(len(Face)):
        F1 = Face[FaceC][0]
        F2 = Face[FaceC][1]
        F3 = Face[FaceC][2]
        F4 = Face[FaceC][3]
        Face[FaceC][4] = Trial[F1][2]+Trial[F2][2]+Trial[F3][2]+Trial[F4][2]

    Face.sort(key=lambda x: x[4])

    
    for FaceC in xrange(len(Face)):
        F1 = Face[FaceC][0]
        F2 = Face[FaceC][1]
        F3 = Face[FaceC][2]
        F4 = Face[FaceC][3]
        FaceColor = Face[FaceC][5]

        if FaceColor < 3:
            color = rgbString(255*(FaceColor%3==0), 255*(FaceColor%3==1), 255*(FaceColor%3==2))
        else:
            color = rgbString(255*(FaceColor%3!=0), 255*(FaceColor%3!=1), 255*(FaceColor%3!=2))
        
        canvas.create_polygon([Trial[F1][0]*scale+100],[Trial[F1][1]*scale+100],[Trial[F2][0]*scale+100],[Trial[F2][1]*scale+100],
                              [Trial[F3][0]*scale+100],[Trial[F3][1]*scale+100],[Trial[F4][0]*scale+100],[Trial[F4][1]*scale+100],
                              fill = color)
        
    for linkC in xrange(len(Link)):
        P1 = Link[linkC][0]
        P2 = Link[linkC][1]
        #canvas.create_line(Trial[P1][0]*scale+100, Trial[P1][1]*scale+100,Trial[P2][0]*scale+100,Trial[P2][1]*scale+100,fill="black", width=1)

    #for x in xrange(len(Trial)):
        #canvas.create_oval(Trial[x][0]*scale-5+100, Trial[x][1]*scale-5+100, Trial[x][0]*scale+5+100, Trial[x][1]*scale+5+100)
    
def RotateXY(Input):
    theta = 1*math.pi/180
    for point in xrange(len(Input)):
        radius = (Input[point][0]**2+Input[point][1]**2)**0.5
        angle = math.atan2(Input[point][1],Input[point][0])
        Input[point][0] = radius*math.cos(angle+theta)
        Input[point][1] = radius*math.sin(angle+theta)
    return Input

def RotateYZ(Input):
    theta = 1*math.pi/180
    for point in xrange(len(Input)):
        radius = (Input[point][2]**2+Input[point][1]**2)**0.5
        angle = math.atan2(Input[point][2],Input[point][1])
        Input[point][1] = radius*math.cos(angle+theta)
        Input[point][2] = radius*math.sin(angle+theta)
    return Input

def RotateZX(Input):
    theta = 1*math.pi/180
    for point in xrange(len(Input)):
        radius = (Input[point][2]**2+Input[point][0]**2)**0.5
        angle = math.atan2(Input[point][0],Input[point][2])
        Input[point][2] = radius*math.cos(angle+theta)
        Input[point][0] = radius*math.sin(angle+theta)
    return Input


def run():
    root = Tk()
    global canvas
    canvas = Canvas(root, width=600, height=600)
    canvas.pack()
    timerFired()
    root.mainloop()

def timerFired():
    delay = 100 # milliseconds
    redrawAll()
    Fun3D()
    canvas.after(delay, timerFired) # pause, then call timerFired again

def redrawAll():
    canvas.delete(ALL)

run()
