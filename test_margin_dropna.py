import pandas as pd
import numpy as np


a = np.array(['foo', 'foo', 'foo', 'bar',
              'bar', 'foo', 'foo'], dtype=object)
b = np.array(['one', 'one', 'two', 'one',
              'two', np.nan, 'two'], dtype=object)
c = np.array(['dull', 'dull', 'dull', 'dull',
              'dull', 'shiny', 'shiny'], dtype=object)

actual = pd.crosstab([a, b], c, rownames=['a', 'b'],
                     colnames=['c'], margins=True, dropna=False)
m = pd.MultiIndex.from_arrays([['bar', 'bar', 'bar', 'foo', 'foo', 'foo', 'All'],
                            [np.nan, 'one', 'two', np.nan, 'one', 'two', '']],
                           names=['a', 'b'], dropna=False)
expected = pd.DataFrame([[0, 0, 0], [1, 0, 1], [1, 0, 1], [0, 1, 1], [2, 0, 2], [1, 1, 2],
                      [5, 2, 7]], index=m)
expected.columns = pd.Index(['dull', 'shiny', 'All'], name='c')

t = actual.index
print actual
print actual.index
print expected
print m
