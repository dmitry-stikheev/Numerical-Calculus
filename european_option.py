import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import market_data
import settings
import utils


class European_Option():
    '''
    European Stock Option Class
    '''

    portfolio = []
    market_data = market_data.md

    def __init__(self, type, ul_price, strike_price, time_to_maturity, long_short, quantity):
        self.type = type
        self.X_0 = ul_price
        self.K = strike_price
        self.T = time_to_maturity
        self.long_short = long_short
        self.q = quantity
        
        self.payoff = self._get_payoff(self.X_0)
        self.bs_price = self._get_bs_price(self.X_0)
        self.greeks = self._get_greeks(self.X_0)

        European_Option.portfolio.append(self)


    def _direction(self):
        if self.long_short == 'long':
            return 1
        elif self.long_short == 'short':
            return -1

    
    def _get_payoff(self, x):
        if self.type == 'call':
            return self._direction() * self.q * np.max([x - self.K, 0])
        elif self.type == 'put':
            return self._direction() * self.q * np.max([self.K - x, 0])


    def _get_bs_price(self, x):
        return utils.bs_price(x,
                              self.K,
                              self.T,
                              European_Option.market_data['r'],
                              European_Option.market_data['sigma'],
                              self.type) * self._direction() * self.q


    def _get_greeks(self, x):
        greeks_functions = [['delta', utils.delta],
                            ['gamma', utils.gamma],
                            ['vega', utils.vega],
                            ['rho', utils.rho],
                            ['theta', utils.theta]]
        
        greeks = {}
        for k in range(0, len(greeks_functions)):
            greeks[f'{greeks_functions[k][0]}'] = greeks_functions[k][1](x,
                                                                         self.K,
                                                                         self.T,
                                                                         European_Option.market_data['r'],
                                                                         European_Option.market_data['sigma'],
                                                                         self.type) * self._direction() * self.q
        return greeks


    def _get_payoff_price_greeks_arrays(self):
        X = [x for x in range(self.K - settings.graph_range, self.K + settings.graph_range + 1)]
        
        payoff = [self._get_payoff(x) for x in X]
        bs_price = [self._get_bs_price(x) for x in X]
        delta = [self._get_greeks(x)['delta'] for x in X]
        gamma = [self._get_greeks(x)['gamma'] for x in X]
        vega = [self._get_greeks(x)['vega'] for x in X]
        rho = [self._get_greeks(x)['rho'] for x in X]
        theta = [self._get_greeks(x)['theta'] for x in X]

        return pd.DataFrame({
            'X(T)': X,
            'payoff': payoff,
            'bs_price': bs_price,
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'rho': rho,
            'theta': theta 
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
                        label = 'option payoff')

                ax.plot(self._get_payoff_price_greeks_arrays().iloc[:, 0],
                        self._get_payoff_price_greeks_arrays().iloc[:, 2],
                        color = f'{settings.price_color}',
                        label = 'option BS price')
                
                ax.set_title('option payoff and price')
                ax.legend()
                ax.grid()
            else:
                ax = plt.subplot(2, 3, k + 1)
                
                ax.plot(self._get_payoff_price_greeks_arrays().iloc[:, 0],
                        self._get_payoff_price_greeks_arrays().iloc[:, k + 2],
                        color = f'{settings.greeks_color}')
                
                ax.set_title(f'{greek_names[k-1]}')
                ax.set_xlabel('X(T)')
                ax.grid()

        plt.tight_layout()
        plt.show()
                    
            