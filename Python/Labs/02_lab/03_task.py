from PIL import Image, ImageDraw, ImageFont


with Image.open("test.jpg") as img:
    with Image.open("watermark.png") as watermark:

        # Я хочу разместить её в центр, следовательно нужно поместить её в координаты ((W - w)/2, (H - h)/2)
        # где W - это ширина исходного изображения, w - ширина ватермарки, H - высота исходного, h - высота ватермарки 

        watermarkX = (img.width - watermark.width) // 2
        watermarkY = (img.height - watermark.height) // 2

        img.paste(watermark, (watermarkX, watermarkY))

        # Теперь пишем текст, его координаты будут ((W - w)/2, (H + h)/2)

        draw = ImageDraw.Draw(img)

        draw.text((watermarkX, watermarkY), "THIS IS A WATERMARK") 

        img.show()

        img.save("image_with_watermark.jpg", "JPEG")
