from flask import Flask, render_template, request, redirect, url_for
import subprocess
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import cv2
# import numpy as np
import json
import time
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup


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


def read_battery_capacity(tag):
    try:
        url = 'https://www.labdoo.org/content/tag-one-dooject?id=0000'+tag
        html = urlopen(url)
        html_soup = BeautifulSoup(html, 'html.parser')

        bat_cap = str(html_soup)[str(html_soup).find(
            'watt-hours:')+16:str(html_soup).find("watt-hours:")+20]

        if bat_cap == "Not ":
            bat_cap = "Not Available"
        else:
            bat_cap = bat_cap + " Wh"

        return bat_cap
    except Exception as e:
        logging.error("Error Reading Battery Capacity")
        logging.error(e)
        return ""


def read_save_qr_code(tag):
    try:
        qr_add = "https://api.qrserver.com/v1/create-qr-code/?"
        qr_add = qr_add+"size=180x180&data=http%3A%2F%2Fwww.labdoo.org%2Flaptop%2F0000"
        urllib.request.urlretrieve(
            qr_add+tag, "img/qr.png")
    except Exception as e:
        logging.error("Error Reading QR Code")
        logging.error(e)


def create_device_label(tag):
    try:
        filename = "img/device_tag.png"

        img = Image.new('RGB', (554, 200), color=(255, 255, 255))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((10, 70), "Device Tag ID:", font=fnt, fill=(0, 0, 0))
        d.text((10, 105), "000"+tag, font=fnt, fill=(0, 0, 0))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 14)
        d.text((10, 140), "This device has to stay at your property",
               font=fnt, fill=(0, 0, 0))
        d.text((10, 165), "or donations will stop", font=fnt, fill=(0, 0, 0))

        im_qr = Image.open('img/qr.png')
        im_logo = Image.open('logo.png')
        img.paste(im_qr, (360, 10))
        img.paste(im_logo.resize((210, 55)), (5, 5))
        img.save(filename)

        return filename
    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


def create_power_adaptor_label(tag):
    try:
        filename = "img/power_tag.png"
        img = Image.new('RGB', (554, 200), color=(255, 255, 255))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((10, 70), "Power Adap.Tag ID:", font=fnt, fill=(0, 0, 0))
        d.text((10, 105), "000"+tag, font=fnt, fill=(0, 0, 0))

        im_qr = Image.open('img/qr.png')
        im_logo = Image.open('logo.png')
        img.paste(im_qr, (360, 10))
        img.paste(im_logo.resize((210, 55)), (5, 5))
        img.save(filename)

        return filename
    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


def create_battery_label(tag, bat_cap):
    try:
        filename = "img/battery_tag.png"
        img = Image.new('RGB', (554, 200), color=(255, 255, 255))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((10, 70), "Battery Comp. ID:", font=fnt, fill=(0, 0, 0))
        d.text((10, 105), "000"+tag, font=fnt, fill=(0, 0, 0))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
        d.text((10, 140), "Battery Watt-Hours", font=fnt, fill=(0, 0, 0))
        d.text((10, 165), bat_cap, font=fnt, fill=(0, 0, 0))

        im_qr = Image.open('img/qr.png')
        im_logo = Image.open('logo.png')
        img.paste(im_qr, (360, 10))
        img.paste(im_logo.resize((210, 55)), (5, 5))
        img.save(filename)

        return filename
    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


def save_tag_images(tag):
    """
    Function to look in labdoo.org for a tag and
    create the images of the labels
    """
    read_save_qr_code(tag)
    bat_cap = read_battery_capacity(tag)

    device_img = create_device_label(tag)
    power_adaptor_img = create_power_adaptor_label(tag)
    battery_img = create_battery_label(tag, bat_cap)

    img_files = [device_img, power_adaptor_img, battery_img]
    # img_files = [device_img]

    return img_files


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
                labdoo_tags = inputs[key].split(';')
                for tag in labdoo_tags:
                    # Read the website tag and create images
                    img_files = save_tag_images(tag)
                    print(tag)

                    if not img_files:
                        continue

                    # Print the Labels
                    for img in img_files:
                        print_label(img, model, printer)

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
    print("Starting Server")
    app.run(host='0.0.0.0', port=80, debug=False)
