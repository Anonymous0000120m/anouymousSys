import numpy as np
from scipy.integrate import odeint
import csv
import configparser

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    parameters = config['MissileParameters']
    initial_conditions = config['InitialConditions']
    simulation_params = config['SimulationParameters']
    
    mass = float(parameters['mass'])
    gravity = float(parameters['gravity'])
    cross_section_area = float(parameters['cross_section_area'])
    drag_coefficient = float(parameters['drag_coefficient'])
    
    x0 = float(initial_conditions['x_position'])
    y0 = float(initial_conditions['y_position'])
    vx0 = float(initial_conditions['x_velocity'])
    vy0 = float(initial_conditions['y_velocity'])
    
    start_time = float(simulation_params['start_time'])
    end_time = float(simulation_params['end_time'])
    num_time_steps = int(simulation_params['num_time_steps'])
    
    return mass, gravity, cross_section_area, drag_coefficient, x0, y0, vx0, vy0, start_time, end_time, num_time_steps

def missile_equations(state, t, mass, gravity, cross_section_area, drag_coefficient):
    x, y, vx, vy = state
    
    v = np.sqrt(vx**2 + vy**2)
    drag_force = 0.5 * drag_coefficient * cross_section_area * v**2
    
    ax = -drag_force / mass
    ay = -gravity - drag_force / mass
    
    return [vx, vy, ax, ay]

def main():
    config_file = 'missile_config.ini'
    mass, gravity, cross_section_area, drag_coefficient, x0, y0, vx0, vy0, start_time, end_time, num_time_steps = read_config(config_file)
    
    t = np.linspace(start_time, end_time, num_time_steps)
    initial_state = [x0, y0, vx0, vy0]
    
    result = odeint(missile_equations, initial_state, t, args=(mass, gravity, cross_section_area, drag_coefficient))
    
    x = result[:, 0]
    y = result[:, 1]
    vx = result[:, 2]
    vy = result[:, 3]
    
    with open('missile_trajectory.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'X Position', 'Y Position', 'X Velocity', 'Y Velocity'])
        for i in range(len(t)):
            writer.writerow([t[i], x[i], y[i], vx[i], vy[i]])
    
    print("CSV file 'missile_trajectory.csv' generated successfully.")

if __name__ == "__main__":
    main()
