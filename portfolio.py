import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import settings
import utils

# plt.style.use('seaborn')

class Portfolio:
    '''
    European Stock Option Portfolio Class
    '''

    def __init__(self, options):
        self.options = options
    
    
    def _get_min_max_K(self):
        min_K = np.min([option.K for option in self.options])
        max_K = np.max([option.K for option in self.options])

        return [min_K, max_K]
    

    def _get_payoff_price_greeks_arrays(self):
        X_portfolio = np.array([x for x in range(self._get_min_max_K()[0] - settings.graph_range,
                                                 self._get_min_max_K()[1] + settings.graph_range + 1)])

        payoff_portfolio = [0 for x in range(0, len(X_portfolio))]
        bs_price_portfolio = payoff_portfolio.copy()
        delta_portfolio = payoff_portfolio.copy()
        gamma_portfolio = payoff_portfolio.copy()
        vega_portfolio = payoff_portfolio.copy()
        rho_portfolio = payoff_portfolio.copy()
        theta_portfolio = payoff_portfolio.copy()  

        for option in self.options:
            payoff_option = [option._get_payoff(x) for x in X_portfolio]
            payoff_portfolio = [sum(x) for x in zip(payoff_portfolio, payoff_option)]

            bs_price_option = [option._get_bs_price(x) for x in X_portfolio]
            bs_price_portfolio = [sum(x) for x in zip(bs_price_portfolio, bs_price_option)]
        
            delta_option = [option._get_greeks(x)['delta'] for x in X_portfolio]
            delta_portfolio = [sum(x) for x in zip(delta_portfolio, delta_option)]

            gamma_option = [option._get_greeks(x)['gamma'] for x in X_portfolio]
            gamma_portfolio = [sum(x) for x in zip(gamma_portfolio, gamma_option)]

            vega_option = [option._get_greeks(x)['vega'] for x in X_portfolio]
            vega_portfolio = [sum(x) for x in zip(vega_portfolio, vega_option)]

            rho_option = [option._get_greeks(x)['rho'] for x in X_portfolio]
            rho_portfolio = [sum(x) for x in zip(rho_portfolio, rho_option)]

            theta_option = [option._get_greeks(x)['theta'] for x in X_portfolio]
            theta_portfolio = [sum(x) for x in zip(theta_portfolio, theta_option)]

        return pd.DataFrame({
            'X(T)': X_portfolio,
            'payoff_portfolio': payoff_portfolio,
            'bs_price_portfolio': bs_price_portfolio,
            'delta_portfolio': delta_portfolio,
            'gamma_portfolio': gamma_portfolio,
            'vega_portfolio': vega_portfolio,
            'rho_portfolio': rho_portfolio,
            'theta_portfolio': theta_portfolio
        })

    def visualize(self):
        greek_names = ['delta', 'gamma', 'vega', 'rho', 'theta']
        plt.figure(figsize = settings.figsize)

        for k in range(0, 6):
            if k == 0:
                ax = plt.subplot(2, 3, k + 1)
                ax.plot(self._get_payoff_price_greeks_arrays().iloc[:, 0],
                        self._get_payoff_price_greeks_arrays().iloc[:, 1],
                        color = f'{settings.payoff_color}',
                        label = 'portfolio payoff')

                ax.plot(self._get_payoff_price_greeks_arrays().iloc[:, 0],
                        self._get_payoff_price_greeks_arrays().iloc[:, 2],
                        color = f'{settings.price_color}',
                        label = 'portfolio BS price')
                
                ax.set_title('portfolio payoff and price')
                ax.legend()
                ax.grid()
            else:
                ax = plt.subplot(2, 3, k + 1)
                
                ax.plot(self._get_payoff_price_greeks_arrays().iloc[:, 0],
                        self._get_payoff_price_greeks_arrays().iloc[:, k + 2],
                        color = f'{settings.greeks_color}')
                
                ax.set_title(f'portfolio {greek_names[k-1]}')
                ax.set_xlabel('X(T)')
                ax.grid()

        plt.tight_layout()
        plt.show()

        
