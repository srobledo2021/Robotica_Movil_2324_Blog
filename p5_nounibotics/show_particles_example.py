import numpy as np
from GUI import GUI
import MAP

N_PARTICLES = 100

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


def main():
    # Create the GUI object
    gui = GUI()
    
    # Initialize some random particles
    particles = initialize_particles()
    print(F"Particles:\n{particles}")
   
    #Ahora lo que queda por hacer es ver a donde apunta con el laser cada particula y comparar esto con los datos del robot de su laser. Los que mas se asemejen se mantieney los que no se descartan. SE usa lo de dda para los láseres virtuales.
    # Show the particles in the GUI
    gui.showParticles(particles [:,:3])

    # Update the GUI image and wait
    gui.updateGUI(block=True)

if __name__ == '__main__':
    main()
