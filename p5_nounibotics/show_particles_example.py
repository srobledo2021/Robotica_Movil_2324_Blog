import numpy as np
from GUI import GUI
from HAL import HAL
import MAP
import time

N_PARTICLES = 300

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

def simulate_lasers(particle, map):
    """ Simula los láseres virtuales para una partícula en el mapa."""
    x, y, yaw = particle[:3]
    laser_angles = np.linspace(-np.pi / 2, np.pi / 2, num=180)  # Ángulos del láser
    laser_distances = []

    for angle in laser_angles:
        dx = np.cos(yaw + angle)
        dy = np.sin(yaw + angle)
        distance = 0.0

        while True:
            distance += 0.1  # Incremento en la distancia
            map_x, map_y, map_yaw = MAP.worldToMap(x + distance * dx, y + distance * dy, yaw)
            
            if not (0 <= map_x < map.shape[1] and 0 <= map_y < map.shape[0]):
                break  # Fuera de los límites del mapa

            if map[map_y, map_x] == 1:  # Si es un obstáculo
                break

        laser_distances.append(distance)

    return np.array(laser_distances)

def compute_particle_weights(particles, robot_laser_data, map):
    """ Calcula los pesos de las partículas basándose en la similitud con los datos del láser del robot."""
    weights = []

    for particle in particles:
        particle_laser_data = simulate_lasers(particle, map)
        similarity = np.exp(-np.linalg.norm(particle_laser_data - robot_laser_data))
        weights.append(similarity)

    weights = np.array(weights)
    weights /= np.sum(weights)  # Normalizar pesos para que sumen 1

    return weights

def resample_particles(particles, weights):
    """ Resamplea las partículas basándose en sus pesos. """
    indices = np.random.choice(np.arange(len(particles)), size=N_PARTICLES, replace=True, p=weights)
    return particles[indices]


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
    print(F"Robot pose: {gui.getRobotPose()}")

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
    
    
        #------------Particle weight-----------------------------------
        
        car_yaw = gui.getRobotPose()[2]
        print(car_yaw)
        coincidence_particles= []
        '''
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

        #-------------LAST THING TO DO IS JUST PRINT------------------------------------------------------------------
        
        # Show the particles in the GUI
        gui.showParticles(particles [:,:3])

        # Update the GUI image and wait
        #gui.updateGUI(block=True)

    
if __name__ == '__main__':
    main()
