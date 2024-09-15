import sys
from multiprocessing import Pool, Process
import time

import numpy as np
import matplotlib.patches as patches

from robot import Robot
from envInfo import EnvInfo
from const import *

import rps.robotarium as robotarium
from rps.utilities.barrier_certificates import *
from rps.utilities.controllers import *
from rps.utilities.misc import *
from rps.utilities.graph import *


class Simulator:
      def __init__(self):
            self.N = 12                          # Number of robots
            self.initial_conditions = np.array(np.mat("\
                              -0.45 -0.15 0.15 0.45 -0.45 -0.15 0.15 0.45 -0.45 -0.15 0.15 0.45;\
                                0.3   0.3  0.3  0.3     0     0    0    0  -0.3 -0.3 -0.3 -0.3;\
                                  0     0    0    0     0     0    0    0     0    0    0    0"))
            self.r = robotarium.Robotarium(
                  number_of_robots=self.N, 
                  show_figure=True, 
                  initial_conditions=self.initial_conditions, 
                  sim_in_real_time=True) 
            self.target_energy = TARGET_ENERGY
            self.simulation_time = SIMULATION_TIME
            self.safety_radius_plotting = False
            self.robots = [
                  Robot(
                        id = i,
                        x = self.initial_conditions[0, i],
                        y = self.initial_conditions[1, i],
                        orientation = self.initial_conditions[2, i],
                        speed = SPEED
                  ) for i in range(self.N)
            ]
            self.g = self.r.axes.scatter(self.initial_conditions[0, :],
                                         self.initial_conditions[1, :], 
                                         s=np.pi/4 * determine_marker_size(self.r, PERCEPTION_RANGE) , 
                                         marker="o", 
                                         facecolors='none',
                                         edgecolors="#007529", 
                                         linewidth=2) if self.safety_radius_plotting else None
            
            self.target_energy_caption = self.r.axes.text(.8, .9, "Energie : ", fontsize=10, color="k")
            self.time_caption = self.r.axes.text(.8, .8, "Temps : ", fontsize=10, color="k")
            
            # g = r.axes.scatter(x[0,:], x[1,:], s=np.pi/4*safety_radius_marker_size, marker='o', facecolors='none',edgecolors=CM,linewidth=7)
            self.target_x = None
            self.target_y = None
      
      def start(self):
            barrier_certificate = create_unicycle_barrier_certificate_with_boundary()
            si_to_uni_dyn, _ = create_si_to_uni_mapping()
            self.generateTargetPosition()
            
            while self.target_energy > 0 and self.simulation_time != 0 :
                  # Update
                  self.simulation_time -= 1
                  
                  # Get Robots position
                  x = self.r.get_poses()
                  
                  # Set Information to robot
                  for robot in self.robots:
                        robot.x = x[0, robot.id]
                        robot.y = x[1, robot.id]
                        robot.orientation = x[2, robot.id]
                  
                  # Detect the neighbors within the perception range in robot
                  for robot in self.robots:
                        environmentInfo = self.setEnvironmentInfo(robot.x, robot.y)
                        
                        environmentInfo.neighbors = [self.robots[i] for i in delta_disk_neighbors(x, robot.id, PERCEPTION_RANGE)]
                        
                        distance_to_target = np.linalg.norm(x[:2, robot.id].reshape((1, -1)) - np.array([[self.target_x, self.target_y]]))
                        
                        if distance_to_target < DETECTION_RANGE:
                              robot.set_info_cible(self.target_x, self.target_y)
                              # ! turn on detection led
                              self.turnOnTargetDetectionLed(id=robot.id)
                        else:
                              robot.set_info_cible(None, None)
                              # ! turn off detection led
                              self.turnOffTargetDetectionLed(id=robot.id)
                              
                        # Attack
                        if robot.cible_detected and distance_to_target < ATTACK_RANGE:
                              robot.start_attack()
                              # ! turn on attack led
                              self.turnOnTargetAttackLed(id=robot.id)
                        else:
                              robot.stop_attack()
                              # ! turn off attack led
                              self.turnOffTargetAttackLed(id=robot.id)
                        
                        # Move Robot
                        robot.update(environmentInfo)
                  
                  # Update target energy
                  for robot in self.robots:
                        if robot.cible_attacked:
                              self.target_energy -= ATTACK_STRENGTH
                              # print(self.target_energy)
                              # ! display target energy
                  
                  # Update velocity
                  dx = np.zeros((2, self.N))
                  for robot in self.robots:
                        v = np.array([[robot.vx], [robot.vy]])
                        
                        # Controll velocity to avoid error
                        norm = np.linalg.norm(v)
                        threshold = .8 * self.r.max_linear_velocity
                        
                        if norm > threshold :
                              v = threshold * v / norm
                        dx[:, robot.id] = v.reshape((-1, ))
                  
                  dx = si_to_uni_dyn(dx, x)
                  # Barrier certificate to avoid collision
                  dxi = barrier_certificate(dx, x)
                  self.r.set_velocities(np.arange(self.N), dxi)
                  
                  self.renderSimulationInformation(x)
                  self.r.step()
            
            # self.renderEndInformation()
            time.sleep(3)
            self.r.call_at_scripts_end()
      
      def renderSimulationInformation(self, x):
            
            time_caption = f"Temps écoule : {self.r.time_step*(SIMULATION_TIME - self.simulation_time):.2f} s"
            target_energy_caption = f"Energie : {self.target_energy:.2f}"
            
            if self.safety_radius_plotting:
                  self.g.set_offsets(x[:2, :].T)
            self.time_caption.set_text(time_caption)
            self.target_energy_caption.set_text(target_energy_caption)
      
      def renderEndInformation(self):
            end_caption = f"Fin de la simulation \nTemps de la simulation {(self.simulation_time*0.033):.2f} secondes"
            self.r.axes.text(0,0,end_caption,fontsize=10, color='k',fontweight='bold',horizontalalignment='center',verticalalignment='center',zorder=20)
      
      def turnOnTargetDetectionLed(self, id):
            self.r.left_led_patches[id].set_fill(True)
            self.r.left_led_patches[id].set_color("#3E4BDE")
      
      def turnOffTargetDetectionLed(self, id):
            self.r.left_led_patches[id].set_fill(False)
            
      def turnOnTargetAttackLed(self, id):
            self.r.right_led_patches[id].set_fill(True)
            self.r.right_led_patches[id].set_color("#FC0101")
            
      def turnOffTargetAttackLed(self, id):
            self.r.right_led_patches[id].set_fill(False)
                        
      def generateTargetPosition(self):
            limit_with_border = .3
            isValid = False
            while not isValid :
                  target_x = np.random.rand() * 3.2 - 1.6
                  target_y = np.random.rand() * 2 - 1
                  
                  if np.abs(target_x) < 1.6 - limit_with_border and np.abs(target_y) < 1 - limit_with_border:
                        isValid = True
            self.target_x = target_x
            self.target_y = target_y
            
            # Put target in Arena
            self.r.axes.add_patch(
                  patches.Circle(
                        [self.target_x, self.target_y],
                        radius=0.04,
                        color="#008D21")
            )
      
      def setEnvironmentInfo(self, x, y) -> EnvInfo :
            envInfo = EnvInfo()
            boundaries = np.array(
                  [[-1.6, 0],   # left boundary
                  [0, -1],     # down boundary
                  [1.6, 0],    # right boundary
                  [0, 1]])     # up boundary
            # Left
            left = np.linalg.norm(np.array([[x], [y]]) - boundaries[0, :])
            envInfo.wallsLeft = left if left < PERCEPTION_RANGE else None
            # down 
            down = np.linalg.norm(np.array([[x], [y]]) - boundaries[1, :])
            envInfo.wallsDown = down if down < PERCEPTION_RANGE else None
            # right
            right = np.linalg.norm(np.array([[x], [y]]) - boundaries[2, :])
            envInfo.wallsRight = right if right < PERCEPTION_RANGE else None
            # up
            up = np.linalg.norm(np.array([[x], [y]]) - boundaries[3, :])
            envInfo.wallsUp = up if up < PERCEPTION_RANGE else None
            
            return envInfo
      
       
if __name__ == "__main__":    
      simulator  = Simulator()
      simulator.start()
      
      
"""

"""