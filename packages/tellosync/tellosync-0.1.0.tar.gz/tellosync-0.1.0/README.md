# tellosync 
[![version info](https://img.shields.io/pypi/pyversions/tellosync.svg)](https://pypi.org/project/tellosync/)
[![liscence](https://img.shields.io/pypi/l/tellosync.svg)](https://pypi.org/project/tellosync/)
[![PyPI](https://img.shields.io/pypi/v/tellosync.svg)](https://pypi.org/project/tellosync/)

**tellosync** is a Python library created to provide users with a simple way to interface and send commands to the DJI Tello drone, as well as to simply and easily teach students how to control the drone using Python 3. All the commands outlined in the DJI Tello SDK 1.3.0.0 are present in this library.
This library is based off of easyTello. tellosync is meant to add the ability to sync multiple computers using Arduinos. Each computer that is communicating with a drone is connected to an Arduino which then syncs with the Arduinos of other drones. This is a work in  progress as of 6/28/2023 and is mostly for the sake of learning. 

## Installation
To install the library, simply run:
```
pip install tellosync 
```
or to install from cloned source:
```
$ git clone https://github.com/vwu1888/easyTello
$ cd easyTello
$ python setup.py install
```
**Note:** tellosync requires OpenCV-Python and pySerial. These should automatically install with tellosync, however, you can manually install it by running:
```
pip install opencv-python

pip install pyserial
```
For more information on OpenCV-Python click [here](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html).

For more information on pySerial click [here](https://pyserial.readthedocs.io/en/latest/index.html#).

## Examples
Creating a drone object in Python:
```python
from easytello import tello

my_drone = tello.Tello()
```
Programming the drone to takeoff, fly in a square and then land:
```python
my_drone.takeoff()

for i in range(4):
	my_drone.forward(100)
	my_drone.cw(90)
	
my_drone.land()
```
Toggling state of video stream:
```python
# Turning on stream
my_drone.streamon()
# Turning off stream
my_drone.streamoff()
```
