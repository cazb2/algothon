
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)
position_size = 1000

def getMyPosition(prcSoFar):
    global currentPos
    # Score: -0.38
    (nInst, nt) = prcSoFar.shape
    positions = np.zeros(nInst)
    trade_count = 0

    daily_returns = np.diff(prcSoFar) / prcSoFar[:, :-1]
    correlation_matrix = np.corrcoef(daily_returns)
    correlation_df = pd.DataFrame(correlation_matrix)
    np.fill_diagonal(correlation_df.values, np.nan)
    most_correlated_instruments = correlation_df.idxmax()
    max_correlations = correlation_df.max()

    for i in range(nInst):
        pair = most_correlated_instruments[i]
        correlation_coefficient = max_correlations[i]
        partners_n_day_mean = np.mean(prcSoFar[most_correlated_instruments[i], -100:])
        partners_3_day_mean = np.mean(prcSoFar[most_correlated_instruments[i], -2:])

        i_n_day_mean = np.mean(prcSoFar[i, -100:])
        i_3_day_mean = np.mean(prcSoFar[i, -2:])


        if (correlation_coefficient > 0.6):
            if partners_3_day_mean > partners_n_day_mean and i_3_day_mean < i_n_day_mean:
                positions[i] += position_size
                trade_count += 1
                positions[pair] -= position_size
            elif partners_3_day_mean < partners_n_day_mean and i_3_day_mean > i_n_day_mean:
                positions[pair] += position_size
                trade_count += 1
                positions[i] -= position_size
        

        """ if correlation_coefficient > 0.1 and prcSoFar[pair, -1] > 1.04 * partners_n_day_mean and prcSoFar[i, -1] < i_n_day_mean:
            positions[i] += position_size
            trade_count += 1
        elif correlation_coefficient > 0.1 and prcSoFar[pair, -1] < 0.96 * partners_n_day_mean and prcSoFar[i, -1] > i_n_day_mean:
            positions[i] -= position_size
            trade_count += 1

        i_acf_val = acf(prcSoFar[i, :], nlags=5)
        if i_acf_val[3] > 0.7:
            if prcSoFar[i, -1] > 1.02 * i_n_day_mean :
                positions[i] += 5
            elif prcSoFar[i, -1] < 0.98 * i_n_day_mean :
                positions[i] -= 5 """

        """ p_acf_val = acf(prcSoFar[pair, :], nlags=5)
        i_acf_val = acf(prcSoFar[i, :], nlags=5)
        if i_acf_val[5] > 0.6 or p_acf_val[5] > 0.6:  # If ACF at lag 1 is above threshold
            # Calculate the mean of the last 50 days
            
            if prcSoFar[i, -1] > 1.06 * i_n_day_mean and prcSoFar[pair, -1] > 1.05 * partners_n_day_mean :
                positions[i] += 100
            elif prcSoFar[i, -1] < 0.95 * i_n_day_mean and prcSoFar[pair, -1] < 0.95 * partners_n_day_mean :
                positions[i] -= 100 """
        
        
            

    print(trade_count)
        
    newPos = positions
    currentPos = newPos
    return newPos

    # Score: -45.77
    # (nins, nt) = prcSoFar.shape
    #     if (nt < 2):
    #         return np.zeros(nins)
    #     lastRet = np.log(prcSoFar[:, -1] / prcSoFar[:, -2])
    #     lNorm = np.sqrt(lastRet.dot(lastRet))
    #     lastRet /= lNorm
    
    #     rpos = np.array([int(x) for x in 5000 * lastRet / prcSoFar[:, -1]])
    #     currentPos = np.array([int(x) for x in currentPos+rpos])
    #     return currentPos
