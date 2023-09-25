from GUI import GUI
from HAL import HAL
import time
import random
# Enter sequential code!

SPIRAL=1
BACKWARDS=2
TURN=3
FORWARD=4

state= 1
radius=0.3

def bumper_hit():
  bumper_value=HAL.getBumperData().bumper
  #print(bumper_value)
  if bumper_value == 0:
    print("izq")
    HAL.setW(1)
    HAL.setV(0)
    return "hit"
  if bumper_value == 1:
    print("centro")
    HAL.setV(-1)
    HAL.setW(0)
    return "hit"
  if bumper_value == 2:
    print("dcha")
    HAL.setV(-1)
    HAL.setW(0)
    return "hit"
  time.sleep(0.5)
  

def spiral(radius):
  bumper_value=HAL.getBumperData().state
  #print(bumper_value)
  if bumper_value == 1:
    print("ouch")
    return "turn"
  print("Spiral time yo!")
  time.sleep(1)
  #time.sleep(1)
  HAL.setV(radius)
  HAL.setW(1.5)
  time.sleep(1)
  
def backwards():
  print("Im Michael Jackson dude!")
  HAL.setV(-1)
  time.sleep(0.5)
  return "turn"
  
def turn():
  print("turn up the music!")
  HAL.setV(0)
  HAL.setW(2)
  #random numbre between 0 and 1
  time_spin= random.uniform(0.8,1.5)
  time.sleep(time_spin)
  return "forward"
  
def forward():
  print("straight and forward as it should be!")
  HAL.setV(1)
  HAL.setW(0)
  bumper_value=HAL.getBumperData().state
  #print(bumper_value)
  if bumper_value == 1:
    print("entra bumper1")
    return "spiral"
  else:
    time.sleep(7)
    return "spiral"
  
while True:
    print(state)
    if state == SPIRAL:
      radius=radius+0.1
      if spiral(radius) == "turn":
        state=TURN
        #if the vel. is too high, reset and go forward
      if radius >= 1.4:
        state=4
      
    if state == BACKWARDS:
      if backwards() == "turn":
        state=TURN
    if state == TURN:
      if turn() == "forward":
        state=FORWARD
    if state == FORWARD:
      if forward() == "spiral":
        #reset velocity
        radius=0.5
        state=SPIRAL