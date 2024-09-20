from argparse import ArgumentParser
from skimage import io, transform, util, exposure, filters
from random import randrange


def parse():

    parser = ArgumentParser()

    parser.add_argument("--dir", default=".", help="the directory to scan from")

    parser.add_argument("--rotate", required=False, action="store_true", help="rotate the images")

    parser.add_argument("--resize", required=False, action="store_true", help="resize the images")

    parser.add_argument("--distort", required=False, action="store_true", help="distort the image colors")

    parser.add_argument("--gaussian", required=False, action="store_true", help="apply a gaussian filter to the images")

    parser.add_argument("--blend", required=False, action="store_true", help="blend the images")

    parser.add_argument("--cut", required=False, action="store_true", help="cut a part of the images")

    return parser.parse_args()


def main():
    
    args = parse()

    images = io.imread_collection(args.dir)

    count = 0

    for image in images:

        if args.rotate:
            transform.rotate(image, randrange(90, 450, 90))

        if args.resize:
            transform.resize(image, (500, 500))

        if args.distort:
            distort(image)

        if args.gaussian:
            gaussian(image)

        if args.blend:
            blend(image)

        if args.cut:
            cut(image)

        io.imsave(args.dir + "/new_" + str(count) + ".jpg", image)

        count += 1


if __name__ == "__main__":
    main()
