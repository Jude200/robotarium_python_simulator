import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
from rps.utilities.misc import *
from rps.utilities.graph import *
from utils import *
from const import *

import numpy as np
import time
import matplotlib.patches as patches

from robot import Robot
from envInfo import EnvInfo

N = 12
initial_conditions = np.array(np.mat("\
        -0.45 -0.15 0.15 0.45 -0.45 -0.15 0.15 0.45 -0.45 -0.15 0.15 0.45;\
          0.3   0.3  0.3  0.3     0     0    0    0  -0.3 -0.3 -0.3 -0.3;\
            0     0    0    0     0     0    0    0     0    0    0    0"))

r = robotarium.Robotarium(number_of_robots=N, show_figure=True, initial_conditions=initial_conditions, sim_in_real_time=True)

# Parameters

# Variables
target_energy = TARGET_ENERGY
simulation_time = SIMULATION_TIME
# target_x, target_y  = generateTargetPosition()
target_x, target_y  = .5, .5

# Unique Cycle Controller
uni_cycle_controller = create_clf_unicycle_position_controller()
# Unique Cycle to Single Interator function
uni_to_si = create_uni_to_si_dynamics()
# barrier certificates for avoid collision
barrier_certificate = create_unicycle_barrier_certificate_with_boundary()
# single integrator to unique cycle
si_to_uni_dyn, _ = create_si_to_uni_mapping()


# Create Robots
robots = [
  Robot(id=i, x=initial_conditions[0, i], y=initial_conditions[1, i], orientation=initial_conditions[2, i], speed=SPEED) for i in range(N)
]

# Start Simulation

# Add target to the arene
r.axes.add_patch(patches.Circle([target_x, target_y], radius=.02))


while target_energy > 0 and simulation_time != 0:
  # update
  simulation_time += -1
  
  # Get Robots position
  x = r.get_poses()

  
  for robot in robots:
    # Set robot info
    robot.x = x[0, robot.id]
    robot.y = x[1, robot.id]
    robot.orientation = x[2, robot.id]
    
  # Detect the neighbors within the perception range
  for robot in robots:

    # Set environment information
    envInfo = setEnvironmentInfo(robot)
    envInfo.neighbors = [robots[i] for i in delta_disk_neighbors(x, robot.id, PERCEPTION_RANGE)]
    
    distance_to_target = np.linalg.norm(x[:2, robot.id].reshape((1, -1)) - np.array([[target_x, target_y]]))
    # 
    if distance_to_target < DETECTION_RANGE :
      robot.set_info_cible(target_x, target_y)
      r.left_led_patches[robot.id].set_fill(True)
      r.left_led_patches[robot.id].set_color("#3E4BDE")
    else:
      robot.set_info_cible(None, None)
      r.left_led_patches[robot.id].set_fill(False)
      
    # Attack
    if robot.cible_detected and distance_to_target < ATTACK_RANGE :
      robot.start_attack()
      r.right_led_patches[robot.id].set_fill(True)
      r.right_led_patches[robot.id].set_color("#FC0101")
    else :
      robot.stop_attack()
      r.right_led_patches[robot.id].set_fill(False)
    
    # Update the states of the robot
    robot.update(envInfo)
    
  # Update target energy
  for robot in robots:
    if robot.cible_attacked :
      target_energy -= ATTACK_STRENGTH
      # print(target_energy)
  
  # Update velocity
  dx = np.zeros((2, N))
  for robot in robots:
    v = np.array([[robot.vx], [robot.vy]])
    
    # Controll velocity to avoid error
    norm = np.linalg.norm(v)
    threshold = r.max_linear_velocity * .8
    if norm > threshold:
      v = threshold*v / norm
    dx[:, robot.id] = v.reshape((-1, ))
  
  # single integrator to uni-cycle dynamic
  dx = si_to_uni_dyn(dx, x)
  # barrier certificate to avoid collision
  dxi = barrier_certificate(dx, x)
  
  # set velocity to robotarium
  r.set_velocities(np.array(N), dxi)
  
  # step
  r.step()


r.call_at_scripts_end()



"""
______________________________________________________________________________
ALGORITHME : 

WHILE target_energy > 0 OR simulation_time != 0 :

    Update global variables
      - iteration
      - simulation time
    
    for robot in robots :
      - set robot attribut
      - get environment info
      
      - robot.move(environment)
      
        
    Control LEDS
        
    Mise à jour de l'affichage
______________________________________________________________________________

"""