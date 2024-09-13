from PIL import Image, ImageDraw


with Image.open("resources/test.jpg") as img:
    with Image.open("resources/watermark.png") as watermark:

        # Я хочу разместить её в центр, следовательно нужно поместить её в координаты ((W - w)/2, (H - h)/2)
        # где W - это ширина исходного изображения, w - ширина ватермарки, H - высота исходного, h - высота ватермарки 

        watermarkX = (img.width - watermark.width) // 2
        watermarkY = (img.height - watermark.height) // 2

        img.paste(watermark, (watermarkX, watermarkY))

        # Теперь пишем текст в тех же координатах

        draw = ImageDraw.Draw(img)

        draw.text((watermarkX, watermarkY), "THIS IS A WATERMARK") 

        img.show()

        img.save("outputs/image_with_watermark.jpg", "JPEG")
