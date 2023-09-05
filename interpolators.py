import numpy as np
import matplotlib.pyplot as plt
import utils

class SplineGenerator:
    def __init__(self, x, y, interpolation_range, spline_order = 'cubic', bc = 'natural', clamp_value = 0):
        
        if len(x) != len(y):
            raise ValueError('Lengths of two sumbitted arrays must be equal')

        self.x = np.array(x)
        self.y = np.array(y)
        self.order = spline_order
        self.bc = bc
        self.clamp_value = clamp_value
        self.x_inter = np.array(interpolation_range)
        

    def _generate_poly_coeffs(self):
        n_points = len(self.x)
        n_polys = n_points - 1
        n_coeffs = 4
        n_interim = n_points - 2

        A = np.zeros([n_coeffs * n_polys, n_coeffs * n_polys])

        ## handling first 2n equations (polynomial evaluation at endpoints)
        for j in range(0, n_polys):
            values_1 = np.array([self.x[j]**3, self.x[j]**2, self.x[j], 1])
            values_2 = np.array([self.x[j+1]**3, self.x[j+1]**2, self.x[j+1], 1])
            
            for k in range(0, n_coeffs):
                A[2*j:(1+2*j), (n_coeffs*j+k):n_coeffs*(1+j)] = values_1[k]
                A[2*j+1:(2+2*j), (n_coeffs*j+k):n_coeffs*(1+j)] = values_2[k]

        ## handling next (n-1) equations (conrinuos first derivatives at interim-points)
        for j in range(0, n_polys - 1):
            values_plus = np.array([3 * self.x[j+1]**2, 2 * self.x[j+1], 1, 0])
            values_minus = np.array([-3 * self.x[j+1]**2, -2 * self.x[j+1], -1, 0])
            values = np.concatenate([values_minus, values_plus])
            
            for k in range(0, n_coeffs - 1):
                A[n_polys*2+j, n_coeffs*j:n_coeffs*(2+j)] = values
            
        ## handling next (n-1) equations (conrinuos second derivatives at interim-points)
        for j in range(0, n_polys - 1):
            values_plus = np.array([6 * self.x[j+1], 2, 0, 0])
            values_minus = np.array([-6 * self.x[j+1], -2, 0, 0])
            values = np.concatenate([values_minus, values_plus])
            
            for k in range(0, n_coeffs - 1):
                A[n_polys*2+n_interim+j, n_coeffs*j:n_coeffs*(2+j)] = values

        ## handling last 2 equations (boundary condition)

        # Natural BC
        if self.bc == 'natural':
            values_start = np.array([6 * self.x[0], 2, 0, 0])
            values_end = np.array([6 * self.x[-1], 2, 0, 0])
                
            A[-2, 0:n_coeffs] = values_start
            A[-1, -n_coeffs:] = values_end

            # fill the b-vector (rhs of Ax = b)
            b = np.zeros(n_coeffs * n_polys)
            b[0] = self.y[0]

            for k in range(1, len(b), 2):
                try:
                    b[k] = self.y[int(k - (k-1)/2)]
                    b[k+1] = self.y[int(k - (k-1)/2)]
                except:
                    continue
            b[int(n_points * 2 - 2)] = 0

        elif self.bc == 'clamped at zero':
            values_start = np.array([3 * self.x[0] ** 2, 2 * self.x[0], 1, 0])
            values_end = np.array([3 * self.x[-1] ** 2, 2 * self.x[-1], 1, 0])
            
            A[-2, 0:n_coeffs] = values_start
            A[-1, -n_coeffs:] = values_end

            b = np.zeros(n_coeffs * n_polys)
            b[0] = self.y[0]

            for k in range(1, len(b), 2):
                try:
                    b[k] = self.y[int(k - (k-1)/2)]
                    b[k+1] = self.y[int(k - (k-1)/2)]
                except:
                    continue
            b[int(n_points * 2 - 2)] = 0

        
        ## fill the b-vector (rhs of Ax = b)
        b = np.zeros(n_coeffs * n_polys)
        b[0] = self.y[0]

        for k in range(1, len(b), 2):
            try:
                b[k] = self.y[int(k - (k-1)/2)]
                b[k+1] = self.y[int(k - (k-1)/2)]
            except:
                continue
        b[int(n_points * 2 - 2)] = 0
        
        ## solve the linear system of equations
        all_coeffs = list(np.dot(np.linalg.inv(A), b))
        
        ## refine result for handy presenrtation
        partitioned_coeffs = []
        for k in range(0, len(all_coeffs), n_coeffs):
            partitioned_coeffs.append(all_coeffs[k: k+n_coeffs])

        partitioned_x = []
        for k in range(0, len(self.x) - 1):
            partitioned_x.append([self.x[k], self.x[k+1]])

        ranges_coeffs = {}
        for k in range(0, n_polys):
            ranges_coeffs[f'Poly {k+1}'] = [partitioned_x[k], partitioned_coeffs[k]]

        
        ## Interpolation routine
        attribution = []
        for j in range(0, len(self.x_inter) - 1):
            for k in range(0, n_polys):
                if k == n_polys:
                    if self.x_inter[j] >= min(ranges_coeffs[f'Poly {k+1}'][0]) and self.x_inter[j] <= max(ranges_coeffs[f'Poly {k+1}'][0]):
                        attribution.append(k)
                else:
                    if self.x_inter[j] >= min(ranges_coeffs[f'Poly {k+1}'][0]) and self.x_inter[j] < max(ranges_coeffs[f'Poly {k+1}'][0]):
                        attribution.append(k)
        attribution.append(n_polys - 1)

        attribution = np.array(attribution)

        y_inter = []
        for k in range(0, len(self.x_inter)):
            y_inter.append(utils.poly_3(self.x_inter[k], ranges_coeffs[f'Poly {attribution[k]+1}'][1]))


        return np.array(y_inter)











    



