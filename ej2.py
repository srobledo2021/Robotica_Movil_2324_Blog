from GUI import GUI
from HAL import HAL
import numpy as np
import cv2
# Enter sequential code!

prev_error =0
accum_error=0

while True:
    # Enter iterative code!
    image=HAL.getImage()
    hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    lower_tresh = np.array([0,0,0])
    upper_tresh =np.array([1,1,360])
    
    mask =cv2.inRange(hsv, lower_tresh,upper_tresh)
    mask = cv2.bitwise_not(mask)
    
    h, w, d =image.shape
    search_top = 3 * h / 4
    search_bot = search_top * 20
    
    GUI.showImage(image)
    
    M = cv2.moments(mask)
    
    if M['m00'] > 0:
      cx = int(M['m10'] / M['m00'])
      cy = int(M['m01'] / M['m00'])
      cv2.circle(image, (cx, cy), 20, (0, 0, 255), 1)
      
      err = cx-w/2
      print(err)
      p=float(err)
      d=float(err) - float(prev_error)
      
      GUI.showImage(image)
      HAL.setV(4)
      HAL.setW(-p/158 - d/150)
      prev_error = float(err)