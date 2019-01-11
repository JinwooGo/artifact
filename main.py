import argparse
import os 

from fenics import *
from fenics_adjoint import *
import sympy as sym
import moola
import numpy as np
import math

from scipy import linalg, sparse
from sklearn.utils import *
from sklearn.utils.extmath import svd_flip
from SVD import safe_sparse_dot, randomized_svd, randomized_range_finder
from initialize import *

from Inverse import *
from discretization import Discretization
from state import State
from misfit import Misfit
from observation import Observation

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--forward", action="store_true", help="solve the forward problem")
parser.add_argument("-i", "--inverse", action="store_true", help="solve the inverse problem")
parser.add_argument("-o", "--observation", action="store_true", help="make the observation")
parser.add_argument("-a", "--add_noise", type=int, default=0, help="add noise with specific standard deviation")
parser.add_argument("-r", "--regularization", type=int, default=0, help="power of regularization term ")


if __name__ == "__main__":
	
	Discretization.add_args(parser)
	args = parser.parse_args()
	disc = Discretization(args)
	
	if args.observation:
		observation = Observation(disc)

	import pdb
	pdb.set_trace()
		

	if args.inverse:
		Size = 32
		mesh, boundaries = get_mesh(Size)
		W, bcs = get_state_space(mesh, boundaries)
		w = get_state_variable(W)
		A = get_function_space(mesh)
		V = Constant(0.5)
		Alpha = Constant(0.0)
		power = 1.
		d_p, d_u, d_W = load_the_data(W)

		ka = interpolate(V, A) # initial guess.
		w = forward_problem(ka) 
		(u,p) = split(w)

		e = Expression("sin(pi * x[0]) * sin(pi * x[1])", degree = 1)
		f = interpolate(e,W.sub(1).collapse())
		J = assemble((0.5*inner(w[1]-d_W[1], f))*dx)
		J = J*J

		n_components = 3
		n_iter = 3
		U, Sigma, VT = randomized_svd(Jhat, n_components= n_components, n_iter= n_iter, size = (Size+1)*(Size+1)) # size should be the discrete vector size of q
		print(Sigma)
