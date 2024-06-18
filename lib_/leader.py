# Import Robotarium utils
import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
from rps.utilities.transformations import *
from rps.utilities.misc import *
from rps.utilities.graph import *

# local import
from utils import *

# Import python package
import numpy as np
import matplotlib.patches as patches

# Parameters
N_agents = 6
initial_conditions = np.array(np.mat("\
    -0.15  0.15 -0.15  0.15; 0.15 -0.15 -0.15 0.15; 0 0 0 0")) ;

r = robotarium.Robotarium(number_of_robots=N_agents, initial_conditions=generate_initial_conditions(N_agents))

x, y = generateTargetPosition()

waypoint = np.array([[x], [y]])

# plot way point
r.axes.add_patch(patches.Circle([x, y], radius=.02))

iterations = 1000 
# leader controller
si_controller = create_si_position_controller()

# certificate barrier
barrier_certificate = create_single_integrator_barrier_certificate_with_boundary()

# Converter
_, uni_to_si = create_si_to_uni_mapping()
si_to_uni = create_si_to_uni_dynamics()

target_found = np.zeros((1, N_agents))

# Leader index
leader_index = 0

# Laplacien Graph
followers = completeGL(N_agents-1)
GL = np.eye(N_agents)
GL[1:, 1:] = followers
GL[1, 1] += 1
GL[1, 0], GL[0, 1] = -1, -1

# 
dxi_ = np.zeros((2, N_agents))

# Velocity Paramaters
# a : coef V_i
# b : coef V_leader
# c : V_others
a, b, c = .7, .2, .1

for i in range(iterations):
    x = r.get_poses()
    x_si = uni_to_si(x)
    
    # for i in range(N_agents) : 
    #     ...
    
    # Leader control
    dxi = si_controller(x_si[:, leader_index].reshape(-1, 1), waypoint)
    dxi_[:, leader_index] = dxi.reshape(-1, )
    
    # Formation Controller
    for i in range(N_agents):
        if i != leader_index :
            neighbors = topological_neighbors(GL, i)
            
            for j in neighbors:
                dxi_[:, i] = (a-c)*dxi_[:, i] + (b-c)*dxi_[:, leader_index] + c * np.sum(dxi_, axis=1)
    
    
    dxu = barrier_certificate(dxi_, x_si)
    
    r.set_velocities(np.arange(N_agents), si_to_uni(dxu, x))

    # controlle LEDs
    if np.linalg.norm(x[:2, leader_index].reshape(-1, 1) - waypoint) < 0.1:
        if not target_found[:, leader_index] :
            r.left_led_patches[leader_index].set_fill(True)
            r.left_led_patches[leader_index].set_color("#3E4BDE")
    
    r.step()
    
r.call_at_scripts_end()