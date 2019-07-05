# Craioveanu Raul & Gigi
# desc: read and save data from excel( just relevant data)

import xlrd 

class readExcel():
	def __init__(selfl):
		self.__excelData = None


	# In: 
	# Out:
	# Desc:
	def readData(self, fileName, sheet, firstRow, lastRow):		

		loc = (fileName) 
		  
		wb = xlrd.open_workbook(loc) 
		sheet = wb.sheet_by_index(sheet) 		  

		data = []
		for i in range(firstRow, lastRow):
			a = []
			
			a.append(sheet.cell_value(i,0))

			date = xlrd.xldate_as_tuple(sheet.cell_value(i,1), wb.datemode)
			time = xlrd.xldate_as_tuple(sheet.cell_value(i,2), wb.datemode)


			a.append(date[0:3])
			a.append(time[3:6])

			a.append((sheet.cell_value(i,9), sheet.cell_value(i,10), sheet.cell_value(i,11)))
			
			a.append((sheet.cell_value(i,12), sheet.cell_value(i,13), sheet.cell_value(i,14)))
				
			data.append(a)

		self.__excelData = data



if __name__ == "__main__":
	test = readExcel()
	test.readData("Sateliti_20160730_Fel_Rev.xls",0 ,31,47)
