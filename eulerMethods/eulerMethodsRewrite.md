*Since I ended up taking a computational astrophysics class this semester, I decided that it might be good to write up a reference for myself and any other undergraduates who plan on flailing their way through a graduate level computational astrophysics class in the future. So this is the first in a series throughout the semester on astrophysics simulations.*

Astrophysics simulations are extremely complex beasts, often utilizing massive codebases like [flash][flash] or [ZEUS][ZEUS] to simulate a variety of cosmic evolutions over time. In this post, we'll start small with `matplotlib` and python to evolve the orbit of the Earth around the Sun in a ten year period on a 2D plane. To accomplish this, we need to solve a couple equations belonging to the [Keplerian Potenial][keplerProblem]. The basics of the Keplerian Potential is that there's two bodies, with one body orbiting around the other. Assuming no other forces outside of gravity, the stable orbit with an eccentricity of 0[^1] is a circle . We'll start by making a few constants known:

*This is just chunks of code, the full code can be found on [github][github]*

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

We'll use 1000 for the number, that way we have 1000 timesteps for 10 years. Now we have the final solution, we can begin modeling. We'll use something called [Euler methods][eulerWikipedia] for this. They're a way of solving ordinary differential equations created by Leonhard Euler, utilizing a Taylor expansion. On paper, this is pretty simple, and it's among one of the simplest ways to start modeling a stellar system. The basic equations for the Forward Euler method are:

\\(v^{n+1}\_p = v^{n}\_p + a(x^{n}\_p)\Delta t\\)

\\(x^{n+1}\_p = x^{n}\_p + v^{n}\_p\Delta t\\)

with \\(x \\) as the dimension, \\(v \\) as the velocity, \\(\Delta t\\) as the change in a timestep. A timestep is simply a timeframe in which something is occurring. The first equation states that the velocity for the next timestep is equal to the velocity of the current timestep plus the product of the acceleration, current space, and the change in a timestep. This is just a reordering of the equation that acceleration is simply the difference between velocities. The second equation is just as simple, telling you that the next position will be the sum of the current position and the product of the velocity and time. The faster something moves, the further away it'll be at the next timestep. How did we get these equations? Well the full Taylor series expansion is: 

\\(x^{n+1}\_p = x^{n}\_p + \dot x^{n}\_p \Delta t + 1/2 \ddot x^{n}\_p \Delta t^{2} + \mathcal{O}(\Delta t^{3}) \\)

\\(= x^{n}\_p + v^{n}\_p \Delta t + \mathcal{O}(\Delta t^{2}) \\)

\\(v^{n+1}\_p= v^{n}\_p + \dot v^{n}\_p \Delta t + 1/2 \ddot v^{n}\_p \Delta t^{2} + \mathcal{O}(\Delta t^{3})\\)


\\(= v^{n}\_p + a^{n}\_p \Delta t + \mathcal{O}(\Delta t^{2}) \\)

where \\(\dot x \\) is just the derivitive of \\(x \\), and \\(\mathcal{O}(\Delta t^{n}) \\) is just the leftovers of the Taylor series, also called the truncation error. The first thing you'll notice is how both of these systems are linear, so we're modeling a system with a bunch of tiny linear equations. Now let's put it into action by writing an acceleration function and a forward Euler function: 

        def getAccel(x, a):
            """returns x step & acceleration"""
            r3 = np.power(np.power(x[0], 2) + np.power(x[1], 2), 1.5)
            a[0] = -GM*x[0]/r3
            a[1] = -GM*x[1]/r3  
            return (x, a)
            
        def fwdEuler(x, v, a):
            """Forward Euler method"""
            tempX, tempA = getAccel(x, a)
            #wonky, but quick and dirty array multiplication hack
            x = map(sum, zip(tempX, [i*dt for i in v]))
            v = map(sum, zip(v, [i*dt for i in tempA]))
            return (x, v)
            
All we're doing is implementing the equations for a single step, which is pretty trivial. Now let's plot it with 3 timesteps[^2], .01 years, .02 years, and .1 years: 

![Stable and Forward Euler methods][stableAndFwd]

...Something went wrong. The forward Euler method is telling us that the Earth's orbit should spin out of control within 10 years, even less if we're taking bigger timesteps!

So why is our Earth in the forward Euler problem spinning into oblivion? We'll have to introduce the concept of [symplectic integrators][symplecticWikipedia]. Basically what it means is that a symplectic system is one that is time reversible, that is, the system itself preserves it's transformations and is time reversible. The reason why the forward Euler method causes the Earth to spin into the outer reaches of the solar system is that the method doesn't preserve the phase of the system, so the tiny phase errors within each timestep add up until our Earth spirals out of orbit. How do we solve this problem? A tiny modification to the Euler method allows us to preserve the phase:

\\(v^{n+1}\_p = v^{n}\_p + a(x^{n}\_p)\Delta t\\)

\\(x^{n+1}\_p = x^{n}\_p + v^{n+1}\_p\Delta t\\)

This doesn't look all that different, except that we're now using the velocity in the *next* timestep to calculate the next dimension. With this, the phase errors are preserved, and we get a much more reasonable orbit. So we'll write some code to fix that as well: 
    
        def modEuler(x, v, a):
            """Modified Euler method"""
            tempX, tempA = getAccel(x, a)
            #wonky, but quick and dirty array multiplication hack
            v = map(sum, zip(v, [i*dt for i in tempA]))
            x = map(sum, zip(tempX, [i *dt for i in v])) 
            return (x, v)
    
Applying this method, we get:

![stable and modified Euler orbits][stableAndMod]

This is much closer to what we want, but there's still noticeable phase errors on the simulation. The errors are caused by the inherent linear-ness of the Euler methods, we're getting pretty close to it, but we need to go an order higher to get more accurate simulations, which is what I'll talk about in my next post. 
    

[^1]: The Earth's orbit is actually ~0.0167, but we'll pretend it's 0 to keep things easy on ourselves.
[^2]: I chose these timesteps because they were easily 10/1000, 10/500, and 10/100. Feel free to experiment around with smaller and larger timesteps. 

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
