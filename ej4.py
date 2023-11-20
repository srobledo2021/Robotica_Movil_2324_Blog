from GUI import GUI
from HAL import HAL
from MAP import MAP
import math
import heapq
import numpy as np
from queue import Queue

map_height= 400
map_width= 400


def gridToWorld(map_cell):
  world_x = map_cell[1] * 500 / 400 -250
  world_y = map_cell[0] * 500 / 400 -250
  
  return (world_x, world_y)
  
def normalize_grid(grid):
    max_grid = np.max(grid)
    return np.clip(grid * 255 / max_grid, 0, 255).astype('uint8')
  
def bfs(grid, start, goal):
    #400x400
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    parent = np.zeros((rows, cols, 2), dtype=int)
    
    start = tuple(start)
    goal = tuple(goal)
    
    
    pq = []  # Priority queue using heapq
    heapq.heappush(pq, (0, start))  # Tuple: (priority, cell)
    visited[start] = True
    
    while pq:
        current_priority, current_cell = heapq.heappop(pq)
        print(current_cell)
        if current_cell == goal:
            # Reconstruct path
            path = []
            while current_cell != start:
                path.append(current_cell)
                current_cell = tuple(parent[current_cell])
            path.append(start)
            print(path)
            return path[::-1]

        for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_cell = (current_cell[0] + i, current_cell[1] + j)
            if 0 <= next_cell[0] < rows and 0 <= next_cell[1] < cols and not visited[next_cell[0]][next_cell[1]] and grid[next_cell[0]][next_cell[1]] == 0:
                priority = np.linalg.norm(np.array(current_cell) - np.array(next_cell))  # Distance as priority
                heapq.heappush(pq, (priority, next_cell))
                visited[next_cell[0]][next_cell[1]] = True
                parent[next_cell] = current_cell
                
                

    # If no path is found
    return []

while True:
    #---------------------------------------
    # get the clicked target
    goal_pose  = GUI.getTargetPose()
    #get coordinates for actual location in map
    new_target_map = tuple(MAP.rowColumn(goal_pose))
    #start pose
    start_pose =(HAL.getPose3d().x, HAL.getPose3d().y)
    #---------------------------------------
    map_url = '/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png'
    map_data = MAP.getMap(map_url)
    #---------------------------------------
    # Convert world coordinates to map coordinates
    start_cell = MAP.rowColumn(start_pose)
    goal_cell = MAP.rowColumn(new_target_map)
    
  
    
    # This is an example test grid
    grid = np.zeros((map_height, map_width))
    for i in range(map_width):
      for j in range(map_height):
        if map_data[j][i] != 0: # Only draw if this cell is not an obstacle
            grid[j][i] = i

    
    
    #path = bfs(grid, start_cell, goal_cell)
    print(path)
    # Create a test path and show it
    path = [MAP.rowColumn(goal_pose),MAP.rowColumn(start_pose)]
    GUI.showPath(path)

    # Normalize the grid to show it
    grid_normalized = normalize_grid(grid)
    GUI.showNumpy(grid_normalized)
    
