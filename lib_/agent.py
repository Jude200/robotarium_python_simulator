from abc import abstractmethod

import numpy as np

class Agent :
    """
    ________________________________________________________
    
    This class
    ________________________________________________________ 
    
    """
    
    def __init__(self, id: int, x:int, y:int, orientation: float, speed: float, **kwargs) :
        self.id = id
        self.x = x
        self.y = y
        self.orientation = orientation
        self.vx = 0
        self.vy = 0
        self.max_speed = speed
        self.cible_detected = False
        self.cible_attacked = False
        self.cible_x = None
        self.cible_y = None
    
    @abstractmethod
    def update(self):
        pass
        
    def move(self, vx, vy):
        vl = np.array([vx, vy])
        if np.linalg.norm(vl) > self.max_speed:
            vl = 0.9 * self.max_speed * vl / np.linalg.norm(vl)
        self.vx, self.vy = vl[0], vl[1]
        
    def set_info_cible(self, x, y):
        # ! assertion
        if x is not None and y is not None:
            self.cible_detected = True
        else:
            self.cible_detected = False
        self.cible_x, self.cible_y = x, y
    
    def start_attack(self) :
        self.cible_attacked = True
    
    def stop_attack(self):
        self.cible_attacked = False
        