
from fenics import *
from fenics_adjoint import *

from initialize import *
from discretization import Discretization
from state import *
from SVD import *
import numpy as np

class Regularization(object):

    def __new__(self, state):
        self.Alpha = None
        self.power = None
        self.state = state
        self.reg = None
        Regularization.__init__(self)
        return self
        
    def __init__(self):
        self.Alpha = 0.1
        self.power = 1.0
        self.reg = assemble(self.Alpha*(np.power(inner(grad(self.state.ka),grad(self.state.ka))+0.001,self.power))*dx)
        

