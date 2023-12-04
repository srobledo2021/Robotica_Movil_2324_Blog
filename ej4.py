from GUI import GUI
from HAL import HAL
from MAP import MAP
import math
import heapq
import numpy as np
import queue
from time import sleep

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
  
def get_car_pos():
  car_position = HAL.getPose3d()
  position = [car_position.x, car_position.y]
  car_position_map = tuple(MAP.rowColumn(position))
  return car_position_map

def bfs_search(map_array, target_map, start_pos):
    priority_queue = queue.PriorityQueue()
    visited = set()
    visited.add(target_map)

    # Step 1: Insert Target Node into the priority queue
    priority_queue.put((0, target_map))

    while not priority_queue.empty(): 
        # Step 2: Pop node from the priority queue
        cost, current = priority_queue.get()
        # Step 3: Check if the current node is the start node
        if current == start_pos:
            break

        # Step 4: Check for obstacles
        if map_array[current[1], current[0]] == 0:  
            # 0 for obstacles
            continue

        # Update the grid with the current cost
        grid[current[1], current[0]] = cost

        # Step 5: Assign weight to neighbors

        # Get neighbors
        neighbors = [
            (current[0] - 1, current[1]),  # L
            (current[0] + 1, current[1]),  # R
            (current[0], current[1] - 1),  # U
            (current[0], current[1] + 1),  # D
            (current[0] - 1, current[1] - 1),  # UL
            (current[0] + 1, current[1] - 1),  # UR
            (current[0] - 1, current[1] + 1),  # DL
            (current[0] + 1, current[1] + 1),  # DR
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

            # Insert neighbors into the priority queue
            priority_queue.put((grid[neighbor[1], neighbor[0]], neighbor))
            # Mark the neighbor as visited
            visited.add(neighbor)
    


    return grid

def get_path_coords(grid, goal_pos, start_pos):
    path = []
    current_pos = start_pos
    while (grid[current_pos[1], current_pos[0]] != 0):
        path.append(current_pos)

        # Obtener vecinos
        neighbors = [
            (current_pos[0] - 1, current_pos[1]),  # L
            (current_pos[0], current_pos[1] - 1),  # U
            (current_pos[0] + 1, current_pos[1]),  # R
            (current_pos[0], current_pos[1] + 1),  # D
            (current_pos[0] - 1, current_pos[1] - 1),  # UL
            (current_pos[0] + 1, current_pos[1] - 1),  # UR
            (current_pos[0] - 1, current_pos[1] + 1),  # DL
            (current_pos[0] + 1, current_pos[1] + 1),  # DR
        ]

        min_cost = float("inf")
        next_pos = None

        for neighbor in neighbors:
            if (0 <= neighbor[0] < grid.shape[1] and 0 <= neighbor[1] < grid.shape[0] and grid[neighbor[1], neighbor[0]] < min_cost ):
                min_cost = grid[neighbor[1], neighbor[0]]
                next_pos = neighbor


        if next_pos is not None:
            current_pos = next_pos
        else:
            print("Error: Could not find path")
            break

    path.append(current_pos)
    return path


def path_into_vectors(path):
    vectors = []

    current_vector = [path[0]]
    for i in range(1, len(path)):
        current_point = path[i]
        previous_point = path[i-1]
        # Condición para el cambio en el eje x
        if (current_point[0] == previous_point[0] or current_point[1] == previous_point[1]):
            continue
        if current_point[0] != previous_point[0]:
            vectors.append(current_vector)
            current_vector = [current_point]
        else:
            continue
    vectors.append(current_vector)
    return vectors
    
    
def att_vect(x_rel, y_rel):
    angle = HAL.getPose3d().yaw 
    pos = [x_rel, y_rel]

    vector_ang = gridToWorld(pos)

    # it makes atan2 to get the angle of the vector target
    att = math.atan2(vector_ang[0], vector_ang[1])
    
    if  att < 0:
      att += 2 * math.pi
    
    if angle < 0:
      angle = -angle 
    else:
      angle = 2 * math.pi - angle
    grados_coche = math.degrees(angle)
    grados_target = (math.degrees(att) - 90)
    while abs(grados_coche - grados_target) > 0.5:
      
      angle = HAL.getPose3d().yaw 
      
      if angle < 0:
        angle = -angle 
      else:
        angle = 2 * math.pi - angle
      grados_coche = math.degrees(angle)

      HAL.setW(abs(grados_coche - grados_target)*0.02)
      print(abs(grados_coche - grados_target))
    HAL.setW(0)
    return  

def move_to_target(x_rel, y_rel):
  while (True) :
    car_pos = HAL.getPose3d()
    pos = [car_pos.x, car_pos.y]
    car_pos_map = tuple(MAP.rowColumn(pos))
    dist_x = abs(x_rel - car_pos_map[0])
    dist_y = abs(y_rel - car_pos_map[1])
    manhattan_dist = math.sqrt((dist_x**2) + (dist_y**2))
    print(manhattan_dist)
    if ((manhattan_dist) > 1):
      HAL.setV(manhattan_dist * 0.4)
    else:
      print(" a menos de 1")
      HAL.setV(0)
      break

    
  return

#---------------------------------------
map_url = '/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png'
map_data = MAP.getMap(map_url)

grid = np.full(map_data.shape, 255)

start_pos = get_car_pos()
current_target = None
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
    
 

while True:
    
    if goal_pose != current_target:
        current_target = goal_pose
    grid = bfs_search(map_data, new_target_map, start_pos)
    if grid[start_pos[1], start_pos[0]] == 0:
      print("starting in an obstacle")
    path = get_path_coords(grid, new_target_map, start_pos)
    # Normalize the grid to show it
    grid_normalized = normalize_grid(grid)
    GUI.showNumpy(grid_normalized)
    path_to_show = [[x, y] for x, y in path]
    GUI.showPath(path_to_show)
    #--------------------------------------
    resulting_vectors = path_into_vectors(path)
    vectors_from_path = [[x, y] for coord in resulting_vectors for x, y in coord]
    result_vector = vectors_from_path[1:]
    print("REsult vector", result_vector)
    #--------------------------------------
    
    for i in range(len(result_vector)):
      sleep(15)
      print("Result Vector")
      print(result_vector[i][0])
      print(result_vector[i][1])
      #spin
      print("SPIN")
      att_vect(result_vector[i][0], result_vector[i][1])
      print("FINISHED SPIN")
      #move
      print("MOVE")
      move_to_target(result_vector[i][0], result_vector[i][1])
      print("FINISHED MOVEMENT")
      
