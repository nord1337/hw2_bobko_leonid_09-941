import numpy as np
import matplotlib.pyplot as plt
import math

class ObjParser:

    def __init__(self, path):
        self.path=path
        self.vertices=list()
        self.faces = list()
        self.maxCoord=int()
        self.minCoord=int()
        self.absMaxCoord=int()
        self.parse()
    def parse(self):
        toParse = list()
        with open(self.path,'r') as ObjFile:
            for line in ObjFile:
                toParse.append(line.replace('\n',''))
        for line in toParse:
            arrData=line.split(' ')
            if arrData[0]=='v':
                self.vertices.append([float(arrData[1]),float(arrData[2]),float(arrData[3])])
            if arrData[0]=='f':
                self.faces.append([int(arrData[1]),int(arrData[2]),int(arrData[3])])
        tempMax=0
        tempMin=0
        for i in range(len(self.vertices)):
            for x in self.vertices[i]:
                if x>tempMax:
                    tempMax=x
                if x<tempMin:
                    tempMin=x
        self.maxCoord=tempMax
        self.minCoord=tempMin
        self.absMaxCoord= abs(tempMax) if abs(tempMax)>abs(tempMin) else abs(tempMin)


class Draw2D:
    @staticmethod
    def OldCoordToNew(x,y,OldMaxCoord,N):
        return int(round(((x+OldMaxCoord)*(N/(2.1*OldMaxCoord))),0)),int(round((y+OldMaxCoord)*(N/(2.1*OldMaxCoord)),0)) 
    @staticmethod
    def Draw(obj3D:ObjParser,base_color:np.array,img:np.array,N:int):
        for i in range(len(obj3D.faces)):
            coordA_x,coordA_y=Draw2D.OldCoordToNew(obj3D.vertices[obj3D.faces[i][0]-1][0],obj3D.vertices[obj3D.faces[i][0]-1][1],obj3D.absMaxCoord,N)
            coordB_x,coordB_y=Draw2D.OldCoordToNew(obj3D.vertices[obj3D.faces[i][1]-1][0],obj3D.vertices[obj3D.faces[i][1]-1][1],obj3D.absMaxCoord,N)
            coordC_x,coordC_y=Draw2D.OldCoordToNew(obj3D.vertices[obj3D.faces[i][2]-1][0],obj3D.vertices[obj3D.faces[i][2]-1][1],obj3D.absMaxCoord,N)
            Draw2D.Bresenham_Drawline(img,base_color,coordA_x,coordA_y,coordB_x,coordB_y,N,obj3D.absMaxCoord)
            Draw2D.Bresenham_Drawline(img,base_color,coordA_x,coordA_y,coordC_x,coordC_y,N,obj3D.absMaxCoord)
            Draw2D.Bresenham_Drawline(img,base_color,coordB_x,coordB_y,coordC_x,coordC_y,N,obj3D.absMaxCoord)
            

    @staticmethod 
    def FillPixel(img:np.array,x:int,y:int,N:int,base_color:np.array):
        d=int(math.sqrt((((N/2)-x)**2 + ((N/2)-y)**2)))
        color=(base_color*((1-d/N)))
        img[x,y]=color

    
    @staticmethod 
    def Bresenham_Drawline(img:np.array,base_color:np.array,x0,y0,x1,y1,N,oldMaxCoord):
        dx,dy=x1-x0,y1-y0
        sign_x = 1 if dx>0 else -1 if dx<0 else 0
        sign_y = 1 if dy>0 else -1 if dy<0 else 0

        if dx < 0: 
            dx = -dx
        if dy < 0: 
            dy = -dy
        
        if dx > dy:
            pdx, pdy = sign_x, 0
            es, el = dy, dx
        else:
            pdx, pdy = 0, sign_y
            es, el = dx, dy
        
        x, y = x1, y1
        
        error, t = el/2, 0        
        
        Draw2D.FillPixel(img,x,y,N,base_color)
        
        while t < el:
            error -= es
            if error < 0:
                error += el
                x += sign_x
                y += sign_y
            else:
                x += pdx
                y += pdy
            t += 1
            Draw2D.FillPixel(img,x,y,N,base_color)
        
        

            


        




              
obj=ObjParser("teapot.obj")
print(obj.faces)

#constants 
N=int(1024)
img=np.zeros((N,N,3),dtype=np.uint8)
img[0:N,0:N]=[255,255,255]
base_color=np.array([255,0,0],dtype=np.uint8)

#drawing
Draw2D.Draw(obj,base_color,img,N)

plt.figure()
img=np.rot90(img)
plt.imshow(img)
plt.show()
plt.imsave("image.png",img)
 


