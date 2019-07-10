from fitsImageProcessing import *
from Ucac4Processing import *
from Operations import *
from readExcel import *



class Controller():
	def __init__(self):
		self.__image = fitsImageProcessing()
		self.__ucacReg = Ucac4Processing()
		self.__operation = Operations()
		self.__exelR = readExcel()


	def readExcel(self):
		self.__exelR.readData("Sateliti_20160730_Fel_Rev.xls",0,31,33)


	def getExcelData(self, pos):
		return self.__exelR.getData(pos)






if __name__ == "__main__":
	c = Controller()

	c.readExcel()

	print(c.getExcelData(1))







 

#fitImg = fitsImageProcessing()

#fitImg.openImages("Res/Red_20160730_Feleac/Galileo/",["Galileo103B022.FIT"])


#fitImg.detection()
#fitImg.sortFilterFirstNmag(20)

#print(fitImg.getSourcesDetection(0))


#print(angle3pt((5, 0), (0, 0), (0, 5)))




