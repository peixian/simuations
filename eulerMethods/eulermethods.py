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

t = 0
dt = tmax/nsteps
def getAcceleration(x, a, GM):
    """returns acceleration"""
    r3 = np.power(np.power(x[0], 2) + np.power(x[1], 2), 1.5)



def fwdEuler(x, v, a, t, dt, GM):
    """Forward Euler method"""

