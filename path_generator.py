import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import settings
import utils
import market_data

class PathGenerator():
    '''
    European Stock Option Monte-Carlo Path Generator Class
    '''
    
    dt = 1 / 252
    n_paths = 25

    def __init__(self):
        pass

    @classmethod
    def generate_ABM_paths(cls, X_0, T, r, sigma):
        
        dt = PathGenerator.dt
        n_paths = PathGenerator.n_paths
        n_steps = int(dt * T)

        Z = np.random.normal(0.0, 1.0, [n_paths, n_steps])
        paths = np.zeros([n_paths, n_steps + 1])
        time = np.zeros(n_steps + 1)
        
        paths[:, 0] = X_0
        for k in range(0, n_steps):
            paths[:, k + 1] = paths[:, k] + r * dt + sigma * np.sqrt(dt) * Z[:, k]
            time[k + 1] = time[k] + dt

        return {'paths': paths, 'time': time}
    
    @classmethod
    def generate_GBM_paths(cls, X_0, T, r, sigma):
        
        dt = PathGenerator.dt
        n_paths = PathGenerator.n_paths
        n_steps = int(dt * T)

        Z = np.random.normal(0.0, 1.0, [n_paths, n_steps])
        log_paths = np.zeros([n_paths, n_steps + 1])
        time = np.zeros(n_steps + 1)
        
        log_paths[:, 0] = np.log(X_0)
        for k in range(0, n_steps):
            log_paths[:, k + 1] = log_paths[:, k] + (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[:, k]
            time[k + 1] = time[k] + dt
        
        paths = np.exp(log_paths)
        
        return {'paths': paths, 'time': time}