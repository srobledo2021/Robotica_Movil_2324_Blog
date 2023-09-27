from GUI import GUI
from HAL import HAL
import time
import random

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
izq = 0
dcha = 0

#bumper funtion, returns run if bumper got hit
#updates global variables for position of the bump
def bumper_hit():
  bumper_state=HAL.getBumperData().state
  if bumper_state == 1:
    bumper_location=HAL.getBumperData().bumper
    if bumper_location==0:
      global izq
      izq=izq+1
    if bumper_location==2:
      global dcha
      dcha=dcha+1
    return "hit"

#create a spiral
def spiral(radius):
  HAL.setV(radius)
  HAL.setW(1)
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="hit":
    HAL.setW(0)
    HAL.setV(0)
    #print("ouch")
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
def turn(left,right):
  #turn right if bumped on left
  if left == 1:
    HAL.setW(2)
  #turn left if bumped on right
  if right == 1:
    HAL.setW(-2)
  #if got hit in the centre, make a random turn
  if (right == 0) and (left == 0):
      HAL.setW(2)
  HAL.setV(0)
  #random number
  time_spin= random.uniform(0.8,1.5)
  time_end=time.time()
  #reset global variables
  global izq
  global dcha
  izq=0
  dcha=0
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
    #print("ouch")
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
      if turn(izq,dcha) == "forward":
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
