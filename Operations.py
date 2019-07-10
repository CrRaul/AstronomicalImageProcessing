import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import FK5
import math

class Operations():
	def __init__(self):
		pass


	# in: [deg, deg] 
	# out: ["hms", "dms"]
	# desc:
	def degCoordToHourDeg(self, skyCoo):

		c = SkyCoord(ra=skyCoo[0]*u.degree, dec=skyCoo[1]*u.degree)

		return str.split(c.to_string('hmsdms'))


	# in: [ra - string "hms"; dec - string "dms"]
	# out: astropy obj (ra(in deg), dec(in deg))
	# desc:		
	def coordToDeg(self, skyCoo):
		fk5c = SkyCoord(skyCoo[0],skyCoo[1], frame=FK5)

		return fk5c


	# in: 
	# out:
	# desc:
	def degCoordToRad(self, skyCoo):
		if type(skyCoo[0]) is str:
			coord = self.coordToDeg(skyCoo)

			return [coord.ra.radian, coord.dec.radian]
		else:
			c = SkyCoord(ra=skyCoo[0]*u.degree, dec=skyCoo[1]*u.degree)
			return [c.ra.radian, c.dec.radian]


	# in: 
	# out:
	# desc:
	def skyToXY(self, skyCoo):
		radRaDec = self.degCoordToRad(skyCoo)

		r = 1

		x = r * math.sin(radRaDec[0]) * math.cos(radRaDec[1])
		y = r * math.sin(radRaDec[0]) * math.sin(radRaDec[1])
		z = r * math.cos(radRaDec[0])

		return [x,y]


	# in: [ra - string "hms"; dec - string "dms"]
	# out:
	# desc:
	def precession(self, skyCoo, year):
		c = SkyCoord(ra=skyCoo[0]*u.degree, dec=skyCoo[1]*u.degree)

		c_fk5 = c.transform_to('fk5')

		c_fk5.transform_to(FK5(equinox=('J'+str(year))))

		return c_fk5


	# in: 
	# out:
	# desc:
	#'1988-12-18 05:11:23.5'
	def properMotion(self, SkyCoo, properMotion, dt):
		c = SkyCoord(ra=skyCoo[0]*u.degree, dec=skyCoo[1]*u.degree,
			pm_l_cosb=properMotion[0]*u.mas/u.yr, 
			pm_b=properMotion[1]*u.mas/u.yr,
			frame='galactic',
			obstime=Time('1999-01-01T00:00:00.123'))

		return c.apply_space_motion(dt=dt * u.year) 





	# in: a - [ax,ay]
	# out:
	# desc:
	def angle3pt(a, b, c):
	    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
	    return ang + 360 if ang < 0 else ang




if __name__=='__main__':
	c = Conversion()

	print("\n** [10.68458, 41.26917] to HMS DMS: " + str(c.degCoordToHourDeg([10.68458, 41.26917])))

	print("\n** Precession of [10.68458, 41.26917]" + str(c.precession([10.68458, 41.26917],2019)))

	print("\n** \"00h42m44.2992s\",\"+41d16m09.012s\" to Deg:   " + str(c.coordToDeg(["00h42m44.2992s","+41d16m09.012s"])))

	print("\n** \"00h42m44.2992s\",\"+41d16m09.012s\" to cartesian: " + str(c.degCoordToRad(["00h42m44.2992s","+41d16m09.012s"])))


