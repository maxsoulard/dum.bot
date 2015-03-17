#!/bin/bash

echo "Updating..."
sudo apt-get update
sudo apt-get upgrade

echo "Installing python..."
sudo apt-get install python python-dev
python get-pip.py
echo "Installing cherrypy..."
pip install cherrypy

echo "Installing Rpio.Gpio..."
sudo apt-get install python-rpi.gpio subversion

echo "Installing Mjpg-streamer..."
cd /home/pi
svn co https://mjpg-streamer.svn.sourceforge.net/svnroot/mjpg-streamer mjpg-streamer
cd mjpg-streamer/mjpg-streamer
make

echo "Installing and configuring I2C..."
sudo apt-get install python-smbus i2c-tools


sudo apt-get install raspi-config
echo "Please enable pi camera module and I2C support, then reboot."
sudo raspi-config

sudo reboot
