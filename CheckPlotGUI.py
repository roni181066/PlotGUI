from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
import PlotGUI as plt
import time
import multiprocessing


def check_window():
    for i in [0]:
    # for i in [0, 1]:
        xlist = [0, 1, 2]
        ylist = [1 + i * 2, 7 + i * 2, 5 + i * 2]
        # figs[i] = Figure()
        # plt.figure(figsize=(20, 10))
        plt.figure()
        # figs[i], ax = plt.subplots(2) # This is not supported
        # ax = figs[i].add_subplot(111)
        plt.plot(xlist, ylist, lw=i + 3, label=str(i))
        # plt.legend(loc=i+1)
        # plt.legend(loc='upper right')
        # plt.legend(loc=0)
        plt.legend()
        plt.ylabel('YYY')
        plt.xlabel('XXX')
        plt.title('TITLE')

        # ax.plot(xlist, ylist, lw=i + 3, label=str(i))
        # ax.legend(loc=i+1)

        x2 = [0, 7, 9]
        y2 = [1 + i * 100, 7 + i * 100, 5 + i * 100]

        # ax2 = ax.twinx()
        plt.twinx()
        plt.plot(x2, y2, label=str(100*i+1))
        # plt.legend(loc=i+3)
        # plt.legend(loc='upper left')
        # plt.legend(loc=0)
        plt.legend()
        plt.ylabel('yyy')
    plt.show()


if __name__ == '__main__':
    p = multiprocessing.Process(target=check_window)
    p.start()
    p.join()

    time.sleep(10)
    p = multiprocessing.Process(target=check_window)
    p.start()
    p.join()

