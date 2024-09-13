from PIL import Image, ImageDraw


for i in range(1, 4):

    img = Image.new("RGB", (100, 100))

    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, 100, 100], outline=(0, 0, 255), width=5)

    draw.text((33, 15), str(i), font_size = 60, fill=(255, 0, 0))

    img.show()

    img.save("outputs/" + str(i) + ".png", "PNG")

