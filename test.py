import numpy as np
import matplotlib.pyplot as plt
from interpolators import *
from scipy.interpolate import CubicSpline


x = np.array([75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125])
y = np.array([31, 28, 25, 23, 21, 20, 20.5, 22, 24, 25, 26])




x_inter = np.linspace(np.min(x), np.max(x), 120)

interpolator_natural = SplineGenerator(x, y, x_inter, 'cubic', 'natural')
interpolator_clamped = SplineGenerator(x, y, x_inter, 'cubic', 'clamped at zero')
y_inter_natural = interpolator_natural._generate_poly_coeffs()
y_inter_clamped = interpolator_clamped._generate_poly_coeffs()
y_inter_scipy = CubicSpline(x, y, bc_type = 'natural')

plt.plot(x, y, 'o', label = 'Data Points')
plt.plot(x_inter, y_inter_natural, 'orange', label = 'My Cubic Spline, natural bc')
# plt.plot(x_inter, y_inter_scipy(x_inter), 'black', label = 'Scipy Cubic Spline')
plt.legend()
plt.show()

plt.plot(x, y, 'o', label = 'Data Points')
plt.plot(x_inter, y_inter_clamped, 'orange', label = 'My Cubic Spline, clamped bc')
# plt.plot(x_inter, y_inter_scipy(x_inter), 'black', label = 'Scipy Cubic Spline')
plt.legend()
plt.show()