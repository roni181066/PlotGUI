from pprint import pprint
from copy import deepcopy, copy
import pickle
import io


import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure, SubplotBase
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

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=1)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        self.frames = {}

        i = 0
        xlist = [0, 1, 2]
        ylist = [1+i*2, 7+i*2, 5+i*2]
        f1 = Figure()
        a1 = f1.add_subplot(111)
        a1.clear()
        lines1 = a1.plot(xlist, ylist)
        line1 = Line2D(xlist, ylist)
        # pprint(a1.lines[0].__dict__)

        frame = GraphPage(container, self, int(i), fig=f1)

        self.frames[i] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        i = 1
        xlist = [0, 1, 2]
        ylist = [1 + i * 2, 7 + i * 2, 5 + i * 2]

        f2 = Figure()
        a2 = f2.add_subplot(111)
        a2.clear()
        lines2 = a2.plot(xlist, ylist)
        line2 = Line2D(xlist, ylist)
        # print(type(lines2), len(lines2))
        # pprint.pprint(lines2[0].__dict__)

        frame = GraphPage(container, self, int(i), fig=f2)

        self.frames[i] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        # buf = io.BytesIO()
        # pickle.dump(f1, buf)
        # buf.seek(0)
        # f3 = pickle.load(buf)
        # a3 = f3.get_axes()[0]

        # pprint(f3.__dict__)
        # line1 = f1.gca().lines[0]
        # line2 = f2.gca().lines[0]
        # a3.add_line(copy(line2))
        # pprint(len(a3.lines))
        # pprint(f3.gca().lines[0].__dict__)
        i = 2

        f3 = Figure()
        a3 = f3.add_subplot(111)
        pprint(a3.figure)
        pprint(f3.axes)
        a3.clear()
        pprint(a2.lines[0])
        pprint(line2)
        # for l in a2.lines:
        a3.add_line(copy(line2)) # This works
        # a3.add_line(copy(a2.lines[0])) # This doesn't work
        line2 = a2.get_lines()[0]
        line2.axes = None
        line2.figure = None
        line2.set_transform(a2.transData)

        # a3.add_line(line2) # This doesn't work

        # buf = io.BytesIO()
        # pickle.dump(line2, buf)
        # buf.seek(0)
        # line2 = pickle.load(buf)
        # a3.add_line(copy(line2)) # This doesn't work

        a3.autoscale()

        frame = GraphPage(container, self, int(i), fig=f3)

        self.frames[i] = frame

        frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(0)

    def show_frame(self, cont):
        frame = self.frames[cont % len(self.frames)]
        frame.tkraise()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller, num, fig):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page "+str(num), font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Next",
                             command=lambda: controller.show_frame(num+1))
        button1.pack()

        # f = Figure()
        # a = f.add_subplot(111)
        # pprint.pprint(a)
        # pprint.pprint(a.__dict__)
        # a.clear()
        # lines = a.plot(xlist, ylist)
        # pprint.pprint(a.__dict__)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = PlotGUI()
app.geometry('1280x720')
# ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()