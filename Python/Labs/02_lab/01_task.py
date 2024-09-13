from PIL import Image


with Image.open("test.jpg") as img:

    img_data = img.getdata()  # получаем информацию об изображении

    # Делим на каналы:

    red_channel, green_channel, blue_channel = [], [], []

    for pixel_data in img_data:

        red_channel.append((pixel_data[0], 0, 0))
        green_channel.append((0, pixel_data[1], 0))
        blue_channel.append((0, 0, pixel_data[2]))

    
    # Выводим эти изображения:

    # Исходное
    img.show()
    
    # Красное
    img.putdata(red_channel)
    img.show()
    
    # Зелёное
    img.putdata(green_channel)
    img.show()

    # Синие 
    img.putdata(blue_channel)
    img.show()
