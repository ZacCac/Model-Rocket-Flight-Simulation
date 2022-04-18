# """
# Created on Wed Dec 29 11:21:52 2021

# @author: Zac
# """

import numpy as np
import os.path
import estes_f15 as es
import pandas as pd
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)

# =============================================================================
# Initial Conditions
# =============================================================================

# Time allotted for the simulation
sim_time = 8.6 # sec

# Initial angle of the rocket (left = negative, right = positive)
initial_angle = 5.0 # deg

# Motor used for the simulation
motor = es.F15()

# Time between each step in the simulation (one millisecond)
dt = 0.001 # sec

# PID interval (10 milliseconds)
PID_interval = 0.010 # sec

# If no thrust curve has been created, create it
if not os.path.exists('interpolated_thrust.csv'):
    motor.interpolate_thrust(sim_time)

# Returns an array of the changing mass of the rocket throughout the simulation
def calculate_mass():

    # Initial mass of the rocket including the motor
    initial_mass = 1.0 # kg

    # Final mass of the rocket, determined from initial mass and subtracting
    # the amount of propellant used
    final_mass = initial_mass - motor.prop_mass # kg

    # Mass of the rocket as it loses mass
    mass = np.linspace(initial_mass, final_mass,
                       num = int(motor.burntime * 1000) + 1)
    
    # Time left in simulation where the rocket does not lose mass
    remaining_time = int ((sim_time - motor.burntime) * 1000) + 1
    
    # Mass does not change for the rest of the sim
    for x in range(remaining_time):
        mass = np.append(mass, final_mass)
        
    return mass

# =============================================================================
# Arrays for Simulation Data
# =============================================================================


arr_size = int(sim_time * 1000 + 1)

thrust = motor.thrust
mass = calculate_mass()

acceleration_x = np.zeros(arr_size)
acceleration_y = np.zeros(arr_size)
velocity_x = np.zeros([arr_size])
velocity_y = np.zeros([arr_size])
position_x = np.zeros([arr_size])
position_y = np.zeros([arr_size])

PID_angle = np.zeros([arr_size])


# =============================================================================
# PID
# =============================================================================

def PID():
    pid_p = 0
    pid_i = 0
    pid_d = 0



# =============================================================================
# Simulation
# =============================================================================

def simulate():
    for x in range(arr_size - 1):

        # Cannot start at time = 0
        row = int(x + 1)

        # Converting angle to radians
        rocket_angle = initial_angle * np.pi / 180

        # Calculating the accelerations [m/s^2]
        acceleration_y[row] = (
            np.cos(rocket_angle) * thrust[row] / mass[row] - 9.8)
        acceleration_x[row] = np.sin(rocket_angle) * thrust[row] / mass[row]

        # Previous values
        prev_position_y = position_y[row - 1]
        prev_position_x = position_x[row - 1]
        prev_velocity_y = velocity_y[row - 1]
        prev_velocity_x = velocity_x[row - 1]

        # Rocket will not go into -y coords if the rocket has negative 
        # acceleration
        if prev_position_y == 0 and acceleration_y[row] < 0:
            acceleration_y[row] = 0
            acceleration_x[row] = 0

        #Calculating velocity and position
        velocity_y[row] = acceleration_y[row] * dt + prev_velocity_y
        velocity_x[row] = acceleration_x[row] * dt + prev_velocity_x
        position_y[row] = velocity_y[row] * dt + prev_position_y
        position_x[row] = velocity_x[row] * dt + prev_position_x
        
# =============================================================================
# Plotting
# =============================================================================

def plot():

    fig, axs = plt.subplots(3, 3)
    fig.suptitle('Simulation Output')
    axs[0, 0].plot(thrust)
    axs[0, 0].set(xlabel='time (ms)', ylabel='Thrust (N)')
    axs[0, 1].plot(mass)
    axs[0, 1].set(xlabel='time (ms)', ylabel='mass (kg)')
    axs[0, 2].plot(acceleration_x)
    axs[0, 2].set(xlabel='time (ms)', ylabel='X Accel (m/s^2)')
    axs[1, 0].plot(acceleration_y)
    axs[1, 0].set(xlabel='time (ms)', ylabel='Y Accel (m/s^2)')
    axs[1, 1].plot(velocity_x)
    axs[1, 1].set(xlabel='time (ms)', ylabel='X Velocity (m/s)')
    axs[1, 2].plot(velocity_y)
    axs[1, 2].set(xlabel='time (ms)', ylabel='Y Velocity (m/s)')
    axs[2, 0].plot(position_x)
    axs[2, 0].set(xlabel='time (ms)', ylabel='X Position (m)')
    axs[2, 1].plot(position_y)
    axs[2, 1].set(xlabel='time (ms)', ylabel='Y Position (m)')
    axs[2, 2].plot(position_x, position_y)
    axs[2, 2].set(xlabel='X Position (m)', ylabel='Y Position (m)')
    
    #df_from_arr.index.name = 'time (ms)'
    #df_from_arr.plot(subplots=True, layout=(3,3))
    #df_from_arr.plot(y='ypos', x='xpos')#use_index=True)
    plt.show()

# =============================================================================
# Main
# =============================================================================

simulate()

#df = pd.DataFrame(
#    data=[thrust, mass, acceleration_x, acceleration_y, velocity_x ,
#    velocity_y, position_x, position_y])
#df = df.T
#df.columns = ['thrust', 'mass', 'accelx', 'accely', 'velocityx', 
#    'velocityy', 'xpos', 'ypos']
#df.to_csv('out.csv', sep=',', index=False)

plot()
