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
radius=0.01


def bumper_hit():
  bumper_state=HAL.getBumperData().state
  if bumper_state == 1:
    bumper_location=HAL.getBumperData().bumper
    if bumper_location==0:
      return "izq"
    if bumper_location==2:
      return "dcha"

def spiral(radius):
  print("spiral")
  HAL.setV(radius)
  HAL.setW(1)
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="izq":
    HAL.setW(2)
    HAL.setV(0)
    return "back"
  if bumper_hit()=="dcha":
    HAL.setW(-2)
    HAL.setV(0)
    return "back"
  else:
    HAL.setW(0)
    HAL.setV(0)
    #print("ouch")
    return "back"

  
def backwards():
  print("Im Michael Jackson dude!")
  HAL.setV(-1)
  time_end=time.time()
  if time_end- time_var >= 0.5:
    return "turn"
  else:
    return "backwards"
  #time.sleep(0.5)
  #return "turn"
  
def turn():
  print("turn up the music!")
  #  if izq == 1:
      HAL.setW(2)
  #  if dcha == 1:
  #    HAL.setW(-2)
  #  else:
  #    HAL.setW(0)
  HAL.setV(0)
  #random numbre between 0 and 1
  time_spin= random.uniform(0.8,1.5)
  #time.sleep(time_spin)
  time_end=time.time()
  if time_end- time_var >= time_spin:
    return "forward"
  else:
    return "turn"
  
def forward():
  print("straight and forward as it should be!")
  HAL.setV(1)
  HAL.setW(0)
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="izq":
    HAL.setW(2)
    HAL.setV(0)
    return "back"
  if bumper_hit()=="dcha":
    HAL.setW(-2)
    HAL.setV(0)
    return "back"
  else:
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
      if turn() == "forward":
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