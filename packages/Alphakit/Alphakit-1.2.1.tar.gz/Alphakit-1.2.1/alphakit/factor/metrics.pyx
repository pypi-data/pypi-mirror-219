# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def factor_stat(dummy, invar):
    test = invar.values * dummy.values
    total_count = np.nansum(dummy.values)
    disp = pd.Series([np.nanmean(test), np.nanmedian(test), np.nanstd(test), np.nanmax(test), np.nanmin(test),
                      1 - np.sum(abs(test) >= 0) / total_count, np.sum(test == 0) / total_count],
                     index=['mean', 'median', 'std', 'max', 'min', 'nanr', 'zeror'])
    return disp


# type='pnl','ic','all'
def factor_pnl(dummy, weight, ret_f1d, skip=0, type='pnl'):
    if skip < 0:
        print('skip must >=0')
        return None
    ret_f1d = ret_f1d * dummy
    ret_f1d_skip = ret_f1d.shift(-skip)
    ret_f1d_skip = np.exp(ret_f1d_skip) - 1
    ret_mkt_fnd = (ret_f1d_skip * dummy).mean(axis=1)
    er_fnd = ret_f1d_skip.sub(ret_mkt_fnd, axis='rows')
    outpnl = []
    turnover = []
    ic_series = []
    if type == 'pnl' or type == 'all':
        outpnl = np.log((er_fnd * weight).sum(axis=1, min_count=1) + 1)
        turnover = abs(weight.sub(weight.shift(1), fill_value=0)).sum(axis=1, min_count=1) * 0.5
        idx = turnover[turnover > 0].index
        if len(idx) > 0:
            turnover[idx[0]] = np.nan
    if type == 'ic' or type == 'all':
        ic_series = weight.corrwith(ret_f1d_skip, axis=1, method='spearman')
    return outpnl, turnover, ic_series


# freq: daily=252，monthly=12,weekly=50
def pnl_metrics(freq, outpnl=None, turnover=None, ic_series=None, usecol=None):
    disp = pd.Series(index=['ret', 'std', 'sharp', 'turnover', 'maxdd', 'calmar', 'win', 'ic', 'icir'], dtype=float)
    if usecol is not None:
        disp = pd.DataFrame(index=['ret', 'std', 'sharp', 'turnover', 'maxdd', 'calmar', 'win', 'ic', 'icir'],
                            columns=usecol, dtype=float)
    if outpnl is not None:
        if usecol is not None:
            outpnl = outpnl[usecol]
        ret = outpnl.mean() * freq
        disp.loc['ret'] = ret
        rstd = outpnl.std() * np.sqrt(freq)
        disp.loc['std'] = rstd
        disp.loc['sharp'] = ret / rstd
        pnlL = outpnl.cumsum()
        rmaxdd = (pnlL.expanding().max() - pnlL).max()
        disp.loc['maxdd'] = rmaxdd
        disp.loc['calmar'] = ret / rmaxdd
        disp.loc['win'] = outpnl[outpnl > 0].count() / outpnl[~outpnl.isna()].count()
    if turnover is not None:
        if usecol is not None:
            turnover = turnover[usecol]
        disp.loc['turnover'] = turnover.mean()
    if ic_series is not None:
        if usecol is not None:
            ic_series = ic_series[usecol]
        icmean = ic_series.mean()
        disp.loc['ic'] = icmean
        disp.loc['icir'] = icmean / ic_series.std()
    return disp


def factor_group(dummy, invar, ret_f1d, group, hold=1, skip=0, checkna=True):
    if skip < 0:
        print('skip must >=0')
        return None
    invar = invar * dummy
    ret_f1d = ret_f1d * dummy
    ret_f1d_skip = ret_f1d.shift(-skip)
    ret_f1d_skip = np.exp(ret_f1d_skip) - 1
    ret_mkt_fnd = (ret_f1d_skip * dummy).mean(axis=1)
    er_fnd = ret_f1d_skip.sub(ret_mkt_fnd, axis='rows')
    # 分层画图
    megedata = np.exp(
        np.log(er_fnd + 1).rolling(hold, min_periods=1).sum().shift(-(hold - 1)).stack() / hold) - 1
    megedata = pd.concat([megedata, invar.stack(), dummy.stack()], axis=1)
    megedata.columns = ['er_fnd', 'factor', 'dummy']
    megedata = megedata.loc[megedata.dummy == 1]
    nanframe = megedata.loc[megedata.factor.isna()]
    megedata = megedata.loc[~megedata.factor.isna()]
    megedata["quantile"] = megedata["factor"].groupby(level=0, group_keys=False).rank(pct=True)
    megedata["quantile"] = (megedata["quantile"] * group).astype('int') + 1
    megedata.loc[megedata['quantile'] == group + 1, 'quantile'] = group
    megedata.index.names = ['tradingday', 'ticker']
    gret = np.log(megedata.reset_index().groupby(['tradingday', 'quantile'])['er_fnd'].mean().unstack() + 1)
    gret.columns = pd.Series(map(lambda x: 'G' + str(x + 1), range(0, gret.shape[1])))
    if not nanframe.empty:
        gnline = nanframe.groupby(axis=0, level=0).er_fnd.mean()
    else:
        gnline = np.nan
    if checkna:
        gret['GN'] = gnline
    gret_stat = gret.mean()
    return gret, gret_stat
