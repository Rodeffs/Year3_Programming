from argparse import ArgumentParser
from skimage import io
from PIL import Image
import matplotlib.pyplot as plt


def main():

    parser = ArgumentParser()

    parser.add_argument("-i", required=True, help="the image to show histograms for")
    
    path = parser.parse_args().i

    with Image.open(path) as img:
        histogram = img.histogram()

        fig, axs = plt.subplots(1, 1)

        axs.hist(histogram)

        plt.show()





if __name__ == "__main__":
    main()
