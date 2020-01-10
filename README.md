# Nonlinear ODEs in 2D

This application interactively plots the trajectories formed by two coupled first order ordinary differential equations.
To obtain this program, first ensure that you already have Python 3 with Numpy, Matplotlib, Tkinter, and Sympy, and then download or clone this repository.

## Usage

<img src="https://raw.githubusercontent.com/marl0ny/Nonlinear-ODE-2D/blob/master/screenshot.PNG" />

To open this program, run the file `tkapp.py`. This launches a GUI window showing a vector field plot of the differential equations with control widgets to the right.
To plot a trajectory starting from an initial condition, click anywhere on the vector field plot. To increase the speed at which this trajectory is rendered, move the `Set simulation speed` slider, which is found
near the bottom right of the GUI window. At the top of the GUI window are the two coupled first order differential equations, expressed as
`x' = f(x, y)` and `y' = g(x, y)`. To change these equations, either select a preset from the `Choose Preset Vector Field` dropdown, or enter
a new equation using the `Enter f(x, y)` and `Enter g(x, y)` entry boxes. Any variable entered that is not x or y becomes parameters that you vary with the sliders.
To close this program, click the `QUIT button`.

## References

Newman, M. (2013). Ordinary differential equations. In <em>[Computational Physics](http://www-personal.umich.edu/~mejn/cp/)</em>, chapter 8. CreateSpace Independent Publishing Platform.

Strogatz, S. (2015). <em>Nonlinear Dynamics and Chaos</em>. Boca Raton: CRC Press, https://doi.org/10.1201/9780429492563
