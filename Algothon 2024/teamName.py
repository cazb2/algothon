
import numpy as np
from statsmodels.tsa.stattools import acf

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)

def getMyPosition(prcSoFar):
    global currentPos
    # Score: -0.38
    (nInst, nt) = prcSoFar.shape
    positions = np.zeros(nInst)
    for i in range(nInst):
        acf_val = acf(prcSoFar[i, :], nlags=1)
        if acf_val[1] > 0.5:  # If ACF at lag 1 is above threshold
            # If price is above the mean, short
            if prcSoFar[i, -1] > np.mean(prcSoFar[i, :]):
                positions[i] = -1  # Short
            else:
                positions[i] = 1  # Long
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
