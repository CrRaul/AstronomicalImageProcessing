# Craioveanu Raul & Gigi
# desc: get UCAC region; filter first N stars from cat(mag);
#		show catalog region(plt)
#		transform stars from J2000 to present

from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5

#catalog_list = Vizier.find_catalogs('UCAC')
#catalogs = Vizier.get_catalogs(catalog_list.keys())
#print(catalogs)20

class Ucac4Processing():

	def __init__(self):
		self.__ucacReg = None


	# in:  ra - '*h*m*s', dec - [d,m,s], w - [d,m,s], h - [d,m,s], n - first n stars(mag)
	# out:
	# desc:
	def getUCACregion(self,ra,dec,w,h,n):

		print(ra, dec)

		fk5c = SkyCoord(ra, dec, frame=FK5)

		print(fk5c)


		Vizier.ROW_LIMIT = -1

		result = Vizier.query_region(SkyCoord(ra=ra, dec=dec, unit=(u.deg, u.deg)),
		width=w, height=h, catalog=["UCAC"])
		print(result[1])

		self.__ucacReg = result[1]


	def sortFilterFirstNmag(self,n):
		for i in range(0,len(self.__ucacReg)-1):
			for j in range(i+1,len(self.__ucacReg)):
				if self.__ucacReg[i]['f.mag'] > self.__ucacReg[j]['f.mag']:
					self.__ucacReg[[i, j]] = self.__ucacReg[[j, i]]



		if n < len(self.__ucacReg):
			self.__ucacReg = self.__ucacReg[:n]

		print(self.__ucacReg)


	def showCatReg(self):
		x,y=[],[]
		for i in range(0,len(self.__ucacReg)):
			x.append(self.__ucacReg[i][1])
			y.append(self.__ucacReg[i][2])


		plt.scatter(x, y)
		plt.show()


	# in: 
	# out:
	# desc:
	def transformJ2000toYear(self):
		for i in range(0, len(self.__ucacReg)):
			ra = self.__ucacReg['RAJ2000'][i]
			dec = self.__ucacReg['DEJ2000'][i]

			fk5c = SkyCoord(ra, dec, frame='icrs',unit=(u.deg, u.deg))
			
			fk5_2015 = FK5(equinox='J2015')  # String initializes an astropy.time.Time object
			fk5_2015 = fk5c.transform_to(fk5_2015)

			self.__ucacReg['RAJ2000'][i] = fk5_2015.ra.deg
			self.__ucacReg['DEJ2000'][i] = fk5_2015.dec.deg


		print(self.__ucacReg)
		#N = year - 2000
		#a1 = a + (3.07420 + 1.33589*np.sin(a)*np.tan(d)) * N
		#d1 = d + (20.0383 * np.cos(a)) * N
		#a1 = a0 + (m + n*sin(a0)*tan(d0)) * N
		#d1 = d0 + (n' * cos(a0)) * N
		# 2000 -  m = 3.07420 sec  n = 1.33589 sec  n' = 20.0383 arcsec
		#print(a1,d1)

if __name__ == "__main__":

	ucacProc = Ucac4Processing()
	ucacProc.getUCACregion('05h14m32.2s','-08d12m05s','0d20m10s','0d20m10s',20)
	ucacProc.sortFilterFirstNmag(20)
	ucacProc.showCatReg()
	ucacProc.transformJ2000toYear()

	ucacProc.showCatReg()