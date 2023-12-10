from GUI import GUI
from HAL import HAL
import random
import math


num_particles = 1000

# Enter sequential code!
def initialize_particles():
    # Initialize particles with random positions and equal weights
    particles = [[random.uniform(0, 400), random.uniform(0, 400), random.uniform(0, 2 * math.pi), 1.0] 
                  for _ in range(num_particles)]
    return particles
    
def move_particles(particles, distance):
    for particle in particles:
        move_particle(particle, distance)
    
    
def move_particle(particle, distance):
    # Implement a simple motion model for particle movement
    angle_noise = random.uniform(-0.1, 0.1)
    distance_noise = random.uniform(-0.1, 0.1)

    particle[0] += distance * math.cos(particle[2]) + distance_noise
    particle[1] += distance * math.sin(particle[2]) + distance_noise
    particle[2] += angle_noise

    # Ensure angles are within [0, 2 * pi)
    particle[2] %= 2 * math.pi

particles = initialize_particles()


# Main loop
while True:
    # Move the robot and read sensor data
    HAL.setV(1.0)  # Set linear speed
    HAL.setW(0.0)  # Set angular velocity
    distance = 1.0  # Example distance moved by the robot
    sensor_data = HAL.getImage()  # Example sensor data
    
    move_particles(particles, distance)
    # Display particles on the GUI
    GUI.showParticles(particles)

    
