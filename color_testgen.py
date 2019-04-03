import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
from os import listdir
from os.path import isfile, join
import xml.etree.cElementTree as ET
import cv2

def text_cleaner (dirty_text):
    # CLEANS NOT WANTED CHARACTERES AND SENDS STRING IN LOWERCASE
    clean_text = ''.join(c for c in dirty_text if c not in '\|"?>.<,`~(){}<>;:!@#$%^&*_-=+-*\\ \/[]\' \|"?>.<,`~')
    return clean_text.lower()

def area(coords, posXmax, posXmin, posYmax, posYmin):  # returns None if rectangles don't intersect
    dx = min(coords[1], posXmax) - max(coords[0], posXmin)
    dy = min(coords[3], posYmax) - max(coords[2], posYmin)
    if (dx >= 0) and (dy >= 0):
        return dx * dy
    return None


mypath = '/home/amafla/.fonts/'
fontFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# Read file of words

with open ("/home/amafla/Documents/Python_Codes/english_words/90K dictionary Jaderberg for IAM and numbers.txt") as f:
    data = f.read()
    words = data.split("\n")
    # Delete the end of file:
    del words[-1]
print("Data Loaded...!")
length = np.shape(words)[0]
print (length," Total words")
y = np.arange(0, length, 1)

# CLEAN THE WORDS:

for i in range (0, len(words)):
    words[i] = text_cleaner(words[i])

folder = 'test90k/'
nimages = 100
dictionary_size = 88623
print (dictionary_size+1," Dictionary size")

for i in range(0, nimages):
    if (i % 100 == 0):
        print("IMAGE NUMBER:", i)
    coords = list()
    textlist = list()
    sizeX = 450 + random.randint(0, 150)
    sizeY = 450 + random.randint(0, 150)
    R = random.randint(0,255)
    G = random.randint(0,255)
    B = random.randint(0,255)
    image = Image.new("RGB", (sizeX, sizeY), (R, G, B))
    draw = ImageDraw.Draw(image)

    number_words = random.randint(7, 12)


    for j in range(0, number_words):

        word_index = random.randint(0, dictionary_size)
        text = words[word_index]
        if (random.random() >= 0.5):
            text = text.upper()
        text_size = random.randint(18, 60)
        randomFont = random.randint(0, 150)
        font = ImageFont.truetype("/home/amafla/.fonts/" + fontFiles[randomFont], text_size, encoding="unic")
        bound = font.getsize(text)

        while bound[0] > (sizeX*3/4):
            text_size = random.randint(18, 60)
            randomFont = random.randint(0, 150)
            font = ImageFont.truetype("/home/amafla/.fonts/" + fontFiles[randomFont], text_size, encoding="unic")
            bound = font.getsize(text)

        if j == 0:
            posX = random.randint(0, (sizeX - bound[0]))
            posY = random.randint(0, (sizeY - bound[1]))
            coordinates = [posX, posX + bound[0], posY, posY + bound[1]]
            coords.append(coordinates)
            textlist.append(text)
            contrast_flag = False
            while contrast_flag == False:

                Rt = random.randint(0,255)
                Gt = random.randint(0,255)
                Bt = random.randint(0,255)

                if ((Rt >= R + 30 or Rt <= R - 30) or (Gt >= G + 30 or Gt <= G - 30) or (Bt >= B + 30 or Bt <= B - 30)):
                    contrast_flag = True

            draw.text((posX, posY), text, (Rt, Gt, Bt), font=font)
            # draw.rectangle(((posX, posY), (posX + bound[0], posY + bound[1])), outline = "blue")
            continue

        verif = False
        while verif == False:


            text_size = random.randint(18, 60)
            randomFont = random.randint(0, 150)
            font = ImageFont.truetype("/home/amafla/.fonts/" + fontFiles[randomFont], text_size, encoding="unic")
            bound = font.getsize(text)
            while bound[0] > (sizeX * 3 / 4):
                text_size = random.randint(18, 60)
                randomFont = random.randint(0, 150)
                font = ImageFont.truetype("/home/amafla/.fonts/" + fontFiles[randomFont], text_size, encoding="unic")
                bound = font.getsize(text)


            # Position of X
            posX = random.randint(0, (sizeX - bound[0]))

            # Postion of Y
            posY = random.randint(0, (sizeY - bound[1]))

            for k in range(0, len(coords)):

                exist = area(coords[k], posX + bound[0], posX, posY + bound[1], posY)

                if exist != None:
                    verif = False
                    break
                if exist == None:
                    verif = True
                    continue

        coordinates = [posX, posX + bound[0], posY, posY + bound[1]]
        coords.append(coordinates)

        contrast_flag = False
        while (contrast_flag == False):

            Rt = random.randint(0,255)
            Gt = random.randint(0,255)
            Bt = random.randint(0,255)

            if ((Rt >= R + 30 or Rt <= R - 30) or (Gt >= G + 30 or Gt <= G - 30) or (Bt >= B + 30 or Bt <= B - 30)):
                contrast_flag = True

        draw.text((posX, posY), text, (Rt, Gt, Bt), font=font)
        textlist.append(text)


        # draw.rectangle(((posX, posY), (posX + bound[0], posY + bound[1])), outline = "blue")

    image.save(folder + 'synthtext' + str(i) + '.jpg')
    image = cv2.imread(folder + 'synthtext' + str(i) + '.jpg')

    root = ET.Element("annotation")
    image_name = str('synthtext' + str(i) + '.jpg')
    ET.SubElement(root, "filename").text = image_name
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(image.shape[1])
    ET.SubElement(size, "height").text = str(image.shape[0])
    ET.SubElement(size, "depth").text = str(image.shape[2])

    for m in range(0, len(textlist)):
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = textlist[m]
        xmlbbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(xmlbbox, "xmin").text = str(coords[m][0])
        ET.SubElement(xmlbbox, "ymin").text = str(coords[m][2])
        ET.SubElement(xmlbbox, "xmax").text = str(coords[m][1])
        ET.SubElement(xmlbbox, "ymax").text = str(coords[m][3])

    tree = ET.ElementTree(root)
    image_name = image_name[:-4] + ".xml"
    tree.write("/home/amafla/Documents/Python_Codes/Synth_dataset_pycharm/test_annotations/%s" % (image_name))

print("Generation of Images and Annotations Done..!")
