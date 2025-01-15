from argparse import ArgumentParser
from skimage import color, exposure, io
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

    for i in range(0, 256):
        new_values.append(values[i] + values[i+256] + values[i+512])

    img = io.imread(path)

    # Зачем-то пытаемся получить гистограмму для отдельных цветов через skimage, хотя мы уже это сделали через Pillow выше
    
    color_histogram = exposure.histogram(img, channel_axis=2)

    # Вывод изображения:

    display_img = plt.subplot2grid((4, 2), (0, 0), rowspan=4)

    display_img.set_title("Image")

    display_img.imshow(img)

    display_img.axis("off")

    # Гистограмма изображения:

    hist_img = plt.subplot2grid((4, 2), (0, 1))

    hist_img.stairs(new_values, fill=True, color=(0, 0, 0))

    hist_img.set_title("Full histogram")

    # Гистограмма красного:

    red_hist = plt.subplot2grid((4, 2), (1, 1))
    
    red_hist.stairs(color_histogram[0][0], fill=True, color=(1, 0, 0))

    red_hist.set_title("Red histogram")

    # Гистограмма зелёного:

    green_hist = plt.subplot2grid((4, 2), (2, 1))

    green_hist.stairs(color_histogram[0][1], fill=True, color=(0, 1, 0))

    green_hist.set_title("Green histogram")

    # Гистограмма синего:

    blue_hist = plt.subplot2grid((4, 2), (3, 1))

    blue_hist.stairs(color_histogram[0][2], fill=True, color=(0, 0, 1))

    blue_hist.set_title("Blue histogram")

    # Вывод всего на экран:

    plt.tight_layout()  # чтобы текст не налезал друг на друга
    
    plt.show()


if __name__ == "__main__":
    main()
