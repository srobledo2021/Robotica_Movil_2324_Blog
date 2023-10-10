from GUI import GUI
from HAL import HAL
import time
import cv2
import numpy as np

# Definir constantes para los controladores PID
kp_linear = 1.1
ki_linear = 0.01
kd_linear = 1.3

kp_angular = 1.1
ki_angular = 0.01
kd_angular = 1.3

# Variables para el control PID lineal
prev_err_linear = 0
accum_err_linear = 0

# Variables para el control PID angular
prev_err_angular = 0
accum_err_angular = 0

# Umbral para detectar curvas (ajusta este valor según tu circuito)
umbral_curva = 1  # Ajusta el valor de acuerdo a tus necesidades

# Función para el control PID lineal
def control_linear(err_linear):
    global prev_err_linear, accum_err_linear
    p = err_linear
    d = err_linear - prev_err_linear
    i = accum_err_linear
    control_signal = kp_linear * p + ki_linear * i + kd_linear * d
    accum_err_linear += err_linear
    prev_err_linear = err_linear
    return control_signal

# Función para el control PID angular
def control_angular(err_angular):
    global prev_err_angular, accum_err_angular
    p = err_angular
    d = err_angular - prev_err_angular
    i = accum_err_angular
    control_signal = kp_angular * p + ki_angular * i + kd_angular * d
    accum_err_angular += err_angular
    prev_err_angular = err_angular
    return control_signal

while True:
    cap = HAL.getImage()
    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([1, 1, 360])
   
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.bitwise_not(mask)
   
    h, w, d = cap.shape
    top = 3 * h/4
    bot = top + 20
   
    M = cv2.moments(mask)
   
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(cap, (cx, cy), 20, (0, 0, 255), -1)
        err_linear = cx - w/2
        err_angular = err_linear  # Para mantener el giro en función del error lineal
        print("Err Linear:", err_linear)
       
        # Detectar si es una curva o una recta (criterio de detección)
        if abs(err_linear) > umbral_curva:
            # Control PID para curvas
            control_signal_linear = control_linear(0)  # Mantener velocidad lineal constante en curvas
            control_signal_angular = control_angular(err_angular)
        else:
            # Control PID para rectas
            control_signal_linear = control_linear(err_linear)
            control_signal_angular = control_angular(err_angular)
       
        linear_speed = 10 + control_signal_linear
        angular_speed = -control_signal_angular / 10
       
        GUI.showImage(cap)
       
        HAL.setV(linear_speed)
        HAL.setW(angular_speed)
