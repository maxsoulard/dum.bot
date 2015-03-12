#!/bin/bash

cd /usr/src/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www -p 8083" -i "input_raspicam.so -x 640 -y 480 -fps 20 -ex night" &

sudo modprobe -r i2c_bcm2708 && sudo modprobe i2c_bcm2708 baudrate=200000

cd /home/pi/workspace/dum.bot
sudo nice -10 python webdumbot.py &

