
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
    newPos = np.zeros(nInst)

    daily_returns = np.diff(prcSoFar) / prcSoFar[:, :-1]
    std_devs = np.std(daily_returns, axis=1)
    mean_std_dev = np.mean(std_devs)

    for i in range(nInst):
        lag1_acf = acf(prcSoFar[i, :], nlags=1)
        if (std_devs[i] < mean_std_dev) and (lag1_acf[1] < 0.98): continue
        if prcSoFar[i,-1] < prcSoFar[i,-2]:
            newPos[i] = -1
        else:
            newPos[i] = 1
        
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
