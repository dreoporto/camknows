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
sudo pip3 install --upgrade pip
# TODO AEO - USE PYTHON3 INSTEAD?
# python3 -m pip install pip --upgrade

echo 'CAMKNOWS SETUP: PIP3 INSTALLS'
# TODO AEO - USE REQUIREMENTS.TXT FOR PIP INSTALLS
# python3 -m pip install -r requirements.txt
# TODO AEO - USE ~ MATCHING ETC
# see https://www.piwheels.org/project/opencv-contrib-python/ for version support
sudo pip3 install opencv-contrib-python==4.5.5.62 --root-user-action=ignore
sudo pip3 install imutils --root-user-action=ignore
sudo pip3 install picamera --root-user-action=ignore
sudo pip3 install -U numpy --root-user-action=ignore
