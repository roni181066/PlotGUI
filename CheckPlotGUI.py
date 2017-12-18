from matplotlib.figure import Figure
from matplotlib.pyplot import plot, figure, legend, twinx
from PlotGUI import PlotGUI

figs = {}
for i in [0, 1]:
    xlist = [0, 1, 2]
    ylist = [1 + i * 2, 7 + i * 2, 5 + i * 2]
    # figs[i] = Figure()
    figs[i] = figure()
    # ax = figs[i].add_subplot(111)
    plot(xlist, ylist, lw=i + 3, label=str(i))
    legend(loc=i+1)

    # ax.plot(xlist, ylist, lw=i + 3, label=str(i))
    # ax.legend(loc=i+1)

    x2 = [0, 7, 9]
    y2 = [1 + i * 100, 7 + i * 100, 5 + i * 100]

    # ax2 = ax.twinx()
    ax2 = twinx()
    ax2.plot(x2, y2, label=str(100*i+1))
    ax2.legend(loc=i+3)


app = PlotGUI(figs=figs)
app.geometry('1280x720')
# ani = animation.FuncAnimation(f, animate, interval=1000)

# app2 = PlotGUI(figs=figs)
# app2.mainloop()

app.mainloop()