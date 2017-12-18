import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib import style

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


class PlotGUI(tk.Tk):

    def __init__(self, figs, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "My PlotGUI")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(self.container)

        filemenu = tk.Menu(menubar, tearoff=1)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        combine_menu = tk.Menu(menubar, tearoff=1)
        combine_menu.add_command(label="Compare 2", command=self.compare_figs)
        menubar.add_cascade(label="Combine", menu=combine_menu)

        tk.Tk.config(self, menu=menubar)

        self.curr_frame = 0

        prev_button = ttk.Button(self, text="Prev", command=self.prev_frame)
        prev_button.pack(side=tk.LEFT)
        next_button = ttk.Button(self, text="Next", command=self.next_frame)
        next_button.pack(side=tk.LEFT)

        self.frames = {}
        self.figs = figs

        for i, f in enumerate(figs):
            frame = GraphPage(self.container, i, fig=figs[i])
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # self.compare_figs(0, 1)

        self.show_frame(self.curr_frame)

    def compare_figs(self):
        d = Compare2Dialog(self)
        comp2 = d.result[0]
        shift_x = d.result[1]
        shift_y = d.result[2]

        if comp2 is not None:
            new_fig = len(self.figs)
            self.figs[new_fig] = Figure()
            new_ax = self.figs[new_fig].add_subplot(111)
            new_ax.clear()

            for ax in self.figs[self.curr_frame].axes:
                for line in ax.get_lines():
                    new_line = self.copy_line(line)
                    new_ax.add_line(new_line)

            for ax in self.figs[comp2].axes:
                for line in ax.get_lines():
                    new_line = self.copy_line(line, shift_x=shift_x, shift_y=shift_y)
                    new_ax.add_line(new_line)

            new_ax.autoscale()

            frame = GraphPage(self.container, new_fig, fig=self.figs[new_fig])

            self.frames[new_fig] = frame

            frame.grid(row=0, column=0, sticky="nsew")

    @staticmethod
    def copy_line(old_line, shift_x=0., shift_y=0.):
        return Line2D(
            xdata=old_line.get_xdata()+shift_x, ydata=old_line.get_ydata()+shift_y,
            color=old_line.get_color(),
            linestyle=old_line.get_linestyle(),
            linewidth=old_line.get_linewidth(),
            marker=old_line.get_marker(),
            markeredgecolor=old_line.get_markeredgecolor(),
            markeredgewidth=old_line.get_markeredgewidth(),
            markerfacecolor=old_line.get_markerfacecolor(),
            markerfacecoloralt=old_line.get_markerfacecoloralt(),
            markersize=old_line.get_markersize()
        )

    def prev_frame(self):
        self.show_frame(self.curr_frame-1)

    def next_frame(self):
        self.show_frame(self.curr_frame+1)

    def show_frame(self, cont):
        self.curr_frame = cont % len(self.frames)
        self.frames[self.curr_frame].tkraise()


class GraphPage(tk.Frame):

    def __init__(self, parent, num, fig):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page "+str(num), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Compare2Dialog(Dialog):

    def body(self, master):

        tk.Label(master, text="Enter figure #:").grid(row=0)
        tk.Label(master, text="Enter shift X:").grid(row=1)
        tk.Label(master, text="Enter shift Y:").grid(row=2)

        self.comp2 = tk.Entry(master)
        self.shift_x = tk.Entry(master)
        self.shift_y = tk.Entry(master)

        self.comp2.grid(row=0, column=1)
        self.shift_x.grid(row=1, column=1)
        self.shift_y.grid(row=2, column=1)
        return self.comp2 # initial focus

    def apply(self):
        try:
            comp2 = int(self.comp2.get())
        except:
            comp2 = None
        try:
            shift_x = float(self.shift_x.get())
        except:
            shift_x = 0.
        try:
            shift_y = float(self.shift_y.get())
        except:
            shift_y = 0.
        self.result = comp2, shift_x, shift_y