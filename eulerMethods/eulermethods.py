#!/usr/bin/env python
import numpy as np
import matplotlib.py as plt
import seaborn as sns

#v^{n+1}_p = v^n_p + a(x^n_p)\Delta T
#x^{n+1}_p = x^n_p + v^n_p\Delta T

#gravitational constant * solar mass
GM = 6.673e-8*2.e33
#astronomical unit
au = 1.495e13
#tropical year (see https://en.wikipedia.org/wiki/Tropical_year)
year = 3.1557e7
#km/s
kms = 1.0e5
#eccentricty of orbit
ecc = 0
#maximum time
tmax = 10.*year

#time counter
t = 0
#change in time per step (take smaller steps for more data and visa versa)
dt = tmax/nsteps

#number of steps to take
nsteps = 200

xn = [au, 0]
vn = [0, np.sqrt(GM/au * (1.-ecc)/(1.+ecc))] #apocenter, see (https://en.wikipedia.org/wiki/Apsis#Mathematical_formulae)

def getAcceleration(x, a, GM):
    """returns acceleration"""
    r3 = np.power(np.power(x[0], 2) + np.power(x[1], 2), 1.5)



def fwdEuler(x, v, a, t, dt, GM):
    """Forward Euler method"""

