from argparse import ArgumentParser
from pathlib import Path
import cv2 as cv


def main():
    parser = ArgumentParser()

    parser.add_argument("-i", required=True, help="the video file to play")

    filepath = parser.parse_args().i

    video = cv.VideoCapture(filepath)

    fps = video.get(cv.CAP_PROP_FPS)
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    name = Path(filepath).name 
    
    if not video.isOpened():
        print("Error opening video file")

    while video.isOpened():

        ret, frame = video.read()

        if ret:

            frame = cv.putText(frame, name, (0, height - 40), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2, cv.LINE_AA)
            frame = cv.putText(frame, "FPS=" + str(fps), (0, height), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2, cv.LINE_AA)

            cv.imshow(name, frame)

            if cv.waitKey(25) & 0xFF == ord("q"): # waitkey это задержка, а ord закрывает видео при нажатии q
                break

        else:
            break

    video.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
