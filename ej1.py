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

#check if the vacuum cleaner bumped
def bumper_hit():
  bumper_state=HAL.getBumperData().state
  if bumper_state == 1:
    return "hit"

def spiral(radius):
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="hit":
    HAL.setV(0)
    HAL.setW(0)
    return "back"
  HAL.setV(radius)
  HAL.setW(1)
  
def backwards():
  HAL.setV(-1)
  time_end=time.time()
  if time_end- time_var >= 0.5:
    return "turn"
  else:
    return "backwards"
  
def turn():
  print("turn up the music!")
  HAL.setV(0)
  HAL.setW(2)
  #random numbre between 0.8 and 1.5
  time_spin= random.uniform(0.8,1.5)
  time_end=time.time()
  if time_end- time_var >= time_spin:
    return "forward"
  else:
    return "turn"
  
def forward():
  print("straight and forward as it should be!")
  HAL.setV(1)
  HAL.setW(0)
  if bumper_hit()=="hit":
    HAL.setV(0)
    HAL.setW(0)
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
        #update time variable
        time_var=time.time()
      #if the vel. is too high, reset and go forward
      if radius >= 2.5:
        state=FORWARD
      #wider spiral while iterating
      radius=radius+0.01
      
    #BACKWARDS STATE
    if state == BACKWARDS:
      if backwards() == "turn":
        state=TURN
        #update time variable
        time_var=time.time()
        
    #TURN STATE
    if state == TURN:
      if turn() == "forward":
        state=FORWARD

    #FORWARD STATE
    if state == FORWARD:
      if forward() == "back":
        state=BACKWARDS
        #update time variable
        time_var=time.time()
      #random spiral event
      if forward() == "spiral":
        radius=0.1
        state=SPIRAL
    
    
