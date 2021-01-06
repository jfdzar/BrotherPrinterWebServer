import subprocess
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np


def print_label(img_file, model, printer):
    """
    Given a image file print the label
    """
    bashCommand = "brother_ql -m "+model+" -p "+printer+" print -l 50 "+img_file
    process = subprocess.Popen(
        bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    logging.info(output.decode('utf-8'))
    logging.error(error.decode('utf-8'))


def create_label(text):
    try:
        filename = "label.png"
        img = Image.new('RGB', (554, 100), color=(255, 255, 255))

        font_size = 70
        if len(text) > 13:
            font_size = 35

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', font_size)
        d = ImageDraw.Draw(img)
        d.text((10, 10), text, font=fnt, fill=(0, 0, 0))

        img.save(filename)
        return filename

    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


if __name__ == "__main__":

    ls_label = []
    with open('labels.txt', 'r') as f:
        ls_label = f.readlines()

    for text in ls_label:
        img_file = create_label(text)
        model = "QL-500"
        printer = "/dev/usb/lp0"
        print_label(img_file, model, printer)

    os.remove(img_file)
