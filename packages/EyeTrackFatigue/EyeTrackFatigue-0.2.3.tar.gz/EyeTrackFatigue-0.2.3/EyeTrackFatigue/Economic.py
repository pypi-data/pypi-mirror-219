# пример
import pandas as pd
import matplotlib.pyplot as matplot

prices = pd.read_csv('htm.csv')
prices.info()
prices.hist(bins=30)
matplot.title('histogram for prices')

matplot.show()