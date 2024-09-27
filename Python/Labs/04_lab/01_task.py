from argparse import ArgumentParser
from moviepy.editor import VideoFileClip


def parse():
    parser = ArgumentParser()

    parser.add_argument("-i", required=True, help="the input file to clip")

    parser.add_argument("-o", required=True, help="the name of the output file, works with mp4 only")

    parser.add_argument("-b", type=float, default=0, help="the start of the clip, will default to 0 if bigger than video duration")

    parser.add_argument("-e", type=float, default=-1, help="the end of the clip, will default to input duration if bigger than it")

    return parser.parse_args()


def main():
    args = parse()

    video = VideoFileClip(args.i)

    begin = args.b if (args.b <= video.duration and args.b >= 0) else 0
    end = args.e if (args.e <= video.duration and args.e >= 0) else video.duration

    if begin > end:  # чтобы не было отрицательных значений
        begin, end = end, begin
    
    clip = video.subclip(begin, end)

    try:
        clip.write_videofile(args.o)

    except:
        print("Error while saving video file. Remember, only mp4 output is supported")

    finally:
        video.close()


if __name__ == "__main__":
    main()
