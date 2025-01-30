from PIL import Image


def decode(image):
    data = ""
    imgdata = iter(image.getdata())

    while True:
        pixels = [
            value
            for value in imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
            + imgdata.__next__()[:3]
        ]
        binstr = ""
        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += "0"
            else:
                binstr += "1"

        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data
