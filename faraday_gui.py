import math

# Import appropriate version of tkinter
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as backend_tkagg
import faraday_numerics
import entry_boxes
import options


class FaradayCageApplication(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        self.parent.wm_title("Faraday cage simulation")

        # Create a frame
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=4, column=0, columnspan=5, sticky="nsew")
        self.parent.grid_rowconfigure(4, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        # Create a figure
        self.fig = plt.figure(figsize=(5, 4), dpi=125)
        self.fig.tight_layout()

        # Create a subplot
        self.sub_plt = self.fig.add_subplot(111)
        self.sub_plt.set_aspect("equal")

        # Create a canvas and shove it into the frame
        self.canvas = backend_tkagg.FigureCanvasTkAgg(self.fig, self.frame)
        # Fill the frame
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Define simulation variables
        # n: number of wires/disks
        # r: wire/disk diameter
        # zs: coordinate of charge on the x axis
        self.n, self.r, self.zs = [tk.IntVar(), tk.DoubleVar(), tk.DoubleVar()]
        [self.n.set(12), self.r.set(0.1), self.zs.set(2.0)]

        # Create entry boxes and bind them to the simulation variables
        self.entry_boxes = entry_boxes.EntryBoxes(self.parent, self.n, self.r, self.zs)

        # Define some options
        self.plot_contour_values = tk.BooleanVar()
        self.save_data_to_csv = tk.BooleanVar()

        # Add check buttons and bind them to the option variables
        self.option_check_buttons = options.Options(
            self.parent, self.plot_contour_values, self.save_data_to_csv
        )

        # Add a button to plot the potential
        self.plot_ptn_btn = tk.Button(
            self.parent,
            text="Plot potential",
            command=lambda: self.attempt_to_plot(),
            width=10,
        )
        self.plot_ptn_btn.grid(row=0, column=2)

        # Add a quit button
        self.quit_btn = tk.Button(master=self.parent, text="Quit", command=self.quit)
        self.quit_btn.grid(row=1, column=2)

        # Choose the toolbar appropriate to the python version
        try:
            self.toolbar = backend_tkagg.NavigationToolbar2Tk(self.canvas, self.frame)
        except AttributeError:
            self.toolbar = backend_tkagg.NavigationToolbar2TkAgg(
                self.canvas, self.frame
            )

    def attempt_to_plot(self):
        """
        Wrapper function. Checks that the user input values are sensible, and
        if so calculates the potential and then plots it.
        """
        self.n_value, self.r_value, self.zs_value = [
            self.n.get(),
            self.r.get(),
            self.zs.get(),
        ]

        if self.sanity_check_input():
            self.xx, self.yy, self.uu = faraday_numerics.run_simulation(
                self.n_value, self.r_value, self.zs_value
            )

            if self.save_data_to_csv.get():
                self.save_output_to_csv()
            self.plot_potential()
        else:
            self.clear_plot()

    def sanity_check_input(self):
        if (self.n_value <= 0) or (self.r_value <= 0):
            self.popup = tk.Toplevel()
            self.label = tk.Label(
                self.popup,
                text="Invalid input. \n Please choose positive values for the \n number of disks and the wire diameter",
                height=10,
                width=50,
            )
            self.label.pack()
            return False
        elif 1 + 0.5 * self.r_value + 0.1 >= abs(self.zs_value):
            self.popup = tk.Toplevel()
            self.label = tk.Label(
                self.popup,
                text="Invalid input. \n Please choose values so that the test \n charge is outside the cage",
                height=10,
                width=40,
            )
            self.label.pack()
            return False
        # TODO: Check that wires don't overlap
        else:
            return True

    def plot_potential(self):
        # clear the subplot
        self.clear_plot()

        wire_lst = range(1, self.n_value + 1)

        # plot wires
        unit_roots = np.array(
            [math.e ** (2j * math.pi * m / self.n_value) for m in wire_lst]
        )
        self.sub_plt.scatter(unit_roots.real, unit_roots.imag, color="blue")

        # plot source charge
        self.sub_plt.plot(self.zs_value.real, self.zs_value.imag, ".r")

        levels = np.arange(-2, 2, 0.1)
        cont_plt = self.sub_plt.contour(
            self.xx, self.yy, self.uu, levels=levels, colors=("black"), corner_mask=True
        )

        if self.plot_contour_values.get():
            self.sub_plt.clabel(cont_plt, inline=1, fontsize=10)

        # redraw the canvas
        self.canvas.draw()

    def save_output_to_csv(self):
        np.savetxt(
            "./numerical_output/n_{}_r_{}_z_{}.csv".format(
                self.n_value, self.r_value, self.zs_value
            ),
            self.uu,
            delimiter=",",
        )

    def clear_plot(self):
        self.sub_plt.cla()
        self.canvas.draw()

    def quit(self):
        self.parent.quit()  # stops mainloop
        self.parent.destroy()


def main():
    root = tk.Tk()
    FaradayCageApplication(root)
    tk.mainloop()


if __name__ == "__main__":
    main()
