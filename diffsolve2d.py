"""
Foward Euler and Runge-Kutta integration methods.

These integration methods are adapted from
euler.py (http://www-personal.umich.edu/~mejn/cp/programs/euler.py) 
and rk4.py (http://www-personal.umich.edu/~mejn/cp/programs/rk4.py)
by Mark Newmann.
 
More detailed information about the theory behind these integration
methods and numerically solving ODEs are found in 
chapter 8 of Mark Newmann's Computational Physics.

Newman, M. (2013). Ordinary differential equations.
In Computational Physics, chapter 8. 
CreateSpace Independent Publishing Platform.
http://www-personal.umich.edu/~mejn/cp/

"""
from typing import Callable
import numpy as np


def forward_euler(f: Callable, t: float, x1: np.ndarray,
                  dt: float) -> np.ndarray:
    """
    The forward Euler method.
    """
    x2 = np.zeros([2])
    dx = f(x1, t)
    x2[0] = x1[0] + dt*dx[0]
    x2[1] = x1[1] + dt*dx[1]
    return x2


def rungekutta(f: Callable, t: float, x1: np.ndarray,
               dt: float) -> np.ndarray:
    """
    4th order Runge-Kutta.
    """
    a1 = dt*np.array(f(x1, t))
    a2 = dt*np.array(f(x1 + a1/2.0, t + dt/2.0))
    a3 = dt*np.array(f(x1 + a2/2.0, t + dt/2.0))
    a4 = dt*np.array(f(x1 + a3, t + dt))
    return x1 + (a1 + 2*a2 + 2*a3 + a4)/6


if __name__ == "__main__":
    pass
