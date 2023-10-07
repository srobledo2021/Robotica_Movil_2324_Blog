
# Index
- [Exercise 1: Vacuum Cleaner](#Vacuum-cleaner)
  - [Introduction](#Introduction)
  - [API](#API)
  - [Steps](#Steps)
  - [Final Code](#Final-code)
- [Exercise 2: F1 Follow Line](#Follow-Line)
  - [Introduction](#Introduction-2)
  - [API](#API-2)
  - [Steps](#Steps-2)

----------------------------------------------------------------------------------
# Vacuum cleaner

### Introduction
Our first practise consists on designing a vacuum cleaner. We will make a FSM(Finite State Machine) to split the code into different states.

This is our FSM:

![gg](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/dfd4db8c-0bae-4da3-8a47-569c797e4ab2)


(Made with: [draw.io](https://app.diagrams.net/) )
### API
- from HAL import HAL - to import the HAL(Hardware Abstraction Layer) library class. This class contains the functions that sends and receives information to and from the Hardware(Gazebo).
- from GUI import GUI - to import the GUI(Graphical User Interface) library class. This class contains the functions used to view the debugging information, like image widgets.
- HAL.getBumperData().state - To establish if the robot has crashed or not. Returns a 1 if the robot collides and a 0 if it has not crashed.
- HAL.getBumperData().bumper - If the robot has crashed, it turns to 1 when the crash occurs at the center of the robot, 0 when it occurs at its left and 2 if the collision is at its right.
- HAL.setV() - to set the linear speed
- HAL.setW() - to set the angular velocity
- HAL.getLaserData() - It allows to obtain the data of the laser sensor, which consists of 180 pairs of values ​​(0-180º, distance in millimeters).

### Steps

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

----------------------------------------------------------------------------------------------------------------

- On our second step we needed to get rid of the  "time.sleep()" function calls, due to the fact that can cause several problems to our code. As it is a non-stopping loop, when time.sleep() is done, we loose the whole control of the system and no matter what happens to our robot, that we cannot respond. That is why the only thing could use is "time.time()" to get to know the actual time and be able to compare it with the same function call but at any other time.

We could change the spiral by deleting the time.sleep(), but this time we needed to calculate again the spiral with brand-new measurements.


```python3
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
    
    
```
Here, we measure the time just before entering into a function so that then when we enter and measure it again, we can take that amount of time that passed between one and another time.time() and use it for several things. Example:

We are going forward and suddenly bump into a wall, our function returns "back" and we change our state so that next time iterating, the new state will be "BACKWARDS". Just before that, we measure the time in the variable "time_var".
```python
#FORWARD STATE
    if state == FORWARD:
      if forward() == "back":
        state=BACKWARDS
        #update time variable
        time_var=time.time()
```
Then we access the function backwards(), in which we find another measuring of time but this time in the variable time_end().
```python
def backwards():
  HAL.setV(-1)
  time_end=time.time()
  if time_end- time_var >= 0.5:
    return "turn"
  else:
    return "backwards"
```
By comparing those 2 variables, we can predict the time that passed between them and then operate like in this case, where we want to wait for half a second.


- When running the code several times, we realize that even though the vacuum cleaner covers almost the whole map for not so long, it passes through some places over and over. That is why the function bumper_hit() has been expanded so that when the bumper of the robot crashes, the performance is quite different. When it crashes on the left side, the robot stops, gets back and turns right. Same thing for the right side but to the right.

We add global variables for the left and right:
```python
#global variables for bumper
left = 0
right = 0
```
In the bumper_hit() function, we update them when necessary
```python
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
```
So that then we can make the vacuum cleaner act different in the 'turn' function() depending on those variables. After that, we need to reinitialize them to iterate again:
```python
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
```
- In the end, as the practise characteristics have been modified throughout the days, there has been made a major change related to laser. Reading the API of the robot, there is an example of the laser performance, which is this one:
```python
#introduce laser data in an array
def parse_laser_data(laser_data):
    laser = []
    for i in range(180):
        dist = laser_data.values[i]
        angle = math.radians(i)
        laser += [(dist, angle)]
    return laser
```
The way it works is pretty simple ,it estimates values and keeps them in the 'laser' array. Those values are angles and distances. That is why we have implemented an update to our code which consists on a different behavior when going on a spiral. The way it worked before, was that whenever the spiral velocity was too high, the vacuum cleaner changed to the FORWARD state. Now it is still working that way, but we have included another behavior. Whenever the robot is doing a spiral, if de distance between the robot and a wall is less than 0.5 meters, it will automatically change to FORWARD state too.
```python
#introduce laser data and compare distance
def laser_detect(laser):
  for i in range(0, 180, 30):
    if i == 180:
      i = 179
    if laser[i][0] < 0.5:
        return 0
```
The condition is written in this part of the code (spiral state):
```python
#get laser data
      laser_data = HAL.getLaserData()
      #if it is to close to a wall, reduce vel, and go straight
      if (laser_detect(parse_laser_data(laser_data)) == 0):
        state =4
```


- Overall, here is the final code:
----------------------------------------------------------------------------------------------------------------------------------------------------------------
### Final code

```python
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
```
Here is a little test of the vacuum cleaner after a couple of minutes performing the last code:

![Sin título](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/37cd7758-ae61-4e82-aa57-8f829c464b0e)

Here is a video showing the behavior:
![Video](./source/Test1.mp4)

Here is a little demo video at x2.00 speed(that can be seen online):

https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/f789a1ca-2fea-4c6b-b480-fd62ae38afaa

-----------------------------------------------------------------------------------------------------------------------------------

# Follow Line


### Introduction 2
The goal of this exercise is to perform a PID reactive control capable of following the line painted on the racing circuit.

### API 2

- from HAL import HAL - to import the HAL(Hardware Abstraction Layer) library class. This class contains the functions that sends and receives information to and from the Hardware(Gazebo).
- from GUI import GUI - to import the GUI(Graphical User Interface) library class. This class contains the functions used to view the debugging information, like image widgets.
- HAL.getImage() - to get the image
- HAL.setV() - to set the linear speed
- HAL.setW() - to set the angular velocity
- GUI.showImage() - allows you to view a debug image or with relevant information

### Steps 2

First of all, we need to implement OpenCV and Python Color Detection, so that we can constantly get the POV of the car. After that we need to apply a mask to the image to get the red color of the line needed to be followed. Our first code implementation was this one:

```python
from GUI import GUI
from HAL import HAL
import numpy as np
import cv2

while True:
    #get raw image
    image=HAL.getImage()
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    #define color thresholds
    lower_tresh = np.array([0,100,100])
    upper_tresh =np.array([10,255,255])
    #a mask is created which identifies pixels in this color range
    mask =cv2.inRange(hsv, lower_tresh,upper_tresh)
    cv2.imshow("mask",mask)
   
```
The main purpose of this code is to segment an image based on a color range in the HSV (Hue, Saturation, Value) color space.
'lower_tresh and upper_tresh are a NumPy array that define the lower limit of the color range you want to detect. In this case, it's looking for red. But we can detect any colour we want with this method.

![image](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/3ae4cd3d-a443-41b0-b4b4-a207d187d3f2)

 In this line:
```python3
mask =cv2.inRange(hsv, lower_tresh,upper_tresh)
```
 a mask is created that identifies the pixels in the original image that fall within the color range defined by lower_thresh and upper_thresh. The resulting mask will be a binary image in black and white, where pixels falling within the color range will be white (255), and those outside the range will be black (0).

After that we wanted an indicator so that we can know whether the car is following the line or not and how is it going to do that. That is why, we added this part of the program:
```python3
 M = cv2.moments(mask)

    if M['m00'] > 0:
      #centroids of X and Y
      cx = int(M['m10'] / M['m00'])
      cy = int(M['m01'] / M['m00'])
      cv2.circle(image, (cx, cy), 20, (0, 0, 255), -1)
```
The 'moments' function from OpenCV is used to calculate the moments of the binary image (the mask we added). Moments are statistical descriptors used to characterize a distribution of pixels in an image. In this case, the moments of the mask 'mask' are being calculated.

For 'cx' and 'cy', which are the coordinates of the center of mass (centroid) of the object in the binary image. The moments m['m10'] and m['m01'] represent the sums of the X and Y coordinates of all pixels in the object, respectively, and m['m00'] represents the area of the object. Dividing these sums by the area of the object gives the centroid coordinates (cx, cy) as integers.
After that, we 'paint' the circle in  the centroid of the line, that we calculated before. Here is how the final image can be seen on screen:

![image](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/6f6c2a14-af81-440c-9e27-9fac2cda7c54)

-------------------------------------------------------------------------

We included another update for the image, so that in this way, it is clearer and much harder for the program to mistake.
```python3
    #process the image and reduce noise and small pixel variations.
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5,5), 0)

    # detect the color of line
    res = cv.inRange(blur, lowest_thresh, top_thresh)
    #dilate and erode the mask
    d = cv.dilate(res, kernel=keneral, iterations=D_iter)
    e = cv.erode(d, kernel=keneral, iterations=E_iter)

```
We will use the cv2.dilate() and cv2.erode() functions to process the image. In this way, we can let the F1 know more about farther road. As a result, the F1 can handle sharp turns better.

----------------------------------------------------------------------------

Now it is time to use the PID to control the F1.
In this situation, we have the: 'HAL.setW(X)' function, so that we can directly set the angular velocity of the F1 and keep adjusting it at every iteration. 
The general equation of the PID is the following:

![Positional_PID](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/b7830c7c-5733-4096-9a91-919ee7ef66ae)

We need to implement this in our code, watching carefully the error every time it iterates and adjusting the constants Kp,Kd and Ki to minimize the error and oscilate less. 
