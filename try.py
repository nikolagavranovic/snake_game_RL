import numpy as np
from enum import Enum


class Existance(Enum):
    DontExist = 0
    Exists = 1

obstacles_infront = np.array([Existance.DontExist, Existance.Exists])

print(obstacles_infront[Existance.Exists.value])