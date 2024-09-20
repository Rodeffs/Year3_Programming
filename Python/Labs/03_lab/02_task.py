from argparse import ArgumentParser
from skimage import exposure, io
from PIL import Image
import matplotlib.pyplot as plt


def main():

    parser = ArgumentParser()

    parser.add_argument("-i", required=True, help="the image to show histograms for")
    
    path = parser.parse_args().i

    values, new_values = [], []

    with Image.open(path) as img:

        values = img.histogram()

    # Суть в том, что Image.histogram() возвращает массив из 768 элементов для RGB картинок, где:
    #   первые 256 элементов отвечают красному цвету
    #   следующие 256 - зелёному
    #   последние 256 - синему
    # Сами индексы отвечают за яркость, а значение, которые они возвращают - кол-во пискелей такой яркости для каждого цвета
    # Т.е. values[0] = кол-во пикселей с R = 0, values[256] = пиксели с G = 0 и values[512] = пиксели с B = 0
    # Поэтому для получения гистограммы их надо сложить

    fig, axs = plt.subplots(1, 1, squeeze=False)

    for i in range(0, 256):
        new_values.append(values[i] + values[i+256] + values[i+512])

    img = io.imread(path)
    
    histogram = exposure.histogram(img, channel_axis=2)

    plt.stairs(new_values, fill=True)

    plt.show()


if __name__ == "__main__":
    main()
