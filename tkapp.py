"""
App for nonlinear_vector_field.py

TODO:
 Need to implement moving the plot view and zooming out
 with the mouse. Initial attempts at this implementation
 are found in the commented out parts of code.
 Setup different ways to plot trajectories, such
 as plotting multiple trajectories.
"""
import tkinter as tk
from nonlinear_vector_field import NonLinearVectorField2D
from matplotlib.backends import backend_tkagg


class App(NonLinearVectorField2D):
    """
    """

    def __init__(self) -> None:
        """
        This is the constructor.
        """

        # Initialize the parent class
        NonLinearVectorField2D.__init__(self)

        # Primary Tkinter GUI
        self.window = tk.Tk()
        self.window.title("Linear Vector Field in 2D")
        self.window.configure()

        # Canvas
        # A short example of how to integrate a Matplotlib animation into a
        # Tkinter GUI is given here:
        # https://stackoverflow.com/a/21198403
        # [Answer by HYRY: https://stackoverflow.com/users/772649/hyry]
        # Link to question: https://stackoverflow.com/q/21197728
        # [Question by user3208454:
        # https://stackoverflow.com/users/3208454/user3208454]
        self.canvas = backend_tkagg.FigureCanvasTkAgg(
            self.figure,
            master=self.window
        )
        maxrowspan = 18
        self.canvas.get_tk_widget().grid(
                row=0, column=0, rowspan=maxrowspan, columnspan=3)
        self._canvas_height = self.canvas.get_tk_widget().winfo_height()
        self.canvas.get_tk_widget().bind("<B1-Motion>", self.mouse_listener)
        
        # Right click menu
        self.menu = tk.Menu(self.window, tearoff=0)
        self.menu.add_command(label="Use Forward-Euler",
                              command=lambda *args:
                              self.particle.set_method(
                                  "Forward-Euler"))
        self.menu.add_command(label="Use Runge-Kutta",
                              command=lambda *args:
                              self.particle.set_method(
                                  "Runge-Kutta"))
        self.window.bind("<ButtonRelease-3>", self.popup_menu)

        # Thanks to stackoverflow user rudivonstaden for
        # giving a way to get the colour of the tkinter widgets:
        # https://stackoverflow.com/questions/11340765/
        # default-window-colour-tkinter-and-hex-colour-codes
        #
        #     https://stackoverflow.com/q/11340765
        #     [Question by user user2063:
        #      https://stackoverflow.com/users/982297/user2063]
        #
        #     https://stackoverflow.com/a/11342481
        #     [Answer by user rudivonstaden:
        #      https://stackoverflow.com/users/1453643/rudivonstaden]
        #
        colour = self.window.cget('bg')
        if colour == 'SystemButtonFace':
            colour = "#F0F0F0"
        # Thanks to stackoverflow user user1764386 for
        # giving a way to change the background colour of a plot.
        #
        #    https://stackoverflow.com/q/14088687
        #    [Question by user user1764386:
        #     https://stackoverflow.com/users/1764386/user1764386]
        #
        self.figure.patch.set_facecolor(colour)

        self._zoom = False
        self._mouse_action = 2
        # self.mouse_dropdown_dict = {"Move Plot Around": 1, 
        #                             "Plot Trajectories": 2}
        # self.mouse_dropdown_string = tk.StringVar(self.window)
        # self.mouse_dropdown_string.set("Set Mouse...")
        # self.mouse_dropdown = tk.OptionMenu(
        #     self.window,
        #     self.mouse_dropdown_string,
        #     *tuple(key for key in self.mouse_dropdown_dict),
        #     command=self.set_mouse_action  
        # )
        # self.mouse_dropdown.grid(
        #     row=0, column=3, padx=(10, 10), pady=(0, 0)
        # )
        # self.canvas.get_tk_widget().bind_all("<MouseWheel>", self.zoom)
        # self.canvas.get_tk_widget().bind_all("<Button-4>", self.zoom)
        # self.canvas.get_tk_widget().bind_all("<Button-5>", self.zoom)

        self.preset_dropdown_dict = {
            "Linear": ["a*x - b*y + k1", "c*x + d*y + k2"],
            "Pendulum 1": ["y", "5*a*sin(k*x/2)"],
            "Pendulum 2": ["y", "5*a*sin(k*x/2)-b*y"],
            # "Rescaled Lotka–Volterra": ["a*(x+10)/2 - b*(x+10)*(y+10)/2", 
            #                    "d*(x+10)*(y+10)/4 - e*(y+10)/2"]
            "Lotka–Volterra": ["10*a*x/2 - 3*b*x*y/2", 
                               "6*d*x*y/4 - 10*e*y/2"]
            }
        self.preset_dropdown_string = tk.StringVar(self.window)
        self.preset_dropdown_string.set("Choose Preset Vector Field")
        self.preset_dropdown = tk.OptionMenu(
            self.window,
            self.preset_dropdown_string,
            *tuple(key for key in self.preset_dropdown_dict),
            command=self.set_preset_dropdown
            )
        self.preset_dropdown.grid(
                row=1, column=3, padx=(10, 10), pady=(0, 0))

        # Enter vx
        self.entervxlabel = tk.Label(self.window,
                                     text="Enter f(x, y)")
        self.entervxlabel.grid(
                row=2,
                column=3,
                columnspan=2,
                sticky=tk.W + tk.E + tk.S,
                padx=(10, 10)
                )
        self.enter_vx = tk.Entry(self.window)
        self.enter_vx.bind("<Return>", self.update_function_by_entry)
        self.enter_vx.grid(
            row=3,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
            padx=(10, 10)
            )
        self.enter_vx_button = tk.Button(self.window,
                                         text="OK",
                                         command=self.update_function_by_entry)
        self.enter_vx_button.grid(
            row=4,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N,
            padx=(10, 10)
            )

        # Enter vy
        self.entervylabel = tk.Label(self.window,
                                     text="Enter g(x, y)")
        self.entervylabel.grid(
                row=5,
                column=3,
                columnspan=2,
                sticky=tk.W + tk.E + tk.S,
                padx=(10, 10)
                )
        self.enter_vy = tk.Entry(self.window)
        self.enter_vy.bind("<Return>", self.update_function_by_entry)
        self.enter_vy.grid(
            row=6,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N + tk.S,
            padx=(10, 10)
            )
        self.enter_vy_button = tk.Button(self.window,
                                         text="OK",
                                         command=self.update_function_by_entry)
        self.enter_vy_button.grid(
            row=7,
            column=3,
            columnspan=2,
            sticky=tk.W + tk.E + tk.N,
            padx=(10, 10)
            )

        # Sliders
        self.sliderslist = []
        self.sliderslist_symbols = []
        self.simulation_speed_slider = None
        self.quit_button = None
        self.set_sliders()
        self.set_preset_dropdown("Linear")
        self.preset_dropdown_string.set("Choose Preset Vector Field")

    def set_preset_dropdown(self, *event: tk.Event) -> None:
        """
        Set the dropdown of the functions.
        """
        event = event[0]
        args_vx, args_vy = self.preset_dropdown_dict[event]
        self._update_function(args_vx, args_vy)
        if event == "Lotka–Volterra":
            if any([self.bounds[i] != [0.0, 10.0, 0.0, 10.0][i] 
                   for i in range(len(self.bounds))]):
                self.set_bounds([0.0, 10.0, 0.0, 10.0])
        else:
            if any([self.bounds[i] != [-10.0, 10.0, -10.0, 10.0][i] 
                   for i in range(len(self.bounds))]):
                self.set_bounds([-10.0, 10.0, -10.0, 10.0])

    # def set_mouse_action(self, *event: tk.Event) -> None:
    #     """
    #     Set the mouse action.
    #     """
    #     event = event[0]
    #     self._mouse_action = self.mouse_dropdown_dict[event]

    def slider_update(self, *event: tk.Event) -> None:
        """
        Update the functions given input from the slider.
        """
        self.particle.remove_line()
        vx_params = self._vx.get_default_values()
        vy_params = self._vy.get_default_values()
        for i in range(len(self.sliderslist)):
            symbol = self.sliderslist_symbols[i]
            if symbol in vx_params:
                vx_params[symbol] = self.sliderslist[i].get()
            if symbol in vy_params:
                vy_params[symbol] = self.sliderslist[i].get()
        # print(self.sliderslist_symbols)
        # print("vx params: ", vx_params)
        # print("vy params: ", vy_params, "\n")
        self.vxparams = []
        for key in self._vx.symbols:
            if key in vx_params:
                self.vxparams.append(vx_params[key])
        self.vyparams = []
        for key in self._vy.symbols:
            if key in vy_params:
                self.vyparams.append(vy_params[key])
        # vx_parameter_set = {s for s in self._vx.get_default_values()}
        # vy_parameter_set = {s for s in self._vy.get_default_values()}
        # self.vxparams = [vx_params[s] for s in vx_parameter_set]
        # self.vyparams = [vy_params[s] for s in vy_parameter_set]
        self.plot_vector_field(change_title=False)
        # self._clear_plot_after_zoom_or_move()

    def mouse_listener(self, event: tk.Event) -> None:
        """
        Listen to mouse input on the canvas and then call further
        functions in order to handle this.
        """
        if self._mouse_action == 2:
            ax = self.figure.get_axes()[0]
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            pixel_xlim = [ax.bbox.xmin, ax.bbox.xmax]
            pixel_ylim = [ax.bbox.ymin, ax.bbox.ymax]
            height = self.canvas.get_tk_widget().winfo_height()
            mx = (xlim[1] - xlim[0])/(pixel_xlim[1] - pixel_xlim[0])
            my = (ylim[1] - ylim[0])/(pixel_ylim[1] - pixel_ylim[0])
            x = (event.x - pixel_xlim[0])*mx + xlim[0]
            y = (height - event.y - pixel_ylim[0])*my + ylim[0]
            self.set_interactive_line(x, y)
        # elif self._mouse_action == 1:
        #     ax = self.figure.get_axes()[0]
        #     xlim = ax.get_xlim()
        #     ylim = ax.get_ylim()

    def _update_function(self, args_vx: str, args_vy: str) -> None:
        """
        Helper function for update_function_by_entry and
        update_function_by_preset.
        """
        self.set_vx(args_vx)
        self.set_vy(args_vy)
        # self.f = Functionx(str_args)
        # ones = ([1 for i in range(len(self.f.symbols) - 1)])
        # self.y = self.f(self.x, *ones)
        self.plot_vector_field()
        # self.text.set_text("f(x) = $%s$" % (self.f.latex_repr))
        self.set_sliders()
        # self.lim_update()
        # self.set_title()

    def update_function_by_entry(self, *event: tk.Event) -> None:
        """
        Update the function.
        """
        args_vx = self.enter_vx.get()
        args_vy = self.enter_vy.get()
        if args_vx.strip() == "":
            args_vx = "zero(x, y)"
        if args_vy.strip() == "":
            args_vy = "zero(x, y)"
        self.preset_dropdown_string.set("Choose Preset Vector Field")
        self._update_function(args_vx, args_vy)

    def set_sliders(self) -> None:
        """
        Create and set sliders.
        """
        rnge = 10.0
        for slider in self.sliderslist:
            slider.destroy()
        self.destroy_widgets_after_sliders()
        self.sliderslist = []
        self.sliderslist_symbols = []
        vx_defaults = self._vx.get_default_values()
        vy_defaults = self._vy.get_default_values()
        parameters = set(self._vx.parameters + self._vy.parameters)
        for i, symbol in enumerate(parameters):
            self.sliderslist_symbols.append(symbol)
            self.sliderslist.append(tk.Scale(self.window,
                                             label="change "
                                             + str(symbol) + ":",
                                             from_=-rnge, to=rnge,
                                             resolution=0.01,
                                             orient=tk.HORIZONTAL,
                                             length=200,
                                             command=self.slider_update))
            self.sliderslist[i].grid(row=i + 8, column=3,
                                     padx=(10, 10), pady=(0, 0))
            if symbol in self._vx.parameters:
                self.sliderslist[i].set(vx_defaults[symbol])
            if symbol in self._vy.parameters:
                self.sliderslist[i].set(vy_defaults[symbol])
        self.set_widgets_after_sliders(len(parameters) + 8)

    def set_widgets_after_sliders(self, index: int) -> None:
        """
        Set the widgets after the each of the parameter sliders.
        """
        slider = tk.Scale(self.window,
                          label="Set simulation speed: ", 
                          from_=0, to=20, resolution=1,
                          length=200,
                          orient=tk.HORIZONTAL,
                          command=self.set_simulation_speed)
        slider.set(1)
        slider.grid(row=index, column=3, 
                    padx=(10, 10), pady=(0, 0))
        self.simulation_speed_slider = slider
        self.quit_button = tk.Button(
            self.window, text='QUIT', command=self.quit)
        self.quit_button.grid(row=index+1, column=3, padx=(10, 10), 
                              pady=(0, 0))

    def destroy_widgets_after_sliders(self) -> None:
        """
        Destroy the widgets after each of the parameter sliders.
        """
        if self.simulation_speed_slider is not None:
            self.simulation_speed_slider.destroy()
        if self.quit_button is not None:
            self.quit_button.destroy()

    def popup_menu(self, event: tk.Event) -> None:
        """
        popup menu upon right click.
        """
        self.menu.tk_popup(event.x_root, event.y_root, 0)

    # def zoom(self, event: tk.Event) -> None:
    #     """
    #     Zoom in and out of the plot.
    #     """
    #     if event.delta == -120 or event.num == 5:
    #         x_scale_factor, y_scale_factor = 1.1, 1.1
    #     elif event.delta == 120 or event.num == 4:
    #         x_scale_factor, y_scale_factor = 0.9, 0.9
    #     ax = self.figure.get_axes()[0]
    #     xlim = ax.get_xlim()
    #     ylim = ax.get_ylim()
    #     dx = xlim[1] - xlim[0]
    #     dy = ylim[1] - ylim[0]
    #     xc = (xlim[1] + xlim[0])/2
    #     yc = (ylim[1] + ylim[0])/2
    #     xlim = (xc - x_scale_factor*dx/2.0, xc + x_scale_factor*dx/2.0)
    #     ylim = (yc - y_scale_factor*dy/2.0, yc + y_scale_factor*dy/2.0)
    #     # self.plot_vector_field()
    #     # self.set_sliders()
    #     self.set_bounds([xlim[0], xlim[1], ylim[0], ylim[1]])
    #     # self.plot_vector_field()
    #     self._zoom = True
    #     # self.set_bounds([xlim[0], xlim[1], ylim[0], ylim[1]])

    # def _clear_plot_after_zoom_or_move(self) -> None:
    #     """
    #     Clear the plot after a zoom or a move.
    #     """
    #     if self._zoom:
    #         self.plot_vector_field()
    #         self._zoom = False

    def quit(self, *event: tk.Event) -> None:
        """
        Quit the application.
        """
        self.window.quit()
        self.window.destroy()


if __name__ == "__main__":
    app = App()
    app.animation_loop()
    tk.mainloop()
