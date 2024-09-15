import numpy as np

from agent import Agent
from envInfo import EnvInfo
from const import *


class Robot(Agent):
    name = "Robot AI"
    
    def update(self, envInfo : EnvInfo) -> tuple:
        # Start robot if it immobile
        if not self.cible_detected and self.vx == 0 and self.vy == 0 :
            self.move(np.random.rand() * 2 - 1, np.random.rand() * 2 - 1)
        else:
            # change random direction
            if np.random.rand() < 0.005 :
                self.move(np.random.rand() * 2 - 1, np.random.rand() * 2 - 1)
            
        # Si le robot n'est pas à distance d'attaque, il s'approche de la cible jusqu'à ce qu'il puisse l'attaquer
        if self.cible_detected and not self.cible_attacked:
            target = np.array([self.cible_x, self.cible_y])
            robot = np.array([self.x, self.y])
            # print(f"Robot {self.id} detected target and attack is {self.cible_attacked}")
            if np.linalg.norm(robot-target) > ATTACK_RANGE:
                # Approach the target
                # print(f"\t Robot {self.id} approch target ...")
                self.move(-self.x + self.cible_x, -self.y + self.cible_y)
        
        if self.cible_detected and self.cible_attacked:
            # Stop
            self.move(0, 0)
        
        # Si le robot connait l'emplacement de la cible, il la communique à ses voision
        if self.cible_detected:
            for neighbor in envInfo.neighbors:
                neighbor.set_info_cible(self.cible_x, self.cible_y)
        