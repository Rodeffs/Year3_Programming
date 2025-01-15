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

    parser.add_argument("--combine", required=False, action="store_true", help="instead of creating a new image for every augmentation, do them all at once")

    parser.add_argument("--everything", required=False, action="store_true", help="apply every augmentation")

    return parser.parse_args()


def zeros(val):  # т.к. имена файлов состоят из 4 цифр, для значений < 1000 нужно приписать недостающие нули

    zero_count = 4        

    while val >= 1:
        val /= 10
        zero_count -= 1

    return zero_count


def save(image, path, count):

    try:  # при аугментациях тип может поменяться с uint 8 на float64, поэтому так
        io.imsave(path + "/" + "0"*zeros(count) + str(count) + ".jpg", util.img_as_ubyte(image))
        return count + 1

    except:
        return count


def combine_augments(images, args):  # если применять сразу несколько аугментаций для каждого изображения

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

        count = save(image, args.dir, count)
     
    
def apply_augments(images, args):  # если для каждой аугментации создавать новое изображение

    count = len(images)

    for image in images:

        width, height = image.shape[0], image.shape[1]

        if args.gaussian or args.everything:
            new_image = filters.gaussian(image, sigma=random())
            count = save(new_image, args.dir, count)

        if args.noise or args.everything:
            new_image = util.random_noise(image)  # добавляет шум
            count = save(new_image, args.dir, count)

        if args.invert or args.everything:
            new_image = util.invert(image)  # обратить цвета
            count = save(new_image, args.dir, count)

        if args.gamma or args.everything:
            new_image = exposure.adjust_gamma(image, uniform(0.5, 3))  # меняет яркость
            count = save(new_image, args.dir, count)

        if args.swirl or args.everything:
            new_image = transform.swirl(image, (randrange(0, width), randrange(0, height)) , randrange(1, 20))  # делает воронку
            count = save(new_image, args.dir, count)

        if args.rotate or args.everything:
            new_image = transform.rotate(image, randrange(90, 360, 90))  # поворачивает изображение случайно
            count = save(new_image, args.dir, count)

        if args.resize or args.everything:
            new_image = transform.resize(image, (350, 350))  # делает изображение квадратным
            count = save(new_image, args.dir, count)

        if args.cut or args.everything:
            squareX, squareY = randrange(0, width-50), randrange(0, height-50)
            draw.set_color(image, draw.rectangle((squareX, squareY), (squareX+50, squareY+50)), (0, 0, 0))  # вырезаем квадрат
            count = save(image, args.dir, count)


def main():
    
    args = parse()

    files = [file for file in Path(args.dir).glob("*")]
    
    images = io.imread_collection(files)

    if args.combine:
        combine_augments(images, args)

    else:
        apply_augments(images, args)


if __name__ == "__main__":
    main()
