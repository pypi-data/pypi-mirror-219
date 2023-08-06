# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from scipy.stats import norm


def factorToWeight(invar_score, hold):
    weighT = invar_score.copy()
    weighT[weighT <= 0] = np.nan
    weighT = weighT.div(weighT.sum(axis=1, min_count=1), axis='rows')
    weighT = weighT.rolling(hold, min_periods=1).sum() / hold
    weightB = invar_score.copy()
    weightB[weightB >= 0] = np.nan
    weightB = weightB.div(weightB.sum(axis=1, min_count=1), axis='rows')
    weightB = weightB.rolling(hold, min_periods=1).sum() / hold
    weight = weighT.sub(weightB, fill_value=0)
    stockNum = pd.concat([weighT.count(axis=1), weightB.count(axis=1)], axis=1)
    stockNum.columns = ['TOP', 'BOT']
    return weighT, weightB, weight, stockNum


def factor_score(invar, n):
    invar_rank = invar.rank(axis=1, method='max')
    invar_score = (invar_rank - 0.5).div(invar_rank.max(axis=1),
                                         axis='rows') - 0.5
    invar_bak = invar_score.copy()
    invar_score = invar_score.pow(n)
    if np.mod(n, 2) == 0:
        invar_score[invar_bak < 0] = -invar_score[invar_bak < 0]
    return invar_score


def factor_score_sig(invar):
    invar_rank = invar.rank(axis=1, method='max')
    count = invar_rank.count(axis=1)
    invar_rank = (invar_rank - 3 / 8).div(count + 1 / 4, axis='rows')
    invar_score = pd.DataFrame(norm.ppf(invar_rank),
                               index=invar.index,
                               columns=invar.columns)
    return invar_score
