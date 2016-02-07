*Since I ended up taking a computational astrophysics class this semester, I decided that it might be good to write up a reference for myself and any other undergraduates who plan on flailing their way through a graduate level computational astrophysics class in the future. So this is the first in a series throughout the semester on astrophysics simulations.*

[Euler methods][eulerWikipedia] are a way of solving ordinary differential equations created by Leonhard Euler, utilizing a Taylor expansion. On paper, this is pretty simple, and it's among one of the simplest ways to start modeling a stellar system. The basic equations for the Forward Euler method are:

\\(v^{n+1}\_p = v^{n}\_p + a(x^{n}\_p)\Delta t\\)

\\(x^{n+1}\_p = x^{n}\_p + v^{n}\_p\Delta t\\)

with *x* as the dimension, *v* as the velocity, \Delta t as the change in a timestep. A timestep is simply a timeframe in which something is occurring. The first equation states that the velocity for the next timestep is equal to the velocity of the current timestep plus the product of the acceleration, current space, and the change in a timestep. This is just a reordering of the equation that acceleration is simply the difference between velocities. The second equation is just as simple, telling you that the next position will be the sum of the current position and the product of the velocity and time. The faster something moves, the further away it'll be at the next timestep. How did we get these equations? Well the full Taylor series expansion is: 

\\(x^{n+1}\_p = x^{n}\_p + \dot x^{n}\_p \Delta t + 1/2 \ddot x^{n}\_p \Delta t^{2} + \mathcal{O}(\Delta t^{3}) \\)

\\(= x^{n}\_p + v^{n}\_p \Delta t + \mathcal{O}(\Delta t^{2}) \\)

\\(v^{n+1}\_p= v^{n}\_p + \dot v^{n}\_p \Delta t + 1/2 \ddot v^{n}\_p \Delta t^{2} + \mathcal{O}(\Delta t^{3})\\)


\\(= v^{n}\_p + a^{n}\_p \Delta t + \mathcal{O}(\Delta t^{2}) \\)

where \\(\dot x \\) is just the derivitive of x, and \\(\mathcal{O}(\Delta t^{n}) \\) is just the leftovers of the Taylor series, also called the truncation error. The first thing you'll notice is how both of these systems are linear, so we're modeling a system with a bunch of tiny linear equations. This is how we'll end up with:
![comparison of forward and modified Euler methods][comparisonPng] 
In this picture, we're modeling the orbit of the Earth around the sun with [Keplerian Potential][keplerProblem] with both forward and modified Euler methods. We'll get to the distinction between these two in a bit, but it should be pretty clear that the forward Euler method spins pretty quickly out of control, while the modified Euler method is much closer to the stable orbit, which is what we should have. 

So why is our Earth in the forward Euler problem spinning into oblivion? We'll have to introduce the concept of [symplectic integrators][symplecticWikipedia]. Basically what it means is that a symplectic system is one that is time reversible, that is, the system itself preserves it's transformations and is time reversible. The reason why the forward Euler method causes the Earth to spin into the outer reaches of the solar system is that the method doesn't preserve the phase of the system, so the tiny phase errors within each timestep add up until our Earth spirals out of orbit. How do we solve this problem? A tiny modification to the Euler method allows us to preserve the phase:

\\(v^{n+1}\_p = v^{n}\_p + a(x^{n}\_p)\Delta t\\)

\\(x^{n+1}\_p = x^{n}\_p + v^{n+1}\_p\Delta t\\)

This doesn't look all that different, except that we're now using the velocity in the *next* timestep to calculate the next dimension. With this, the phase errors are preserved, and we get a much more reasonable orbit. 


[eulerWikipedia]: https://en.wikipedia.org/wiki/Euler_method
[comparisonPng]: https://raw.githubusercontent.com/peixian/simuations/master/eulerMethods/fwdModEuler3d.png
[keplerProblem]: https://en.wikipedia.org/wiki/Kepler_problem
[symplecticWikipedia]: https://en.wikipedia.org/wiki/Symplectic_integrator