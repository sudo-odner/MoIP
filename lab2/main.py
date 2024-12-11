import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Label, Button, StringVar, OptionMenu, Frame
from tkinter.scrolledtext import ScrolledText
import math

# 1. Линейный конгруэнтный генератор (LCG)
def lcg(a, c, m, seed, size):
    numbers = []
    x = seed
    for _ in range(size):
        x = (a * x + c) % m
        numbers.append(x)
    return numbers

# 2. Генератор BBS (Blum Blum Shub)
def bbs(p, q, seed, size):
    numbers = []
    x = seed * seed % (p * q)
    for _ in range(size):
        x = x * x % (p * q)
        numbers.append(x % 256)
    return numbers

# 3. Линейный рекуррентный генератор (LFSR)
def lfsr(seed, taps, size):
    state = seed
    numbers = []
    for _ in range(size):
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        state = [feedback] + state[:-1]
        numbers.append(int(''.join(map(str, state)), 2) % 256)
    return numbers

class GeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Generator with Histogram")
        self.root.geometry("900x700")

        # Algorithm Selection
        Label(root, text="Select Algorithm:", font=("Arial", 12)).pack(pady=5)
        self.algorithm_var = StringVar(value="LFSR")
        OptionMenu(root, self.algorithm_var, "LFSR", "LCG", "BBS").pack(pady=5)

        # Number Selection
        self.number_var = StringVar(value="50")
        Label(root, text="Select Number of Values:", font=("Arial", 12)).pack(pady=5)
        OptionMenu(root, self.number_var, "1", "50", "100", "1000").pack(pady=5)

        # Output Frame
        self.output_frame = Frame(root)
        self.output_frame.pack(pady=10, fill="both", expand=True)

        self.output_text = ScrolledText(self.output_frame, height=10, font=("Courier", 12))
        self.output_text.pack(side="left", fill="both", expand=True, padx=5)

        self.plot_frame = Frame(self.output_frame)
        self.plot_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Generate Button
        Button(root, text="Generate", command=self.generate, font=("Arial", 12)).pack(pady=10)

    def generate(self):
        try:
            algorithm = self.algorithm_var.get()
            size = int(self.number_var.get())

            if algorithm == "LFSR":
                seed = [1, 0, 0, 1, 1, 0, 1, 0]  # Example seed
                taps = [7, 5, 3, 0]  # Example taps
                data = lfsr(seed, taps, size)
            elif algorithm == "LCG":
                a, c, m, seed = 1103515245, 12345, 2**31, 42  # Example LCG parameters
                data = lcg(a, c, m, seed, size)
            elif algorithm == "BBS":
                p, q, seed = 499, 547, 2173  # Example BBS parameters
                data = bbs(p, q, seed, size)
            else:
                raise ValueError("Unsupported algorithm selected.")

            self.display_output(data)
            self.display_histogram(data, algorithm)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_output(self, data):
        self.output_text.delete(1.0, "end")
        self.output_text.insert("insert", "Generated Numbers:\n")
        self.output_text.insert("insert", " ".join(map(str, data)))

    def display_histogram(self, data, algorithm):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.hist(data, bins=20, color="blue", edgecolor="black")
        ax.set_title(f"{algorithm} Histogram")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = Tk()
    app = GeneratorApp(root)
    root.mainloop()
