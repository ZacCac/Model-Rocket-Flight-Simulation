# -*- coding: utf-8 -*-
# """
# Created on Wed Dec 29 11:21:52 2021

# @author: Zac
# """

import numpy as np
import os.path
import estes_f15 as es

# =============================================================================
# Initial Conditions
# =============================================================================

# Time allotted for the simulation
sim_time = 8.6 # sec

# Initial angle of the rocket (left = negative, right = positive)

# Motor used for the simulation
motor = es.F15()

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

time = np.arange(0.0, sim_time + 0.001, 0.001)
mass = calculate_mass()
thrust = motor.thrust

accel = np.array([0.0])
velocity = np.array([0.0])
position = np.array([0.0])










