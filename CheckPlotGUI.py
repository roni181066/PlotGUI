from matplotlib.figure import Figure
from PlotGUI import PlotGUI

figs = {}
for i in [0, 1]:
    xlist = [0, 1, 2]
    ylist = [1 + i * 2, 7 + i * 2, 5 + i * 2]
    figs[i] = Figure()
    ax = figs[i].add_subplot(111)
    ax.clear()
    ax.plot(xlist, ylist, lw=i + 3)

app = PlotGUI(figs=figs)
app.geometry('1280x720')
# ani = animation.FuncAnimation(f, animate, interval=1000)

# app2 = PlotGUI(figs=figs)
# app2.mainloop()

app.mainloop()