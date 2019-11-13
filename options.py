# Import appropriate version of tkinter
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class Options(object):
    def __init__(self, root, plot_contour_values, save_data_to_csv):
        self.root = root
        self.plot_contour_values = plot_contour_values
        self.save_data_to_csv = save_data_to_csv

        self.plot_contour_values_btn = tk.Checkbutton(
            self.root,
            text="Plot contour values",
            variable=self.plot_contour_values
        )
        self.plot_contour_values_btn.grid(row=2, column=2)

        self.save_data_to_csv_btn = tk.Checkbutton(
            self.root,
            text="Save numerical data to disk as a csv file",
            variable=self.save_data_to_csv
        )
        self.save_data_to_csv_btn.grid(row=3, column=2)

  