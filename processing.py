import numpy as np
import cv2


class Processing():

	def __init__(self):
		pass


    # f(u) = 0    	      ,   0 <= u <= a
    # f(u) = (u-a)/(b-a)*L    ,   a < u <= b
    # f(u) = L    	      ,   b < u <= L
	def reduceNoise(self, imageL, a, b):
		shape = imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)
        
		for i in range(0,shape[0]):
			for j in range(0,shape[1]):
				for k in range(0,shape[2]):
					if  imageL.item(i, j, k) < a:
						im2.itemset((i,j,k),0)
					elif imageL.item(i,j,k) > b: 
						im2.itemset((i,j,k),255)
					else:
						im2.itemset((i,j,k), (imageL.item(i,j,k)-a)/(b-a) * 255)  
		return im2

    
    # f(u) = 0    	      ,   0 <= u <= a
    # f(u) = L    	      ,   a < u <= L
	def binarizare(self, imageL, a):	
	
		shape = imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)

		for i in range(0,shape[0]):
			for j in range(0,shape[1]):
				s = 0 
				for k in range(0,shape[2]):
					s += imageL.item(i,j,k)
				s/=3
				if  s < a:
					im2.itemset((i,j,0),0)
					im2.itemset((i,j,1),0)
					im2.itemset((i,j,2),0)
				else: 
					im2.itemset((i,j,0),255)
					im2.itemset((i,j,1),255)
					im2.itemset((i,j,2),255)

		return im2

    # im1 - im2
	def scadeImage(self, imageL, imageR):	

		shape = imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)
        
		for i in range(0,shape[0]):
			for j in range(0,shape[1]):
				for k in range(0,shape[2]):
					elem  =  abs(imageL.item(i,j,k) - imageR.item(i,j,k))
                  
					im2.itemset((i, j, k),(255-elem))
		return im2


	def blackWhite(self, imageL):

		shape = imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)
        
		for i in range(0,shape[0]):
			for j in range(0,shape[1]):
				gray = imageL.item(i, j, 0) + imageL.item(i, j, 1) + imageL.item(i, j, 2)
				gray /= 3
				for k in range(0,shape[2]):
					im2.itemset((i, j, k),(gray))
		return im2
######################################################    ^  



######################################################    v
	
    # f(u) = (sin(pi*u/L-pi/2)+1)/2*L
	def accentuareContrast(self,imageL,a,b):

		shape = imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)
        
		for i in range(0,shape[0]):
			for j in range(0,shape[1]):
				for k in range(0,shape[2]):
					u = imageL.item(i,j,k)
					fu = (math.sin(math.pi*u/255-math.pi/2)+1)/2*255
					im2.itemset((i,j,k), (fu))
		return im2

###################################################################   ^


######################################################    
	#  DILATAREA
	def dilatare(self, imageL):
		shape = self.imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)

		for i in range(1,shape[0]-1):
			for j in range(1,shape[1]-1):
				for k in range(0,shape[2]):
					if imageL.item(i,j,k) == 0:
						im2.itemset((i, j, k),(0))
	                    #im2.itemset((i-1, j-1, 0),(0))
						im2.itemset((i-1, j, k),(0))
	                    #im2.itemset((i-1, j+1, 0),(0))
						im2.itemset((i, j-1, k),(0))
						im2.itemset((i, j+1, k),(0))
	                    #im2.itemset((i+1, j-1, 0),(0))
						im2.itemset((i+1, j, k),(0))
	                    #im2.itemset((i+1, j+1, 0),(0))
					else:
						im2.itemset((i, j, k),(255))
		return im2


	#  EROZIUNEA
	def eroziunea(self, imageL):

		shape = imageL.shape        

		im2 = np.zeros((shape[0],shape[1],shape[2]), np.uint8)

		for i in range(1,shape[0]-1):
			for j in range(1,shape[1]-1):
				for k in range(0,shape[2]):
					if self.imageL.item(i,j,k) == 0:
						if self.imageL.item(i-1,j,k) == 255 or self.imageL.item(i,j+1,k) == 255 or self.imageL.item(i+1,j,k) == 255 or self.imageL.item(i,j-1,k) == 255:
							im2.itemset((i, j, k),(255))

	                    #im2.itemset((i-1, j-1, 0),(0))
	                    #im2.itemset((i-1, j, k),(0))
	                    #im2.itemset((i-1, j+1, 0),(0))
	                    #im2.itemset((i, j-1, k),(0))
	                    #im2.itemset((i, j+1, k),(0))
	                    #im2.itemset((i+1, j-1, 0),(0))
	                    #im2.itemset((i+1, j, k),(0))
	                    #im2.itemset((i+1, j+1, 0),(0))
					else:
						im2.itemset((i, j, k),(255))
		return im2

###################################################################  ^