from GUI import GUI
from HAL import HAL
from MAP import MAP
import math
import heapq
import numpy as np
import queue
import time

map_height= 400
map_width= 400

DISTANCE = 1
KSPEED = 0.02
ANG_DIFF = 0.1
K_MANHATTAN=0.5

def gridToWorld(map_cell):
  world_x = map_cell[1] * 500 / map_height -250
  world_y = map_cell[0] * 500 / map_width -250
  
  return (world_x, world_y)
  
def normalize_grid(grid):
    max_grid = np.max(grid)
    return np.clip(grid * 255 / max_grid, 0, 255).astype('uint8')
  

def get_path_coords(grid, start_pos):
    current_coord = start_pos
    path = []
    while (grid[current_coord[1], current_coord[0]] != 0):
        path.append(current_coord)

        neighbors = [
            # U
            (current_coord[0], current_coord[1] - 1),
            # D
            (current_coord[0], current_coord[1] + 1), 
            # L
            (current_coord[0] - 1, current_coord[1]), 
            # R
            (current_coord[0] + 1, current_coord[1]),
            # UL
            (current_coord[0] - 1, current_coord[1] - 1),
            # DL
            (current_coord[0] - 1, current_coord[1] + 1), 
            # UR
            (current_coord[0] + 1, current_coord[1] - 1), 
            # DR
            (current_coord[0] + 1, current_coord[1] + 1),  
        ]

        next_pos = None
        less_cost = float("inf")

        for neighbor in neighbors:
            if (0 <= neighbor[0] < grid.shape[1] and 0 <= neighbor[1] < grid.shape[0] and grid[neighbor[1], neighbor[0]] < less_cost ):
                less_cost = grid[neighbor[1], neighbor[0]]
                next_pos = neighbor


        if next_pos is not None:
            current_coord = next_pos

    path.append(current_coord)
    return path


def path_into_vectors(full_path,goal):

    current_vector = [full_path[0]]
    result_vectors  = []
    for i in range(1, len(full_path)):
      if i == len(full_path) - 1:
          next_grid = full_path[i]
      else:
        next_grid = full_path[i + 1]
        grid_on = full_path[i]
        prev_grid = full_path[i - 1]

        # Upwards vector
        if grid_on[1] == prev_grid[1] and grid_on[1] != next_grid[1]:
            current_vector.append(grid_on)
            continue

        # Right vector
        if grid_on[0] == prev_grid[0] and grid_on[0] != next_grid[0]:
            current_vector.append(grid_on)
            continue
        
        # UP-Left
        if (grid_on[0] - grid_on[1] == prev_grid[0] - prev_grid[1]) and \
                (grid_on[0] - grid_on[1] != next_grid[0] - next_grid[1]):
            current_vector.append(grid_on)
            continue

        #UP-RIGHT
        if (grid_on[0] + grid_on[1] == prev_grid[0] + prev_grid[1]) and \
                (grid_on[0] + grid_on[1] != next_grid[0] + next_grid[1]):
            current_vector.append(grid_on)
            continue

        else:
            continue

    result_vectors.append(current_vector)
    result_vectors.append([goal])
    return result_vectors

    
def orientate(x_rel, y_rel):

    pos = [x_rel, y_rel]
    angle = gridToWorld(pos)
    car_yaw = HAL.getPose3d().yaw 

    #get car and goal angles
    atan_val = math.atan2(angle[0] - HAL.getPose3d().x , angle[1]- HAL.getPose3d().y)
    if  atan_val <= 0:
      atan_val += 2 * math.pi
    
    if car_yaw < 0:
      car_yaw = -car_yaw 
    else:
      car_yaw = 2 * math.pi - car_yaw
    car_angl = math.degrees(car_yaw)
    goal_ang = (math.degrees(atan_val) - 90)

    #difference in angles (face objective)
    while abs(car_angl - goal_ang) > ANG_DIFF:
      car_yaw = HAL.getPose3d().yaw 
      if car_yaw < 0:
        car_yaw = -car_yaw 
      else:
        car_yaw = 2 * math.pi - car_yaw
      car_angl = math.degrees(car_yaw)

      HAL.setW((car_angl - goal_ang)*KSPEED)
    HAL.setW(0)
    return  


def move_forward(x_rel, y_rel):
  while True :
    car_pos = tuple(MAP.rowColumn([HAL.getPose3d().x, HAL.getPose3d().y]))
    manhattan_dist = math.sqrt((abs(x_rel - car_pos[0])**2) + (abs(y_rel - car_pos[1])**2))
    if ((manhattan_dist) > DISTANCE):
      HAL.setV(manhattan_dist * K_MANHATTAN)
    else:
      HAL.setV(0)
      break

  return

def bfs_search(map_array, target_map, start_pos):

    priority_queue = queue.PriorityQueue()
    visited_positions = set()
    visited_positions.add(target_map)

    #Insert Target Node into the priority queue
    priority_queue.put((0, target_map))

    while not priority_queue.empty(): 
        #Pop node from priority queue
        cost, current_node = priority_queue.get()
        #Atart node End
        if current_node == start_pos:
            break

        # Whenever you find an obstacle
        if map_array[current_node[1], current_node[0]] == 0:  
            # obstacle value = 0
            continue

        # Assign weight to neighbors of c if previously unassigned
        grid[current_node[1], current_node[0]] = cost

        # Get neighbors and insert them
        neighbors = [
            # U
            (current_node[0], current_node[1] - 1),
            # D
            (current_node[0], current_node[1] + 1), 
            # L
            (current_node[0] - 1, current_node[1]), 
            # R
            (current_node[0] + 1, current_node[1]),
            # UL
            (current_node[0] - 1, current_node[1] - 1),
            # DL
            (current_node[0] - 1, current_node[1] + 1), 
            # UR
            (current_node[0] + 1, current_node[1] - 1), 
            # DR
            (current_node[0] + 1, current_node[1] + 1),  
        ]

        for neighbor in neighbors:
            if (neighbor[0] < 0 or neighbor[0] >= grid.shape[1] or neighbor[1] < 0 or neighbor[1] >= grid.shape[0]):
                continue

            # Already visited neighbor?
            if neighbor in visited_positions:
                continue

            # Grid with costs
            if neighbor[0] == current_node[0] or neighbor[1] == current_node[1]:
                grid[neighbor[1], neighbor[0]] = cost + 1
            else:
                grid[neighbor[1], neighbor[0]] = cost + math.sqrt(2)

            # Update priority queue
            priority_queue.put((grid[neighbor[1], neighbor[0]], neighbor))
            # Mark as visited
            visited_positions.add(neighbor)
    return grid


def check_reached_goal(result_path):
    if i == len(result_path) - 1:
        HAL.setV(0)
        HAL.setW(0)
        return True

#---------------------------------------
map_url = '/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png'
map_data = MAP.getMap(map_url)
grid = np.full(map_data.shape, 255)
#---------------------------------------
#start pose
start_pose =HAL.getPose3d()
pos=[start_pose.x, start_pose.y]
#---------------------------------------
# Convert world coordinates to map coordinates
start_cell = tuple(MAP.rowColumn(pos))
# get the clicked target
goal_pose  = GUI.getTargetPose()
#get coordinates for actual location in map
new_target_map = tuple(MAP.rowColumn(goal_pose))

 
while True:
    
    #get map with costs using BFS search algorythm
    grid = bfs_search(map_data, new_target_map, start_cell)
    #get the path
    path = get_path_coords(grid, start_cell)
    # Normalize the grid to show it
    grid_normalized = normalize_grid(grid)
    GUI.showNumpy(grid_normalized)
    #show path on display
    path_to_show = [[x, y] for x, y in path]
    GUI.showPath(path_to_show)
    #--------------------------------------
    #split path into vectors
    resulting_vectors = path_into_vectors(path,new_target_map)
    vectors_from_path = [[x, y] for coord in resulting_vectors for x, y in coord]
    result_path = vectors_from_path[1:]
    #--------------------------------------
    while True:
        for i in range(len(result_path)):
            orientate(result_path[i][0], result_path[i][1])
            move_forward(result_path[i][0], result_path[i][1])
            #Reach goal
            if (check_reached_goal(result_path) == True):
                break
                
