import numpy as np


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