import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

dicto = {
    'normal': [ 1.18967414,  0.6890354 ,  np.nan,  0.59974108, -0.60540635,
                -1.09386669, np.nan, -0.76832405, -0.39621923, -0.91401358],
    'categories': ['a', 'b', '--', np.nan, 'c', 'a', 'a', 'c', 'a', np.nan],
    'continuous': [1, 2, 3, 4, np.nan, 6, 7, np.nan, 9, 10]
}

# populating pandas data frame
df = pd.DataFrame.from_dict(dicto)

# Creating and saving the data 
# as a csv file for further analysis.

df.to_csv('out.csv', index=False)

# Creating and saving a figure for
# explanations.

print(df.to_markdown(index=False))

