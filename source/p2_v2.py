from GUI import GUI
from HAL import HAL
import numpy as np
import cv2 as cv


keneral = np.ones((4,4))

#angular error handling
prev_error = 0
integral_e = 0

#linear error handling
prev_error_lin=0
integral_e_lin =0


lowest_thresh = np.array([0, 43, 46])
top_thresh = np.array([26,255,255])

curve_threshold = 0.7

#curves
Kp = 1
Ki = 0.0001
Kd = 2.5

#straight lines
Kp_l=1
Ki_l=0.0001
Kd_l= 2.5
counter = 0

D_iter = 5
E_iter = 1


def get_red_mask(img):
  #process the image and reduce noise and small pixel variations.
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv, (5,5), 0)

    # detect the color of line
    res = cv.inRange(blur, lowest_thresh, top_thresh)
    #dilate and erode the mask
    d = cv.dilate(res, kernel=keneral, iterations=D_iter)
    e = cv.erode(d, kernel=keneral, iterations=E_iter)
    
    return e


def get_centroid(mask):
  # caculate the center of the line
  m = cv.moments(mask)
  cx = int(m['m10']/m['m00'])
  cy = int(m['m01']/m['m00'])
  cv.circle(img, (cx, cy), 20, (0, 0, 255), -1)
  centroid = (cx,cy)
  return centroid

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
  

def calculate_angular_velocity(error):
  global prev_error, integral_e
  #proportional error
  P = Kp * error
  
  D = Kd * ( error - prev_error)
  
  prev_error = error
  
  integral_e += error
  I = Ki * integral_e
  
  
  angular= P + I + D
  return angular
  
  
def calculate_linear_velocity(error):
  global prev_error_lin, integral_e_lin
  #proportional error
  P = Kp_l * error
  
  D = Kd_l * ( error - prev_error_lin)
  
  prev_error_lin = error
  
  integral_e_lin += error
  I = Ki_l * integral_e_lin
  
  
  angular= P + I + D
  return angular




while True:
    #get image
    img = HAL.getImage()
    #image info
    height, width, channel = img.shape
    #get the mask with the red filters
    mask=get_red_mask(img)
    top_centroid = get_top_centroid(mask)
    #get the centroid of the red line at every time
    centroid=get_centroid(mask)
    
    #print("centroid= ",centroid)
    #print("top_centroid= ",top_centroid)
    
    #PID control
    cur_error = -(centroid[0] - (width/2)) /300
    linear_error = cur_error
    
    
    curve_threshold=abs(centroid[0]- top_centroid[0])
    print(curve_threshold)
    
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
    #print("Err: ", cur_error)
    
    #if abs(cur_error) > curve_threshold:
    #Curve PID
      
   
    GUI.showImage(img)
