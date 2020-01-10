"""
General vector field in 2D
"""

import numpy as np
from vector_field import BaseVectorField2D
from functions import FunctionR2toR, abc
from diffsolve2d import forward_euler, rungekutta
from typing import Callable, Union, List, Tuple
from matplotlib.pyplot import Artist


class ParticleModel:
    """
    Particle model class.
    """

    def __init__(self, ax) -> None:
        """
        Constructor.
        """
        self._pointmodel = ax.scatter(0.0, 0.0, s=12.0, color="black")
        self._bounds = list(ax.get_xlim())
        self._bounds.extend(ax.get_ylim())
        linemodel, = ax.plot([0.0], [0.0])
        self._linemodel = linemodel
        self._xy = [0.0, 0.0]
        self._xarr = [0.0]
        self._yarr = [0.0]
        self._FORWARD_EULER = 1
        self._RUNGE_KUTTA = 4
        self._method = self._RUNGE_KUTTA

    def set_method(self, method_name: str) -> None:
        """
        Set the method used to numerically solve
        the ODE,
        """
        if method_name == "Forward Euler":
            self._method = self._FORWARD_EULER
        elif method_name == "Runge-Kutta":
            self._method = self._RUNGE_KUTTA

    def set_bounds(self, bounds: Tuple[Union[int, float]]) -> None:
        """
        Setter for the bounds
        """
        self._bounds = list(bounds)

    def get_plots(self) -> List[Artist]:
        """
        Get the plot objects
        """
        return [self._linemodel, self._pointmodel]

    def _update_appearance(self) -> None:
        """
        Update the appearance
        """
        self._pointmodel.set_offsets([self._xy])
        self._linemodel.set_xdata(self._xarr)
        self._linemodel.set_ydata(self._yarr)

    def set_initial_position(self, x: float, y: float) -> None:
        """
        Set the initial position
        """
        self._xarr = [x]
        self._yarr = [y]
        self._xy = [x, y]
        self._update_appearance()

    def update(self, f: Callable, delta_t: float) -> None:
        """
        Update the position, given an integration function and
        a time interval.
        """
        # x_prev, y_prev = self._xy
        if self._method is self._RUNGE_KUTTA:
            self._xy = rungekutta(
                f, 0.0, self._xy, delta_t / 2)
        elif self._method is self._FORWARD_EULER:
            self._xy = forward_euler(
                f, 0.0, self._xy, delta_t/2)
        # TODO: This is to stop adding points to be line plotted
        # if the particle moves too far away from the centre of the plot.
        # Think of a better strategy.
        # if not (self._xy[0] < 2*self._bounds[0]
        #     or self._xy[0] > 2*self._bounds[1]
        #     or self._xy[1] < 2*self._bounds[2]
        #     or self._xy[1] > 2*self._bounds[3]):
            # if not (((self._xy[0] - x_prev)**2 +
            #         (self._xy[1] - y_prev)**2) < 1e-10):
        self._xarr.append(self._xy[0])
        self._yarr.append(self._xy[1])
        self._update_appearance()

    def remove_line(self) -> None:
        """
        Remove a line.
        """
        self._xarr = []
        self._yarr = []
        self._update_appearance()


class NonLinearVectorField2D(BaseVectorField2D):
    """
    Nonlinear vector field in 2d class.
    """
    def __init__(self) -> None:
        """
        Initializer.
        """
        self._vx = FunctionR2toR("a*x - b*y + k1")
        self._vy = FunctionR2toR("c*x + d*y + k2")
        vx_params = self._vx.get_default_values()
        vy_params = self._vy.get_default_values()
        self.vxparams = [vx_params[s] for s in self._vx.get_default_values()]
        self.vyparams = [vy_params[s] for s in self._vy.get_default_values()]
        BaseVectorField2D.__init__(self, [-10.0, 10.0, -10.0, 10.0])
        self.particle = ParticleModel(self.figure.get_axes()[0])
        self.add_plots(self.particle.get_plots())

    def set_vx(self, args_vx: str) -> None:
        """
        Set vx.
        """
        self._vx = FunctionR2toR(args_vx)
        vx_params = self._vx.get_default_values()
        self.vxparams = [vx_params[s] for s in self._vx.get_default_values()]

    def set_vy(self, args_vy: str) -> None:
        """
        Set vy.
        """
        self._vy = FunctionR2toR(args_vy)
        vy_params = self._vy.get_default_values()
        self.vyparams = [vy_params[s] for s in self._vy.get_default_values()]

    def set_bounds(self, bounds):
        """
        Set the axes.
        """
        self.toggle_blit()
        # ax = self.figure.get_axes[0]
        self.bounds = bounds
        self.set_coords(*bounds)
        self.set_values()
        ax = self.figure.get_axes()[0]
        ax.set_xlim([self.bounds[0], self.bounds[1]])
        ax.set_ylim([self.bounds[2], self.bounds[3]])
        xdot, ydot = self.f(self.xy)
        print(self._plots)
        self.line.set_alpha(0.0)
        # self.line.set_visible(False)
        # self.line.remove()
        self.line = ax.quiver(self.xy[0], self.xy[1],
                              xdot, ydot, color="black")
        self.line.set_UVC(xdot, ydot)
        self.set_plot(2, self.line)
        # self.text = text(self.bounds[0] + 1, self.bounds[3] - 1,
        #                  "", color="black")
        # self.text.set_bbox({"facecolor": "white", "alpha": 1.0})
        # self.title = text(self.bounds[0]/2 + self.bounds[1]/3,
        #                   self.bounds[3]
        #                   - 0.1*(self.bounds[3] - self.bounds[2]),
        #                   "", color="black")
        # self.set_plot(-1, self.title)
        # self.title.set_bbox({"facecolor": "white", "alpha": 1.0})
        self.toggle_blit()
        self.plot_vector_field()

    def f(self, xy: np.ndarray,
          *t: float) -> Union[list, np.ndarray]:
        """
        Function that dictates the mapping of the vector field.
        """
        vx = None
        vy = None
        # print(self._vx.domain_variables)
        if len(self._vx.domain_variables) == 2:
            vx = self._vx(xy[0], xy[1], *self.vxparams)
        elif len(self._vx.domain_variables) == 1:
            if self._vx.domain_variables[0] == abc.x:
                vx = self._vx(xy[0], *self.vxparams)
            elif self._vx.domain_variables[0] == abc.y:
                vx = self._vx(xy[1], *self.vxparams)

        if len(self._vy.domain_variables) == 2:
            vy = self._vy(xy[0], xy[1], *self.vyparams)
        elif len(self._vy.domain_variables) == 1:
            if self._vy.domain_variables[0] == abc.x:
                vy = self._vy(xy[0], *self.vyparams)
            elif self._vy.domain_variables[0] == abc.y:
                vy = self._vy(xy[1], *self.vyparams)

        return [vx, vy] if isinstance(xy, list) else np.array([vx, vy])

    def set_values(self) -> None:
        """
        Set values.
        """
        pass

    def set_interactive_line(self, x: float, y: float) -> None:
        """
        Set interative line.
        """
        self.particle.set_initial_position(x, y)

    def update(self, delta_t: float) -> None:
        """
        Update the vector field at each time step.
        """
        for _ in range(self.simulation_speed):
            self.particle.update(self.f, delta_t)

    def plot_trajectories(self, init_call: bool = False) -> None:
        """
        Plot trajectories.
        """
        pass

    def _set_title(self) -> None:
        """
        Helper function for set title.
        """
        vx_string = self._vx.latex_repr
        vy_string = self._vy.latex_repr
        # for i, s in enumerate(self._vx.parameters):
        #    vx_string2 = vx_string.replace(str(s), "%.2f" % self.vxparams[i])
        # for i, s in enumerate(self._vy.parameters):
        #    vy_string2 = vy_string.replace(str(s), "%.2f" % self.vyparams[i])
        ax = self.figure.get_axes()[0]
        ax.set_title("x' = f(x, y) = $%s$\n"
                     "y' = g(x, y) = $%s$" % (
                                    vx_string,
                                    # vx_string2,
                                    vy_string,
                                    # vy_string2
                                    ))

    def set_title(self) -> None:
        """
        Set title.
        """
        if self.is_blit():
            self.toggle_blit()
            self._set_title()
            self.toggle_blit()
        else:
            self._set_title()
