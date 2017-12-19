from copy import copy, deepcopy
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.artist import getp
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

        self.show_frame(self.curr_frame)

    def compare_figs(self):
        d = Compare2Dialog(self)
        if d.result is None:
            return
        comp2 = d.result[0]
        if comp2 is None:
            return
        shift_x = d.result[1]
        shift_y = d.result[2]

        if self.have_non_twin_subplots(self.figs[self.curr_frame]) or self.have_non_twin_subplots(self.figs[comp2]):
            popupmsg('Comparing multiple subplot figures is not supported')
            raise NotImplementedError('Comparing multiple subplot figures is not supported')

        new_fig = len(self.figs)
        self.figs[new_fig] = Figure()
        # new_ax = self.figs[new_fig].add_subplot(111)

        new_ax = self.figs[new_fig].add_subplot(111)
        twinx_ax = None
        twiny_ax = None
        hh = {}
        ll = {}
        for ax in self.figs[self.curr_frame].axes:
            i_am_twinx = getattr(ax, '_sharex') is not None
            i_am_twiny = getattr(ax, '_sharey') is not None
            if not i_am_twinx and not i_am_twiny:
                self.copy_axes_properties(source=ax, target=new_ax)
            elif i_am_twinx:
                if twinx_ax is not None:
                    popupmsg('Comparing plots with multiple twinx is not supported')
                    raise NotImplementedError('Comparing plots with multiple twinx is not supported')
                else:
                    twinx_ax = new_ax.twinx()
                    self.copy_axes_properties(source=ax, target=twinx_ax)
            elif i_am_twiny:
                if twiny_ax is not None:
                    popupmsg('Comparing plots with multiple twiny is not supported')
                    raise NotImplementedError('Comparing plots with multiple twiny is not supported')
                else:
                    twiny_ax = new_ax.twiny()
                    self.copy_axes_properties(source=ax, target=twiny_ax)


            # h, l = ax.get_legend_handles_labels()
            # hh[position] = h
            # ll[position] = l
            # for line in ax.get_lines():
            #     new_line = self.copy_line(line)
            #     new_ax[position].add_line(new_line)

        # for ax in self.figs[comp2].axes:
        #     position = ax.xaxis.get_ticks_position(), ax.yaxis.get_ticks_position()
        #     h, l = ax.get_legend_handles_labels()
        #     hh[position] += h
        #     ll[position] += l
        #     for line in ax.get_lines():
        #         new_line = self.copy_line(line, shift_x=shift_x, shift_y=shift_y)
        #         new_ax[position].add_line(new_line)
        #
        # for position in new_ax.keys():
        #     new_ax[position].legend(hh[position], ll[position])
        #     new_ax[position].autoscale()

        frame = GraphPage(self.container, new_fig, fig=self.figs[new_fig])
        self.frames[new_fig] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def copy_axes_properties(self, source, target):
        target.xaxis.set_ticks_position(source.xaxis.get_ticks_position())
        target.yaxis.set_ticks_position(source.yaxis.get_ticks_position())
        target.xaxis.set_label_position(source.xaxis.get_label_position())
        target.yaxis.set_label_position(source.yaxis.get_label_position())
        target.xaxis.set_label_text(source.xaxis.get_label_text())
        target.yaxis.set_label_text(source.yaxis.get_label_text())

        for line in source.get_lines():
            new_line = self.copy_line(line)
            target.add_line(new_line)

        h, l = source.get_legend_handles_labels()
        target.legend(h ,l)
        target.autoscale()

    @staticmethod
    def have_non_twin_subplots(fig):
        have = False
        ax = fig.axes[0]
        for other_ax in fig.axes:
            if other_ax is ax:
                continue
            if other_ax.bbox.bounds != ax.bbox.bounds:
                have = True
        return have

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