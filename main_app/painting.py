import base64
import random
import math

from functools import reduce
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw


def make_painting(name = 'Overlay Apple'):
    image = Image.new('RGB', (500, 500), (245, 237, 218))
    d = ImageDraw.Draw(image)

    str_list = name.split()
    for word in str_list:
        str_val = reduce(lambda x, y: x+y, map(ord, word))
        random.seed(str_val)

        for char in word:
            x = math.floor(random.random() * 500)
            y = math.floor(random.random() * 500)
            
            r = math.floor(random.random() * 256)
            g = math.floor(random.random() * 256)
            b = math.floor(random.random() * 256)
            while x < 500 and y < 500 and x >= 0 and y >= 0:
                d.point((x, y), (r, g, b))
                direction = math.floor(random.random() * 4)
                if(direction == 0):
                    y -= 1
                elif(direction == 1):
                    x += 1
                elif(direction == 2):
                    y += 1
                elif(direction == 3):
                    x -= 1
                else:
                    print('Invalid value!')
                    break

    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)

    return image_io.getvalue()