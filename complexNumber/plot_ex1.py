# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:17:11 2020

@author: jslee
"""
from matplotlib import pyplot as plt
import numpy as np

#a = [1 + 6j, 2+3j, 3+2j, 4+1j, 5]
re = np.array([0.7741, 0.7517, 0.763, 0.7744, 0.8052, 0.834, 0.8712, 0.9084, 0.9471, 0.995, 1.0325, 1.0757, 1.1215, 1.1681, 1.2245, 1.2765, 1.3431, 1.3823, 1.4168, 1.4416, 1.4596, 1.4873, 1.5055, 1.542])
img = -1j * np.array([1.8285, 0.8832, 0.5564, 0.3861, 0.1577, 0.0608, -0.0197, -0.0645, -0.0988, -0.1236, -0.1385, -0.1573, -0.1759, -0.1904, -0.1966, -0.1588, -0.1752, -0.1464, -0.1289, -0.1166, -0.1072, -0.1165, -0.1065, -0.1449])

a = re + img

fix, ax = plt.subplots()

ax.scatter(a.real, a.imag)
plt.xlim(0.5,2)
plt.ylim(-0.25, 0.25)
plt.grid(True,linestyle='--')
plt.savefig('plot_complex_number_geometric_representation_01.png', bbox_inches='tight')


"""
import matplotlib.pyplot as
import numpy as np
import math


z1 = 4.0 + 2.*1j

x_min = -5.0
x_max = 5.0

y_min = -5.0
y_max = 5.0
"""
"""
def plot_complex_number_geometric_representation(z,x_min,x_max,y_min,y_max):

    fig = plt.figure()

    ax = plt.gca()

    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

    a = [0.0,0.0]
    b = [z.real,z.imag]

    head_length = 0.2

    dx = b[0] - a[0]
    dy = b[1] - a[1]

    vec_ab = [dx,dy]

    vec_ab_magnitude = math.sqrt(dx**2+dy**2)

    dx = dx / vec_ab_magnitude
    dy = dy / vec_ab_magnitude

    vec_ab_magnitude = vec_ab_magnitude - head_length

    ax = plt.axes()

    ax.arrow(a[0], a[1], vec_ab_magnitude*dx, vec_ab_magnitude*dy, head_width=head_length, head_length=head_length, fc='black', ec='black')

    plt.scatter(a[0],a[1],color='black',s=2)
    plt.scatter(b[0],b[1],color='black',s=2)

    #ax.annotate('A', (a[0]-0.4,a[1]),fontsize=14)
    ax.annotate('z1', (b[0]+0.3,b[1]),fontsize=10)


    ax.text(0, y_max+0.5, r'Img', fontsize=10, horizontalalignment='center')
    ax.text(x_max+0.5, 0, r'Real', fontsize=10, verticalalignment='center')

    plt.xlim(x_min,x_max)
    plt.ylim(y_min,y_max)

    plt.grid(True,linestyle='--')

    plt.savefig('plot_complex_number_geometric_representation_01.png', bbox_inches='tight')
    plt.show()
    plt.close()


plot_complex_number_geometric_representation(z1,x_min,x_max,y_min,y_max)
"""