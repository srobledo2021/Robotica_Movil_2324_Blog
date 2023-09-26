# Robótica Móvil 

## Sergio Robledo Sarrión
#
#
#
# Introduction
Our first practise consists on designing a vacuum cleaner. We will make a FSM(Finite State Machine) to split the code into different states.

This is our FSM:


(Made with: [draw.io](https://app.diagrams.net/) )

# Steps

First of all we have solved the problem with those four states using a while loop, so that the code works at a certain frecuency. Every time the while loop iterates, it evaluates whether the state of the code is forward, backward, spiral or turn, and then effectuates as so. Those states are constantly changing and can interact with each other in order to achieve the behavior we want for our vacuum cleaner.

```python
from GUI import GUI
from HAL import HAL
import time
import random

SPIRAL=1
BACKWARDS=2
TURN=3
FORWARD=4

state= 1
radius=0.3

#check if the vacuum cleaner crashed a wall
def bumper_hit():
  bumper_state=HAL.getBumperData().state
  if bumper_state == 1:
    bumper_value=HAL.getBumperData().bumper
    HAL.setV(0)
    if bumper_value == 0:
      print("izq")
      HAL.setW(1)
      return "hit"
    if bumper_value == 1:
      print("centro")
      HAL.setW(2)
      return "hit"
    if bumper_value == 2:
      print("dcha")
      HAL.setW(-1)
      return "hit"
  
#spiral state
def spiral(radius):
  var=bumper_hit()
  if var=="hit":
    HAL.setV(0)
    HAL.setW(0)
    return "back"
  time.sleep(1)
  HAL.setV(radius)
  HAL.setW(1.5)
  time.sleep(1)

#backwards state
def backwards():
  HAL.setV(-1)
  time.sleep(0.5)
  return "turn"
  
#turn state
def turn():
  HAL.setV(0)
  HAL.setW(2)
  time_spin= random.uniform(0.8,1.5)
  time.sleep(time_spin)
  return "forward"

#forward state
def forward():
  print("straight and forward as it should be!")
  HAL.setV(1)
  HAL.setW(0)
  var=bumper_hit()
  if var=="hit":
    HAL.setV(0)
    HAL.setW(0)
    return "back"
  else:
    time.sleep(7)
    return "spiral"
  
while True:

    if state == SPIRAL:
      radius=radius+0.1
      if spiral(radius) == "turn":
        state=TURN
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
        radius=0.5
        state=SPIRAL
      elif forward() == "back":
        state=BACKWARDS
    

```
There are several things that we need to point out in our code, the first thing is the variables assignment:
```python
SPIRAL=1
BACKWARDS=2
TURN=3
FORWARD=4
```
In this way, we will be able to call any state by its name instead of the number that represents it. For instance, we can see the way it is implemented in this snippet:

```python
if state == FORWARD:
      if forward() == "spiral":
        radius=0.5
        state=SPIRAL
      elif forward() == "back":
        state=BACKWARDS
```
Here, it is clear that the state we are in is the "FORWARD" state, and while iterating in that state, if the function returns "spiral", the state changes to SPIRAL and so does it to BACKWARDS when returnning "back".

The function "bumper_hit()" simply checks if the vacuum cleaner bumped into something and where was it.

When the code is running and we take an example map, after a few minutes, we obtain this percentage of the whole house floor covered:

![Screenshot from 2023-09-24 20-06-14](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/0a82fc8b-8b5b-4c18-9751-6a0ac9416071)

- On our second step we needed to get rid of the  "time.sleep()" function calls, due to the fact that can cause several problems in our code, as it is a non-stopping loop operating without stopping. That is why the only thing could use is "time.time()" to get to know the actual time and be able to compare it with the same function call but at any other time.

We could change the spiral by deleting the time.sleep(), but this time we needed to calculate again the spiral with brand-new measurements.


```python3
from GUI import GUI
from HAL import HAL
import time
import random

time_var=time.time()
#States:
SPIRAL=1
BACKWARDS=2
TURN=3
FORWARD=4
#initial state
state= SPIRAL
radius=0.01

def chrono(start,finish,time_reachable):
  duration=finish-start
  if duration >= time_reachable:
    return 1
  else:
    return 0

def bumper_hit():
  bumper_state=HAL.getBumperData().state
  if bumper_state == 1:
    return "hit"

def spiral(radius):
  print("spiral")
  #if the robot hitted a wall, then stop and turn back
  if bumper_hit()=="hit":
    HAL.setV(0)
    HAL.setW(0)
    #print("ouch")
    return "back"
  #time.sleep(1)
  HAL.setV(radius)
  HAL.setW(1)
  
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
  HAL.setV(0)
  HAL.setW(2)
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
    print("estado: "+str(state))
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
    
```


![Captura de pantalla 2023-09-25 200056](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/943d7b2b-8798-43d1-b148-497dc2fe392e)


![Captura desde 2023-09-26 09-53-29](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/bf2918cd-039d-4276-83d8-8c63ea580ddb)

