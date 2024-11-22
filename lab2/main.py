import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter


# 3. Линейный рекуррентный генератор (LFSR)
def lfsr(seed, taps, size):
    state = seed

    numbers = []
    for _ in range(size):
        numbers.append(state[-1])
        feedback = 0
        for t in taps:
            feedback ^= state[t]
        state = [feedback] + state[:-1]
    return [int(''.join(map(str, numbers[i:i+8])), 2) for i in range(0, len(numbers), 8)]


# Построение гистограммы
def plot_histogram(data, title, bins=256, range=(0, 255)):
    plt.hist(data, bins=bins, range=range, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

seed = [1, 0, 0, 1, 1, 0, 1, 1]
taps = [0, 1, 3, 4]
lfsr_numbers = lfsr(seed, taps, 50)
plot_histogram(lfsr_numbers, "LFSR Histogram 50")
lfsr_numbers = lfsr(seed, taps, 100)
plot_histogram(lfsr_numbers, "LFSR Histogram 100")
lfsr_numbers = lfsr(seed, taps, 1000)
plot_histogram(lfsr_numbers, "LFSR Histogram 1000")
