from PIL import Image
from classify import *

import cv2 as cv
import os


def neuralEngine(filename):
    try:
        results = []
        latin = 0
        cyrillic = 0
        none = 0

        number = cutout.cutout(filename)

        for i in range(number):
            print('Image {}/{}'.format(i, number))
            results.append(classify(str(i) + '_' + filename))

        for image in range(number):
            for position in range(3):
                if results[image][position][0] == 'cyrylica po segregacji':
                    cyrillic += results[image][position][1]
                elif results[image][position][0] == 'lacina po segregacji':
                    latin += results[image][position][1]
                elif results[image][position][0] == 'zaden jezyk':
                    none += results[image][position][1]

        latin_percentage = round(latin * 100 / number, 2)
        cyrillic_percentage = round(cyrillic * 100 / number, 2)
        none_percentage = round(none * 100 / number, 2)

        final = 'Cyrillic = {}%, Latin = {}%, None = {}%'.format(str(cyrillic_percentage), str(latin_percentage),
                                                                 str(none_percentage))
        return final
    except:
        results = []
        latin = 0
        cyrillic = 0
        none = 0
        img = cv.imread('static/img/' + filename)
        cv.imwrite('static/img/marked' + filename, img)
        number = 1
        results.append(classify(filename))

        for image in range(number):
            for position in range(3):
                if results[image][position][0] == 'cyrylica po segregacji':
                    cyrillic += results[image][position][1]
                elif results[image][position][0] == 'lacina po segregacji':
                    latin += results[image][position][1]
                elif results[image][position][0] == 'zaden jezyk':
                    none += results[image][position][1]

        latin_percentage = round(latin * 100 / number, 2)
        cyrillic_percentage = round(cyrillic * 100 / number, 2)
        none_percentage = round(none * 100 / number, 2)

        final = 'Cyrillic = {}, Latin = {}, None = {}'.format(str(cyrillic_percentage), str(latin_percentage),
                                                              str(none_percentage))
        return final
