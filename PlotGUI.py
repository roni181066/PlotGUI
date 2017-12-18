from pprint import pprint
from copy import deepcopy, copy
import pickle
import io


import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure, Axes
# from matplotlib._axes import Axes
from matplotlib.lines import Line2D
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

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

    def __init__(self, *args, **kwargs):
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

        tk.Tk.config(self, menu=menubar)

        self.curr_frame = 0

        button1 = ttk.Button(self, text="Next",
                             command=lambda: self.show_frame(self.curr_frame+1))
        button1.pack()

        self.frames = {}
        self.figs = {}

        for i in [0, 1]:
            xlist = [0, 1, 2]
            ylist = [1+i*2, 7+i*2, 5+i*2]
            self.figs[i] = Figure()
            ax = self.figs[i].add_subplot(111)
            ax.clear()
            ax.plot(xlist, ylist, lw=i+3)

            frame = GraphPage(self.container, i, fig=self.figs[i])

            self.frames[i] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        self.compare_figs(0, 1)

        self.show_frame(self.curr_frame)


    def compare_figs(self, n1, n2):
        new_fig = len(self.figs)
        self.figs[new_fig] = Figure()
        new_ax = self.figs[new_fig].add_subplot(111)
        new_ax.clear()

        for ax in self.figs[n1].axes + self.figs[n2].axes:
            for line in ax.get_lines():
                new_line = Line2D(xdata=line.get_xdata(), ydata=line.get_ydata(), linewidth=line.get_linewidth())
                new_ax.add_line(new_line)  # This works

        new_ax.autoscale()

        frame = GraphPage(self.container, new_fig, fig=self.figs[new_fig])

        self.frames[new_fig] = frame

        frame.grid(row=0, column=0, sticky="nsew")

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



class MyAxes(Axes):
    def __init__(self, *args, **kwargs):
        self.mylines = []
        Axes.__init__(self, *args, **kwargs)

    def plot(self, *args, **kwargs):
        for line in self._get_lines(*args, **kwargs):
            self.mylines.append(line)

        Axes.plot(self, *args, **kwargs)


class MyFigure(Figure):
    def __init__(self, *args, **kwargs):
        Figure.__init__(self, *args, **kwargs)


app = PlotGUI()
app.geometry('1280x720')
# ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()