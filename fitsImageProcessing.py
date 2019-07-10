# Craioveanu Raul & Gigi
# desc: open fits image; stars position detection & magnitude; 
#		filter first N stars(mag); show fits image & detection


from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.utils.data import get_pkg_data_filename
import numpy as np
from PIL import Image


from astropy.stats import sigma_clipped_stats
from astropy.visualization import SqrtStretch
from astropy.visualization.mpl_normalize import ImageNormalize
from photutils import CircularAperture



class fitsImageProcessing():
	def __init__(self):
		self.__fitsImg = []
		self.__starsDetection = []


	# in:  
	# out: 
	# desc:
	def getImage(self,pos):
		return self.__fitsImg[pos]


	# in:  
	# out: 
	# desc:
	def getSourcesDetection(self,pos):
		return self.__starsDetection[pos]


	# In:   path - folder path; imageName - ["img1","img2"...]
	# Out:  array with [nameImage, image data]
	# Desc: 
	def openImages(self,path,imageName):

		for im in imageName:
			imPath = path + im


			# Try to read data from first HDU in fits file
			data = fits.open(imPath)[0].data
			# If nothing is there try the second one
			if data is None:
			    data = fits.open(imPath)[1].data

			self.__fitsImg.append([im,data])


	# in:  
	# out: 
	# desc:
	def get8BitFitsData(self, pos):
		data = self.__fitsImg[pos][1]

		# Clip data to brightness limits
		data[data > 500] = 500
		data[data < 100] = 100
			
		# Scale data to range [0, 1] 
		data = (data - 100)/(500 - 100)
			
		# Convert to 8-bit integer  
		data = (255*data).astype(np.uint8)
			
		# Invert y axis
		data = data[::-1, :]

		return data


	# in:  
	# out: 
	# desc:
	def showDrawLines(self, pos):
		pass



	# in:  
	# out: 
	# desc:
	def showImage(self, pos):
		data = self.get8BitFitsData(pos)

		# Create image from data array
		image = Image.fromarray(data, 'L')

		plt.imshow(image)
		plt.gray()
		plt.show()



	# in:  
	# out: 
	# desc:
	def detection(self):

		for data1 in self.__fitsImg:
			data = data1[1]

			#hdu = datasets.load_star_image()    
			mean, median, std = sigma_clipped_stats(data, sigma=3.0)    
			#print((mean, median, std))    


			from photutils import DAOStarFinder
			daofind = DAOStarFinder(fwhm=3.0, threshold=5.*std)    
			sources = daofind(data - median)    
			for col in sources.colnames:    
				sources[col].info.format = '%.8g'  # for consistent table output

			sources.keep_columns(['xcentroid', 'ycentroid', "mag"])

			self.__starsDetection.append(sources)



	# in:  
	# out: 
	# desc:
	def showDetection(self, pos):

		data = self.get8BitFitsData(pos)

		# Create image from data array
		image = Image.fromarray(data, 'L')
		image = image.transpose(Image.FLIP_TOP_BOTTOM)
		
		sources = self.__starsDetection[pos]
		
		positions = (sources['xcentroid'], sources['ycentroid'])
		apertures = CircularAperture(positions, r=5.)
		norm = ImageNormalize(stretch=SqrtStretch())
		plt.imshow(image, cmap='Greys', origin='lower')
		apertures.plot(color='blue', lw=1.5, alpha=0.5)
		plt.show()


	# in:  
	# out: 
	# desc:
	def sortFilterFirstNmag(self, n):
		for pos in range(0, len(self.__starsDetection)):
			if len(self.__starsDetection[pos]) > n:
				self.__starsDetection[pos].sort(['mag'], reverse=True)
				
				self.__starsDetection[pos] = self.__starsDetection[pos][:n]
				print(self.__starsDetection[pos])




# test
if __name__=="__main__":
	fitImg = fitsImageProcessing()

	fitImg.openImages("Res/Red_20160730_Feleac/Galileo/",["Galileo103B022.FIT"])

	fitImg.detection()
	fitImg.sortFilterFirstNmag(40)
	fitImg.showDetection(0)
