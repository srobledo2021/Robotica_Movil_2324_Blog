
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
  - [Final Code](#Final-code-2)
- [Exercise 3: Obstacle Avoidance](#Obstacle-Avoidance)
  - [Introduction](#Introduction-3)
  - [API](#API-3)
  - [Steps](#Steps-3)
  - [Video](#Video)
- [Exercise 4: Obstacle Avoidance](#Global-Navigation)
  - [Introduction](#Introduction-4)
  - [API](#API-4)
  - [Steps](#Steps-4)
  - [Video](#Video-4)
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
 
Before applying the PID in our code we need to create several functions, so that it will be much easier to undesrtand and work with.

- get_red_mask(img) It receives the image, applies a mask so that we only get the red colour, and then 'depurates' it and returns it. Returns the mask
- get_centroid(mask) It calculates the centroid of the line from the mask that is introduced. Returns the centroid (cx,cy)
- calculate_angular_velocity(error) It calculates the angular speed by applying a PID inside, which is already explained.


------------------------------------------------------------------------------

Now it is time to use the PID to control the F1.
In this situation, we have the: 'HAL.setW(X)' function, so that we can directly set the angular velocity of the F1 and keep adjusting it at every iteration. 
The general equation of the PID is the following:

![Positional_PID](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/b7830c7c-5733-4096-9a91-919ee7ef66ae)

We need to implement this in our code, watching carefully the error every time it iterates and adjusting the constants Kp,Kd and Ki to minimize the error and oscilate less. 

We included the PID by calling our function 'calculate_angular_velocity()'. In our while loop, we did this:
```python3
#PID control
    cur_error = -(centroid[0] - (width/2))/300
    angular=calculate_angular_velocity(cur_error)
    HAL.setW(angular)
```
Here, as it can be seen, the loop handles the error and deals with it by calling a function that will have the PID and will return the angular speed after the PID is implemented. We implement the PID this way:
```pytho3
#proportional error
  P = Kp * error
  D = Kd * ( error - prev_error)
  
  prev_error = error
  
  integral_e += error
  I = Ki * integral_e
  
  angular= P + I + D
```
This is our code right now:

[source code](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/blob/main/source/p2_v1.py)

This code was taking less than 3 minutes.
Which actually works pretty accurate, but the car needs to be faster, we are not in a Fiat 500 :)

After implementing this PID, we realized that although the code is working perfectly and the car stays on the line the whole time with smooth movements. We needed to do something else so that the car could go faster and complete one entire lap in less than one or two minutes. That is when we came up with an idea, a new PID controller for the linear speed so that the car itself can regulate the way it behaves, depending on the track. So that if it is following the line in a straight line, the speed will work different than when the car is turning. 

After trials and errors, we came up with a brand-new idea, which is the following:
We need to have 2 PID controllers. Both of them will be handling the angular speed, but this time we will be measuring a threshold to determinate whether the car is in a straight line or in a curve. 
Errors for both controllers:
```python3
#angular error handling
prev_error = 0
integral_e = 0

#linear error handling
prev_error_lin=0
integral_e_lin =0
```
PIDs:
```python3
#curves
Kp = 1
Ki = 0.0001
Kd = 2.5

#straight lines
Kp_l=1
Ki_l=0.0001
Kd_l= 2.5
```

The way we are going to implement this is by measuring where the centroid of the line is at every time ( after getting the mask) and comparing it to the location of the center of the line, but a bit higher. In this way we can get the difference between coordinates in the X axis and stablish a threshold. This threshold is there to decide whether the car is taking a straight line at a high-speed or just turning in a curve. Here is the implementation in the 'get_top_centroid' function which returns that point mentioned before:

```python3
def get_top_centroid(mask):
  contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  highest_point = None
  for contour in contours:
    if len(contour) > 0:
        top_point = tuple(contour[contour[:, :, 1].argmin()][0])
        if highest_point is None or top_point[1] < highest_point[1]:
            highest_point = top_point

  if highest_point is not None:
    cv.circle(img, highest_point, 5, (0, 0, 255), -1)

  centroid = (highest_point)
  return centroid
```

![image](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/76b859b2-0df6-4872-8d03-26650b6a825e)

Now we can get the difference in X axis coordinates and depending on that, effectuate our code:
```python3
#get threshold
curve_threshold=abs(centroid[0]- top_centroid[0])
    
    if (curve_threshold < 15):
      counter +=1
      if counter >= 5:
        print("straight")
        linear=calculate_linear_velocity(linear_error)
        HAL.setW(linear)
        HAL.setV(15)
      
    if (curve_threshold > 20):
      print("Curve")
      angular=calculate_angular_velocity(cur_error)
      HAL.setW(angular)
      HAL.setV(4)
      counter = 0
```
As we can notice, we left a gap in the conditionals for the threshold. We did this on purpose to apply 'histeresis' so that instead of an abrupt change, we make it smooth.

The counter that can be seen is perfectly studied and used so that when the car recognises more than 5 times in a row that it is in a straight line, the car speeds up. This is because sometimes when the car is turning, a few iterations recognized the line as straight. By using this we can ensure that the car is really in a straight line, and not just turning but heading the front.

[Code for this version here](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/blob/main/source/p2_v2.py)

The code works but there is still something missing. This is the time when we realize that it is much better for the car to keep the reference of the central point (cx, cy) instead of the 'line' point. This is why the same code as before was implemented but using this new point, as we can see here:

![image](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/b55a7fd9-0048-414f-b877-e82961908460)

We changed the function that originated the other point with this new one:
```python3
def get_mid_centroid():
  cx=320
  cy=225
  cv.circle(img, (cx, cy), 20, (0, 0, 255), -1)
  centroid=(cx,cy)
  
  return centroid
```

The main issue with this code is that it takes much longer to proccess itself, that is why the PIDs are not working the same way as before and the code is really unestable, allowing the car to get out of the track and hit himself. Apart from that we could complete a lap in approximately 30 seconds less than before, but this is not good enough, comparing it with all the issues we got.

[This is the code with the implementation](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/blob/main/source/p2_v3.py)

-----------------------------------------------------------------------------------

### Final code 2

Overall, we decided to take the first code as the final one. Even though it is the easiest one to implement, it is incredibly reliable, and that is what we are looking for in this exercise. The other implementations worked well and were well designed but the objective is to follow the line, and they made the car speed up much more, however, the line was not followed as expected.

We even realized that once you run the code more than once, the car works different at the very beginning, this may be because the page saves previous data and once you run the code, it will start with that data saved. This can be seen when you stop running the code and leave the car turning. When re-running the code again, it works for a couple of seconds as if it was still turning, and then it behaves slightly different as the previous time.

Now it is time to adjust the PID even more. After trials and errors adjusting the PID values, we came up with the final ones, which are:
Kp = 1
Ki = 0.001
Kd = 2.5

Now you can run the code and the car will keep on the track forever!

This code can be seen in here:
[Accurate Implementation](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/blob/main/source/p2_v1.py)


https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/73f3e8ab-d263-4081-b48e-5f2f63e001f4


---------------------------------------------------------------------------------------

## Obstacle Avoidance

### Introduction 3
The goal of this exercise is to control a car so that it keeps on track as well as it is avoiding other cars which are displayed on different parts of the racing circuit.

### API 3

- from HAL import HAL - to import the HAL(Hardware Abstraction Layer) library class. This class contains the functions that sends and receives information to and from the Hardware(Gazebo).
- from GUI import GUI - to import the GUI(Graphical User Interface) library class. This class contains the functions used to view the debugging information, like image widgets.
- HAL.getPose3d().x - to get the position of the robot (x coordinate)
- HAL.getPose3d().y - to obtain the position of the robot (y coordinate)
- HAL.getPose3d().yaw - to get the orientation of the robot with regarding the map
- HAL.getLaserData() - to obtain laser sensor data It is composed of 180 pairs of values: (0-180º distance in millimeters)
- HAL.getImage() - to get the image
- HAL.setV() - to set the linear speed
- HAL.setW() - to set the angular velocity
- GUI.showImage() - allows you to view a debug image or with relevant information

To simplify, the implementation of control points is offered. To use it, only two actions must be carried out:

- currentTarget = GUI.map.getNextTarget() - Obtain the following point:
- currentTarget.setReached(True) - Mark it as visited when necessary:

The graphical interface (GUI) allows to visualize each of the vectors of calculated forces. There is a function for this purpose:
```python3
# Car direction  (green line in the image below)
carForce = [2.0, 0.0]
# Obstacles direction (red line in the image below)
obsForce = [0.0, 2.0]
# Average direction (black line in the image below)
avgForce = [-2.0, 0.0]

GUI.showForces(carForce, obsForce, avgForce)
```
As well as the destination that we have assigned:

 Current target
```python3
target = [1.0, 1.0]
GUI.showLocalTarget(target)
```

More can be seen at Unibotics webpage:
[Webpage Link](https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/obstacle_avoidance)

Taking all of this, now it is time for the implementation:

### Steps 3

First of all we will be implementing the laser. We will be doing it with this function:

```python3
def parse_laser_data (laser_data):
    laser = []
    i = 0
    while (i < 180):
        dist = laser_data.values[i]
        if dist > 10:
            dist = 10
        angle = math.radians(i-90) # because the front of the robot is -90 degrees
        laser += [(dist, angle)]
        i+=1
    return laser
```
The  function parses laser data taking into account that the laser only has 180º of  coverage and that the measure read at 90º corresponds to the ‘front’ of the robot.

-----------------------------------------------------------

Navigation using VFF (Virtual Force Field), is going to be the navigation algorithm that we will be using this time. The way it is done is the following:

Each object in the environment generates a repulsive force towards the robot. Destiny generates an attractive force in the robot. This makes it possible for the robot to go towards the target, distancing itself of the obstacles, so that their address is the vector sum of all the forces.

In this pic we can see the three vectors all together:

![vff_forces](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/9b6a3792-2d15-4e63-829d-23a7ee142634)

 Car direction  (green line in the image)
 Obstacles direction (red line in the image)
 Average direction (black line in the image)

Now it is time to implement the coordinate system that we will be using to create the VFF mentioned:

We have 2 different coordinate systems in this exercise.

- Absolute coordinate system: Its origin (0,0) is located in the finish line of the circuit (exactly where the F1 starts the lap).
- Relative coordinate system: It is the coordinate system solidary to the robot (F1). Positive values of X means ‘forward’, and positive values of Y means ‘left’.

We will be using the following function to convert absolute coordinates to relative ones:

```python3
def absolute2relative (x_abs, y_abs, robotx, roboty, robott):

    # robotx, roboty are the absolute coordinates of the robot
    # robott is its absolute orientation
    # Convert to relatives
    dx = x_abs - robotx
    dy = y_abs - roboty

    # Rotate with current angle
    x_rel = dx * math.cos (-robott) - dy * math.sin (-robott)
    y_rel = dx * math.sin (-robott) + dy * math.cos (-robott)

    return x_rel and y_rel
```

Now the first part of our 'while' loop in the code, will work like this:
```python3
    #get image
    image=HAL.getImage()
    #get laser
    laser_data = HAL.getLaserData()
    laser = parse_laser_data(laser_data)
    #----------------------------------------------
    # Get absolute position of current target
    currentTarget = GUI.map.getNextTarget()
    target_abs_x = currentTarget.getPose().x
    target_abs_y = currentTarget.getPose().y
    #----------------------------------------------
    absolute_target = target_abs_x, target_abs_y
    #----------------------------------------------
    # Get robot position and orientation
    robot_x = HAL.getPose3d().x
    robot_y = HAL.getPose3d().y
    robot_yaw = HAL.getPose3d().yaw
    #----------------------------------------------
    #get relative coordinates of target
    target_rel_x,target_rel_y = absolute2relative(target_abs_x,target_abs_y,robot_x,robot_y,robot_yaw)
    relative_target = target_rel_x, target_rel_y

```

We will also implement the 'get_repulsive_force()' function, which can be defined as:

```python3
def get_repulsive_force(parse_laser):
    laser = parse_laser
    
    laser_vectorized = []
    for dist, angle in laser:
      
        x = 1/dist * math.cos(angle) * -1
        y = 1/dist * math.sin(angle) * -1

        v = (x,y)
        laser_vectorized += [v]
    laser_mean = np.mean(laser_vectorized, axis=0)
    return laser_mean
```
This function usage is pretty simple, the parameter is the laser data (already parsed) and it returns a vector pointing to the opposite way of where the 'mean of obstacles detected' are. We take both distance and angle (polar coordinates) from the laser data of the parameter and we convert them into Cartesian coordinates (x and y). Then we create the vector 'v' with both coordinates and add it to our list. In the end we can create a mean so that we only return one vector with the direction of the repulsive force. As the code is iterating the whole time, whenever a car is spotted, it instantly evades it as the mean of vectors changes instantly.

-------------------------------------------------------------------------------------

After that, it is time to define the three vectors that we already mentioned at the beginning. 
The first one is the car vector. We need it to keep constantly pointing at targets, that is why we use the target relative coordinates to define it. However, as we need it for the total/average force vector, and later for the speed, we will need to reduce and control it.
When we display the vectors(will be seen later) there is kind of a little 'bounding box' that can be used as a reference. Taking this into account, we can define the values that are defined on the code below, defining coordinates for the lenght of x and the lenght of y maximum so that in this way the vector is always 'locked' in that 3.5 x 3.2 box.

The second one is the obstacle vector, which will be using the function we mentioned before to get the repulsive force vector and we can multiply it by a number so that in this way we can reduce or enlarge it. It is important to add that these values are arbitrary and will be changed later.

Same is done with the third vector, the average vector (or mean vector). Which calculates the total force taking into account both vectors repuslive and car vector. We will also use some numbers to modify results by multiplying them by both coordinates.

```python3
    # Car direction defined in a green vector
    car_vect = [max(min(target_rel_x, 3.5), -3.5), max(min(target_rel_y, 3.2), -3.2)]
    # obstacle direction defined in a red vector
    obs_vect = [get_repulsive_force(laser)[0]*5, get_repulsive_force(laser)[1]*15]
    # average direction defined in a black line
    avg_vector = [(car_vect[0]+obs_vect[0])*1.5, (car_vect[1] + obs_vect[1]) *0.6]
```

Check if the robot is close to the objective(2 units) and if so, set the current objective as 'reached'. It will later try to reach the next one.
```python3
    if (target_rel_x < 2 and target_rel_y < 2):
        currentTarget.setReached(True)
```        

Now we define the linear and angular speed. We set the both speeds depending on the total/average vector.
```python3
      HAL.setW(tan * 1.5)
      HAL.setV(avg_vector[0])
```
Now we show the target, as well as the vectors of the three forces and the current image on the screen.
```python3
    GUI.showLocalTarget(relative_target)
    GUI.showForces(car_vect, obs_vect, avg_vector)
    GUI.showImage(image)
```
----------------------------------------------------------------------------------------

After all of this, the code will work. However, it took a very long time to check different values to multiply the vectors so that the robot evaded other cars perfectly. At first, most of the cars were evaded perfectly but there were 3 of them which our robot could not. That is why I came up with a brand-new solution, which was to decrease speed, allowing us to react with more time and precission. How did we manage to do that? By reducing the total vector or average vector (the sum of other both). In this way we can reduce the speed(as it is used for setting the robot speed).

Then I came up with the idea of increasing the repulsion vector so that the sooner the car detects an 'anomaly' (and by anomaly, I mean an obstacle that pops out of nowhere), the better reaction it can have, allowing the car to take a sharp turn when necessary.

We also decided to change the distance that the robot needs to be from the objective so that it will be able to change it when it is closer. First time it was 2 units, but we decided to make it even more precise, changing it into 1.5.

Another little change was to declare the global values of the AngularValue= 1.5 that will be used to set the angular speed and the DistanceToObjective = 1.5 that we mentioned before.

In the end, after lots of changes, improvements and by trials and errors, these are the values that make the code work perfectly:

```python3
# Car direction defined in a green vector
    car_vect = [max(min(target_rel_x, 3.5), -3.5), max(min(target_rel_y, 3.2), -3.2)]
    # obstacle direction defined in a red vector
    obs_vect = [get_repulsive_force(laser)[0]*3, get_repulsive_force(laser)[1]*8]
    # average direction defined in a black line
    avg_vector = [(car_vect[0]+obs_vect[0])*1, (car_vect[1] + obs_vect[1]) *0.3]
```

# Video
[Video testing the code](https://youtu.be/Oz9GYynMgoA)


--------------------------------------------------------------------

# Global Navigation


### Introduction 4
         

Global Navigation using TeleTaxi
TOC Global Navigation


The objective of this practice is to implement the logic of a Gradient Path Planning (GPP) algorithm. Global navigation through GPP, consists of:
Selected a destination, the GPP algorithm is responsible for finding the shortest path to it, avoiding, in the case of this practice, everything that is not road.

Once the path has been selected, the logic necessary to follow this path and reach the objective must be implemented in the robot.


### API 4

- from HAL import HAL - to import the HAL(Hardware Abstraction Layer) library class. This class contains the functions that sends and receives information to and from the Hardware(Gazebo).
- from GUI import GUI - to import the GUI(Graphical User Interface) library class. This class contains the functions used to view the debugging information, like image widgets.
- from MAP import MAP - This class contains functions that interact with data related to the map and Gazebo world.
- HAL.setV() - to set the linear speed
- HAL.setW() - to set the angular velocity
- HAL.getPose3d() - returns x,y and theta components of the robot in world coordinates
- GUI.showNumpy(numpy) - shows Gradient Path Planning field on the user interface. It represents the values of the field that have been assigned to the array passed as a parameter. Accepts as input a two-dimensional uint8 numpy array whose values can range from 0 to 255 (grayscale). In order to have a grid with the same resolution as the map, the array should be 400x400
- GUI.showPath(array) - shows a path on the map. The parameter should be a 2D array containing each of the points of the path
- GUI.getTargetPose() - returns x,y coordinates of chosen destionation in the world. Destination is set by clicking on the map image
- MAP.getMap(url) - - Returns a numpy array with the image data in grayscale as a 2 dimensional array. The URL of the Global Navigation map is ‘/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png’, so the instruction to get the map is
```
array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')
```
- MAP.rowColumn(vector) - returns the index in map coordinates corresponding to the vector in world coordinates passed as parameter

### STEPS 4

Before iterating in the while loop, we need to get the map from the Unibotics files:
```python
map_url = '/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png'
map_data = MAP.getMap(map_url)
```
Define the grid:
```
grid = np.full(map_data.shape, 255)
```
Then we need to get the position where the car is placed at the very beginning and get the target that has to be reached.

The way this is implemented is:
```python3
#---------------------------------------
# get the clicked target
goal_pose  = GUI.getTargetPose()
#get coordinates for actual location in map
new_target_map = tuple(MAP.rowColumn(goal_pose))
#start pose
start_pose =(HAL.getPose3d().x, HAL.getPose3d().y)
#---------------------------------------
# Convert world coordinates to map coordinates
start_cell = MAP.rowColumn(start_pose)
goal_cell = MAP.rowColumn(new_target_map)
```
As so, we get the starting position and the goal position with the actual map coordinates.

In our main loop, we are following this algorythm to generate the grid with actual values, then get the best path and after that, move to the target. The way it is implemented is as so:

Inside a 'while' loop, first of all we implement a BFS algorythm to get the grid and assign costs to its cells: 
```python3
grid = bfs_search(map_data, new_target_map, start_pos)
```
This are the steps we are following to implement the algorythm(all defined in the bfs_search function):
Step1: insert Target Node into priority queue
Step2: c = pop node from priority queue
Step3: if c == start node End
Step4: if c == obstacle Save to another list and goto Step2
Step5: assign weight to neighbors of c if previously unassigned
Step6: insert neighbors of c to priority queue
Step7: goto Step2


After that, we need to get the path with the lowest cost from the actual position to the goal. We will implement this in our function:
```python3
path = get_path_coords(grid, start_pos)
```
Then we normalize the grid using 'normalize_grid' function and show it on display afterwards:
```python3
grid_normalized = normalize_grid(grid)
GUI.showNumpy(grid_normalized)
```
This is how we get the grid normalized:
```python
def normalize_grid(grid):
    max_grid = np.max(grid)
    return np.clip(grid * 255 / max_grid, 0, 255).astype('uint8')
```
After all of that the map should look like this(dependind on the goal selected):

![image](https://github.com/srobledo2021/Robotica_Movil_2324_Blog/assets/113594786/73acdc10-3f46-4fc8-a67a-a2ab39076134)


----------------------------------------------------------------------------------------


Now the strategy that we are using is to simplify the whole path and split it into little vectors so that it is much easier to navegate.
The way we are implementig it is by doing this:
```python
resulting_vectors = path_into_vectors(path,new_target_map)
vectors_from_path = [[x, y] for coord in resulting_vectors for x, y in coord]
result_path = vectors_from_path[1:]
```
The function 'path_into_vectors' gets the whole path that we already made before and checks for similar coordinates so that instead off having a straight line with 30 coordinates, it has a vector with the origin and end of it. 

By doing this, we are able to simplify the whole path.

----------------------------------------------------------
Now it is time to navigate, for that we are using one easy algorythm which is rotating (to search for the next coordinate) and then move until the car reaches it. We are doing it this way:
```python3
while True:
        for i in range(len(result_path)):
            orientate(result_path[i][0], result_path[i][1])
            move_forward(result_path[i][0], result_path[i][1])
            #Reach goal
            if (check_reached_goal(result_path) == True):
                break
```
The way 'orientate' is being done is by gettting to know the yaw of the car so that comparing it afterwards with the angle of the goal coordinate, we can iterate to reduce the error (the difference) and spin the car until it faces the coordinate we are searching for.

The way 'move_forward' is being done is by comparing the actual position with the actual target coordinate and move in a straight line until the goal is reached.

The fuction 'check_reached_goal' simply checks if the coordinate we are in is the goal selected on the map or not. And if so, it stops iterating.

### Video 4
[LINK]()
