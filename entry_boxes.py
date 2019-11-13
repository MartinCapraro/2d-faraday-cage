# Import appropriate version of tkinter
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class EntryBoxes(object):
    def __init__(self, root, n, r, zs):
        self.root = root
        self.n = n
        self.n_entry = tk.Entry(self.root, textvariable=self.n, width=3)
        self.n_label = tk.Label(self.root, text="Number of wires/disks")
        self.n_label.grid(row=0)

        self.r = r
        self.r_entry = tk.Entry(self.root, textvariable=self.r, width=3)
        self.r_label = tk.Label(self.root, text="Wire/disk diameter")
        self.r_label.grid(row=1)

        self.zs = zs
        self.zs_entry = tk.Entry(self.root, textvariable=self.zs, width=3)
        self.zs_label = tk.Label(self.root, text="Coordinate of the source charge on the x-axis")
        self.zs_label.grid(row=2)

        self.n_entry.grid(row=0, column=1)
        self.r_entry.grid(row=1, column=1)
        self.zs_entry.grid(row=2, column=1)
