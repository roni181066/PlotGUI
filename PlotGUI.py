from copy import copy, deepcopy
import pickle

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plto
from matplotlib.pyplot import *

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog
from tkinter import filedialog

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

style.use("ggplot")

figs = []


def figure(*args, **kwargs):
    figs.append(plto.figure(*args, **kwargs))


def draw():
    global app
    global figs
    app = PlotGUI(figs=figs)
    app.update()
    app.update_idletasks()
    figs = []


def show():
    global app
    global figs
    app = PlotGUI(figs=figs)
    app.mainloop()
    figs = []


# def quit():
#     app._quit()


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

        self.figs = figs
        self.init_frames()

    def init_menubars(self):
        menubar = tk.Menu(self.container)

        file_menu = tk.Menu(menubar, tearoff=0)
        # file_menu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        # file_menu.add_separator()
        file_menu.add_command(label="Open", command=self.open_figs)
        file_menu.add_command(label="Add", command=self.add_figs)
        file_menu.add_command(label="Save", command=self.dump_figs)
        file_menu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Enter Scale", command=self.enter_scale)
        menubar.add_cascade(label="View", menu=view_menu)

        combine_menu = tk.Menu(menubar, tearoff=0)
        combine_menu.add_command(label="Compare 2", command=self.compare_figs)
        menubar.add_cascade(label="Combine", menu=combine_menu)

        # try_menu = tk.Menu(menubar, tearoff=1)
        # try_menu.add_command(label="Try", command=self.try_me)
        # menubar.add_cascade(label="Try", menu=try_menu)

        tk.Tk.config(self, menu=menubar)

    def init_buttons(self):
        prev_button = ttk.Button(self, text="Prev", command=self.prev_frame)
        prev_button.pack(side=tk.LEFT)
        next_button = ttk.Button(self, text="Next", command=self.next_frame)
        next_button.pack(side=tk.LEFT)
        goto_label = ttk.Label(self, text='Goto Frame')
        goto_label.pack(side=tk.LEFT)
        goto_entry = ttk.Entry(self, width=5)
        goto_entry.pack(side=tk.LEFT)
        goto_entry.bind('<Return>', self.goto_entry_do)

    def init_frames(self):
        self.curr_frame = 0
        self.frames = {}

        for i, f in enumerate(self.figs):
            frame = GraphPage(self.container, str(i), fig=self.figs[i])
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(self.curr_frame)

    def _quit(self):
        global figs
        self.quit()
        self.destroy()
        figs = []

    def goto_entry_do(self, event):
        num_frame = event.widget.get()
        event.widget.delete(0)
        try:
            num_frame = int(num_frame)
            self.show_frame(num_frame)
        except:
            pass

    def compare_figs(self):
        d = SmartDialog(master=self, title='Compare to',
                        fields=[EA(name='comp2',   label='Enter Figure #', operator=int,   default=None),
                                EA(name='shift_x', label='Enter Shift X',  operator=float),
                                EA(name='shift_y', label='Enter Shift Y',  operator=float),
                                ])
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
        self.curr_frame = new_fig
        frame.grid(row=0, column=0, sticky="nsew")

    def enter_scale(self):
        d = SmartDialog(master=self, title='Enter Scale',
                        fields=[EA(name='xmin_bottom', label='Xmin Bottom', operator=float, default=None),
                                EA(name='xmax_bottom', label='Xmax Bottom', operator=float, default=None),
                                EA(name='ymin_left',   label='Ymin Left',   operator=float, default=None),
                                EA(name='ymax_left',   label='Ymax Left',   operator=float, default=None),
                                EA(name='xmin_top',    label='Xmin Top',    operator=float, default=None),
                                EA(name='xmax_top',    label='Xmax Top',    operator=float, default=None),
                                EA(name='ymin_right',  label='Ymin Right',  operator=float, default=None),
                                EA(name='ymax_right',  label='Ymax Right',  operator=float, default=None),
                                ])
        for ax in self.figs[self.curr_frame].axes:
            xpos = ax.xaxis.get_ticks_position()
            ypos = ax.yaxis.get_ticks_position()
            xbounds = list(ax.get_xbound())
            ybounds = list(ax.get_ybound())
            if xpos == 'bottom':
                if d.results['xmin_bottom'] is not None:
                    xbounds[0] = d.results['xmin_bottom']
                if d.results['xmax_bottom'] is not None:
                    xbounds[1] = d.results['xmax_bottom']
            elif xpos == 'top':
                if d.results['xmin_top'] is not None:
                    xbounds[0] = d.results['xmin_top']
                if d.results['xmax_top'] is not None:
                    xbounds[1] = d.results['xmax_top']
            else:
                raise AttributeError('unexpected xpos '+xpos)

            if ypos == 'left':
                if d.results['ymin_left'] is not None:
                    ybounds[0] = d.results['ymin_left']
                if d.results['ymax_left'] is not None:
                    ybounds[1] = d.results['ymax_left']
            elif ypos == 'right':
                if d.results['ymin_right'] is not None:
                    ybounds[0] = d.results['ymin_right']
                if d.results['ymax_right'] is not None:
                    ybounds[1] = d.results['ymax_right']
            else:
                raise AttributeError('unexpected ypos '+ypos)

            ax.set_xbound(xbounds)
            ax.set_ybound(ybounds)

        self.figs[self.curr_frame].canvas.draw()

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

    def dump_figs(self):
        file = filedialog.asksaveasfilename()
        with open(file=file, mode='wb') as f:
            pickle.dump(self.figs, file=f, protocol=pickle.HIGHEST_PROTOCOL)

    def open_figs(self):
        self.figs = self.load_figs()
        self.init_frames()

    def add_figs(self):
        self.figs.extend(self.load_figs())
        self.init_frames()

    @staticmethod
    def load_figs():
        file = filedialog.askopenfilename()
        with open(file=file, mode='rb') as f:
            return pickle.load(file=f)


class GraphPage(tk.Frame):

    def __init__(self, parent, num, fig):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Graph Page "+str(num), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class EntryAttributes():
    def __init__(self, name, label, operator=str, default='empty'):
        self.name = name
        self.label = label
        self.operator = operator
        if default == 'empty':
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
            ttk.Label(master, text=f.label).grid(row=i)
            self.entries[f.name] = ttk.Entry(master)
            self.entries[f.name].grid(row=i, column=1)

        return self.entries[self.fields[0].name] # initial focus

    def apply(self):
        for i, f in enumerate(self.fields):
            try:
                self.results[f.name] = f.operator(self.entries[f.name].get())
            except:
                self.results[f.name] = f.default
