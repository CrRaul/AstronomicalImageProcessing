# Craioveanu Raul & Gigi
# desc: get UCAC region; filter first N stars from cat(mag);
#		show catalog region(plt)
#		transform stars from J2000 to present: precession

from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
from Operations import *


#catalog_list = Vizier.find_catalogs('UCAC')
#catalogs = Vizier.get_catalogs(catalog_list.keys())
#print(catalogs)20

class Ucac4Processing():

	def __init__(self):
		self.__oper = Operations()
		self.__ucacReg = None


	# in:  ra - '*h*m*s', dec - [d,m,s], w - [d,m,s], h - [d,m,s], n - first n stars(mag)
	# out:
	# desc:
	def getUCACregion(self,ra,dec,w,h):

		print(ra, dec, "\n")

		fk5c = SkyCoord(ra, dec, frame=FK5)

		print(fk5c, "\n")


		Vizier.ROW_LIMIT = -1

		result = Vizier.query_region(SkyCoord(ra=fk5c.ra, dec=fk5c.dec, unit=(u.deg, u.deg)),
		width=w, height=h, catalog=["UCAC"])
		#print(result)

		result[0].keep_columns(['RAJ2000', 'DEJ2000', "f.mag","pmRA","pmDE"])

		#print(result[0])

		self.__ucacReg = result[0]


	def sortFilterFirstNmag(self,n):

		self.__ucacReg = self.__ucacReg.filled(9999)
		self.__ucacReg.sort(['f.mag'], reverse=False)

		if n < len(self.__ucacReg):
			self.__ucacReg = self.__ucacReg[:n]

		#print(self.__ucacReg)


	def showCatReg(self):
		x,y=[],[]
		for i in range(0,len(self.__ucacReg)):
			xxyy = self.__oper.skyToXY([self.__ucacReg[i][0], self.__ucacReg[i][1]])

			x.append(xxyy[0])
			y.append(xxyy[1])


		plt.scatter(x, y)
		plt.show()



if __name__ == "__main__":

	ucacProc = Ucac4Processing()
	ucacProc.getUCACregion('21h6m5s','52d44m42.9s','5d00m10s','5d00m10s')
	ucacProc.sortFilterFirstNmag(30)
	#ucacProc.showCatReg()

	ucacProc.showCatReg()