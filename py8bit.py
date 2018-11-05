import numpy as np
import cv2
from PIL import Image
import json
from tkinter.ttk import Progressbar
import tkinter as tk

COLORS = [ [ 0.0 for y in range( 3 ) ] for x in range( 256 ) ]
MAX = 255.0+1

SCALE_8 = 8-1
SCALE_4 = 4-1
OFFSET_8 = MAX/SCALE_8
OFFSET_4 = MAX/SCALE_4

def bit_effect(IMAGE,scale,root):



    img =  cv2.imread(IMAGE)
    new_width  = img.shape[0]
    new_height = img.shape[1]

    # 1) scale smaller
    new_size = (int(new_width * scale), int(new_height * scale))
    print("scale " + str(scale) + " new size " +str(new_size) )
    img = cv2.resize(img, new_size, interpolation = cv2.INTER_LINEAR  ) # done wrong on purpose

    # 2) 8 bit color
    img = color_reduction(img,root)

    # 3) scale real size
    img = cv2.resize(img, ( new_height , new_width), interpolation =cv2.INTER_AREA ) # done wrong on purpose
    img = Image.fromarray(img, 'RGB')
    #img.save(IMAGE + ' A my.png')
    return img

# fill COLORS with the 8 bit colors from a json file
def load_from_json():
    with open('colors/colors.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    for i in range(len(COLORS)) :
        COLORS[i][0] =  data[i]['rgb']['r']
        COLORS[i][1] =  data[i]['rgb']['g']
        COLORS[i][2] =  data[i]['rgb']['b']

# subsitute for every pixel the closest 8 bit color
def color_reduction(img,root):
    print(img)

    w = tk.Label(root, text="Loading...")
    w.pack()
    p = Progressbar(root, length=100, mode="determinate", takefocus=True, maximum=img.shape[0])
    p.pack()

    #side effect on COLORS
    load_from_json()

    print(img.size)
    for i in range(img.shape[0]): # size or shape if cv2
        for j in range(img.shape[1]):

            min = 255.0
            index = -1
            for k in range(len(COLORS)):

                dist = np.linalg.norm(img[i][j] - COLORS[k])
                if (dist < min):
                    min = dist
                    index = k
            # should use this if this is the last function called
            img[i][j][0] = COLORS[index][2]
            img[i][j][1] = COLORS[index][1]
            img[i][j][2] = COLORS[index][0]

        p.step()
        root.update()
        print(str(i) + " / " + str(img.shape[0]))

    p.destroy()
    w.destroy()

    return img
