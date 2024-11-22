import math
import numpy as np

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

# Тестирование шифрования и дешифрования
text = "Текст для шифрованиявфыафваы вв"
print("Исходный текст:", text)

# Шифруем
encrypted_text, shift_key = triangle_encrypt(text)
print(f"\nЗашифрованный текст: {encrypted_text}")

# Расшифровываем
decrypted_text = triangle_decrypt(encrypted_text, shift_key)
print(f"\nРасшифрованный текст: {decrypted_text}")
