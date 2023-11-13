from GUI import GUI
from HAL import HAL
from MAP import MAP
import numpy as np

map_height= 400
map_width= 400



def get_map_v24():
  map_array = MAP.getMap('/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png')
  return map_array

while True:
    
    new_target = GUI.getTargetPose()
    new_target_map = tuple(MAP.rowColumn(new_target))
      
      
    if new_target != target:
      print(F"New target: {new_target}")
      print(F"New target(map): {new_target}")
      target = new_target
      grid= compute_grid(map_array,new_target_map)
      print("Cos grid:")
      print(grid)
      start_pos= get_car_pos()
      print(F"Cost in start position:{grid[start_pos[1],start_pos[0]]})
      
      #path = get_path(grid_now,target_map)
      (F"New target: (new_target)")
    path = [MAP.rowColumn(GUI.getTargetPose()),MAP.rowColumn((HAL.getPose3d().x,HAL.getPose3d().y))]  
    
    GUI.showPath(path)
    
    map_img = get_map_v24()
    #0 obst snd 255 free
    #obs con coste muy grande y esquinas con mas coste ej raiz d 2
    
    grid = np.zeros((map_height,map_width))

    for i in range(map_width):
        for j in range(map_height):
            #if map_img[j][i] != 0:  # Solo dibujar si esta celda no es un obstáculo
            grid[j][i] = 0.5*i + 0.5*j
    
    GUI.showNumpy(grid)
