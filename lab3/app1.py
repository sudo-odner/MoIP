import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import math


# Функция для шифрования методом Маршрутной перестановки(Треугольник с использованием случайных сдвигов и транспозицией)
def triangle_encrypt(text):
    num_rows = int(np.ceil((-1 + math.sqrt(1 + 8 * len(text))) / 2))
    table = np.full((num_rows, num_rows), '')

    index = 0
    for i in range(num_rows):
        for j in range(i + 1):
            if index < len(text):
                table[i, j] = text[index]
                index += 1

    shift_key = np.random.randint(1, 5, size=num_rows)

    # Шифруем
    for i in range(num_rows):
        table[i][table[i] != ''] = np.roll(table[i][table[i] != ''], shift=shift_key[i])

    # Транспонируем треугольник (меняем строки и столбцы местами)
    transposed_table = table.T

    # Соединяем строки транспонированной таблицы в зашифрованный текст
    encrypted_text = ''.join([''.join(row) for row in transposed_table])

    return encrypted_text, shift_key

# Функция для расшифровки методом Треугольника с использованием ключа сдвигов
def triangle_decrypt(encrypted_text, shift_key):
    num_rows = int(np.ceil((-1 + math.sqrt(1 + 8 * len(encrypted_text))) / 2))
    table = np.full((num_rows, num_rows), '')
    elementLastBase = min(num_rows, len(encrypted_text) - (num_rows - 1) * num_rows // 2)

    # Заполняем таблицу зашифрованными строками
    index = 0
    for i in range(num_rows):
        if i < elementLastBase:
            for j in range(num_rows - i):
                if index < len(encrypted_text):
                    table[i, i + j] = encrypted_text[index]
                    index += 1
        else:
            for j in range(num_rows - i - 1):
                if index < len(encrypted_text):
                    table[i, i + j] = encrypted_text[index]
                    index += 1

    # Транспонируем матрицу
    transposed_table = table.T

    # Шифруем
    for i in range(num_rows):
        transposed_table[i][transposed_table[i] != ''] = np.roll(transposed_table[i][transposed_table[i] != ''], shift= (-1 * shift_key[i]))

    # Соединяем строки транспонированной таблицы в зашифрованный текст
    decrypted_text = ''.join([''.join(row) for row in transposed_table])

    return decrypted_text

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Application")

        self.filename = None

        self.text = tk.Text(self.root, wrap=tk.WORD, height=20, width=60)
        self.text.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Open File", command=self.open_file).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Encrypt", command=self.encrypt_text).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Decrypt", command=self.decrypt_text).grid(row=0, column=2, padx=5, pady=5)

    def open_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.filename:
            with open(self.filename, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)

    def encrypt_text(self):
        raw_text = self.text.get(1.0, tk.END).strip()
        if not raw_text:
            messagebox.showwarning("Warning", "No text.txt to encrypt")
            return

        encrypted_text, self.shift_key = triangle_encrypt(raw_text)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, encrypted_text)

        with open("output/encrypted_text_method/encrypted.txt", "w", encoding="utf-8") as f:
            f.write(encrypted_text)
        messagebox.showinfo("Info", "Text encrypted and saved as 'encrypted.txt'")

    def decrypt_text(self):
        encrypted_text = self.text.get(1.0, tk.END).strip()
        if not encrypted_text:
            messagebox.showwarning("Warning", "No text.txt to decrypt")
            return

        if not hasattr(self, 'shift_key'):
            messagebox.showerror("Error", "No key available for decryption")
            return

        decrypted_text = triangle_decrypt(encrypted_text, self.shift_key)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, decrypted_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()