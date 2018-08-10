from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np
import random

font = ImageFont.truetype("simhei.ttf", 60, encoding="utf-8")

img=Image.new('RGB', (60,60), (0,0,0))

for i in range(0,10):
    imgtemp=img.copy()
    ImageDraw.Draw(imgtemp).text((0, 0), str(i), (255, 255, 255), font)
    imgtemp.save(str(i)+".jpg",'jpeg')

img.show()