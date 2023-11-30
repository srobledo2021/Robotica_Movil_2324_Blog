from GUI import GUI
from HAL import HAL
from MAP import MAP
import math
import heapq
import numpy as np
import queue

map_height= 400
map_width= 400

obstacles = []

def gridToWorld(map_cell):
  world_x = map_cell[1] * 500 / 400 -250
  world_y = map_cell[0] * 500 / 400 -250
  
  return (world_x, world_y)
  
def normalize_grid(grid):
    max_grid = np.max(grid)
    return np.clip(grid * 255 / max_grid, 0, 255).astype('uint8')
  
def get_car_position_gui():
  car_position = HAL.getPose3d()
  position = [car_position.x, car_position.y]
  car_position_map = tuple(MAP.rowColumn(position))
  #print(F"Car position: {car_position}")
  #print(F"Car position map: {car_position_map}")
  #print(F"Map at car position: {map_array[car_position_map[1], car_position_map[0]]}")
  return car_position_map

def compute_grid(map_array, target_map, start_position):
    priority_queue = queue.PriorityQueue()
    visited = set()
    visited.add(target_map)

    # Step 1: Insert Target Node into the priority queue
    priority_queue.put((0, target_map))

    while not priority_queue.empty(): 
        # Step 2: Pop node from the priority queue
        cost, current = priority_queue.get()
        # Step 3: Check if the current node is the start node
        if current == start_position:
            break

        # Step 4: Check for obstacles
        if map_array[current[1], current[0]] == 0:  # si es 0 es un obstáculo
            continue  # Skip this cell

        # Update the grid with the current cost
        grid[current[1], current[0]] = cost

        # Step 5: Assign weight to neighbors

        # Get neighbors
        neighbors = [
            (current[0] - 1, current[1]),  # Left
            (current[0] + 1, current[1]),  # Right
            (current[0], current[1] - 1),  # Up
            (current[0], current[1] + 1),  # Down
            (current[0] - 1, current[1] - 1),  # Up Left
            (current[0] + 1, current[1] - 1),  # Up Right
            (current[0] - 1, current[1] + 1),  # Down Left
            (current[0] + 1, current[1] + 1),  # Down Right
        ]

        # Compute the cost of each neighbor
        for neighbor in neighbors:
            # Check if the neighbor is out of bounds
            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[1] or neighbor[1] < 0 or neighbor[1] >= grid.shape[0]):
                continue

            # Check if the neighbor has been visited
            if neighbor in visited:
                continue

            # Update the grid with the current cost for the neighbor
            if neighbor[0] == current[0] or neighbor[1] == current[1]:
                grid[neighbor[1], neighbor[0]] = cost + 1
            else:
                grid[neighbor[1], neighbor[0]] = cost + math.sqrt(2)
            # print(F"grid: {grid[neighbor[1], neighbor[0]]}")

            # Insert neighbors into the priority queue
            priority_queue.put((grid[neighbor[1], neighbor[0]], neighbor))
            # Mark the neighbor as visited
            visited.add(neighbor)
    


    return grid

def get_path(grid, target_position, start_position):
    path = []
    current = start_position
    while (grid[current[1], current[0]] != 0):
        path.append(current)

        # Obtener vecinos
        neighbors = [
            (current[0] - 1, current[1]),  # Left
            (current[0], current[1] - 1),  # Up
            (current[0] + 1, current[1]),  # Right
            (current[0], current[1] + 1),  # Down
            (current[0] - 1, current[1] - 1),  # Up Left
            (current[0] + 1, current[1] - 1),  # Up Right
            (current[0] - 1, current[1] + 1),  # Down Left
            (current[0] + 1, current[1] + 1),  # Down Right
        ]

        # Encontrar el vecino con el menor costo
        min_cost = float("inf")
        next_position = None

        for neighbor in neighbors:
            if (0 <= neighbor[0] < grid.shape[1] and 0 <= neighbor[1] < grid.shape[0] and grid[neighbor[1], neighbor[0]] < min_cost ):
                min_cost = grid[neighbor[1], neighbor[0]]
                next_position = neighbor


        if next_position is not None:
            current = next_position
        else:
            # No se encontró un vecino válido, terminar el bucle
            print("no se encontro vecino")
            break

    path.append(current)
    print(F"current: {current}")
    print(F"target: {target_position}")
    print(F"start: {start_position}")
    # print(F"Final Path: {path}")
    return path


import math
from time import sleep

def move_robot_along_path(path):
  #hacerlo por tramos, es decir por segmentos. Marcando donde siempre
  # primero sube, mandamos la velocidad durante ese segmento hasta que  cambie, luego podemos
  #dividir el tramo en tramos mas pequeños y solo necesitamos girar yu ya etre tramos
  # cuando sube  la coordenada y ( en el mapa la x) es siempre la misma y hasta que no vcambie, sigue esa recta
    for i in range(len(path) - 5):
        current_position = path[i]
        next_position = path[i + 5]

        # Calcular la diferencia entre la posición actual y la siguiente posición
        delta_x = next_position[0] - current_position[0]
        delta_y = next_position[1] - current_position[1]

        if delta_x > 0 and delta_y == 0:
            angle_to_target = math.pi / 2
        elif delta_x == 0 and delta_y > 0:
            angle_to_target = 0
        elif delta_x > 0 and delta_y > 0:
            angle_to_target = math.pi / 4
        elif delta_x > 0 and delta_y < 0:
            angle_to_target = 3 * math.pi / 4
        elif delta_x == 0 and delta_y < 0:
            angle_to_target = math.pi
        else:
            angle_to_target = 0
        print(angle_to_target - HAL.getPose3d().yaw )
        if(angle_to_target - HAL.getPose3d().yaw > 0 and angle_to_target - HAL.getPose3d().yaw < 0.5):
          HAL.setW(0)
          HAL.setV(3)
          sleep(10000)
        # Configurar la velocidad angular y lineal del robot hacia la siguiente posición
        else:
          HAL.setW(angle_to_target)



    # Detener el robot cuando alcanza el destino
    HAL.setV(0)
    HAL.setW(0)



#---------------------------------------
map_url = '/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png'
map_data = MAP.getMap(map_url)

grid = np.full(map_data.shape, 255)

start_position = get_car_position_gui()
target = None
while True:
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
    
 

    if goal_pose != target:

        target = goal_pose
        # GUI.showNumpy(map_array)
        grid = compute_grid(map_data, new_target_map, start_position)
        print(F"Cost Grid: {grid}")
        print(F"Cost in Start position: {grid[start_position[1], start_position[0]]}")
        print(F"Cost in Target position: {grid[new_target_map[1], new_target_map[0]]}")
        print(F"Cost in x position: {grid[330, 106]}")
        if grid[start_position[1], start_position[0]] == 0:
          print("obstacle in start position")
        path_ = get_path(grid, new_target_map, start_position)
        print(F"Path: {path_}")
        # Normalize the grid to show it
        grid_normalized = normalize_grid(grid)
        GUI.showNumpy(grid_normalized)
        path_en_2D = [[x, y] for x, y in path_]
        GUI.showPath(path_en_2D)
        
    # Llamada a la función para mover el robot a lo largo del path
    move_robot_along_path(path_en_2D)
