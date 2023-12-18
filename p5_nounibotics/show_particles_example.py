import numpy as np
from GUI import GUI
from HAL import HAL
import MAP
import time

N_PARTICLES = 100

# Constant robot velocities
LINEAR_VEL = 0.5
ANGULAR_VEL = 0.8

# Time of the last propagation of the particles
last_update_time = time.time()

map = MAP.getMap()


def initialize_particles():
    """ Generate random particles in world coordinates (meters).
        X/Y values are constrained within the map limits.
        Yaw values are in the [0, 2*pi] range.
    """
    # Allocate space
    particles = np.zeros((N_PARTICLES, 4))
    # Get the limits from the MAP module
    x_low, y_low = MAP.WORLD_LIMITS_LOW
    x_high, y_high = MAP.WORLD_LIMITS_HIGH
    # Distribute randomly in the map
    for i in range(N_PARTICLES):
        particle = np.random.uniform(low=[x_low, y_low, 0.0],
                                  high=[x_high, y_high, 2*np.pi],
                                  size=(3,))
        particle_map = MAP.worldToMap(particle[0], particle[1], particle[2])
        while (map[particle_map[1], particle_map[0]] == 0):  # si es 0 es un obstáculo
            particle = np.random.uniform(low=[x_low, y_low, 0.0],
                                    high=[x_high, y_high, 2*np.pi],
                                    size=(3,))
            particle_map = MAP.worldToMap(particle[0], particle[1], particle[2])
        particles[i,:3] = particle

    return particles
'''

def simulate_lasers(particle, map):
    """ Simula los láseres virtuales para una partícula en el mapa usando el algoritmo DDA."""
    x, y, yaw = particle[:3]
    laser_angles = np.linspace(-np.pi / 2, np.pi / 2, num=180)  # Ángulos del láser
    laser_distances = []

    for angle in laser_angles:
        dx = np.cos(yaw + angle)
        dy = np.sin(yaw + angle)

        start_x, start_y, _ = MAP.worldToMap(x, y, yaw)
        end_x = int(round(x + 10 * dx))  # Extend the ray by 10 units
        end_y = int(round(y + 10 * dy))

        points = dda_algorithm(start_x, start_y, end_x, end_y)

        for point in points:
            if not (0 <= point[0] < map.shape[1] and 0 <= point[1] < map.shape[0]):
                break  # Fuera de los límites del mapa

            if map[point[1], point[0]] == 1:  # Si es un obstáculo
                distance = np.sqrt((point[0] - start_x)**2 + (point[1] - start_y)**2)
                laser_distances.append(distance)
                break

    return np.array(laser_distances)

# Rest of the code remains unchanged





def resample_particles(particles, weights,threshold=0.5):
    """Resamplea las partículas basándose en sus pesos."""
    indices = np.where(weights >= threshold)[0]
    if len(indices) == 0:
        # If no particles exceed the threshold, randomly select a subset
        indices = np.random.choice(np.arange(len(particles)), size=N_PARTICLES, replace=True)
    return particles[indices], indices

'''

def compute_particle_weights(particles):
    """ Compute the weight of each particle.
        This function should generate a virtual laser measurement
        for each particle and compute the error (difference)
        between the virtual laser and the actual sensor measurement.

        This example function just generates silly weights.
    """
    weights = np.arange(particles.shape[0], dtype=np.float32)
    return weights

'''
def compute_particle_weights(particles):
    """ Calcula los pesos de las partículas basándose en la similitud con los datos del láser del robot."""
    weights = []

    for particle in particles:
        particle_laser_data = simulate_lasers(particle, robot)
        robot_laser_data = HAL.getLaserData()
        if len(particle_laser_data) == 0 or len(robot_laser_data) == 0:
            similarity = 0.0
        else:
            similarity = np.dot(particle_laser_data, robot_laser_data) / (
                np.linalg.norm(particle_laser_data) * np.linalg.norm(robot_laser_data)
            )

        weight = 0.5 + 0.5 * similarity  # Scales similarity to the range [0, 1]
        weights.append(weight)

    weights = np.array(weights)
    weights /= np.sum(weights)  # Normalizar pesos para que sumen 1

    return weights
'''

def resample_particles(old_particles, weights):
    """ Resample the set of particles given their weights. """
    # Allocate space for new particles
    particles = np.zeros((N_PARTICLES, 3))

    # Normalize the weights so the total sum is 1
    weights /= np.sum(weights)
    print(F"Normalized weights: {weights}")

    # Get random indices from the list of particles
    selected_idx = np.random.choice(N_PARTICLES, replace=True, size=N_PARTICLES, p=weights)
    print(F"Selected indices:\n{selected_idx}")
    print(F"Selected particles:\n{old_particles[selected_idx]}")
    particles = old_particles[selected_idx]
    return particles

def update_particle_pose(particle, dt):
    """ Update the pose of a particle in the dt period.
        Add a random Gaussian noise to the movement.
    """
    yaw = particle[2]
    # Estimate robot movement in dt according to the set velocities
    dx = dt * LINEAR_VEL * np.cos(yaw)
    dy = dt * LINEAR_VEL * np.sin(yaw)
    dyaw = dt * ANGULAR_VEL
    # Add this movement to the particle, with an extra Gaussian noise
    particle[0] += dx + np.random.normal(0.0, 0.02)
    particle[1] += dy + np.random.normal(0.0, 0.02)
    particle[2] += dyaw + np.random.normal(0.0, 0.01)

def propagate_particles(particles):
    """ Estimate the movement of the robot since the last update
        and propagate the pose of all particles according to this movement.
    """
    global last_update_time
    # Get the time diference since the last update
    current_time = time.time()
    dt = current_time - last_update_time
    # Update all particles according to dt
    for p in particles:
        update_particle_pose(p, dt)
    # Reset the update time
    last_update_time = current_time
    return particles


def simulate_lasers(particle):
    """ Simula los láseres virtuales para una partícula en el mapa usando el algoritmo DDA."""
    x, y, yaw = particle[:3]
    laser_angles = np.linspace(-np.pi / 2, np.pi / 2, num=180)  # Ángulos del láser
    laser_distances = []

    for angle in laser_angles:
       
        laser_data = HAL.getLaserData()

        for point in laser_data:
            if not (np.isinf(point[0]) and np.isinf(point[1])):
                laser_distances.append(np.sqrt(point[0]**2 + point[1]**2))
                break

    return np.array(laser_distances)

#Ahora lo que queda por hacer es ver a donde apunta con el
# laser cada particula y comparar esto con los datos del 
# robot de su laser. Los que mas se asemejen se mantiene y los que no se descartan.
# Se usa lo de dda para los láseres virtuales.
def main():
    #START
    #-------------Set of particles--------------------------------------------
    # Create the GUI object
    gui = GUI()
    # Initialize random particles
    particles = initialize_particles()
    #print(F"Particles:\n{particles}")
   
    #---------Robot moves----------------------------------------------------------------------
    # Create a HAL (robot) object
    robot = HAL()
    # Set a custom initial pose
    robot.pose[0] = 1.1
    # Create a GUI object and link it with the robot
    gui = GUI(robot=robot)
    #print(F"Robot pose: {gui.getRobotPose()}")

    # Set a small velocity
    robot.setV(0.3)
    robot.setW(0.8)
    
    
    while True:
        # Get some laser data and show it in the GUI
        robot_laser_data = robot.getLaserData()
        gui.showLaser(robot_laser_data)

        # Robot pose is automatically updated inside the GUI "updateGUI"
        # robot.updatePose()
        gui.updateGUI()
        time.sleep(0.1)

        #----------Particles mimic movement---------------------------------------------
        # Move the particles to mimic the movement of the robot
        particles = propagate_particles(particles)

        #------------Particle weight-----------------------------------
        # Compute particle weights based on similarity to robot's laser data
        #weights = compute_particle_weights(particles, robot_laser_data, map)
        weights = compute_particle_weights(particles)
        # Resample particles based on their weights
        particles = resample_particles(particles, weights)
    
        #-------------LAST THING TO DO IS JUST PRINT------------------------------------------------------------------
        
        # Show the particles in the GUI
        gui.showParticles(particles [:,:3])

        # Update the GUI image and wait
        gui.updateGUI(block=True)


    
if __name__ == '__main__':
    main()
