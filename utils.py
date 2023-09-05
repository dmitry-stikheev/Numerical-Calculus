import numpy as np
from scipy.stats import norm


def bs_price(X_0, K, T, r, sigma, type):
    d1 = (np.log(X_0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if type == 'call':
        return X_0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - X_0 * norm.cdf(-d1)

def delta(X_0, K, T, r, sigma, type):
    d1 = (np.log(X_0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

    if type == 'call':
        return norm.cdf(d1)
    elif type == 'put':
        return - norm.cdf(-d1)
    
def gamma(X_0, K, T, r, sigma, type):
    d1 = (np.log(X_0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    return 1 / (X_0 * sigma * np.sqrt(T)) * norm.pdf(d1)

def vega(X_0, K, T, r, sigma, type):
    d1 = (np.log(X_0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    return X_0 * np.sqrt(T) * norm.pdf(d1)

def rho(X_0, K, T, r, sigma, type):
    d1 = (np.log(X_0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if type == 'call':
        return K * np.exp(-r * T) * T * norm.cdf(d2)
    elif type == 'put':
        return -K * np.exp(-r * T) * T * norm.cdf(-d2)

def theta(X_0, K, T, r, sigma, type):
    d1 = (np.log(X_0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if type == 'call':
        return -K * np.exp(-r * T) * r * norm.cdf(d2) - X_0 * sigma / (2 * np.sqrt(T)) * norm.pdf(d1)
    elif type == 'put':
        return K * np.exp(-r * T) * r * norm.cdf(-d2) - X_0 * sigma / (2 * np.sqrt(T)) * norm.pdf(d1)


def poly_3(x, coeffs):
    return coeffs[0] * x**3 + coeffs[1] * x**2 + coeffs[2] * x + coeffs[3]

