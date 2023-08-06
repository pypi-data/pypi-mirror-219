# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

maxi = np.maximum
mini = np.minimum


## 基础运算
def sign(df1):
    '''sign'''
    return np.sign(df1)


def vneg(df1):
    '''vneg'''
    return -1 * df1


def vpower(df1, df2):
    '''power'''
    return np.power(df1, df2)


def dfabs(df1):
    '''abs'''
    return np.abs(df1)


def vlog(df1):
    '''log'''
    return np.log(df1)


def rank(df):
    '''cross-sectional rank'''
    return df.rank(axis=1, pct=True)


def ts_argmax(df, n):
    '''ts_argmax(x, d) = which day ts_max(x, d) occurred on'''
    return n - df.rolling(n, min_periods=int(n / 3)).apply(lambda x: np.argmax(x), raw=True)


def ts_argmin(df, n):
    '''ts_argmin(x, d) = which day ts_min(x, d) occurred on'''
    return n - df.rolling(n, min_periods=int(n / 3)).apply(lambda x: np.argmin(x), raw=True)


def condop(logic, df1, df2):
    '''condop(logic, df1, df2) = logic?df1:df2'''
    return logic.astype(np.float) * df1 + (~logic).astype(np.float) * df2


def corr(df1, df2, n):
    '''time-serial correlation of x and y for the past d days'''
    r = df1.rolling(n, min_periods=int(n / 3)).corr(df2)
    r[~np.isfinite(r)] = np.nan
    return r


def covariance(df1, df2, n):
    '''time-serial covariance of x and y for the past d days'''
    r = df1.rolling(n, min_periods=int(n / 3)).cov(df2)
    r[~np.isfinite(r)] = np.nan
    return r


def dfsum(df1, n):
    '''sum(x, d) = time-series sum over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).sum()


def sma(df1, n):
    '''mean(x, d) = time-series mean over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).mean()


def dfmin(df1, df2):
    '''min(df1, df2) = np.minimum(df1, df2)'''
    return np.minimum(df1, df2)


def dfmax(df1, df2):
    '''max(df1, df2) = np.maximum(df1, df2)'''
    return np.maximum(df1, df2)


def vdelta(df1, n):
    '''today value of x minus the value of x d days ago'''
    return df1 - df1.shift(n)


def signedpower(df1, a):
    '''signedpower(x, a) = x^a'''
    return np.sign(df1) * (df1.abs().pow(a))


def delay(df1, n):
    '''value of x d days ago'''
    return df1.shift(n)


def scale(df1, a=1.0):
    '''rescaled x such that sum(abs(x)) = a (the default is a = 1)'''
    return df1.apply(lambda x: (x / (x.abs().sum()) * a), axis=1, raw=False)


def ts_zscore(df1, n):
    return (df1 - df1.rolling(n, min_periods=int(n / 3)).mean()) / df1.rolling(n, min_periods=int(n / 3)).std()


def ts_rank(df1, n):
    '''ts_rank(x, d) = time-series rank in the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).apply(
        lambda x: np.argmax(np.argsort(x)) if np.isfinite(x[-1]) else np.nan, raw=True)


def ts_max(df1, n):
    '''ts_max(x, d) = time-series max over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).max()


def ts_min(df1, n):
    '''ts_min(x, d) = time-series min over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).min()


def ts_median(df1, n):
    '''ts_median(x, d) = time-series median over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).median()


def ts_prod(df1, n):
    '''ts_prod(x, d) = time-series prod over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).apply(lambda x: x.prod(), raw=True)


def ts_stdev(df1, n):
    '''ts_stdev(x, d) = time-series std over the past d days'''
    return df1.rolling(n, min_periods=int(n / 3)).std()


def decay_linear(df1, n):
    '''decay_linear'''
    c = (np.arange(n) + 1.0)
    c /= np.sum(c)
    return df1.fillna(0).rolling(n).apply(lambda x: np.dot(x, c), raw=True)


def neutralize(df1):
    '''market neutralization'''
    return df1.apply(lambda x: x - x.mean(), axis=1, raw=False)
    # return df1.apply(lambda x: x - np.nanmean(x), axis=1, raw=True)


def rank_sub(df1, df2):
    return df1.rank(axis=1, pct=True) - df2.rank(axis=1, pct=True)


def rank_div(df1, df2):
    temp = df2.rank(axis=1, pct=True) + 0.001
    temp[temp == 0] = np.nan
    return df1.rank(axis=1, pct=True).div(temp)


def Convolve(df1, df2, n):
    line_number, column_number = df1.shape[0], df1.shape[1]
    long_list = []
    for i in range(line_number):
        i += 1
        if i >= n:
            df1_sub = df1.loc[df1.index[i - n:i], :]
            df2_sub = df2.loc[df2.index[i - n:i], :]
            long_list.append([np.convolve(map(float, list(df1_sub.loc[:, df1_sub.columns[t]])),
                                          map(float, list(df2_sub.loc[:, df2_sub.columns[t]]))).sum() for t in
                              range(column_number)])
        else:
            long_list.append([np.nan] * column_number)
    return pd.DataFrame(long_list, index=df1.index, columns=df1.columns)


def sigmoid(df):
    return 1.0 / (1 + np.exp(-df.astype('float')))


def skew(df, n):
    return df.rolling(n, min_periods=int(n / 3)).skew()


def kurt(df, n):
    return df.rolling(n, min_periods=int(n / 3)).kurt()


def Convolve_skew(df1, df2, n):
    line_number, column_number = df1.shape[0], df1.shape[1]
    long_list = []
    for i in range(line_number):
        print(i)
        i += 1
        if i >= n:
            df1_sub = df1.loc[df1.index[i - n:i], :]
            df2_sub = df2.loc[df2.index[i - n:i], :]
            long_list.append([pd.Series(np.convolve(map(float, list(df1_sub.loc[:, df1_sub.columns[t]])),
                                                    map(float, list(df2_sub.loc[:, df2_sub.columns[t]])))).skew() for t
                              in range(column_number)])
        else:
            long_list.append([np.nan] * column_number)
    return pd.DataFrame(long_list, index=df1.index, columns=df1.columns)


def regbeta(A, B, n):
    return A.rolling(n, min_periods=int(n / 3)).corr(B) * A.rolling(n, min_periods=int(n / 3)).std() / B.rolling(n,
                                                                                                                 min_periods=int(
                                                                                                                     n / 3)).std()


def regsemibeta(A, B, n, Asemi, Bsemi):
    # 半beta,求解A，B在正负不同情况下的beta
    # Asemi为1表示正，0为负
    subA = A.copy()
    subA[:] = np.nan
    subB = B.copy()
    subB[:] = np.nan
    subA[(Asemi * (A > 0) + (1 - Asemi) * (A < 0)) > 0] = A[(Asemi * (A > 0) + (1 - Asemi) * (A < 0)) > 0]
    subB[(Bsemi * (B > 0) + (1 - Bsemi) * (B < 0)) > 0] = B[(Bsemi * (B > 0) + (1 - Bsemi) * (B < 0)) > 0]
    return subA.rolling(n, min_periods=int(n / 3)).corr(subB) * subA.rolling(n, min_periods=int(
        n / 3)).std() / subB.rolling(n, min_periods=int(n / 3)).std()


def wma(A, n, m):
    return A.ewm(com=float(n) / m - 1).mean()


'''TR = MAX(MAX(HIGH-LOW,ABS(HIGH-DELAY(CLOSE,1))),ABS(LOW-DELAY(CLOSE,1)))'''


def TR(data):
    return maxi(maxi(data['df_high'] - data['df_low'], abs(data['df_high'] - delay(data['df_close'], 1))),
                abs(data['df_low'] - delay(data['df_close'], 1)))


'''HD = HIGH-DELAY(HIGH,1)'''


def HD(data):
    return data['df_high'] - delay(data['df_high'], 1)


'''LD = DELAY(LOW,1)-LOW'''


def LD(data):
    return delay(data['df_low'], 1) - data['df_low']


def count(cond, n):
    return (cond).rolling(n, min_periods=int(n / 3)).sum()


def sumif(df1, n, cond):
    return (cond * df1).rolling(n, min_periods=int(n / 3)).sum()


def vadd(df1, df2):
    return df1.add(df2)


def vsub(df1, df2):
    return df1.sub(df2)


def vmul(df1, df2):
    return df1.mul(df2)


def vdiv(df1, df2):
    return df1.div(df2)


def vsqrt(df1):
    return df1.pow(1 / 2)


def condition(A, B, C):
    B.mul(A) + C.mul(~A)


def clear_by_cond(A, B, C):
    return C.mul(A < B)


def if_then_else(A, B, C, D):
    temp = (A < B)
    return C.mul(temp) + D.mul(~temp)


def mean2(a, b):
    return (a + b) / 2


def mean3(a, b, c):
    return (a + b + c) / 3


def itself(A):
    return A
