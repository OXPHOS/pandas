import pandas as pd

M = pd.DataFrame([
[1, 'a', 'A'],
[1, 'b', 'B'],
[1, 'c', None]],
columns=['x', 'y', 'z'])
P = M.pivot_table(values='x', index='y', columns='z', aggfunc='sum', fill_value=0, margins=True, dropna=True)

print P