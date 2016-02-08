*Since I ended up taking a computational astrophysics class this semester, I decided that it might be good to write up a reference for myself and any other undergraduates who plan on flailing their way through a graduate level computational astrophysics class in the future. So this is the first in a series throughout the semester on astrophysics simulations.*

Astrophysics simulations are extremely complex beasts, often utilizing massive codebases like [flash][flash] or [ZEUS][ZEUS] to simulate a variety of cosmic evolutions over time. In this post, we'll start small with `matplotlib` and python to evolve the orbit of the Earth around the Sun in a ten year period on a 2D plane. To accomplish this, we need to solve a couple equations belonging to the [Keplerian Potenial][keplerProblem]. The basics of the Keplerian Potential is that there's two bodies, with one body orbiting around the other. Assuming no other forces outside of gravity, the stable orbit with an eccentricity of 0 is a circle (the Earth's orbit is actually ~0.0167, but we'll make it 0 to keep things easy on ourselves). We'll start by making a few constants known:

*this is just chunks of code, the full code can be found on [github][github]*

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


Next, we need to plot the a circle with radius of 1 AU around the center of the graph, so we'll write a function to generate a basic circle and stick it onto a 2D plane represented by 2 arrays. 
        
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

We'll use 1000 for the number, that way we have 1000 timesteps for 10 years. Now we have the final solution, we can begin modeling. We'll use something called [Euler methods][eulerWikipedia] for this. 

[^1]: The code can be found at https://github.com/peixian/simuations/blob/master/eulerMethods/eulermethods.py

[github]: https://github.com/peixian/simuations/blob/master/eulerMethods/eulermethods.py
[flash]: http://flash.uchicago.edu/
[ZEUS]: http://www.astro.princeton.edu/~jstone/zeus.html
[eulerWikipedia]: https://en.wikipedia.org/wiki/Euler_method
[stable]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/stable.png
[stableAndFwd]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/stableFwdEuler.png
[stableAndMod]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/stableModEuler.png
[forwardEuler]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/fwdEuler.png
[modEuler]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/modEuler.png
[comparisonPng]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/fwdModEuler3d.png
[keplerProblem]: https://en.wikipedia.org/wiki/Kepler_problem
[symplecticWikipedia]: https://en.wikipedia.org/wiki/Symplectic_integrator
