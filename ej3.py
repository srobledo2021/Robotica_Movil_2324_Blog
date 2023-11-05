from GUI import GUI
from HAL import HAL
import math
import numpy as np
# Enter sequential code!

AngularValue= 1.5
DistanceToObjective = 1.5

def absolute2relative (x_abs, y_abs, robotx, roboty, robott):

    # robotx, roboty are the absolute coordinates of the robot
    # robott is its absolute orientation
    # Convert to relatives
    dx = x_abs - robotx
    dy = y_abs - roboty

    # Rotate with current angle
    x_rel = dx * math.cos (-robott) - dy * math.sin (-robott)
    y_rel = dx * math.sin (-robott) + dy * math.cos (-robott)

    return x_rel, y_rel

def parse_laser_data(laser_data):
    laser = []
    i = 0
  
    for i, dist in enumerate(laser_data.values):
        if dist > 10:
            dist = 10
        angle = math.radians(i-90)
        laser += [(dist, angle)]
        i+=1
    return laser

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

def distance(x, y):
    return math.sqrt(abs(x)*2 + abs(y)*2)

while True:
    # Enter iterative code!
    image=HAL.getImage()
    laser_data = HAL.getLaserData()
    laser = parse_laser_data(laser_data)
    #----------------------------------------------
    # Obtener la posición absoluta del objetivo actual
    currentTarget = GUI.map.getNextTarget()
    target_abs_x = currentTarget.getPose().x
    target_abs_y = currentTarget.getPose().y
    #----------------------------------------------
    absolute_target = target_abs_x, target_abs_y
    #----------------------------------------------
    # Obtener la posición y orientación del robot
    robot_x = HAL.getPose3d().x
    robot_y = HAL.getPose3d().y
    robot_yaw = HAL.getPose3d().yaw
    #----------------------------------------------
    target_rel_x,target_rel_y = absolute2relative(target_abs_x,target_abs_y,robot_x,robot_y,robot_yaw)
    relative_target = target_rel_x, target_rel_y
    
    # Car direction defined in a green vector
    car_vect = [max(min(target_rel_x, 3.5), -3.5), max(min(target_rel_y, 3.2), -3.2)]
    # obstacle direction defined in a red vector
    obs_vect = [get_repulsive_force(laser)[0]*3, get_repulsive_force(laser)[1]*8]
    # average direction defined in a black line
    avg_vector = [(car_vect[0]+obs_vect[0])*1, (car_vect[1] + obs_vect[1]) *0.3]


    tan = math.tan(avg_vector[1]/avg_vector[0])

    if (target_rel_x < DistanceToObjective and target_rel_y < DistanceToObjective):
        currentTarget.setReached(True)
        
  
    HAL.setV(avg_vector[0])
    HAL.setW(tan * AngularValue)

    GUI.showLocalTarget(relative_target)
    GUI.showForces(car_vect, obs_vect, avg_vector)
    GUI.showImage(image)
    
