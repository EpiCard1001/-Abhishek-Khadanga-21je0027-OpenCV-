import cv2
import numpy as np
import cv2.aruco
import cvzone
import math
def angleofaruco(x):                         #used this function to get angle by which aruco image should be rotated to grt straight square
  
  
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners1, ids1, rejected1) = cv2.aruco.detectMarkers(x, arucoDict,
	parameters=arucoParams)
    for (markerCorner,markerId) in zip (corners1,ids1):
                        bbox=markerCorner.reshape((4,2))
                        (tl,tr,br,bl)=bbox
    if (float(tl[0])-float(bl[0]))==0.0:
        return 0.0
    else:                        
     ang=(float(tl[1])-float(bl[1]))/(float(tl[0])-float(bl[0]))  
     rang=math.degrees(math.atan(ang))
     return rang
def subimage(image):                        #used this function to change orientation of aruco image
   arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
   arucoParams = cv2.aruco.DetectorParameters_create()
   (corners1, ids1, rejected1) = cv2.aruco.detectMarkers(image, arucoDict,
       parameters=arucoParams)
       
   for (markerCorner,markerId) in zip (corners1,ids1):
                        bbox=markerCorner.reshape((4,2))
                        (tl,tr,br,bl)=bbox
   shape = ( image.shape[1], image.shape[0] ) # cv2.warpAffine expects shape in (length, height)
   center=(tl+br)/2
   matrix = cv2.getRotationMatrix2D( center=center, angle=angleofaruco(image), scale=1 )
   image = cv2.warpAffine( src=image, M=matrix, dsize=shape )   
                                    

   return image
def cropar(image):                           #used this function to crop only the aruco part of image
   arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
   arucoParams = cv2.aruco.DetectorParameters_create()
   (corn, id, rejected1) = cv2.aruco.detectMarkers(image, arucoDict,
       parameters=arucoParams)
       
   for (markerCorner,markerId) in zip (corn,id):
                        box=markerCorner.reshape((4,2))
                        (tr2,br2,bl2,tl2)=box   
   tl2=(int(tl2[0]),int(tl2[1]))
   tr2=(int(tr2[0]),int(tr2[1]))
   br2=(int(br2[0]),int(br2[1]))         
   bl2=(int(bl2[0]),int(bl2[1]))
   #these point are random points of vertices of square so i used the following code to get just the x-coordinates of Top left and Top right and to get Y-coordinates of Top left and bottom right which will be used to crop the image
   lop=[tl2,tr2,br2,bl2]
   xcol=[lop[0][0]]
   ycol=[lop[0][1]]
   for i in lop:
       z=False 
       for j in xcol:
        if abs(j-i[0])<3:
         z=True   
         break
       if z==False:  
         xcol=xcol+[i[0]]
   for i in lop:
       z=False 
       for j in ycol:
        if abs(j-i[1])<3:
         z=True   
         break
       if z==False:  
         ycol=ycol+[i[1]]
   xcol.sort()                                    #
   ycol.sort()         
   image = image[ xcol[0]:xcol[1], ycol[0]:ycol[1]]
   return image
def arcd(x):                #usede this code to get aruco ids and rename the name of images according to their ids. eg-a4rc2(will be read as aruco4 with id 2)
    
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners1, ids1, rejected1) = cv2.aruco.detectMarkers(x, arucoDict,
	parameters=arucoParams)
    return ids1
def box(x):
    xgray= cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
    #key=getattr(cv2.aruco,f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_250)
    arucoParams = cv2.aruco.DetectorParameters_create()
    (corners, ids1, rejected1) = cv2.aruco.detectMarkers(xgray, arucoDict,
	parameters=arucoParams)
    return corners
img = cv2.imread("CVtask.jpg")

a1rc3=cv2.imread("arucoID3.png")
a2rc4=cv2.imread("arucoID4.png")
a3rc1=cv2.imread("arucoID1.png")
a4rc2=cv2.imread("arucoID2.png")
#img=cv2.resize(img, (877,620), interpolation = cv2.INTER_AREA) #1754*1240
imgco=img.copy()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_,thres=cv2.threshold(gray,240,250,cv2.THRESH_BINARY)
cont, hier = cv2.findContours(thres,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
for i,cont in enumerate(cont):
    if i!=0:
        ep=0.01*cv2.arcLength(cont,True )
        approx=cv2.approxPolyDP(cont,ep,True)
        if len(approx)==4:
            x,y,w,h=cv2.boundingRect(approx)
            p=float(w)/h
            M=cv2.moments(approx)
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"]) 

            if p>0.94 and p<1.03:

                           n = approx.ravel() 
                           i = 0
                           li=[]
                           for j in n :
                               if(i % 2 == 0):
                                   x = n[i]
                                   y = n[i + 1]
                               i = i + 1
                               li=li+[(x,y)]
                          
                           if np.any(img[cy,cx]==[9, 127, 240]): ######################
                            sqc1=li[0]
                            sqc2=li[2]
                            sqc3=li[4]
                            sqc4=li[6]
                            pts1=np.array([sqc1,sqc2,sqc3,sqc4])
                            bbox=box(a4rc2)
                            ids1=arcd(a4rc2)
                          
                            rightorientated=subimage(a4rc2)
                          
                            cuttedaruco=cropar(rightorientated)
             
                          
                            hit,wdt,k9k=cuttedaruco.shape
                            pts2=np.float32([[0,0],[wdt,0],[wdt,hit],[0,hit]])
                            matrix,_=cv2.findHomography(pts2,pts1)
                            imgout=cv2.warpPerspective(cuttedaruco,matrix,(img.shape[1],img.shape[0]))
                            
                            cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))
                            img=img+imgout
                                                     
                           elif np.any(img[cy,cx]==[79, 209, 146]):          ##########################
                            sqc1=li[0]
                            sqc2=li[2]
                            sqc3=li[4]
                            sqc4=li[6]
                            pts1=np.array([sqc1,sqc2,sqc3,sqc4])
                            bbox=box(a3rc1)
                            ids1=arcd(a3rc1)
                          
                            rightorientated=subimage(a3rc1)            
                            cuttedaruco=cropar(rightorientated)
                            hit,wdt,k9k=cuttedaruco.shape
                            pts2=np.float32([[0,0],[wdt,0],[wdt,hit],[0,hit]])
                            matrix,_=cv2.findHomography(pts2,pts1)
               
                            imgout= cv2.warpPerspective(cuttedaruco,matrix,(img.shape[1],img.shape[0]))
                           
                            cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))
                            img=img+imgout
               
           
                           elif np.any(img[cy,cx]==[210, 222, 228]):  #######################
                            sqc1=li[0]
                            sqc2=li[2]
                            sqc3=li[4]
                            sqc4=li[6]
                            pts1=np.array([sqc1,sqc2,sqc3,sqc4])
                            bbox=box(a2rc4)
                            ids1=arcd(a2rc4)
                          
                            rightorientated=subimage(a2rc4)
                 
                            cuttedaruco=cropar(rightorientated)
                          
                            hit,wdt,k9k=cuttedaruco.shape
                            pts2=np.float32([[0,0],[wdt,0],[wdt,hit],[0,hit]])
                            matrix,_=cv2.findHomography(pts2,pts1)
                            imgout=cv2.warpPerspective(cuttedaruco,matrix,(img.shape[1],img.shape[0]))
                            cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))
                            img=img+imgout
                           elif np.any(img[cy,cx]==[0,0,0]):  #######################
                            sqc1=li[0]
                            sqc2=li[2]
                            sqc3=li[4]
                            sqc4=li[6]
                            pts1=np.array([sqc1,sqc2,sqc3,sqc4])
                            bbox=box(a1rc3)
                            ids1=arcd(a1rc3)
                          
                            rightorientated=subimage(a1rc3)
                 
                            cuttedaruco=cropar(rightorientated)
                          
                            hit,wdt,k9k=cuttedaruco.shape
                            pts2=np.float32([[0,0],[wdt,0],[wdt,hit],[0,hit]])
                            matrix,_=cv2.findHomography(pts2,pts1)
                            imgout=cv2.warpPerspective(cuttedaruco,matrix,(img.shape[1],img.shape[0]))
                            cv2.fillConvexPoly(img,pts1.astype(int),(0,0,0))
                            img=img+imgout
cv2.imwrite("final.jpg",img)
cv2.imshow("sff",img)
cv2.imshow("kjd",imgco)
cv2.waitKey(0)
cv2.destroyAllWindows()