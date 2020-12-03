
from win32com.client import DispatchEx  #module needed for opening MagNet

MN = DispatchEx("MagNet.Application")   #open MagNet
MN.Visible = True                       #make the MagNet window visible

#Get Handles to MAGNET Scripting Interfaces
Doc = MN.newDocument()                  
View = Doc.getView()

#define function for drawing circles x,y are the coordinates of the centre, r is radius
def DrawCircle(x, y, r):
    View.newCircle(x, y, r)
#define function for drawing sqaures x,y are the coordinates of the centre, l is side length
def DrawSquare(x, y, l):
    View.newLine(x-l/2,y-l/2,x+l/2,y-l/2)
    View.newLine(x+l/2,y-l/2,x+l/2,y+l/2)
    View.newLine(x+l/2,y+l/2,x-l/2,y+l/2)
    View.newLine(x-l/2,y+l/2,x-l/2,y-l/2)

DrawCircle(0, 0, 50)

DrawSquare(0, 0, 30)

    
View.viewAll() #zoom out to view whole geometry
