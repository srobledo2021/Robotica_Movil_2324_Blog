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


def update_particle_weight(particle, sensor_data):
    # Implement an observation model to calculate the weight based on sensor data
    expected_image = generate_expected_image(particle)
    image_difference = calculate_image_difference(sensor_data, expected_image)

    # Update the particle's weight based on the image difference
    particle[3] = 1.0 / (1.0 + image_difference)

#def generate_expected_image(particle):
    # Implement a function to generate the expected image based on the particle's position
    # You can use HAL.getImage(), HAL.getPose3d().x, HAL.getPose3d().y, etc.
    # Return the expected image
def generate_expected_image(particle):
    # Assume a simple grid-based environment
    grid_size = 400
    grid_cell_size = 5

    # Initialize an empty image
    expected_image = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    # Simulate the presence of an object in the environment
    object_position = (50, 50)
    object_radius = 5

    for i in range(grid_size):
        for j in range(grid_size):
            # Check if the pixel is within the object's radius
            distance_to_object = math.sqrt((i - object_position[0])**2 + (j - object_position[1])**2)
            if distance_to_object <= object_radius:
                expected_image[i][j] = 255  # Set pixel intensity to simulate an object

    return expected_image


#def calculate_image_difference(observed_image, expected_image):
    # Implement a function to calculate the difference between observed and expected images
    # You may use image processing techniques or simple pixel-wise comparison
    # Return a value indicating the difference
def calculate_image_difference(observed_image, expected_image):
    # Ensure both images have the same dimensions
    if len(observed_image) != len(expected_image) or len(observed_image[0]) != len(expected_image[0]):
        print("Image dimensions do not match")

    # Calculate pixel-wise absolute difference
    total_difference = 0
    for i in range(len(observed_image)):
        for j in range(len(observed_image[0])):
            total_difference += abs(observed_image[i][j] - expected_image[i][j])

    # Normalize the difference by the total number of pixels
    num_pixels = len(observed_image) * len(observed_image[0])
    normalized_difference = total_difference / num_pixels

    return normalized_difference

#-----------------------------------------------------------------------------------

particles = initialize_particles()

# Main loop
while True:
    # Move the robot and read sensor data
    HAL.setV(1.0)  # Set linear speed
    HAL.setW(0.0)  # Set angular velocity
    distance = 1.0  # Example distance moved by the robot
    sensor_data = HAL.getImage()  # Example sensor data
    
    move_particles(particles, distance)
    
    for particle in particles:
        update_particle_weight(particle, sensor_data)

    # Display particles on the GUI
    GUI.showParticles(particles)

    
