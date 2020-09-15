import base64
import random
import math

from functools import reduce
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw

def make_painting(name = 'Apple'):
    image = Image.new('RGB', (500, 500), (245, 237, 198))
    d = ImageDraw.Draw(image)

    str_val = reduce(lambda x, y: x+y, map(ord, name))

    random.seed(str_val)
    x = math.floor(random.random() * 500)
    y = math.floor(random.random() * 500)

    while x < 500 and y < 500 and x >= 0 and y >= 0:
        d.point((x, y), (255, 0, 0))
        direction = math.floor(random.random() * 4)
        # print(str(x) + ' ' + str(y))
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

    random.seed(str_val + 1)
    x = math.floor(random.random() * 500)
    y = math.floor(random.random() * 500)

    while x < 500 and y < 500 and x >= 0 and y >= 0:
        d.point((x, y), (100, 0, 0))
        direction = math.floor(random.random() * 4)
        # print(str(x) + ' ' + str(y))
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
    image_string = base64.b64encode(image_io.getvalue())
    return image_string