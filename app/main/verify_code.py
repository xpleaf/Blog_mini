#coding:utf-8
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random



def validate_pic():
    # 随机大写字母和数字:
    def rndChar():
        total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
        return random.choice(total)

    # 随机颜色1:
    def rndColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2:
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 200 x 34:
    width = 50 * 4
    height = 34
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype('FreeSans', 28)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    str = ''
    for t in range(4):
        text = rndChar()
        str += text
        draw.text((50 * t + 10, 1), text, font=font, fill=rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.FIND_EDGES)#ImageFilter.BLUR
    #image.save('static/images/code.jpg', 'jpeg')
    return image, str
