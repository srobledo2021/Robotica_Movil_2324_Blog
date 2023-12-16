import numpy as np
from GUI import GUI
from HAL import HAL
import MAP
import time

N_PARTICLES = 10

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

def dda_algorithm(x0, y0, x1, y1):
    """ DDA algorithm for line drawing between two points (x0, y0) and (x1, y1)."""
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x, y = x0, y0
    points = []

    for _ in range(steps):
        points.append((int(round(x)), int(round(y))))
        x += x_increment
        y += y_increment

    return points

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



def compute_particle_weights(particles, robot_laser_data, map):
    """ Calcula los pesos de las partículas basándose en la similitud con los datos del láser del robot."""
    weights = []

    for particle in particles:
        particle_laser_data = simulate_lasers(particle, map)
        #print(robot_laser_data)
        #print(particle_laser_data)
        # Ensure that both particle_laser_data and robot_laser_data are non-empty
        if len(particle_laser_data) == 0 or len(robot_laser_data) == 0:
            similarity = 0.0
        else:
            # Compute cosine similarity
            similarity = np.dot(particle_laser_data, robot_laser_data) / (
                np.linalg.norm(particle_laser_data) * np.linalg.norm(robot_laser_data)
            )

        # Convert similarity to a weight between 0 and 1
        weight = 0.5 + 0.5 * similarity  # Scales similarity to the range [0, 1]
        weights.append(weight)

    weights = np.array(weights)
    weights /= np.sum(weights)  # Normalizar pesos para que sumen 1

    return weights


def resample_particles(particles, weights,threshold=0.5):
    """Resamplea las partículas basándose en sus pesos."""
    indices = np.where(weights >= threshold)[0]
    if len(indices) == 0:
        # If no particles exceed the threshold, randomly select a subset
        indices = np.random.choice(np.arange(len(particles)), size=N_PARTICLES, replace=True)
    return particles[indices], indices


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
        for i in range(N_PARTICLES):
            v = 0.3 
            w = 0.8 

            particles[i, 0] += v * np.cos(particles[i, 2])
            particles[i, 1] += v * np.sin(particles[i, 2])
            particles[i, 2] += w
            

        #------------Particle weight-----------------------------------
        '''
        car_yaw = gui.getRobotPose()[2]
        print(car_yaw)
        coincidence_particles= []
        
        for particle in particles:
            x, y, yaw = particle[:3]
            #print(F"Laser X, Y, yaw:\n{x,y,yaw}")
            if ((car_yaw <= 0.5 + yaw) and (car_yaw >= yaw - 0.5)):
                coincidence_particles.append(particle)
                print("DENTROOO")
                print(particle)
        
        # Iterar sobre el tiempo
        for _ in range(10):  # Puedes ajustar el número de iteraciones según tus necesidades
            # Calcular pesos de las partículas
            weights = compute_particle_weights(particles, robot_laser_data, map)

            # Resamplear partículas
            particles = resample_particles(particles, weights)

            # Actualizar la GUI y esperar
            gui.updateGUI(block=True)


        gui.showParticles(particles[:, :3],weights)
        '''
        # Compute particle weights based on similarity to robot's laser data
        #weights = compute_particle_weights(particles, robot_laser_data, map)

        # Resample particles based on their weights
        #particles = resample_particles(particles, weights)
    
        #-------------LAST THING TO DO IS JUST PRINT------------------------------------------------------------------
        
        # Show the particles in the GUI
        gui.showParticles(particles [:,:3])

        # Update the GUI image and wait
        gui.updateGUI(block=True)


    
if __name__ == '__main__':
    main()
