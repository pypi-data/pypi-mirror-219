# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from alphakit.factor.metrics import *
from alphakit.factor.transform import *


def factor_plot(dummy, invar=None, gret=None, outpnl=None, savepath=''):
    plt.figure(figsize=(16, 9))
    if invar is not None:
        invar = invar * dummy
        ax1 = plt.subplot(221)
        values = ax1.hist(invar.unstack(), bins=100)
    if gret is not None:
        ax2 = plt.subplot(222)
        df_factor_plt = gret.cumsum()
        df_factor_plt.index = df_factor_plt.index.astype('datetime64[ns]')
        ax2.plot(df_factor_plt, label=gret.columns)
        ax2.legend(loc='lower left')

        ax4 = plt.subplot(224)
        gnline = None
        if 'GN' in gret.columns:
            gnline = gret['GN'].mean()
            gret.drop('GN', axis=1, inplace=True)
        gretplt = pd.DataFrame(gret.mean())
        gretplt['level'] = 0
        ax4.plot(gretplt, marker='.')
        if gnline is not None:
            po = abs(gretplt[0] - gnline).reset_index(drop=True)
            po1 = po.nsmallest(1).index[0]
            if not np.isnan(gnline):
                ax4.scatter(po1, gnline, s=150, marker='*', color='green')
                ax4.text(po1 + 0.2, gnline, 'GN')
        group = len(gretplt) - 1
        ax4.set_xticks(np.linspace(0, group, group, endpoint=True))
    if outpnl is not None:
        ax3 = plt.subplot(223)
        pnlplt = outpnl.cumsum()
        pnlplt.index = pnlplt.index.astype('datetime64[ns]')
        ax3.plot(pnlplt)
    if savepath != '':
        plt.savefig(savepath)
        plt.show(block=False)
        plt.pause(3)
        plt.close('all')
    else:
        plt.show(block=True)


def factor_one(dummy,
               invar,
               ret_f1d,
               freq=252,
               hold=1,
               group=10,
               skip=0,
               checkna=True,
               savepath=''):
    invar = dummy * invar
    disp = factor_stat(dummy, invar)
    invar_score = factor_score_sig(invar)
    weighT, weightB, weight, stockNum = factorToWeight(invar_score, hold)
    disp['TopNum'] = stockNum['TOP'].mean()
    disp['BotNum'] = stockNum['BOT'].mean()
    outpnl1, turnover1, ic_series1 = factor_pnl(dummy,
                                                weighT,
                                                ret_f1d,
                                                skip,
                                                type='all')
    outpnl2, turnover2, ic_series2 = factor_pnl(dummy,
                                                weightB,
                                                ret_f1d,
                                                skip,
                                                type='all')
    outpnl3, turnover3, ic_series3 = factor_pnl(dummy,
                                                weight,
                                                ret_f1d,
                                                skip,
                                                type='all')
    outpnl = pd.concat([outpnl1, outpnl2, outpnl3], axis=1)
    outpnl.columns = ['TOP', 'BOT', 'TMB']
    turnover = pd.concat([turnover1, turnover2, turnover3], axis=1)
    turnover.columns = ['TOP', 'BOT', 'TMB']
    ic_series = pd.concat([ic_series1, ic_series2, ic_series3], axis=1)
    ic_series.columns = ['TOP', 'BOT', 'TMB']
    pnlstat = pnl_metrics(freq,
                          outpnl,
                          turnover,
                          ic_series,
                          usecol=['TOP', 'BOT', 'TMB'])
    gret, gret_stat = factor_group(dummy, invar, ret_f1d, group, hold, skip,
                                   checkna)
    factor_plot(dummy, invar, gret, outpnl, savepath)
    return disp, outpnl, pnlstat, gret_stat
