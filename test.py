
import pytest
from datetime import datetime
from numpy.random import randn
from numpy import nan
import numpy as np
import random

import pandas as pd
from pandas.compat import lrange, lzip
from pandas.core.reshape.concat import concat
from pandas.core.reshape.merge import merge, MergeError
from pandas.util.testing import assert_frame_equal, assert_series_equal
from pandas.core.dtypes.dtypes import CategoricalDtype
from pandas.core.dtypes.common import is_categorical_dtype, is_object_dtype
from pandas import DataFrame, Index, MultiIndex, Series, Categorical
import pandas.util.testing as tm

# from pandas.core.algorithms import _ensure_data
# from pandas._libs import algos, lib, hashtable as htable
# from pandas._libs.tslib import iNaT
#
# _hashtables = {
#     'float64': (htable.Float64HashTable, htable.Float64Vector),
#     'uint64': (htable.UInt64HashTable, htable.UInt64Vector),
#     'int64': (htable.Int64HashTable, htable.Int64Vector),
#     'string': (htable.StringHashTable, htable.ObjectVector),
#     'object': (htable.PyObjectHashTable, htable.ObjectVector)
# }
#
#
#
# values = ['a', np.nan]
# values, dtype, ndtype = _ensure_data(values)
# (hash_klass, vec_klass) = _hashtables.get('string')
# table = hash_klass(len(values))
# unique = vec_klass()
# table.set_item(values[0], 1)


# household = (
#     DataFrame(
#         dict(household_id=[1, 2, 3],
#              male=[0, 1, 0],
#              wealth=[196087.3, 316478.7, 294750]),
#         columns=['household_id', 'male', 'wealth'])
#     .set_index('household_id'))
# portfolio = (
#     DataFrame(
#         dict(household_id=[1, 2, 2, 3, 3, 3, 4],
#              asset_id=["nl0000301109", "nl0000289783", "gb00b03mlx29",
#                        "gb00b03mlx29", "lu0197800237", "nl0000289965",
#                        np.nan],
#              name=["ABN Amro", "Robeco", "Royal Dutch Shell",
#                    "Royal Dutch Shell",
#                    "AAB Eastern Europe Equity Fund",
#                    "Postbank BioTech Fonds", np.nan],
#              share=[1.0, 0.4, 0.6, 0.15, 0.6, 0.25, 1.0]),
#         columns=['household_id', 'asset_id', 'name', 'share'])
#     .set_index(['household_id', 'asset_id']))
# result = household.join(portfolio, how='inner')
# expected = (
#     DataFrame(
#         dict(male=[0, 1, 1, 0, 0, 0],
#              wealth=[196087.3, 316478.7, 316478.7,
#                      294750.0, 294750.0, 294750.0],
#              name=['ABN Amro', 'Robeco', 'Royal Dutch Shell',
#                    'Royal Dutch Shell',
#                    'AAB Eastern Europe Equity Fund',
#                    'Postbank BioTech Fonds'],
#              share=[1.00, 0.40, 0.60, 0.15, 0.60, 0.25],
#              household_id=[1, 2, 2, 3, 3, 3],
#              asset_id=['nl0000301109', 'nl0000289783', 'gb00b03mlx29',
#                        'gb00b03mlx29', 'lu0197800237',
#                        'nl0000289965']))
#     .set_index(['household_id', 'asset_id'])
#     .reindex(columns=['male', 'wealth', 'name', 'share']))
# lindex = result.index
# rindex = expected.index
# for level in range(lindex.nlevels):
#     print lindex.levels[level], rindex.levels[level]
#
# assert_frame_equal(result, expected)



icols = ['1st', '2nd', '3rd']


def bind_cols(df):
    iord = lambda a: 0 if a != a else ord(a)
    f = lambda ts: ts.map(iord) - ord('a')
    return (f(df['1st']) + f(df['3rd']) * 1e2 +
            df['2nd'].fillna(0) * 1e4)


def run_asserts(left, right):
    for sort in [False, True]:
        res = left.join(right, on=icols, how='left', sort=sort)
        # print '--'
        # print res
        assert len(left) < len(res) + 1
        assert not res['4th'].isnull().any()
        assert not res['5th'].isnull().any()

        tm.assert_series_equal(
            res['4th'], - res['5th'], check_names=False)
        result = bind_cols(res.iloc[:, :-2])
        tm.assert_series_equal(res['4th'], result, check_names=False)
        assert result.name is None

        if sort:
            tm.assert_frame_equal(
                res, res.sort_values(icols, kind='mergesort'))

        out = merge(left, right.reset_index(), on=icols,
                    sort=sort, how='left')

        res.index = np.arange(len(res))
        tm.assert_frame_equal(out, res)


lc = list(map(chr, np.arange(ord('a'), ord('z') + 1)))
left = DataFrame(np.random.choice(lc, (50, 2)),
                 columns=['1st', '3rd'])
left.insert(1, '2nd', np.random.randint(0, 1000, len(left)))

i = np.random.permutation(len(left))
right = left.iloc[i].copy()

left['4th'] = bind_cols(left)
right['5th'] = - bind_cols(right)
right.set_index(icols, inplace=True)
run_asserts(left, right)

# inject some nulls
left.loc[1::23, '1st'] = np.nan
left.loc[2::37, '2nd'] = np.nan
left.loc[3::43, '3rd'] = np.nan
left['4th'] = bind_cols(left)
i = np.random.permutation(len(left))
right = left.iloc[i, :-1]
right['5th'] = - bind_cols(right)
# print right['5th']
# print right
right.set_index(icols, inplace=True)
# print right
# print '--'
# print left
run_asserts(left, right)

