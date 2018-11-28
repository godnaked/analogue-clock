#!/usr/bin/env python

import time
import signal
import threading
import math

from graphics import Drawing, Color
import unicornhathd as unicorn

unicorn.set_layout(unicorn.HAT)
unicorn.rotation(0)
unicorn.brightness(0.5)

print("""
Displays an analog clock which automatically dims at night.
""")

class UnicornDrawing(Drawing):
  def __init__(self):
    Drawing.__init__(self,16,16)

  def pixel(self, x, y, col):
    if x < 0 or x > 15 or y < 0 or y > 15:
      return False
    self.buffer[(x,y)] = col
    unicorn.set_pixel(x, y, col.r, col.g, col.b)

  def show(self):
    unicorn.show()

d = UnicornDrawing()

# X offset of clock centre
O_X = 7.5
# Y offset of clock centre
O_Y = 7.5
# Radius of clock
R = 7
# Rotation offset of clock, set to 0, 90, 180, 270, etc
unicorn.rotation(270)

def setBrightness(currenttime):
  currenthour = currenttime.tm_hour
  # if it's between 10 am and 8 pm,
  # use dimmer brightness
  if(currenthour < 10 or currenthour > 20):
    unicorn.brightness(0.5)
  else:
    unicorn.brightness(0.8)

def tick():
  currenttime = time.localtime()
  currenthour = currenttime.tm_hour
  currentmin  = currenttime.tm_min
  currentsec  = currenttime.tm_sec
  
  # Set seconds counter
  float_sec = (time.time() % 60) / 59.0
  seconds_progress = float_sec * 15

  # Set daytime or nighttime brightness
  setBrightness(currenttime)
  d.clear()
  
  # Draw the circle around the clock
  d.circle(O_X,O_Y,R,Color(22,0,22))
  if int(time.time()) % 2 == 0:
    d.circle(O_X,O_Y,R,Color(22,22,22))
  d.circle(O_X,O_Y,R+1,Color(22,0,22))
  d.circle(O_X,O_Y,R+2,Color(22,0,22))
  d.circle(O_X,O_Y,R+3,Color(22,0,22))
  unicorn.set_pixel(1, 1, 22, 0, 22)
  unicorn.set_pixel(1, 13, 22, 0, 22)
  unicorn.set_pixel(13, 13, 22, 0, 22)
  unicorn.set_pixel(13, 1, 22, 0, 22)

  # Draw the clock hands
  d.circle_line(O_X,O_Y,R,(360.0*(currentmin/60.0)), Color(152,83,80))
  d.circle_line(O_X,O_Y,R-2,(360.0*((currenthour % 12)/12.0)),Color(122,0,122))
  
  # Display seconds progress by blinking dot
  if int(time.time()) % 2 == 0:
    unicorn.set_pixel(math.floor(seconds_progress), 0, 81, 81, 82)
  
  # draw buffer to hardware
  d.show()

  threading.Timer(1,tick).start()

tick()