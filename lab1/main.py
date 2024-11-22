import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def privateAnalysisText(path: str, encode="cp1251") -> np.ndarray:
    with open(path, 'r') as f:
        text = f.read()

    privateAnalysis = np.zeros(shape=256, dtype=int)
    for char in text:
        privateAnalysis[char.encode(encode)[0]] += 1

    return privateAnalysis


def privateAnalysisPhoto(path: str) -> np.ndarray:
    img = Image.open(path)
    dataPixelIn1D = np.array(img).reshape(-1)

    privateAnalysis = np.zeros(shape=256, dtype=int)
    for pixel in dataPixelIn1D:
        privateAnalysis[pixel] += 1

    return privateAnalysis


def entropy(privateAnalysis):
    total = sum(privateAnalysis)
    probabilities = privateAnalysis / total
    entropy = -np.nansum(probabilities * np.log2(probabilities, where=privateAnalysis != 0))
    return entropy


def plotHistogram(histogramCords: np.ndarray, title: str):
    plt.bar(np.arange(256), histogramCords)
    plt.title(title)
    plt.xlabel("Range 0-255")
    plt.xlim(-10, 265)
    plt.ylabel("frequency")
    plt.show()


data_file_bmp = [
    "data/bmp/tree.bmp",        # tree photo
    "data/bmp/mandrill.bmp",    # mandrill photo
    "data/bmp/red.bmp"          # red picture
]
data_file_txt = [
    "data/txt/news_english.txt",               # News text on english
    "data/txt/news_russian.txt",               # News text on russian
    "data/txt/water_magicians_zgut_msit.txt"   # Big text about book "water magicians zgut msit"
]

for file in data_file_bmp:
    fileName = file.split("/")[-1].split(".")[0]
    privateAnalysis = privateAnalysisPhoto(file)
    plotHistogram(privateAnalysis, fileName)
    print(f"entropy {fileName}:", entropy(privateAnalysis))

for file in data_file_txt:
    fileName = file.split("/")[-1].split(".")[0]
    privateAnalysis = privateAnalysisText(file)
    plotHistogram(privateAnalysis, fileName)
    print(f"entropy {fileName}:", entropy(privateAnalysis))
