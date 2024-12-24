import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image

# Функции для анализа
def privateAnalysisText(path: str, encode="cp1251") -> np.ndarray:
    privateAnalysis = np.zeros(shape=256, dtype=int)

    with open(path, 'r') as f:
        text = f.read()
    for char in text:
        privateAnalysis[char.encode(encode)[0]] += 1
    return privateAnalysis


def privateAnalysisPhotoRGB(path: str) -> tuple:
    img = Image.open(path).convert('RGB')
    data = np.array(img)

    # Отдельный анализ для каждого канала
    red_channel = np.histogram(data[:, :, 0].flatten(), bins=256, range=(0, 256))[0]
    green_channel = np.histogram(data[:, :, 1].flatten(), bins=256, range=(0, 256))[0]
    blue_channel = np.histogram(data[:, :, 2].flatten(), bins=256, range=(0, 256))[0]

    return red_channel, green_channel, blue_channel


def entropy(privateAnalysis):
    total = sum(privateAnalysis)
    probabilities = privateAnalysis / total
    entropy = -np.nansum(probabilities * np.log2(probabilities, where=privateAnalysis != 0))
    return entropy

# Класс приложения на Tkinter
class PrivateAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Private Analysis Application")
        self.root.geometry("600x600")

        # Метки и кнопки
        self.label = tk.Label(root, text="Выберите файл для анализа", font=("Arial", 16))
        self.label.pack(pady=10)

        self.btn_select_file = tk.Button(root, text="Выбрать файл", command=self.load_file, font=("Arial", 12))
        self.btn_select_file.pack(pady=5)

        # Гистограмма
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

        # Энтропия
        self.entropy_label = tk.Label(root, text="", font=("Arial", 14))
        self.entropy_label.pack(pady=10)

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showwarning("Ошибка", "Файл не выбран")
            return

        try:
            # Определяем, текст это или картинка
            if file_path.endswith(('.txt')):
                analysis = privateAnalysisText(file_path)

                # Вычисляем энтропию
                ent = entropy(analysis)
                self.entropy_label.config(text=f"Энтропия файла: {ent:.4f}")

                # Строим график
                self.ax.clear()
                self.ax.bar(range(256), analysis, color='blue')
                self.ax.set_title("Private Analysis")
                self.ax.set_xlabel("Символы / Значения пикселей")
                self.ax.set_ylabel("Частота")

            elif file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                red_channel, green_channel, blue_channel = privateAnalysisPhotoRGB(file_path)

                # Строим график для трех каналов с прозрачностью
                self.ax.clear()
                self.ax.bar(range(256), red_channel, color='red', alpha=0.33, label='Red Channel')
                self.ax.bar(range(256), green_channel, color='green', alpha=0.33, label='Green Channel')
                self.ax.bar(range(256), blue_channel, color='blue', alpha=0.33, label='Blue Channel')
                self.ax.set_title("RGB Analysis")
                self.ax.set_xlabel("Значения пикселей")
                self.ax.set_ylabel("Частота")
                self.ax.legend()

                # Отображаем примерную энтропию (для красного канала как примера)
                self.entropy_label.config(text=f"Энтропия всех каналов: {entropy(red_channel + green_channel + blue_channel):.4f}")

            else:
                messagebox.showerror("Ошибка", "Неподдерживаемый формат файла")
                return

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Точка входа в приложение
if __name__ == "__main__":
    root = tk.Tk()
    app = PrivateAnalysisApp(root)
    root.mainloop()
