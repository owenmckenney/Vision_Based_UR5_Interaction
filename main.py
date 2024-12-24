# Main file to achieve real-time handtracking and UR5 movement

import time
import numpy as np
from UR5ClampedControl import UR5ClampedControl
from Camera import Camera
from PID import PID
        
def error(p1, p2):
    x_error = p1[0] - p2[0]
    y_error = p1[1] - p2[1]
    return x_error, y_error

def error_magnitude(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


if __name__ == "__main__":
    camera = Camera(0)
    
    # UR5 setup
    ip = "10.168.18.25"
    x_min, x_max = 0.2, 0.8
    y_min, y_max = -0.3, 0.3
    z_min, z_max = -0.01, 0.2
    
    ur5 = UR5ClampedControl(ip, x_min, x_max, y_min, y_max, z_min, z_max)
    
    # PID setup
    dt = 0.1
    kp = 0.5
    ki = 0.05 
    kd = 0.0
    x_pid = PID(dt, kp=kp, ki=ki, kd=kd)
    y_pid = PID(dt, kp=kp, ki=ki, kd=kd)
    
    # Home UR5 to inital position
    initial_ur5_position = [0.4, 0.2, 0.25, 0, -np.deg2rad(270), 0]
    initial_ur5_x = initial_ur5_position[0]
    initial_ur5_y = initial_ur5_position[1]
    ur5.moveL(initial_ur5_position ,velocity=0.05, acceleration=0.1)
    p = ur5.get_joint_positions()
    p[5] = np.deg2rad(65)
    ur5.moveJ(p, velocity=0.5)
    
    goal_reached = False
    start_number = "1432"
    start_sequence_init = False
    last_cube_pos = []

    while not goal_reached:
        st = time.time()
        
        if not start_sequence_init:
            start_sequence_init = camera.detect_startup(start_number)
            print("Starting movement sequence.")
            time.sleep(1)
        else:
            camera.get_frame()
            
            cube_position = camera.detect_cubes(output=False)[0]["centroid"]
            
            if cube_position is None:
                cube_position = last_cube_pos
                
            finger_count, hand_position = camera.detect_hand(output=False)
            
            x_e, y_e = error(cube_position, hand_position)
            error_mag = error_magnitude(cube_position, hand_position)
            
            x_control = x_pid.control(x_e) / 1000
            y_control = y_pid.control(y_e) / 1000
            
            if error_mag < 15:
                goal_reached = True
                ur5.close()
            try:
                xd = [x_control, y_control, 0, 0, 0, 0]
                ur5.speedL(xd, time=0.1, acceleration=0.1)
            except KeyboardInterrupt:
                print("Exit.")

            et = time.time()
            rt = et - st
            
            if abs(rt) < dt:
                time.sleep(dt - rt)
            
            et = time.time()
            rt = et - st
            
            print("----------")
            print(f"Frequency: {rt:.8f}, ")
            print(f"Error: ({x_e:.2f}, {y_e:.2f}), Error Magnitude: {error_mag:.2f}, Control: ({x_control:.2f}, {y_control:.2f})")
            print(f"Cube Position: ({cube_position[0]}, {cube_position[1]}), Hand Position: ({hand_position[0]}, {hand_position[1]})")
