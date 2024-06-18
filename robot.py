class Robot :
    """
    ________________________________________________________
    
    This class
    ________________________________________________________ 
    
    """
    name = "Agent AI"
    
    def __init__(self, id: int, x:int, y:int, orientation: float, speed: float) :
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
    
    def move(self) :
        ...
        
    def set_info_cible(self):
        ...
        
    def  start_attack(self) :
        self.cible_attacked = True
    
    def stop_attack(self):
        self.cible_attacked = False
        