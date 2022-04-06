import numpy as np
import pandas as pd
import os.path

class F15:
    '''
    A class used to contain all necessary information about the Estes F15 motor

    Attributes
    ----------
    burntime : float
        burntime of the motor [sec]
    total_mass : float
        total mass of the motor and propellant [kg]
    prop_mass : float
        mass of the propellant only [kg]
    thrust : ndarray
        thrust curve for the motor in 0.001 sec intervals

    Methods
    -------
    interpolate_thrust(self, sim_time)
        creates a thrust curve csv with the specified sim_time
        updates the thrust attribute

    '''
    def __init__(self):
        self.burntime = 3.450 # sec
        self.total_mass = 0.102 # kg
        self.prop_mass = 0.060 # kg

        # if the thrust curve is created, assign it to thrust variable
        if os.path.exists('interpolated_thrust.csv'):
            self.thrust = np.loadtxt('interpolated_thrust.csv', delimiter=',')


    def interpolate_thrust(self, sim_time):
        '''
        Parameters
        ----------
        sim_time : float
            length of simulation, used to create interpolated thrust [sec]
        ''' 

        # Initializing empty thrust array
        arr_size = int(sim_time * 1000 + 1)
        thrust = np.empty(arr_size, dtype='float')
        thrust[:] = np.NaN

        # Original array containing the thrust for the motor
        temp_thrust = np.loadtxt('original_thrust.csv', delimiter=',', comments='#')

        # Adding the values from the temp_thrust into new thrust array
        for row in temp_thrust:
            time_index = int(row[0] * 1000)

            thrust[time_index] = row[1]

        # No thrust after the motor burns out
        if sim_time > self.burntime:
            thrust[int(self.burntime * 1000):arr_size] = 0.0

        # Interpolating between data points
        thrust = pd.Series(thrust).interpolate().tolist()

        np.savetxt('interpolated_thrust.csv', thrust, delimiter=',', header='Thrust [N]')
               
        self.thrust = thrust
