# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:21:52 2021

@author: Zac
"""

import numpy as np

# =============================================================================
# Adjustable Variables
# =============================================================================

# Time allotted for the simulation
sim_time = 8.6 # sec

# Mass of the rocket including the motor
initial_mass = 1.0 # kg

# Final mass of the rocket, determined from the initial mass and subtracting
# the amount of propellant used. Based on Estes F-15 motor 
final_mass = initial_mass - 0.0600 # kg



# =============================================================================
# idk what to call yet
# =============================================================================

# Returns an array of the changing mass of the rocket throughout the simulation
def calculate_mass():
    # Burntime of the Estes F-15 motor, used to calculate the change of mass as
    # propellant is used up
    burntime = 3.450 # sec
    
    # Mass of the rocket as it loses mass
    mass = np.linspace(initial_mass, final_mass,
                       num = int(burntime * 1000) + 1)
    
    # Time left in simulation where the rocket does not lose mass
    remaining_time = int ((sim_time - burntime) * 1000) + 1
    
    # Mass does not change for the rest of the sim
    for x in range(remaining_time):
        mass = np.append(mass, final_mass)
        
    return mass




# =============================================================================
# Arrays for Simulation Data
# =============================================================================

time = np.arange(0.0, sim_time + 0.001, 0.001)
mass = calculate_mass()
thrust = []
accel = []
velocity = []
position = []








