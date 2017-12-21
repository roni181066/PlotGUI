from copy import copy, deepcopy
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.artist import getp
from matplotlib.lines import Line2D
import matplotlib.legend as mlegend
from matplotlib import style
import matplotlib.pyplot as plto
from matplotlib.pyplot import *

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")

figs = {}
curr_fig = 0


def figure(*args, **kwargs):
    global curr_fig
    figs[curr_fig] = plto.figure(*args, **kwargs)
    curr_fig += 1


def show():
    app = PlotGUI(figs=figs)
    app.mainloop()


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

        self.protocol("WM_DELETE_WINDOW", self._quit)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "My PlotGUI")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.init_menubars()
        self.init_buttons()

        self.curr_frame = 0
        self.frames = {}
        self.figs = figs

        for i, f in enumerate(figs):
            frame = GraphPage(self.container, i, fig=figs[i])
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.curr_frame)

    def init_menubars(self):
        menubar = tk.Menu(self.container)

        file_menu = tk.Menu(menubar, tearoff=1)
        file_menu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=1)
        view_menu.add_command(label="Enter Scale", command=self.enter_scale)
        menubar.add_cascade(label="View", menu=view_menu)

        combine_menu = tk.Menu(menubar, tearoff=1)
        combine_menu.add_command(label="Compare 2", command=self.compare_figs)
        menubar.add_cascade(label="Combine", menu=combine_menu)

        try_menu = tk.Menu(menubar, tearoff=1)
        try_menu.add_command(label="Try", command=self.try_me)
        menubar.add_cascade(label="Try", menu=try_menu)

        tk.Tk.config(self, menu=menubar)

    def init_buttons(self):
        prev_button = ttk.Button(self, text="Prev", command=self.prev_frame)
        prev_button.pack(side=tk.LEFT)
        next_button = ttk.Button(self, text="Next", command=self.next_frame)
        next_button.pack(side=tk.LEFT)

    def _quit(self):
        self.quit()
        self.destroy()

    def compare_figs(self):
        d = SmartDialog(master=self, title='Compare to',
                        fields=[EA(name='comp2',   label='Enter Figure #', operator=int,   default=None),
                                EA(name='shift_x', label='Enter Shift X',  operator=float),
                                EA(name='shift_y', label='Enter Shift Y',  operator=float),
                                ])
        print(d)
        if d.results is None:
            return
        comp2 = d.results['comp2']
        if comp2 is None:
            return
        shift_x = d.results['shift_x']
        shift_y = d.results['shift_y']

        new_fig = len(self.figs)
        self.figs[new_fig] = Figure()
        new_ax = self.figs[new_fig].add_subplot(111)

        for ax in self.figs[self.curr_frame].axes:
            print(ax.get_xbound())
            for line in ax.get_lines():
                new_line = self.copy_line(line)
                new_ax.add_line(new_line)

        for ax in self.figs[comp2].axes:
            for line in ax.get_lines():
                new_line = self.copy_line(line)
                new_line.set_xdata(new_line.get_xdata()+shift_x)
                new_line.set_ydata(new_line.get_ydata()+shift_y)
                new_ax.add_line(new_line)

        new_ax.legend()
        new_ax.autoscale()

        frame = GraphPage(self.container, new_fig, fig=self.figs[new_fig])
        self.frames[new_fig] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def enter_scale(self):
        d = SmartDialog(master=self, title='Enter Scale',
                        fields=[EA(name='xmin_bottom', label='Xmin Bottom', operator=float),
                                EA(name='xmax_bottom', label='Xmax Bottom', operator=float),
                                EA(name='ymin_left',   label='Ymin Left',   operator=float),
                                EA(name='ymax_left',   label='Ymax Left',   operator=float),
                                EA(name='xmin_top',    label='Xmin Top',    operator=float),
                                EA(name='xmax_top',    label='Xmax Top',    operator=float),
                                EA(name='ymin_right',  label='Ymin Right',  operator=float),
                                EA(name='ymax_right',  label='Ymax Right',  operator=float),
                                ])

    def try_me(self):
        x = EntryAttributes('bbb', 'aaa', str, None)
        y = []
        y.append(x)

        d = SmartDialog(self, 'AAA', y)


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
            markersize=old_line.get_markersize(),
            label=old_line.get_label()
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


class EntryAttributes():
    def __init__(self, name, label, operator=str, default=None):
        self.name = name
        self.label = label
        self.operator = operator
        if default is None:
            if operator == str:
                self.default = ''
            elif operator == int:
                self.default = 0
            elif operator == float:
                self.default = 0.
            else:
                self.default = default
        else:
            self.default = default


EA = EntryAttributes


class SmartDialog(Dialog):

    def __init__(self, master, title, fields):
        self.fields = fields
        self.entries = {}
        self.results = {}
        Dialog.__init__(self, master, title)

    def body(self, master):
        for i, f in enumerate(self.fields):
            tk.Label(master, text=f.label).grid(row=i)
            self.entries[f.name] = tk.Entry(master)
            self.entries[f.name].grid(row=i, column=1)

        return self.entries[self.fields[0].name] # initial focus

    def apply(self):
        for i, f in enumerate(self.fields):
            try:
                self.results[f.name] = f.operator(self.entries[f.name].get())
            except:
                self.results[f.name] = f.default
