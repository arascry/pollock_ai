import base64
import random
import math

from functools import reduce
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw

class StrokeInstructions:
    def __init__(self, name):
        self.name

def make_painting(name = 'Overlay Apple'):
    image = Image.new('RGB', (500, 500), (245, 237, 218))
    d = ImageDraw.Draw(image)

    str_list = name.split()

    for word in str_list:
        str_val = reduce(lambda x, y: str(x)+str(y), map(ord, word))
        random.seed(int(str_val))
        #poly_path(500, 500, d, word)
        #chord_path(500, 500, d, word)
        #stroke_path(500, 500, d, word)
        random_walk(500, 500, d, word)

    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)

    return image_io.getvalue()

def random_walk(img_w, img_h, d, word):
    for char in word:
        x = math.floor(random.random() * img_w)
        y = math.floor(random.random() * img_h)
        
        r = math.floor(random.random() * 256)
        g = math.floor(random.random() * 256)
        b = math.floor(random.random() * 256)
        while x < img_w and y < img_h and x >= 0 and y >= 0:
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
    return

def stroke_path(img_w, img_h, d, word):
    for char in word:
        x1 = math.floor(random.random() * img_w)
        y1 = math.floor(random.random() * img_h)
        x2 = math.floor(random.random() * img_w)
        y2 = math.floor(random.random() * img_h)            
        
        r = math.floor(random.random() * 256)
        g = math.floor(random.random() * 256)
        b = math.floor(random.random() * 256) 
        while x1 < img_w and y1 < img_h and x1 >= 0 and y1 >= 0:
            d.line([x1, y1, x2, y2], (r, g, b), 5)
            direction = math.floor(random.random() * 4)
            if(direction == 0):
                y1 -= 10
            elif(direction == 1):
                x1 += 10
            elif(direction == 2):
                y1 += 10
            elif(direction == 3):
                x1 -= 10
            else:
                print('Invalid value!')
                break
    return

def chord_path(img_w, img_h, d, word):
    for char in word:
        r = math.floor(random.random() * 256)
        g = math.floor(random.random() * 256)
        b = math.floor(random.random() * 256)

        xS = math.floor(random.random() * img_w)
        yS = math.floor(random.random() * img_h)
        xE = math.floor(random.random() * img_w)
        yE = math.floor(random.random() * img_h)            
        
        min_w = min(xS, xE)
        min_h = min(yS, yE)
        max_w = max(xS, xE)
        max_h = max(yS, yE)
        
        x = (max_w + min_w) / 2
        y = (max_h + min_h) / 2
        coord_list = [x, y]

        while x < max_w and y < max_h and x >= min_w and y >= min_h:
            direction = math.floor(random.random() * 4)
            if(direction == 0):
                y -= 5
            elif(direction == 1):
                x += 5
            elif(direction == 2):
                y += 5
            elif(direction == 3):
                x -= 5
            else:
                print('Invalid value!')
                break
            coord_list.append(x)
            coord_list.append(y)
        d.line(coord_list, (r, g, b), 3)
    return

def poly_path(img_w, img_h, d, word):
    for char in word:
        r = math.floor(random.random() * 256)
        g = math.floor(random.random() * 256)
        b = math.floor(random.random() * 256)

        xS = math.floor(random.random() * img_w)
        yS = math.floor(random.random() * img_h)
        xE = math.floor(random.random() * img_w)
        yE = math.floor(random.random() * img_h)            
        
        min_w = min(xS, xE)
        min_h = min(yS, yE)
        max_w = max(xS, xE)
        max_h = max(yS, yE)
        
        x = (max_w + min_w) / 2
        y = (max_h + min_h) / 2
        coord_list = [x, y]

        while x < max_w and y < max_h and x >= min_w and y >= min_h:
            direction = math.floor(random.random() * 4)
            if(direction == 0):
                y -= 5
            elif(direction == 1):
                x += 5
            elif(direction == 2):
                y += 5
            elif(direction == 3):
                x -= 5
            else:
                print('Invalid value!')
                break
            coord_list.append(x)
            coord_list.append(y)
        d.polygon(coord_list, (r, g, b), (r, g, b))
    return