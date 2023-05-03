import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def func(x, gamma):
    # return np.exp(-x ** 2 / gamma ** 2)
    return (1 / gamma) * (1 / (x ** 2 + (gamma / 2) ** 2))


def display_window():
    def _quit():
        root.quit()  # остановка цикла
        root.destroy()  # закрытие приложения

    validation = True

    def validate(entry, param):
        global validation
        # text = entry.get()
        # try:
        #     param(text)
        #     if param == int:
        #         if int(text) >= 0:
        #             entry.configure(bg='white')
        #             return param(text)
        #         else:
        #             entry.configure(bg='red')
        #             validation = False
        #             return -1
        #     else:
        #         entry.configure(bg='white')
        #         return param(text)
        # except ValueError:
        #     try:
        #         if float(text).is_integer():
        #             entry.configure(bg='white')
        #             return int(float(text))
        #         else:
        #             entry.configure(bg='red')
        #             validation = False
        #             return -1
        #     except ValueError:
        #         entry.configure(bg='red')
        #         validation = False
        #         return -1
        return float(entry.get())

    def update_plot(params): # a, b, n, gamma, x, v, i, t, ticks
        if params[6] == 0:
            ax.clear()
            ax.relim(visible_only=True)
            ax.autoscale_view(True)
            ax.plot(params[4], params[5], color='black')
            ax.set_title("t = 0")
            canvas.draw_idle()
            params[6] += 1
            root.after(params[8], update_plot, params)  # Создание цикла обновления графика каждые
        elif params[6] <= params[7]:  # i <= t
            ax.clear()
            a = params[0]
            b = params[1]
            n = params[2]
            gamma = params[3]
            x = params[4]
            v = params[5]
            t = params[6]
            x_1 = np.linspace(a, b, num=n, endpoint=True)
            # v_1 = x - v * t
            v_1 = v
            ax.relim(visible_only=True)
            ax.autoscale_view(True)
            ax.plot(x_1, v_1, color='black')
            ax.set_title("t = " + str(params[6]))
            canvas.draw_idle()
            params[0] += 1
            params[1] += 1
            params[4] = x_1
            params[5] = v_1
            params[6] += 1
            root.after(params[8], update_plot, params)  # Создание цикла обновления графика каждые
        return

    def count():
        global validation
        validation = True
        a = validate(entry1, 1)
        b = validate(entry2, 1)
        h = validate(entry3, 1)
        n = int(np.abs(b - a) / h)
        t = validate(entry4, 1)
        ticks = int(validate(entry5, 1))
        gamma = validate(entry6, 1)
        if validation:
            ax.clear()
            x = np.linspace(a, b, num=n, endpoint=True)
            v = func(x, gamma)
            update_plot([a + h, b + h, n, gamma, x, v, 0, t, ticks])

    root = tk.Tk()
    root.wm_title("Распад волн")

    frame1 = tk.LabelFrame(root, text="График")
    frame2 = tk.LabelFrame(root, text="Параметры")

    # frame 1
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_xlabel('x')
    ax.set_ylabel('v')

    canvas = FigureCanvasTkAgg(fig, master=frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, frame1)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # frame 2
    button1 = tk.Button(master=frame2, text="Рассчитать", command=count)
    frame1.columnconfigure(index=0, weight=1)
    frame1.columnconfigure(index=1, weight=1)
    entry1 = tk.Entry(master=frame2)
    entry2 = tk.Entry(master=frame2)
    entry3 = tk.Entry(master=frame2)
    entry4 = tk.Entry(master=frame2)
    entry5 = tk.Entry(master=frame2)
    entry6 = tk.Entry(master=frame2)
    entry1.insert(0, "-1")
    entry2.insert(0, "1")
    entry3.insert(0, "0.001")
    entry4.insert(0, "10")
    entry5.insert(0, "100")
    entry6.insert(0, "1")
    tk.Label(text="Функция", master=frame2).grid(row=0, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="1/gamma * 1/x^2+gamma^2/4}", master=frame2).grid(row=0, column=1, padx=15, sticky=tk.NSEW)
    tk.Label(text="a", master=frame2).grid(row=1, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="b", master=frame2).grid(row=2, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="h", master=frame2).grid(row=3, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="t", master=frame2).grid(row=4, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="Скорость", master=frame2).grid(row=5, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="gamma", master=frame2).grid(row=6, column=0, padx=15, sticky=tk.NSEW)
    entry1.grid(row=1, column=1, padx=15, sticky=tk.NSEW)
    entry2.grid(row=2, column=1, padx=15, sticky=tk.NSEW)
    entry3.grid(row=3, column=1, padx=15, sticky=tk.NSEW)
    entry4.grid(row=4, column=1, padx=15, sticky=tk.NSEW)
    entry5.grid(row=5, column=1, padx=15, sticky=tk.NSEW)
    entry6.grid(row=6, column=1, padx=15, sticky=tk.NSEW)
    button1.grid(row=7, column=0, columnspan=2, pady=2)

    frame1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
    frame2.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky=tk.NSEW)

    tk.mainloop()


if __name__ == "__main__":
    display_window()
