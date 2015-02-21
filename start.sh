#!/bin/bash

cd /usr/src/mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www -p 8083" -i "input_raspicam.so -x 640 -y 480 -fps 15 -ex night" &

cd /home/pi/workspace/dum.bot
sudo python webdumbot.py &