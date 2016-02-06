#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#v^{n+1}_p = v^n_p + a(x^n_p)\Delta T
#x^{n+1}_p = x^n_p + v^n_p\Delta T

GM = 6.673e-8*2.e33 #gravitational constant * solar mass

au = 1.495e13 #astronomical unit

year = 3.1557e7 #tropical year (see https://en.wikipedia.org/wiki/Tropical_year)

kms = 1.0e5 #km/s

ecc = 0 #eccentricty of orbit

tmax = 10.*year #maximum time

nsteps = 200 #number of steps to take

dt = tmax/nsteps #change in time per step (take smaller steps for more data and visa versa)

an = [0, 0] #acceleration 

def getAccel(x, a):
    """returns x step & acceleration"""
    r3 = np.power(np.power(x[0], 2) + np.power(x[1], 2), 1.5)
    a[0] = -GM*x[0]/r3
    a[1] = -GM*x[1]/r3  
    return (x, a)

def modEuler(x, v, a):
    """Modified Euler method"""
    tempX, tempA = getAccel(x, a)
    #wonky, but quick and dirty array multiplication hack
    v = map(sum, zip(v, [i*dt for i in tempA])) #v^{n+1}_p = v^n_p + a(x^n_p)\Delta T
    x = map(sum, zip(tempX, [i *dt for i in v])) #x^{n+1}_p = x^n_p + v^n_p\Delta T
    return (x, v)

def fwdEuler(x, v, a):
    """Forward Euler method"""
    tempX, tempA = getAccel(x, a)
    #see modEuler, same principle
    x = map(sum, zip(tempX, [i*dt for i in v]))
    v = map(sum, zip(v, [i*dt for i in tempA]))
    return (x, v)
    
def main():
    """Main method"""
    
    xn = [au, 0] #x distance moved
    vn = [0, np.sqrt(GM/au * (1.-ecc)/(1.+ecc))] #apocenter, see (https://en.wikipedia.org/wiki/Apsis#Mathematical_formulae)
    t = 0 #time counter
    
    with open("orbit.out", "w+") as outFile:
        outFile.write("{0}, {1}, {2}, {3}, {4}, {5}\n".format('#', 't', 'x', 'y', 'vx', 'vy'))
        xn, vn = modEuler(xn, vn, an)

        t += dt
        outFile.write("{0}, {1}, {2}, {3}, {4}, {5}\n".format(1, t/year, xn[0], xn[1], vn[0], vn[1]))
        for i in range (2, nsteps):
            xn, vn = fwdEuler(xn, vn, an)
            t += dt
            outFile.write("{0}, {1}, {2}, {3}, {4}, {5}\n".format(i, t/year, xn[0], xn[1], vn[0], vn[1]))

main()