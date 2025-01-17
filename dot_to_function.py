from fenics import *
from fenics_adjoint import *
import numpy as np

def dot_to_function(V,u,y):
    v = Function(V)
    v.vector().set_local(np.ascontiguousarray(u.dot(y)))
    return v
