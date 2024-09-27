from argparse import ArgumentParser
import cv2


def main():
    parser = ArgumentParser()

    parser.add_argument("-i", required=True, help="the video file to play")

    filepath = parser.parse_args().i

    video = cv2.VideoCapture(filepath)


if __name__ == "__main__":
    main()
