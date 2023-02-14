# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /BrotherPrinterWebServer

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "BrotherPrinterWebServer.py"]