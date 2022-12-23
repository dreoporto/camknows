#!/bin/bash

echo 'CAMKNOWS SETUP: RUNNING APT-GET UPDATE'
sudo apt-get update

echo 'CAMKNOWS SETUP: INSTALLING LIBRARIES'
sudo apt-get install -y libhdf5-dev libhdf5-serial-dev libhdf5-103

sudo apt-get install -y python3-pyqt5

sudo apt-get install -y libatlas-base-dev

sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev

sudo apt-get install -y libilmbase25

sudo apt-get install -y libopenexr-dev

# PIP SETUPS

echo 'CAMKNOWS SETUP: INSTALLING PIP3'
sudo apt-get install -y python3-pip

echo 'CAMKNOWS SETUP: REQUIREMENTS.TXT'
python3 -m pip install pip --upgrade
python3 -m pip install -r requirements.txt
