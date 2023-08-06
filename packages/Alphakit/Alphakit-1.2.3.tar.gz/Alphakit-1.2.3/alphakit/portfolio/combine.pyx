# -*- coding: utf-8 -*-
import pandas as pd
from alphakit.factor.processing import *


def factor_merge(indata):
    outframe = pd.DataFrame()
    tradingday = indata[0].index
    ticker = indata[0].columns
    for df in indata:
        dfs = standardize(winsorize(df))
        outframe = pd.concat([outframe, dfs.unstack()], axis=1)
    out = outframe.sum(axis=1, min_count=1)
    out = out.unstack(level=0)
    out = out.reindex(index=tradingday, columns=ticker)
    return out
