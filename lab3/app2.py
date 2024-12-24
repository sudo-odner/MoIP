import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Частотный анализ текста
def privateAnalysisText(text: str, encode="cp1251") -> np.ndarray:
    privateAnalysis = np.zeros(shape=256, dtype=int)
    for char in text:
        privateAnalysis[char.encode(encode, errors="replace")[0]] += 1
    return privateAnalysis


# Энтропия
def entropy(privateAnalysis):
    total = sum(privateAnalysis)
    probabilities = privateAnalysis / total
    entropy = -np.nansum(probabilities * np.log2(probabilities, where=privateAnalysis != 0))
    return entropy


# Шифрование текста
def encrypt_with_constant_cp1251(text, constant):
    def char_shift_cp1251(char, constant):
        byte_value = char.encode('cp1251')[0]
        shifted_value = (byte_value + constant) % 256
        return bytes([shifted_value]).decode('cp1251', errors='replace')

    return ''.join(char_shift_cp1251(char, constant) for char in text)


def encrypt_with_proverb_cp1251(text, key_phrase):
    def char_to_cp1251_byte(char):
        return char.encode('cp1251')[0]

    def byte_to_cp1251_char(byte):
        return bytes([byte]).decode('cp1251', errors='replace')

    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'
    key = [(alphabet.index(char.upper()) + 1) for char in key_phrase if char.upper() in alphabet]

    encrypted = []
    for i, char in enumerate(text):
        char_byte = char_to_cp1251_byte(char)
        shifted_byte = (char_byte + key[i % len(key)]) % 256
        encrypted_char = byte_to_cp1251_char(shifted_byte)
        encrypted.append(encrypted_char)

    return ''.join(encrypted)

# Реализация LFSR с использованием битовых операций и двоичного представления
def lfsr(seed, length):
    # Параметры для LFSR
    taps = [7, 4, 3, 2] # Полином x^8 + x^5 + x^4 + x^3 + 1
    state = seed % 256 # Обрезаем если сид больше 8

    sequence = []
    for _ in range(length):
        new_bit = 0
        for tap in taps:
            new_bit ^= state >> (tap % 8)
        new_bit = new_bit & 1

        state = ((state >> 1) | (new_bit << 7)) & 0xFF # Последние 8 бит результата
        sequence.append(state)
    return sequence


def encrypt_with_psp_cp1251(text, psp):
    def char_to_cp1251_byte(char):
        return char.encode('cp1251')[0]

    def byte_to_cp1251_char(byte):
        return bytes([byte]).decode('cp1251', errors='replace')

    encrypted = []
    for i, char in enumerate(text):
        char_byte = char_to_cp1251_byte(char)
        shifted_byte = (char_byte + psp[i % len(psp)]) % 256
        encrypted_char = byte_to_cp1251_char(shifted_byte)
        encrypted.append(encrypted_char)

    return ''.join(encrypted)


def plot_histogram_in_tkinter(analysis, root):
    # Create a new figure and axis for the plot
    fig, ax = plt.subplots(figsize=(5, 3))  # Adjust the size as needed
    x = list(range(256))

    # Plot the histogram
    ax.bar(x, analysis, width=1.0, color='blue', edgecolor='black')
    ax.set_title("Frequency Histogram")
    ax.set_xlabel('Byte Value')
    ax.set_ylabel('Frequency')
    ax.grid(True)

    # Remove any old plot from the canvas if it exists
    if hasattr(root, 'canvas'):
        root.canvas.get_tk_widget().destroy()

    # Create the FigureCanvasTkAgg object and embed it in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()

    # Pack the canvas widget into the Tkinter window
    canvas.get_tk_widget().pack(pady=20)

    # Store the canvas to update it later if needed
    root.canvas = canvas


# Tkinter GUI Application
class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Encryption and Analysis")
        self.text = ""

        self.text_box = tk.Text(root, height=10, width=50)
        self.text_box.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Text", command=self.load_text)
        self.load_button.pack(pady=5)

        # Combobox for selecting encryption method
        self.method_var = tk.StringVar()
        self.method_menu = ttk.Combobox(root, textvariable=self.method_var, values=["Const", "Proverb", "PSP"])
        self.method_menu.set("Const")  # Default value
        self.method_menu.pack(pady=5)

        # Entry for constant and proverb inputs
        self.constant_label = tk.Label(root, text="Enter constant key:")
        self.constant_label.pack(pady=5)
        self.constant_entry = tk.Entry(root)
        self.constant_entry.pack(pady=5)

        self.proverb_label = tk.Label(root, text="Enter proverb key:")
        self.proverb_label.pack(pady=5)
        self.proverb_entry = tk.Entry(root)
        self.proverb_entry.pack(pady=5)

        self.encrypt_button = tk.Button(root, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.pack(pady=5)

        self.histogram_button = tk.Button(root, text="Generate Histogram", command=self.generate_histogram)
        self.histogram_button.pack(pady=5)

        self.entropy_button = tk.Button(root, text="Calculate Entropy", command=self.calculate_entropy)
        self.entropy_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Text", command=self.save_text)
        self.save_button.pack(pady=5)

        self.result_label = tk.Label(root, text="Entropy will be displayed here.", wraplength=400)
        self.result_label.pack(pady=10)

    def load_text(self):
        file_path = filedialog.askopenfilename(title="Select a Text File", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as f:
                self.text = f.read()
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.text)

    def encrypt_text(self):
        if not self.text:
            messagebox.showerror("Error", "Please load text.txt first.")
            return

        method = self.method_var.get()

        if method == "Const":
            try:
                constant_key = int(self.constant_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer for the constant key.")
                return
            encrypted_text = encrypt_with_constant_cp1251(self.text, constant_key)

        elif method == "Proverb":
            proverb_key = self.proverb_entry.get()
            if not proverb_key:
                messagebox.showerror("Error", "Please enter a proverb key.")
                return
            encrypted_text = encrypt_with_proverb_cp1251(self.text, proverb_key)

        elif method == "PSP":
            try:
                psp = lfsr(2134, len(self.text))
                encrypted_text = encrypt_with_psp_cp1251(self.text, psp)
            except Exception as e:
                messagebox.showerror("Error", f"Error generating PSP: {e}")
                return

        else:
            messagebox.showerror("Error", "Invalid encryption method selected.")
            return

        self.encrypted_text = encrypted_text
        self.text = self.encrypted_text
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, self.text)
        messagebox.showinfo("Encryption", f"Text successfully encrypted using {method} method.")

    def generate_histogram(self):
        if not self.text:
            messagebox.showerror("Error", "Please input text.txt first.")
            return

        analysis = privateAnalysisText(self.text)
        plot_histogram_in_tkinter(analysis, self.root)

    def calculate_entropy(self):
        if not self.text:
            messagebox.showerror("Error", "Please input text.txt first.")
            return

        analysis = privateAnalysisText(self.text)
        result = entropy(analysis)
        self.result_label.config(text=f"Entropy: {result:.4f}")

    def save_text(self):
        if not self.text:
            messagebox.showerror("Error", "Please load text.txt first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text)
            messagebox.showinfo("Save", "Text saved successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
