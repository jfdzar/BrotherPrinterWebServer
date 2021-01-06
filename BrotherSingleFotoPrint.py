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


def create_label(file):
    """
    Given the full path a an image
    Resize it and convert it to black and white
    """

    # Base width of the label
    basewidth = 554

    # Opens a image in RGB mode
    img = Image.open(file)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))

    # Resize it to match label length
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img_file = "last_print.jpg"
    img.save(img_file)
    # Convert it to Black and White
    # img = img.convert('1')

    # reading image
    img = cv2.imread(img_file)

    # Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)

    cv2.imwrite(img_file, edges)
    # Save the new image to print file

    return img_file


if __name__ == "__main__":

    img_filename = "single_foto.jpg"

    for i in range(0, 4):
        img_file = create_label(img_filename)
        model = "QL-500"
        printer = "/dev/usb/lp0"
        print_label(img_file, model, printer)
