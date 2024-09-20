from argparse import ArgumentParser
from skimage import io, transform, util, exposure, filters, draw
from random import randrange, random, uniform
from pathlib import Path


def parse():

    parser = ArgumentParser()

    parser.add_argument("--dir", default=".", help="the directory to scan from and to output to")

    parser.add_argument("--rotate", required=False, action="store_true", help="rotate the images randomly")

    parser.add_argument("--resize", required=False, action="store_true", help="resize the images to a square")

    parser.add_argument("--swirl", required=False, action="store_true", help="swirl the images")

    parser.add_argument("--invert", required=False, action="store_true", help="invert the colors of the images")

    parser.add_argument("--noise", required=False, action="store_true", help="apply random noise to the images")

    parser.add_argument("--gaussian", required=False, action="store_true", help="apply a gaussian filter to the images")
    
    parser.add_argument("--gamma", required=False, action="store_true", help="adjust gamma randomly")

    parser.add_argument("--cut", required=False, action="store_true", help="cut a part of the images")

    parser.add_argument("--everything", required=False, action="store_true", help="apply every augmentation")

    return parser.parse_args()


def zeros(val):  # т.к. имена файлов состоят из 4 цифр, для значений < 1000 нужно приписать недостающие нули

    zero_count = 4        

    while val >= 1:
        val /= 10
        zero_count -= 1

    return zero_count


def main():
    
    args = parse()

    files = [file for file in Path(args.dir).glob("*")]
    
    images = io.imread_collection(files)

    count = len(images)

    for image in images:

        width, height = image.shape[0], image.shape[1]

        if args.gaussian or args.everything:
            image = filters.gaussian(image, sigma=random())  # фильтр Гаусса

        if args.noise or args.everything:
            image = util.random_noise(image)  # добавляет шум

        if args.invert or args.everything:
            image = util.invert(image)  # обратить цвета

        if args.gamma or args.everything:
            image = exposure.adjust_gamma(image, uniform(0.5, 3))  # меняет яркость

        if args.swirl or args.everything:
            image = transform.swirl(image, (randrange(0, width), randrange(0, height)) , randrange(1, 20))  # делает воронку

        if args.rotate or args.everything:
            image = transform.rotate(image, randrange(90, 360, 90))  # поворачивает изображение случайно

        if args.resize or args.everything:
            image = transform.resize(image, (350, 350))  # делает изображение квадратным

        if args.cut or args.everything:
            squareX, squareY = randrange(0, width-50), randrange(0, height-50)

            draw.set_color(image, draw.rectangle((squareX, squareY), (squareX+50, squareY+50)), (0, 0, 0))  # вырезаем квадрат
        
        try:
            io.imsave(args.dir + "/" + "0"*zeros(count) + str(count) + ".jpg", util.img_as_ubyte(image))
            count += 1

        except:
            continue


if __name__ == "__main__":
    main()
