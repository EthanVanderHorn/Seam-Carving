from PIL import Image, ImageDraw
import math

def energyMap (image, Emap,width,height):
    for y in range(0,height):
        Emap=Emap+[[]]
        for x in range(0,width):
            if x == width-1 and y!=height-1:
                energy = abs(greyScale(x-1,y,image)-greyScale(x,y,image))+abs(greyScale(x,y+1,image)-greyScale(x,y,image))
                Emap[y]=Emap[y]+[energy]
            elif x != width-1 and y == height-1:
                energy = abs(greyScale(x+1,y,image)-greyScale(x,y,image))+abs(greyScale(x,y-1,image)-greyScale(x,y,image))
                Emap[y]=Emap[y]+[energy]
            elif x == width-1 and y == height-1:
                energy = abs(greyScale(x-1,y,image)-greyScale(x,y,image))+abs(greyScale(x,y-1,image)-greyScale(x,y,image))
                Emap[y]=Emap[y]+[energy]
            else:
                energy = abs(greyScale(x+1,y,image)-greyScale(x,y,image))+abs(greyScale(x,y+1,image)-greyScale(x,y,image))
                Emap[y]=Emap[y]+[energy]
    return Emap



def readEmap(x,y,Emap):
    return Emap[y][x]


def writeEmap(x,y,N,Emap):
    Emap[y][x] = N


def greyScale(x,y,image):
    (r,g,b) = image.getpixel((x, y))
    grey = int(r*.21)+int(g*.72)+int(b*.07)
    return grey

def shortestPath(image,Emap,width,height):
    for y in range( 1, height ):
        for x in range( width ):
            if (x==0):
                best = readEmap(x,y-1,Emap) + readEmap(x,y,Emap)
                n1 = readEmap(x+1,y-1,Emap) + readEmap(x,y,Emap)
                if best > n1:
                    best = n1
            elif (x==width-1):
                best = readEmap(x,y-1,Emap) + readEmap(x,y,Emap)
                n1 = readEmap(x-1,y-1,Emap) + readEmap(x,y,Emap)
                if best > n1:
                    best = n1
            else:
                best = readEmap(x-1,y-1,Emap) + readEmap(x,y,Emap)
                n1 = readEmap(x,y-1,Emap) + readEmap(x,y,Emap)
                n2 = readEmap(x+1,y-1,Emap) + readEmap(x,y,Emap)
                if best > n1:
                    best = n1
                if best > n2:
                    best = n2
            writeEmap(x,y,best,Emap)
    best = readEmap(0,height-1,Emap)
    bestx=0
    for x in range(width):
        n1 = readEmap(x,height-1,Emap)
        if best > n1:
            best = n1
            bestx = x
    return bestx


def pixelShift(image,startx,y,width,height):
    draw = ImageDraw.Draw(image)
    for x in range(startx, width-1):
        r,g,b = image.getpixel((x+1, y))
        draw.point([(x, y)], (r, g, b))
    draw.point([(width-1,y)], (0, 0, 0))
     
    

def carveSeam(image,Emap,x,width,height):
    y = height-1
    while y > 0:
        y = y-1
        pixelShift(image,x,y,width,height)
        if (x==0):
            best = readEmap(x,y-1,Emap)
            loc=x
            n1 = readEmap(x+1,y-1,Emap)
            if best > n1:
                best = n1
                loc=x+1
        elif x==width-1:
            best = readEmap(x,y-1,Emap)
            loc = x
            n1 = readEmap(x-1,y-1,Emap)
            if best > n1:
                best = n1
                loc = x-1
        else:
            best = readEmap(x-1,y-1,Emap)
            loc=x-1
            n1 = readEmap(x,y-1,Emap)
            n2 = readEmap(x+1,y-1,Emap)
            if best > n1:
                best = n1
                loc = x
            if best > n2:
                best = n2
                loc = x+1
        x = loc
    

def seamCarving (imageName, finalwidth,finalheight):
    image = Image.open(imageName)
    width,height = image.size
    #Calculate number of seams to carve for height and width.
    N=width-finalwidth
    if N<0:
        print 'You can not remove this many seams.'
        return N
    M=height-finalheight
    if M<0:
        print 'You can not remove this many seams.'
        return M
    #Rotate image.
    image=image.rotate(90)
    image1=image
    for var in range(M):
        if var>0:
            image=image1
        width,height = image.size
        Emap=[]
        Emap=energyMap(image,Emap,width,height)
        bestx = shortestPath(image,Emap,width,height)
        carveSeam(image,Emap,bestx,width,height)
        image1=Image.new('RGB',(width-1,height),(0,0,0))
        draw=ImageDraw.Draw(image1)
        for y in range(height):
            for x in range(width-1):
                r,g,b=image.getpixel((x, y))
                draw.point([(x, y)], (r,g,b))
        print var+1, ' Horizontal seams removed'
    image=image1
    image=image.rotate(270)
    for var in range(N):
        width,height = image.size
        Emap=[]
        Emap=energyMap(image,Emap,width,height)
        bestx = shortestPath(image,Emap,width,height)
        carveSeam(image,Emap,bestx,width,height)
        image1=Image.new('RGB',(width-1,height),(0,0,0))
        draw=ImageDraw.Draw(image1)
        for y in range(height):
            for x in range(width-1):
                r,g,b=image.getpixel((x, y))
                draw.point([(x, y)], (r,g,b))
        print var+1, 'Vertical seams removed'
        image=image1
    image.show()
    image.save(imageName[:-4]+'After'+'.jpg')
    



