from flask import Flask, render_template, request, redirect, url_for
import subprocess
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import cv2
# import numpy as np


app = Flask(__name__)


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


def create_photo_label(file):
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


def create_txt_label(text):
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    inputs = request.form.to_dict()
    no_copies = 1

    for key in inputs:

        # If a single tag is written print single tag
        if key == 'stag':
            if inputs[key] != "":
                print("Printing Single Tag: ", inputs[key])
                img_file = create_txt_label(inputs[key])
                model = "QL-500"
                printer = "/dev/usb/lp0"
                print_label(img_file, model, printer)
        
        # If several labdoo tags are passed then print them
        if key == 'tags':
            if inputs[key] != "":
                print("Printing Labdoo Tags: ", inputs[key])

        if key == 'copies':
            if inputs[key] != "":
                no_copies = int(inputs[key])
                print(no_copies)

    # If File is uploaded print the Foto
    if uploaded_file.filename != '':

        uploaded_file.save(uploaded_file.filename)
        img_file = create_photo_label(uploaded_file.filename)
        model = "QL-500"
        printer = "/dev/usb/lp0"
        for i in range(0, no_copies):
            print_label(img_file, model, printer)

        os.remove(uploaded_file.filename)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
