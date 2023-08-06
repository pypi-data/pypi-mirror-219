# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from ultron.factor.data.neutralize import neutralize


def standardize(raw_data):
    returndata = raw_data.sub(raw_data.mean(axis=1), axis='rows').div(raw_data.std(axis=1), axis='rows')
    returndata.replace(np.inf, np.nan)
    returndata.replace(-np.inf, np.nan)
    return returndata


def winsorize(indata, win_type='N', n_draw=5, pvalue=0.05):
    '''
    极值处理函数

    :param raw_data: 输入待处理因子，data_array
    :param win_type: [String] 去极值处理的类型选择, 包括正态分布去极值和分位数去极值，分别为'N'/'Q', 默认为前者
    :param n_draw: [int] 正态分布去极值的迭代次数，只有当win_type='NormDistDraw'，更改该参数才有意义；合法输入为正整数，默认值为5
    :param pvalue: [float] 分位数去极值的分位数指定，只有当win_type='QuantileDraw'，更改该参数才有意义；合法输入为(0,1)区间内的浮点数，默认值为0.05
    :return: 经过去极值处理之后的因子值 data_array
    '''

    # Local Process
    raw_data = indata.values
    data = raw_data.copy()  # do not modify input data
    l = data.shape[1]
    if win_type == 'Q':
        bott = np.nanquantile(data, pvalue / 2, axis=1, keepdims=True)
        upper = np.nanquantile(data, 1 - pvalue / 2., axis=1, keepdims=True)
        tbott = np.repeat(bott, l, axis=1)
        tupper = np.repeat(upper, l, axis=1)
        data[data < bott] = tbott[data < bott]
        data[data > upper] = tupper[data > upper]
    else:
        for i in range(n_draw):
            std = np.nanstd(data, axis=1, keepdims=True)
            mean = np.nanmean(data, axis=1, keepdims=True)
            bott = mean - 3 * std
            upper = mean + 3 * std
            tbott = np.repeat(bott, l, axis=1)
            tupper = np.repeat(upper, l, axis=1)
            data[data < bott] = tbott[data < bott]
            data[data > upper] = tupper[data > upper]
    return pd.DataFrame(data, index=indata.index, columns=indata.columns)


def indfill_median(indf, sw1):
    indf.index.name = 'tradingday'
    indf.columns.name = 'ticker'
    sw1.index.name = 'tradingday'
    sw1.columns.name = 'ticker'
    dfall = pd.concat([indf.unstack(), sw1.unstack()], axis=1)
    dfall.columns = ['factor', 'sw1']
    dfall.reset_index(inplace=True)
    ddf = dfall.groupby(['tradingday', 'sw1'])['factor'].median().reset_index()
    ddf.rename(columns={'factor': 'sw1_mean'}, inplace=True)
    alldata = dfall.merge(ddf, on=['tradingday', 'sw1'], how='left')
    alldata.loc[alldata['factor'].isna(), 'factor'] = alldata.loc[alldata['factor'].isna(), 'sw1_mean']
    rdata = alldata.pivot(index='tradingday', columns='ticker', values='factor')
    rdata = rdata.reindex(index=indf.index, columns=indf.columns)
    rdata.index.name = 'tradingday'
    rdata.columns.name = 'ticker'
    return rdata


# 行业线性中性化
def indLineNeu(invar, ind):
    tradingday = invar.index
    ticker = invar.columns
    data = pd.concat([invar.unstack(), ind.unstack()], axis=1)
    data.columns = ['factor', 'ind']
    ind_mean = data.groupby(['tradingday', 'ind']).mean().reset_index()
    indmean = data.reset_index().drop('factor', axis=1).merge(ind_mean, on=['tradingday', 'ind'], how='left').drop(
        'ind', axis=1)
    dmean = indmean.pivot_table(index='tradingday', columns='ticker', values='factor')
    dmean = dmean.reindex(index=tradingday, columns=ticker)
    return invar - dmean


# riskfactor: ['tradingday','ticker,'riskfactor1','riskfactor2']
def alphaOpNeu(invar, riskfactor):
    tradingday = invar.index
    ticker = invar.columns
    invar = invar.copy()
    invar.index.name = 'tradingday'
    invar.columns.name = 'ticker'
    tvar = invar.unstack()
    tvar.name = 'testvar'
    risk_col = riskfactor.columns
    dfall = pd.concat([tvar, riskfactor], axis=1)
    dfall[risk_col] = dfall[risk_col].astype('float64')
    dfall['testvar'] = dfall['testvar'].astype('float64')
    dfall.reset_index(inplace=True)
    dfall.drop_duplicates(['tradingday', 'ticker'], inplace=True)
    dfall.dropna(inplace=True)
    dfall.reset_index(inplace=True, drop=True)
    dfall['tradingday'] = dfall['tradingday'].astype('datetime64[ns]')
    retdbeta = neutralize(dfall[risk_col].values, dfall['testvar'].values, groups=dfall['tradingday'].values)
    ret_dbeta = dfall[['tradingday', 'ticker']].copy()
    ret_dbeta['adjfactor'] = retdbeta
    adjdata = ret_dbeta.pivot_table(index='tradingday', columns='ticker', values='adjfactor')
    redata = adjdata.reindex(index=tradingday, columns=ticker)
    redata.index.name = 'tradingday'
    redata.columns.name = 'ticker'
    return redata
