import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
from rps.utilities.misc import *
from utils import *
from const import *

import numpy as np
import time
import matplotlib.patches as patches

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
target_x, target_y  = generateTargetPosition()

# Affichage

# Unique Cycle Controller
unique_cycle_controller = create_clf_unicycle_position_controller()
# Unique Cycle to Single Interator function
uni_to_si = create_uni_to_si_dynamics()
# barrier certificates for avoid collision
si_barrier_certificate = create_single_integrator_barrier_certificate()
# single integrator to unique cycle
si_to_uni_dyn, _ = create_si_to_uni_mapping()

# Create Robots
robots = []


# Start Simulation

# Algo 
r.axes.add_patch(patches.Circle([target_x, target_y], radius=.02))

"""
______________________________________________________________________________
ALGORITHME : 

WHILE target_energy > 0 OR simulation_time == 0 :
    Update global variables
    
    Environment information
    for robot in robots :
    
        robot.move()
        
    Control LEDS
        
    Mise à jour de l'affichage
______________________________________________________________________________
"""

for i in range(SIMULATION_TIME):
  poses = r.get_poses()

  dxu = unique_cycle_controller(poses, target_coordinate[:2, :])
  
  dxu = uni_to_si(dxu, poses)
  
  dxu = si_barrier_certificate(dxu, poses[:2, :])
  
  dx = si_to_uni_dyn(dxu, poses)
  
  r.set_velocities(np.arange(N), dx)
  
  r.step()
  

  # axes.plot(target_coordinate[0, :], target_coordinate[1, :], 'ro')

r.call_at_scripts_end()