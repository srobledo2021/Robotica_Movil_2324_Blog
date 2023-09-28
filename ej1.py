from GUI import GUI
from HAL import HAL
import time
import random
import math

#States:
SPIRAL=1
BACKWARDS=2
TURN=3
FORWARD=4

#initial state
state= SPIRAL

#initial radius to increase
radius=0.01

#global variables for bumper
left = 0
right = 0

#introduce laser data in an array
def parse_laser_data(laser_data):
    laser = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i)
        laser += [(dist, angle)]
    return laser

#introduce laser data and compare distance
def laser_detect(laser):
  for i in range(0, 180, 30):
    if i == 180:
      i = 179
    if laser[i][0] < 0.5:
        return 0

#bumper funtion, returns run if bumper got hit
#updates global variables for position of the bump
def bumper_hit():
  bumper_state=HAL.getBumperData().state
  if bumper_state == 1:
    bumper_location=HAL.getBumperData().bumper
    if bumper_location==0:
      global left
      left=left+1
    if bumper_location==2:
      global right
      right=right+1
    return "hit"

#create a spiral
def spiral(radius):
  HAL.setV(radius)
  HAL.setW(1)
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="hit":
    HAL.setW(0)
    HAL.setV(0)
    return "back"

#go back for half a second
def backwards():
  HAL.setV(-1)
  time_end=time.time()
  if time_end- time_var >= 0.5:
    return "turn"
  else:
    return "backwards"
  
#turn depending on where
#the bumper got hit a random amount of time
def turn(left_,right_):
  #turn right if bumped on left
  if left_ == 1:
    HAL.setW(2)
  #turn left if bumped on right
  if right_ == 1:
    HAL.setW(-2)
  #if got hit in the centre, make a random turn
  if (right_ == 0) and (left_ == 0):
      HAL.setW(2)
  HAL.setV(0)
  #random number
  time_spin= random.uniform(0.8,1.5)
  time_end=time.time()
  #reset global variables
  global left
  global right
  left=0
  right=0
  if time_end- time_var >= time_spin:
    #reset of bumper
    return "forward"
  else:
    return "turn"

#move forward
def forward():
  HAL.setV(1)
  HAL.setW(0)
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="hit":
    HAL.setW(0)
    HAL.setV(0)
    return "back"
  #at a random moment, do a spiral
  random_num=random.randint(1,300)
  if random_num== 5:
    return "spiral"
  
while True:
    #SPIRAL STATE
    if state == SPIRAL:
      if spiral(radius) == "back":
        state=BACKWARDS
        #update global time variable
        time_var=time.time()
      #if the vel. is too high, reset and go forward
      if radius >= 2.5:
        state=4
      #----------
      #get laser data
      laser_data = HAL.getLaserData()
      #if it is to close to a wall, reduce vel, and go straight
      if (laser_detect(parse_laser_data(laser_data)) == 0):
        state =4
      #----------
      #wider spiral while iterating
      radius=radius+0.01
    #BACKWARDS STATE
    if state == BACKWARDS:
      if backwards() == "turn":
        state=TURN
        #update global time variable
        time_var=time.time()
    #TURN STATE
    if state == TURN:
      if turn(left,right) == "forward":
        state=FORWARD
    #FORWARD STATE
    if state == FORWARD:
      if forward() == "back":
        state=BACKWARDS
        #update global time variable
        time_var=time.time()
      #random spiral event
      if forward() == "spiral":
        radius=0.1
        state=SPIRAL
