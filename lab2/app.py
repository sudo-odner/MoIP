import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Параметры для LCG
a, c, m = 1664525, 1013904223, 2**32  # Классические параметры LCG
# Параметры для BBS
p, q = 383, 503  # Простые числа Блюма
# Параметры для LFSR
lfsr_taps = [7, 5, 4, 3]  # Полином x^8 + x^5 + x^4 + x^3 + 1

# Реализация линейного конгруэнтного генератора (LCG)
def lcg_numpy(a, c, m, seed, length):
    x = np.empty(length, dtype=np.uint8)
    value = seed
    for i in range(length):
        value = (a * value + c) % m
        x[i] = value % 256 # Последние 8 бит результата
    return x.tolist()

# Реализация генератора BBS (Blum Blum Shub) с использованием двоичных операций
def bbs_binary(p, q, seed, length):
    M = p * q
    x = seed % M
    sequence = []
    for _ in range(length):
        x = pow(x, 2, M)
        sequence.append(x & 0xFF)  # Последние 8 бит результата
    return sequence

# Реализация LFSR с использованием битовых операций и двоичного представления
def lfsr_bitwise(seed, taps, length):
    state = seed
    sequence = []
    for _ in range(length):
        sequence.append(state & 0xFF)
        new_bit = 0
        for tap in taps:
            new_bit ^= (state >> tap) & 1
        state = ((state << 1) | new_bit) & 0xFF # Последние 8 бит результата
    return sequence

class RNGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pseudorandom Number Generator")

        # Начальные размеры окна
        self.root.geometry("600x600")
        self.root.resizable(width=True, height=True)

        # Переменные
        self.method_var = tk.StringVar(value="LCG")
        self.length_var = tk.StringVar()
        self.seed_var = tk.StringVar()

        # Выбор метода
        ttk.Label(root, text="Select Method:").pack(pady=5)
        self.method_menu = ttk.Combobox(root, textvariable=self.method_var, values=["LCG", "BBS", "LFSR"])
        self.method_menu.pack()

        # Ввод длины
        ttk.Label(root, text="Number of Values to Generate:").pack(pady=5)
        self.length_entry = ttk.Entry(root, textvariable=self.length_var)
        self.length_entry.pack()

        # Ввод начального значения
        ttk.Label(root, text="Seed Value:").pack(pady=5)
        self.seed_entry = ttk.Entry(root, textvariable=self.seed_var)
        self.seed_entry.pack()

        # Кнопка генерации
        self.generate_button = ttk.Button(root, text="Generate", command=self.generate_numbers)
        self.generate_button.pack(pady=10)

        # Фрейм для графика
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.canvas_frame.pack_propagate(True)

    def generate_numbers(self):
        method = self.method_var.get()
        length = int(self.length_var.get())
        seed = int(self.seed_var.get())

        # Выбор метода генерации
        if method == "LCG":
            numbers = lcg_numpy(a, c, m, seed, length)
        elif method == "BBS":
            numbers = bbs_binary(p, q, seed, length)
        elif method == "LFSR":
            numbers = lfsr_bitwise(seed, lfsr_taps, length)

        self.plot_histogram(numbers)

    def plot_histogram(self, numbers):
        # Очистка старого графика
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Создание графика
        fig, ax = plt.subplots(figsize=(6, 4))
        bins = 64  # Увеличиваем количество интервалов для более узких столбцов
        hist, bin_edges, _ = ax.hist(numbers, bins=bins, range=(0, 256), color='blue', alpha=0.7)
        ax.set_title("Histogram of Generated Numbers")
        ax.set_x
        label("Value")
        ax.set_ylabel("Frequency")

        # Добавление графика в tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Обновление высоты окна в зависимости от графика
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = RNGApp(root)
    root.mainloop()