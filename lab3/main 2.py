import numpy as np
import matplotlib.pyplot as plt
import os

# Частотный анализ текста
def privateAnalysisText(path: str, encode="cp1251") -> np.ndarray:
    with open(path, 'r', encoding=encode) as f:
        text = f.read()

    privateAnalysis = np.zeros(shape=256, dtype=int)
    for char in text:
        privateAnalysis[char.encode('cp1251')[0]] += 1

    return privateAnalysis

# Энтропия
def entropy(privateAnalysis):
    total = sum(privateAnalysis)  # Общая сумма частот
    probabilities = privateAnalysis / total  # Вероятности для каждого символа
    entropy = -np.nansum(probabilities * np.log2(probabilities, where=privateAnalysis != 0))  # Рассчитываем энтропию
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

def lfsr(seed, taps, size):
    state = seed
    numbers = []
    for _ in range(size):
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        numbers.append(state[-1])
        state = [feedback] + state[:-1]
    return [int(''.join(map(str, numbers[i:i+8])), 2) for i in range(0, len(numbers), 8)]

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

def plot_histogram(privateAnalysis, title):
    x = list(range(256))
    plt.bar(x, privateAnalysis, width=1.0, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

text_path = "text.txt"
constant_key = 11
proverb_key = "Порозно думать вместе не жить"
seed = [1, 0, 0, 1, 1, 0, 1, 1]
taps = [0, 1, 3, 4]

with open(text_path, 'r', encoding="cp1251") as f:
    original_text = f.read()

encrypted_constant = encrypt_with_constant_cp1251(original_text, constant_key)
encrypted_proverb = encrypt_with_proverb_cp1251(original_text, proverb_key)
psp = lfsr(seed, taps, len(original_text))
encrypted_psp = encrypt_with_psp_cp1251(original_text, psp)

os.makedirs("encrypted_texts", exist_ok=True)
with open("encrypted_texts/encrypted_constant1.txt", "w", encoding="cp1251", errors='replace') as f:
    f.write(encrypted_constant)
with open("encrypted_texts/encrypted_proverb1.txt", "w", encoding="cp1251", errors='replace') as f:
    f.write(encrypted_proverb)
with open("encrypted_texts/encrypted_psp1.txt", "w", encoding="cp1251", errors='replace') as f:
    f.write(encrypted_psp)

print("Метод 1: Константа")
analysis_constant = privateAnalysisText("encrypted_texts/encrypted_constant1.txt", "cp1251")
plot_histogram(analysis_constant, "Histogram (Constant Key)")
entropy_constant = entropy(analysis_constant)
print(f"Entropy: {entropy_constant:.4f} {len(encrypted_constant)}")

print("Метод 2: Поговорка")
analysis_proverb = privateAnalysisText("encrypted_texts/encrypted_proverb1.txt")
plot_histogram(analysis_proverb, "Histogram (Proverb Key)")
entropy_proverb = entropy(analysis_proverb)
print(f"Entropy: {entropy_proverb:.4f} {len(encrypted_proverb)}")

print("Метод 3: ПСП")
analysis_psp = privateAnalysisText("encrypted_texts/encrypted_psp1.txt")
plot_histogram(analysis_psp, "Histogram (LFSR Key)")
entropy_psp = entropy(analysis_psp)
print(f"Entropy: {entropy_psp:.4f}, {len(encrypted_psp)}")

print("Метод 4: Исходный текст")
analysis_original = privateAnalysisText(text_path)
plot_histogram(analysis_original, "Histogram (Original Text)")
entropy_original = entropy(analysis_original)
print(f"Entropy: {entropy_original:.4f} {len(original_text)}")
