from GUI import GUI
from HAL import HAL
from MAP import MAP
import numpy as np
from queue import Queue

map_height= 400
map_width= 400


def bfs(grid, start, goal):
    rows, cols = grid.shape
    visited = set()
    queue = Queue()
    parent = {}

    queue.put(start)
    visited.add(tuple(start))

    while not queue.empty():
        current = queue.get()

        if current == goal:
            break

        for neighbor in get_neighbors(current, rows, cols):
            if neighbor not in visited and grid[neighbor[0], neighbor[1]] == 0:  # Check if the neighbor is free
                queue.put(neighbor)
                visited.add(tuple(neighbor))
                parent[neighbor] = current

    path = reconstruct_path(start, goal, parent)
    return path

def get_neighbors(cell, rows, cols):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dir in directions:
        neighbor = (cell[0] + dir[0], cell[1] + dir[1])
        if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
            neighbors.append(neighbor)

    return neighbors
    
def reconstruct_path(start, goal, parent):
    path = [goal]
    current = goal

    while current != start:
        current = parent[current]
        path.append(current)

    path.reverse()
    return path
    

while True:
    #---------------------------------------
    # get the clicked target
    goal_pose  = GUI.getTargetPose()
    #get coordinates for actual location in map
    new_target_map = tuple(MAP.rowColumn(goal_pose))
    #start pose
    start_pose = HAL.getPose3d()
    print(start_pose)
    #---------------------------------------
    map_url = '/RoboticsAcademy/exercises/static/exercises/global_navigation_newmanager/resources/images/cityLargenBin.png'
    map_data = MAP.getMap(map_url)
    #---------------------------------------
    grid = (map_data > 127).astype(int)
    # Convert world coordinates to map coordinates
    start_cell = MAP.rowColumn(start_pose)
    goal_cell = MAP.rowColumn(new_target_map)
    
    
    # Find path using BFS
    path = bfs(grid, start_cell, goal_cell)
    
    # Display the path on the map
    GUI.showPath(path)
    

    #grid = (map_data > 127).astype(int)
    #grid = np.zeros((map_height,map_width))
    #GUI.showNumpy(grid)
    
    #path = [MAP.rowColumn(goal_pose ),MAP.rowColumn((HAL.getPose3d().x,HAL.getPose3d().y))]  
    #GUI.showPath(path)
