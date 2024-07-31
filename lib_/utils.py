import numpy as np
from robot import *
from const import PERCEPTION_RANGE
from envInfo import EnvInfo

def generateTargetPosition() -> tuple:
    """
    
    -> tuple(x, y)
    """
    LIMIT_WITH_BORDER = .5
    isValid = False
    while not isValid :
        x_target = np.random.rand() * 3.2 - 1.6
        y_target = np.random.rand() * 2 - 1
        
        if np.abs(x_target) > LIMIT_WITH_BORDER or np.abs(y_target) > LIMIT_WITH_BORDER:
            isValid = True
    
    return (x_target, y_target)


def setEnvironmentInfo(robot: Robot) -> EnvInfo :
  envInfo = EnvInfo()
  boundaries = np.array(
      [[-1.6, 0],   # left boundary
       [0, -1],     # down boundary
       [3.2, 0],    # right boundary
       [0, 2]])     # up boundary
  # Left
  left = np.linalg.norm(np.array([[robot.x], [robot.y]]) - boundaries[0, :])
  envInfo.wallsLeft = left if left < PERCEPTION_RANGE else None
  
  # down 
  down = np.linalg.norm(np.array([[robot.x], [robot.y]]) - boundaries[1, :])
  envInfo.wallsDown = down if down < PERCEPTION_RANGE else None
  
  # right
  right = np.linalg.norm(np.array([[robot.x], [robot.y]]) - boundaries[2, :])
  envInfo.wallsRight = right if right < PERCEPTION_RANGE else None
  
  # up
  up = np.linalg.norm(np.array([[robot.x], [robot.y]]) - boundaries[3, :])
  envInfo.wallsUp = up if up < PERCEPTION_RANGE else None
  
  return envInfo
  