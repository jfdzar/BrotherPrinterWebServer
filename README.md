# BrotherPrinterWebServer
Small Webserver with Python and flask to run the QL-500 in a Raspberry Pi

- Upload a foto, process it and print it
- Print a random tag
- Print Labdoo Tags 

# Installation

## Linux

The easiest way is to install it using virtualenv
First of all install Python, I used version 3.7.3 any 3.7+ should work
Once install, instal the virtualenv library

```bash
pip install virtualenv
```

then clone the repository

```bash
git clone https://github.com/jfdzar/BrotherPrinterWebServer.git
```

Once cloned navigate to the folder and run 

```bash
virtualenv BrotherPrinterWebServer/
```

navigate to BrotherPrinterWebServer/bin and run the command

```bash
cd BrotherPrinterWebServer/bin
source activate
```

You are know in the virtual enviroment, all the libraries installed will only be installed in this instance
Then next step would be to install all the libraries from  requirements.txt

```bash
cd ..
pip install -r requirements.txt
```

Once everything installed run 

```bash
python BrotherPrinterWebServer.py
```

In your Browser navigate to http://localhost:8080/ and the website should appear


In Linux you will have to extra add your user to lp group to give access to the printer

```bash
sudo adduser YOURUSER lp
```

Additionally you main need to install extra dependencies to work with the OpenCV library. It is just used for the image processing of the foto function. You just need to execute following:

```bash
pip3 install opencv-contrib-python; sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test
```


## Windows

Similar instructions, pay attention to the slash direction / \

```bash
pip install virtualenv
```

then clone the repository

```bash
git clone https://github.com/jfdzar/BrotherPrinterWebServer.git
```

Once cloned navigate to the folder and run 

```bash
python -m venv BrotherPrinterWebServer
```

navigate to BrotherPrinterWebServer/Script

```bash
cd BrotherPrinterWebServer/Script
activate
```

You are know in the virtual enviroment, all the libraries installed will only be installed in this instance
Then next step would be to install all the libraries from  requirements.txt

```bash
cd ..
pip install -r requirements.txt
```

Once everything installed run 

```bash
python BrotherPrinterWebServer.py
```

In your Browser navigate to http://localhost:8080/ and the website should appear

For Windows extra steps need to be taken
Download [libusb-win32-devel-filter-1.2.6.0.exe](https://sourceforge.net/projects/libusb-win32/files/libusb-win32-releases/1.2.6.0/) from sourceforge and install it.
After installing, you have to use the "Filter Wizard" to setup a "device filter" for the label printer.

# Usage

To use it just modify the config.json file with your printer information and label size

then navigate to your installation and activate the virtual environment and run the script

```bash
cd ~/BrotherPrinterWebServer/bin
source activate
python BrotherPrinterWebServer.py
```







