import numpy as np 
import cv2



class Detection():
	def __init__(self):
		pass



	def fill(self):
		pass


	def detection(self, imageL):
		shape = imageL.shape        

		im2 = imageL
        
		for i in range(0,shape[0]):
			for j in range(0,shape[1]):
					if imageL.item(i,j,0) == 255:
						for k in range(1,10):
							im2.itemset((i-k,j,2), (255))
							im2.itemset((i-k,j,1), (0))
							im2.itemset((i-k,j,0), (0))
							
							im2.itemset((i,j-k,2), (255))
							im2.itemset((i,j-k,1), (0))
							im2.itemset((i,j-k,0), (0))
		return im2