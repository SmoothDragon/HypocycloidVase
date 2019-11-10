#!/usr/bin/env python3

import numpy as np

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *



k = 5
resolution = 256
limit = k+2

# big circle:
theta = np.linspace(0, 2*np.pi, resolution+1)
circle = np.exp(1j*theta)

# hypocycloid
hypo_inner = (k-1)*np.exp(1j*theta) + np.conj(np.exp(1j*(k-1)*theta))
hypo_outer = (k)*np.exp(1j*theta) + np.conj(np.exp(1j*(k)*theta))

level = []

def frame_generator(step=8):
    # Drawing path
    for i in range(0, len(theta), step):
        rotate = np.exp(1j*-theta[i]/k)
        hypo_rotate = rotate*hypo_inner + circle[i]
        level.append(hypo_rotate[:-1])
        yield


def no_op(*args, **kwargs):
    return

for f in frame_generator():
    pass

h_array = np.concatenate(level)
n = resolution
height = .2
points = [(point.real, point.imag, (i//n)*height) for i,point in enumerate(h_array)]
faces = [(i*n + j, (i+1)*n + (j+1)%n, (i+1)*n +j) for i in range(len(level)-1) for j in range(n)]
faces.extend([(i*n + j, i*n + (j+1)%n, (i+1)*n +(j+1)%n) for i in range(len(level)-1) for j in range(n)])
faces.append(list(range(n-1,0,-1)))
N = len(level)
faces.append(list(range((N-1)*n, N*n)))

piece = polyhedron(points=points, faces=faces)
piece = scale([10,10,15])(piece)
# piece = union()(piece, translate([0,0,height*(N-1)])(piece))
# print(scad_render(piece))
scad_render_to_file(piece, 'HypocycloidVase.scad')

