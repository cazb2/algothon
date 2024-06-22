
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import adfuller

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)
position_size = 1000


def getMyPosition(prcSoFar):
    global currentPos
    (nInst, nt) = prcSoFar.shape
    newPos = currentPos

    stationary_instruments = [7,28,43,49]

    # for i in range(nInst):
    #     adf_result = adfuller(prcSoFar[i, :])
    #     p_value = adf_result[1]

    #     if p_value < 0.05:
    #         stationary_instruments.append(i)

    window_size = 160
    for i in stationary_instruments:
        # if i == 7:
        #     window_size = 90
        # elif i == 28:
        #     window_size = 142 
        # elif i == 43:
        #     window_size = 185
        # else:
        #     window_size = 155
        rolling_window = prcSoFar[i, -window_size:]
        moving_average = np.mean(rolling_window)
        moving_std_dev = np.std(rolling_window)


        if prcSoFar[i, -1] < moving_average - 2 * moving_std_dev:
            if newPos[i] < 0:
                newPos[i] = 0
            newPos[i] += 1
        elif prcSoFar[i, -1] > moving_average + 2 * moving_std_dev:
            if newPos[i] > 0:
                newPos[i] = 0
            newPos[i] -= 1
        
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
