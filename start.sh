#!/bin/bash

cd /usr/src/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www -p 8083" -i "input_raspicam.so -x 1280 -y 1024 -fps 20 -ex night" &

cd /home/pi/workspace/dum.bot
sudo python webdumbot.py &

sudo modprobe -r i2c_bcm2708 && sudo modprobe i2c_bcm2708 baudrate=200000
