import base64
import random
import math

from functools import reduce
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw

from .models import Word

class StrokeInstructions:
    def __init__(self, word):
        db_word = Word.objects.filter(word=word).first()
        if db_word:
            self.word = db_word.word
            self.seed = db_word.seed
            self.init_random()
            self.instructions = []
            for i in range(len(db_word.instruction)):
                self.instructions.append({'instruction': db_word.instruction[i], 'max_step': db_word.max_step[i]})
            print(self.instructions)
        else:
            self.word = word
            self.init_seed(word)
            self.init_random()
            self.instructions = []

    def init_seed(self, word):
        self.seed = reduce(lambda x, y: str(x) + str(y), map(ord, word))

    def init_random(self):
        self.rand = random
        self.rand.seed(self.seed)

    def nudge_seed(self, amount):
        self.seed += str(amount)
        print(self.seed)
        db_word = Word.objects.filter(word=self.word).first()
        db_word.seed = self.seed
        db_word.save()

    def generate_instruction(self):
        instruction = math.floor(self.rand.random() * 4)
        max_step = math.floor((self.rand.random() * 999) + 1)
        self.instructions.append({'instruction': instruction, 'max_step': max_step})
        self.save_to_db()

    def save_to_db(self):
        instruction = []
        max_step = []
        for stroke in self.instructions:
            instruction.append(stroke.get('instruction', 0))
            max_step.append(stroke.get('max_step', 0))
        word = Word.objects.filter(word=self.word).first()
        if word:
            word.instruction = instruction
            word.max_step = max_step
        else:
            word = Word(
                word=self.word, 
                seed=self.seed,
                instruction=instruction,
                max_step=max_step)
        word.save()


    def draw(self, img_w, img_h, d):
        for stroke in self.instructions:
            instruction = stroke.get('instruction', 0)
            max_step = stroke.get('max_step', 0)
            if instruction == 0:
                self.draw_poly(img_w, img_h, d, self.word, max_step)
            elif instruction == 1:
                self.draw_chord(img_w, img_h, d, self.word, max_step)
            elif instruction == 2:
                self.draw_walk(img_w, img_h, d, self.word)
            elif instruction == 3:
                self.draw_line(img_w, img_h, d, self.word, max_step)
                
    def draw_poly(self, img_w, img_h, d, word, max_step):
        for char in word:
            step = max_step
            
            r = math.floor(self.rand.random() * 256)
            g = math.floor(self.rand.random() * 256)
            b = math.floor(self.rand.random() * 256)

            xS = math.floor(self.rand.random() * img_w)
            yS = math.floor(self.rand.random() * img_h)
            xE = math.floor(self.rand.random() * img_w)
            yE = math.floor(self.rand.random() * img_h)            
            
            while xS == xE:
                xE = math.floor(self.rand.random() * img_w)
            
            while yS == yE:
                yE = math.floor(self.rand.random() * img_h)

            min_w = min(xS, xE)
            min_h = min(yS, yE)
            max_w = max(xS, xE)
            max_h = max(yS, yE)
            
            x = (max_w + min_w) / 2
            y = (max_h + min_h) / 2
            coord_list = [x, y]

            while x < max_w and y < max_h and x >= min_w and y >= min_h and step != 0:
                direction = math.floor(self.rand.random() * 4)
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
                step -= 1
            d.polygon(coord_list, (r, g, b), (r, g, b))
    
    def draw_chord(self, img_w, img_h, d, word, max_step):
        for char in word:
            step = max_step
            r = math.floor(self.rand.random() * 256)
            g = math.floor(self.rand.random() * 256)
            b = math.floor(self.rand.random() * 256)

            xS = math.floor(self.rand.random() * img_w)
            yS = math.floor(self.rand.random() * img_h)
            xE = math.floor(self.rand.random() * img_w)
            yE = math.floor(self.rand.random() * img_h)       
            
            while xS == xE:
                xE = math.floor(self.rand.random() * img_w)
            
            while yS == yE:
                yE = math.floor(self.rand.random() * img_h)                 
            
            min_w = min(xS, xE)
            min_h = min(yS, yE)
            max_w = max(xS, xE)
            max_h = max(yS, yE)
            
            x = (max_w + min_w) / 2
            y = (max_h + min_h) / 2
            coord_list = [x, y]

            while x < max_w and y < max_h and x >= min_w and y >= min_h and step != 0:
                direction = math.floor(self.rand.random() * 4)
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
                step -= 1
            d.line(coord_list, (r, g, b), 3)

    def draw_line(self, img_w, img_h, d, word, max_step):
        for char in word:
            step = max_step

            xS = math.floor(self.rand.random() * img_w)
            yS = math.floor(self.rand.random() * img_h)
            xE = math.floor(self.rand.random() * img_w)
            yE = math.floor(self.rand.random() * img_h)         

            while xS == xE:
                xE = math.floor(self.rand.random() * img_w)
            
            while yS == yE:
                yE = math.floor(self.rand.random() * img_h)

            r = math.floor(self.rand.random() * 256)
            g = math.floor(self.rand.random() * 256)
            b = math.floor(self.rand.random() * 256)

            min_w = min(xS, xE)
            min_h = min(yS, yE)
            max_w = max(xS, xE)
            max_h = max(yS, yE)
            
            x2 = (max_w + min_w) / 2
            y2 = (max_h + min_h) / 2

            while x2 < max_w and y2 < max_h and x2 >= min_w and y2 >= min_h and step != 0:
                x1 = x2
                y1 = y2
                direction = math.floor(self.rand.random() * 4)
                if(direction == 0):
                    y2 -= 10
                elif(direction == 1):
                    x2 += 10
                elif(direction == 2):
                    y2 += 10
                elif(direction == 3):
                    x2 -= 10
                else:
                    print('Invalid value!')
                    break
                d.line([x1, y1, x2, y2], (r, g, b), 5)
                step -= 1

    def draw_walk(self, img_w, img_h, d, word):
        for char in word:

            xS = math.floor(self.rand.random() * img_w)
            yS = math.floor(self.rand.random() * img_h)
            xE = math.floor(self.rand.random() * img_w)
            yE = math.floor(self.rand.random() * img_h)         

            while xS == xE:
                xE = math.floor(self.rand.random() * img_w)
            
            while yS == yE:
                yE = math.floor(self.rand.random() * img_h)

            r = math.floor(self.rand.random() * 256)
            g = math.floor(self.rand.random() * 256)
            b = math.floor(self.rand.random() * 256)

            min_w = min(xS, xE)
            min_h = min(yS, yE)
            max_w = max(xS, xE)
            max_h = max(yS, yE)

            x = (max_w + min_w) / 2
            y = (max_h + min_h) / 2

            while x < max_w and y < max_h and x >= min_w and y >= min_h:
                d.point((x, y), (r, g, b))
                direction = math.floor(self.rand.random() * 4)
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

def make_painting(name = 'Overlay Apple'):
    image = Image.new('RGB', (500, 500), (245, 237, 218))
    d = ImageDraw.Draw(image)

    str_list = name.split()

    for word in str_list:
        temp = StrokeInstructions(word)
        temp.generate_instruction()
        if (word == 'The'):
            print('Nudging!')
            temp.nudge_seed(5)
            temp.generate_instruction()
        temp.draw(500, 500, d)

        

    image_io = BytesIO()
    image.save(image_io, format='PNG')
    image_io.seek(0)

    return image_io.getvalue()
