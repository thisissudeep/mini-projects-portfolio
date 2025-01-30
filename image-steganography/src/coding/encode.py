from PIL import Image
import os
from tkinter import messagebox
from io import BytesIO


class Encoder:
    def __init__(self):
        self.output_image_size = 0
        self.o_image_w = 0
        self.o_image_h = 0
        self.d_image_size = 0
        self.d_image_w = 0
        self.d_image_h = 0

    def genData(self, data):
        newd = []
        for i in data:
            newd.append(format(ord(i), "08b"))
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pix = [
                value
                for value in imdata.__next__()[:3]
                + imdata.__next__()[:3]
                + imdata.__next__()[:3]
            ]

            for j in range(0, 8):
                if (datalist[i][j] == "0") and (pix[j] % 2 != 0):
                    if pix[j] % 2 != 0:
                        pix[j] -= 1
                elif (datalist[i][j] == "1") and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if i == lendata - 1:
                if pix[-1] % 2 == 0:
                    pix[-1] -= 1
            else:
                if pix[-1] % 2 != 0:
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1
