#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

sns.set(style="whitegrid")

#CONSTANTS
GM = 6.673e-8*2.e33 #gravitational constant * solar mass
au = 1.495e13 #astronomical unit
year = 3.1557e7 #tropical year (see https://en.wikipedia.org/wiki/Tropical_year)
kms = 1.0e5 #km/s
ecc = 0 #eccentricty of orbit
tmax = 10.*year #maximum time
nsteps = 100 #number of steps to take
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
    
def writeOrbits():
    """writes the orbit.out file"""
    
    xn = [au, 0] #x distance moved
    vn = [0, np.sqrt(GM/au * (1.-ecc)/(1.+ecc))] #apocenter, see (https://en.wikipedia.org/wiki/Apsis#Mathematical_formulae)
    t = 0 #time counter
    outFormat = "{0},{1},{2},{3},{4},{5}\n"
    
    with open("fwdEulerOrbit-{}.out".format(nsteps), "w+") as outFile:
        outFile.write(outFormat.format('#', 't', 'x', 'y', 'vx', 'vy'))
        xn, vn = modEuler(xn, vn, an) #first step is a modified Euler to setup the accleration (this is sorta a dirty hack)
        t += dt
        outFile.write(outFormat.format(1, t/year, xn[0], xn[1], vn[0], vn[1]))
        for i in range (2, nsteps):
            xn, vn = fwdEuler(xn, vn, an)
            t += dt
            outFile.write(outFormat.format(i, t/year, xn[0], xn[1], vn[0], vn[1]))
    
    xn = [au, 0] 
    vn = [0, np.sqrt(GM/au * (1.-ecc)/(1.+ecc))]
    t = 0
    with open("modEulerOrbit-{}.out".format(nsteps), "w+") as outFile:
        outFile.write(outFormat.format('#', 't', 'x', 'y', 'vx', 'vy'))
        xn, vn = modEuler(xn, vn, an)
        t += dt
        outFile.write(outFormat.format(1, t/year, xn[0], xn[1], vn[0], vn[1]))
        for i in range (2, nsteps):
            xn, vn = modEuler(xn, vn, an)
            t += dt
            outFile.write(outFormat.format(i, t/year, xn[0], xn[1], vn[0], vn[1]))

def stableOrbit(r, phi):
    return r*np.cos(phi), r*np.sin(phi)

def plotStbOrbit(number):
    phis = np.linspace(0, np.pi*2, number/(tmax/year))
    stableX = []
    stableY = []
    for i in range (0, int(tmax/year)):
        sX, sY = stableOrbit(1*au, phis)    
        stableX = np.append(stableX, sX)
        stableY = np.append(stableY, sY)
    stableX = stableX[:len(stableX)-1]
    stableY = stableY[:len(stableY)-1]
    return stableX, stableY

def makePlots():
    """makes the plots"""
    fig = plt.figure()
    ax = fig.gca()
    fwdEulerOrbit100 = pd.read_csv("fwdEulerOrbit-100.out")
    modEulerOrbit100 = pd.read_csv("modEulerOrbit-100.out")
    
    fwdEulerOrbit500 = pd.read_csv("fwdEulerOrbit-500.out")
    modEulerOrbit500 = pd.read_csv("modEulerOrbit-500.out")
    
    fwdEulerOrbit1000 = pd.read_csv("fwdEulerOrbit-1000.out")
    modEulerOrbit1000 = pd.read_csv("modEulerOrbit-1000.out")
    
    stableX, stableY = plotStbOrbit(1000)

    
    ax.plot(stableX, stableY, label="Stable Orbit", linestyle="dashed")
    ax.plot(fwdEulerOrbit100["x"], fwdEulerOrbit100["y"], label="t = .1")
    ax.plot(fwdEulerOrbit500["x"], fwdEulerOrbit500["y"], label="t = .02")
    ax.plot(fwdEulerOrbit1000["x"], fwdEulerOrbit1000["y"], label="t = .01")
    
    # ax.plot(modEulerOrbit100["x"], modEulerOrbit100["y"], label="t = .1")
    # ax.plot(modEulerOrbit500["x"], modEulerOrbit500["y"], label="t = .02")
    # ax.plot(modEulerOrbit1000["x"], modEulerOrbit1000["y"], label="t = .01")
    
    
    #ax.plot(modEulerOrbit["x"], modEulerOrbit["y"], modEulerOrbit["t"], label="Modified Euler Orbit", color="#91AA9D")
    ax.set_xlim(-2.0*au,2.0*au)
    ax.set_ylim(-2.0*au, 2.0*au)
    ax.set_xlabel("AU")
    ax.set_ylabel("AU")
#    ax.set_zlabel("Time (Years)")
    ax.set_title("Kepler Potential for Forward Euler")
    ax.legend(frameon=True)
    fig.set_size_inches(12, 8, forward=True)
    plt.savefig("stableFwdEuler.png", format='png', bbox_inches='tight')
    

#writeOrbits()
makePlots()