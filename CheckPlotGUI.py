from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PlotGUI import PlotGUI

figs = {}
for i in [0, 1]:
    xlist = [0, 1, 2]
    ylist = [1 + i * 2, 7 + i * 2, 5 + i * 2]
    # figs[i] = Figure()
    figs[i] = plt.figure()
    # figs[i], ax = plt.subplots(2) # This is not supported
    # ax = figs[i].add_subplot(111)
    plt.plot(xlist, ylist, lw=i + 3, label=str(i))
    plt.legend(loc=i+1)
    plt.ylabel('YYY')

    # ax.plot(xlist, ylist, lw=i + 3, label=str(i))
    # ax.legend(loc=i+1)

    x2 = [0, 7, 9]
    y2 = [1 + i * 100, 7 + i * 100, 5 + i * 100]

    # ax2 = ax.twinx()
    ax2 = plt.twinx()
    plt.plot(x2, y2, label=str(100*i+1))
    plt.legend(loc=i+3)
    plt.ylabel('yyy')


app = PlotGUI(figs=figs)
app.geometry('1280x720')
# ani = animation.FuncAnimation(f, animate, interval=1000)

# app2 = PlotGUI(figs=figs)
# app2.mainloop()

app.mainloop()