"""
Created on Sun Dec 19 12:39:27 2021

@author: Zac
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style('ticks')
sns.set_context('paper')


# =============================================================================
# Adjustable Variables
# =============================================================================

# The length between the bottom of the rocket and the TVC axis of rotation
length_TVC = 0.055 # meters

# The length between the bottom of the rocket and the center of mass
length_COM = 0.5 # meters

# The total mass of the rocket 
rocket_total_mass = 1.0000 # kg

# The initial angle that the rocket is positioned at
initial_theta = 0.0 # deg

# Target angle of the rocket
target_theta = 0.0 # deg

# The initial angle of the TVC
initial_alpha = 0.0 # deg

# Simulation time
sim_time = 8.6 # sec

# Runtime frequency of flight computer

# print(end_time - start_time) = 0.010 # sec

# PID Constants
kp = 0.1
ki = 0
kd = 0.05


# =============================================================================
# Thrust curve of the Estes F15 motor
# =============================================================================

def interpolate_thrust(sim_time):
    # Initial dataframe df from the .csv file
    df = pd.read_csv('Estes_F15.csv')

    # Getting rid of unwanted data from the .csv
    df = df.drop(range(0,3), axis=0)
    df = df.rename(columns={'motor:':'time','Estes F15':'thrust'})
    df = df.astype(float)
    df = df.reset_index(drop=True)

    # New dataframe df1 for interpolated data
    temp1 = np.empty(int(sim_time * 1000))
    temp1[:] = np.NaN
    dat = {'time': np.arange(0.0, sim_time, 0.001), 'thrust': temp1}
    df1 = pd.DataFrame(data=dat)
    
    # Merging the initial dataframe to new dataframe with 0.001s time intervals
    for x in range(len(df.index)):
        time = df.at[x, 'time']         # time reference for each thrust
        thrust = df.at[x, 'thrust']     # thrust at specified time
        
        index = int(time * 1000)
        df1.iloc[index, 1] = thrust
    
    # Linear interpolation of the data
    df1 = df1.interpolate(method='linear')

    return df1

def interpolate_mass(df, rocket_total_mass):
    # Estes F15 mass
    ''' F15_total_mass  = 0.1044 # kg '''
    F15_propellant_mass = 0.0600 # kg
    
    # New column for rocket mass
    df['mass'] = np.nan
    df.iloc[0, 2] = rocket_total_mass
    df.iloc[3450, 2] = rocket_total_mass - F15_propellant_mass
    
    # Linear interpolation of mass
    return df.interpolate(method='linear')

# Initializes the dataframe that stores sim data
def init():
    df = interpolate_thrust(sim_time)
    df = interpolate_mass(df, rocket_total_mass)
    df['acceleration'] = np.nan
    df['velocity'] = np.nan
    df['position'] = np.nan
    
    # at time = 0, initial values are 0
    df.iloc[0, 3:] = 0
    
    return df


# =============================================================================
# Simulation
# =============================================================================

def simulate(df, sim_time):
    for time in range(1, int(sim_time * 1000)): # milliseconds
    
        #Thrust and mass at current time of simulation
        thrust = df.at[time, 'thrust'] # N
        mass = df.at[time, 'mass'] # kg
        
        prev_position = df.at[time - 1, 'position'] # m   
        acceleration = thrust / mass - 9.8 # m/s^2
        
        # Thrust isn't high enough to lift off
        if prev_position == 0 and acceleration < 0:
            df.iloc[time, 3:] = 0
        # Lifted off
        else:
            # simulation step time
            dt = 0.001 # s
            prev_velocity = df.at[time - 1, 'velocity'] # m/s
            
            velocity = acceleration * dt + prev_velocity
            position = velocity * dt + prev_position
            
            # If the rocket is still in air, push values to dataframe
            if position > 0:
                df.loc[time, 'acceleration':'position'] = (acceleration, 
                                                           velocity, position)
            # Acceleration, velocity, and position stop when it lands
            else:
                df.iloc[time, 3:] = 0
            
    
# =============================================================================
# Plotting the Thrust Curve
# =============================================================================

def plot_graphs(df):
    # Subplot 1
    plt.subplot(211)
    ax = sns.lineplot(data=df, x='time', y='thrust', color='r')
    ax2 = ax.twinx()
    sns.lineplot(data=df, x='time', y='mass', color='g', ax=ax2)
    plt.xticks(np.arange(0.0, sim_time, 0.5))
    
    # Subplot 2
    plt.subplot(212)
    ax = sns.lineplot(data=df, x='time', y='position', color='b')
    ax2 = ax.twinx()
    sns.lineplot(data=df, x='time', y='acceleration', color='c', ax=ax2)
    plt.xticks(np.arange(0.0, sim_time, 0.5))
    
    # Saving to computer
    fig = ax.get_figure()
    fig.savefig('fig.png')
 
    
# =============================================================================
# PID Loop Control   
# =============================================================================
    
def PID(kp, ki, kd, expected_angle, current_angle, dt):
    
    global pid_i
    if pid_i is None:
        pid_i = 0
    global previous_error
    if previous_error is None:
        previous_error = 0
    
    pid_error = expected_angle - current_angle
    
    pid_p = kp * pid_error
    pid_i += ki * pid_error
    pid_d = kd * ((pid_error - previous_error) / dt)
    
    output = pid_p + pid_i + pid_d
    
    previous_error = pid_error
    
    return output
    
    
    
    
    
    
    
    
    
# =============================================================================
# Main
# =============================================================================    

df = init()
simulate(df, sim_time)
plot_graphs(df)

#output = PID(kp, ki, kd, target_theta, , loop_time)
   


    
# ADD ANGLE CALCULATIONS
# THEN NEED TO CALCULATE PID SHIT
# CONTACT RELLE?

    


    

    
    
    
    
    
    
    