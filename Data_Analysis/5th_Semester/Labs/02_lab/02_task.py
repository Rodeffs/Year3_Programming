from PIL import Image
from sys import argv

# Т.к. в произвольном изображении будут использоваться все цвета, то
# я так понял смысл задания в том, что нужно просто посчитать значение
# какого цвета в битах больше


def main():

    with Image.open(argv[1]) as img:
        
        img_data = img.getdata()

        red, green, blue = 0, 0, 0

        for pixel_data in img_data:

            red += pixel_data[0]
            green += pixel_data[1]
            blue += pixel_data[2]


        if max(red, green, blue) == red:
            print("The color RED is used the most")

        elif max(red, green, blue) == green:
            print("The color GREEN is used the most")

        elif max(red, green, blue) == blue:
            print("The color BLUE is used the most")


if __name__ == "__main__":
    main()
