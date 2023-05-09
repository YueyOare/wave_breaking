import random
import tkinter as tk

import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

validation = True
work = False
count_to_t = False
max_steps = 10000


def display_window():
    def _quit():
        root.quit()  # остановка цикла
        root.destroy()  # закрытие приложения
        return

    def config_table(num, action, weights):
        for i in range(num):
            action(index=i, weight=weights[i])

    def get_func(entry):
        global validation
        try:
            expr = entry.get()

            def test_func(x, gamma):
                return eval(expr)

            for _ in range(10):
                a = random.randint(-10, 10)
                b = random.randint(1, 10)
                if isinstance(test_func(a, b), complex):
                    validation = False
                    entry.configure(bg='red')
                    return -1
            entry.configure(bg='white')
            return lambda x, gamma: test_func(x, gamma)
        except ZeroDivisionError:
            entry.configure(bg='red')
            validation = False
            return -1
        except SyntaxError:
            entry.configure(bg='red')
            validation = False
            return -1
        except NameError:
            entry.configure(bg='red')
            validation = False
            return -1
        except TypeError:
            entry.configure(bg='red')
            validation = False
            return -1
        except ValueError:
            entry.configure(bg='red')
            validation = False
            return -1

    def validate(entry):
        def validate_value(text, cond):
            global validation
            val = text.get()
            try:
                value = float(val)
                if cond(value):
                    text.configure(bg='white')
                    return value
                else:
                    text.configure(bg='red')
                    validation = False
                    return -1
            except ValueError:
                text.configure(bg='red')
                validation = False
                return -1

        func = get_func(entry[0])
        a = validate_value(entry[1], lambda x: 1)
        b = validate_value(entry[2], lambda x: 1)
        h = validate_value(entry[3], lambda x: x > 0)
        t = validate_value(entry[4], lambda x: x > 0)
        dt = validate_value(entry[5], lambda x: x > 0)
        gamma = validate_value(entry[6], lambda x: x > 0)

        return func, a, b, h, t, dt, gamma

    def update_plot(func, a, b, n, gamma, x, t, dt):
        i = 0
        while i <= t or i <= max_steps / dt:  # i <= t
            ax.clear()
            x = x + func(np.linspace(a, b, num=n, endpoint=True), gamma) * i
            v = func(np.linspace(a, b, num=n, endpoint=True), gamma)
            ax.relim(visible_only=True)
            ax.autoscale_view(True)
            ax.plot(x, v, color='black')
            ax.set_title("t = " + str("{:.4f}".format(i)))
            canvas.draw_idle()
            if not count_to_t:
                if not np.array_equal(np.sort(x), x):
                    i = t
            root.update()
            if not work:
                return
            i += dt
        return

    def stop():
        global work
        work = False

    def count():
        global validation, count_to_t
        validation = True
        count_to_t = False
        func, a, b, h, t, dt, gamma = validate(entries)
        if validation:
            n = int(np.abs(b - a) / h)
            ax.clear()
            x = np.linspace(a, b, num=n, endpoint=True)
            v = np.array(func(x, gamma))
            ax.clear()
            ax.relim(visible_only=True)
            ax.autoscale_view(True)
            ax.plot(x, v, color='black')
            ax.set_title("t = 0")
            canvas.draw_idle()
            root.update()
            global work
            work = True
            update_plot(func, a + h, b + h, n, gamma, x, max_steps / dt, dt)

    def count_t():
        global validation, count_to_t
        validation = True
        count_to_t = True
        func, a, b, h, t, dt, gamma = validate(entries)
        if validation:
            n = int(np.abs(b - a) / h)
            ax.clear()
            x = np.linspace(a, b, num=n, endpoint=True)
            v = np.array(func(x, gamma))
            ax.clear()
            ax.relim(visible_only=True)
            ax.autoscale_view(True)
            ax.plot(x, v, color='black')
            ax.set_title("t = 0")
            canvas.draw_idle()
            root.update()
            global work
            work = True
            update_plot(func, a + h, b + h, n, gamma, x, t, dt)

    root = tk.Tk()
    root.wm_title("Распад волн")

    frame1 = tk.LabelFrame(root, text="График")
    frame2 = tk.LabelFrame(root, text="Параметры")

    # frame 1
    fig = Figure(figsize=(5, 4), dpi=100)
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
    button2 = tk.Button(master=frame2, text="Рассчитать до t", command=count_t)
    button3 = tk.Button(master=frame2, text="Остановить", command=stop)
    buttons = [button1, button2, button3]
    entries = []
    for i in range(7):
        entries.append(tk.Entry(master=frame2))
    entries[0].insert(0, "(1 / gamma) * (1 / (x ** 2 + (gamma / 2) ** 2))")
    entries[1].insert(0, "-1")
    entries[2].insert(0, "1")
    entries[3].insert(0, "0.001")
    entries[4].insert(0, "2")
    entries[5].insert(0, "0.001")
    entries[6].insert(0, "1")
    config_table(2, frame2.columnconfigure, [1, 4])
    tk.Label(text="Функция", master=frame2).grid(row=0, column=0, padx=15, sticky=tk.NSEW)
    # tk.Label(text="1/gamma * 1/x^2+gamma^2/4}", master=frame2).grid(row=0, column=1, padx=15, sticky=tk.NSEW)
    tk.Label(text="a", master=frame2).grid(row=1, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="b", master=frame2).grid(row=2, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="h", master=frame2).grid(row=3, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="t", master=frame2).grid(row=4, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="dt", master=frame2).grid(row=5, column=0, padx=15, sticky=tk.NSEW)
    tk.Label(text="gamma", master=frame2).grid(row=6, column=0, padx=15, sticky=tk.NSEW)
    for i in range(len(entries)):
        entries[i].grid(row=i, column=1, padx=15, sticky=tk.NSEW)
    for i in range(len(buttons)):
        buttons[i].grid(row=len(entries) + i + 1, column=0, columnspan=2, pady=5, padx=5, sticky=tk.NSEW)

    config_table(3, root.columnconfigure, [1, 1, 1])
    config_table(1, root.rowconfigure, [1])
    frame1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW)
    frame2.grid(row=0, column=2, columnspan=1, padx=5, pady=5, sticky=tk.NSEW)

    tk.mainloop()


if __name__ == "__main__":
    display_window()
