from GUI import GUI
from HAL import HAL
import random

# Enter sequential code!

particle_filter = ParticleFilter(num_particles=100)
self.num_particles = num_particles
self.particles = self.initialize_particles()

def initialize_particles(self):
    # Initialize particles with random positions and equal weights
    particles = [[random.uniform(0, 100), random.uniform(0, 100), random.uniform(0, 2 * 3.1416), 1.0] 
                  for _ in range(self.num_particles)]
    return particles

def move_particles(self, distance, sensor_data):
    for i in range(self.num_particles):
        # Move the particle
        self.move_particle(i, distance)
        
        # Update the particle's weight based on sensor data
        self.update_particle_weight(i, sensor_data)
    
    # Resample particles based on weights
    self.resample_particles()

def move_particle(self, index, distance):
    # Implement your motion model here based on the robot's movement
    # You can use HAL.setV() and HAL.setW() to control the robot's motion
    # Update the particle's position (x, y, angle) accordingly

def update_particle_weight(self, index, sensor_data):
    # Implement the observation model here based on sensor data
    # You can use HAL.getImage() and other relevant functions
    # Update the particle's weight based on the observation model

def resample_particles(self):
    # Resample particles based on their weights
    weights = [particle[3] for particle in self.particles]
    new_particles = random.choices(self.particles, weights=weights, k=self.num_particles)
    self.particles = new_particles



# Main loop
while True:
        # Move the robot and read sensor data
        HAL.setV(1.0)  # Set linear speed
        HAL.setW(0.0)  # Set angular velocity
        distance = 1.0  # Example distance moved by the robot
        sensor_data = HAL.getImage()  # Example sensor data
        
        # Perform particle filter update
        particle_filter.move_particles(distance, sensor_data)
        
        # Display particles on the GUI
        GUI.showParticles(particle_filter.particles)
    
    # Cleanup
    HAL.close()
    
