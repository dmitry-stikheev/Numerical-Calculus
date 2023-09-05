import numpy as np
import pandas as pd1
import matplotlib.pyplot as plt

from european_option import *
from portfolio import *
import utils


call_1 = European_Option(type = 'call',
                        ul_price = 100,
                        strike_price = 80,
                        time_to_maturity = 1,
                        long_short = 'long',
                        quantity = 1)

call_2 = European_Option(type = 'call',
                        ul_price = 100,
                        strike_price = 100,
                        time_to_maturity = 1,
                        long_short = 'short',
                        quantity = 2)

call_3 = European_Option(type = 'call',
                        ul_price = 100,
                        strike_price = 120,
                        time_to_maturity = 1,
                        long_short = 'long',
                        quantity = 1)

butterfly = Portfolio([call_1,
                        call_2,
                        call_3])
                        
butterfly.visualize()
