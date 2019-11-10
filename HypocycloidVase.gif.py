#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
plt.axis('off')
resolution = 512

k = 5
limit = k+2
bound = (-limit, limit)
ax.set_aspect('equal')
ax.set_xlim(*bound)
ax.set_ylim(*bound)

# big circle:
theta = np.linspace(0, 2*np.pi, resolution+1)
circle = np.exp(1j*theta)

# hypocycloid
hypo_inner = (k-1)*np.exp(1j*theta) + np.conj(np.exp(1j*(k-1)*theta))
hypo_outer = (k)*np.exp(1j*theta) + np.conj(np.exp(1j*(k)*theta))

big_circle, = ax.plot((k+1)*circle.real, (k+1)*circle.imag, 'b', linewidth=2)
hypocycloid_a, = ax.plot([], [], 'r-', linewidth=3.3)
hypocycloid_b, = ax.plot(hypo_outer.real, hypo_outer.imag, 'g-', linewidth=3.3)

level = []

def frame_generator(step=8):
    # Drawing path
    for i in range(0, len(theta), step):
        rotate = np.exp(1j*-theta[i]/k)
        hypo_rotate = rotate*hypo_inner + circle[i]
        hypocycloid_a.set_data(hypo_rotate.real, hypo_rotate.imag)
        level.append(hypo_rotate[:-1])
        yield


def no_op(*args, **kwargs):
    return


ani = FuncAnimation(fig, no_op, frames=frame_generator(), save_count=300, blit=False)

ani.save('HypocycloidVase.gif', writer='imagemagick', fps=10, dpi=75)
# plt.show()
