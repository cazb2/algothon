
import numpy as np
import pandas as pd

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
    mean_reversion_adjustment = 50
    window_size = 250
    for i in stationary_instruments:
        rolling_window = prcSoFar[i, -window_size:]
        moving_average = np.mean(rolling_window)
        moving_std_dev = np.std(rolling_window)


        if prcSoFar[i, -1] < moving_average - 2 * moving_std_dev:
            if newPos[i] < 0:
                newPos[i] = 0
            newPos[i] += mean_reversion_adjustment
        elif prcSoFar[i, -1] > moving_average + 2 * moving_std_dev:
            if newPos[i] > 0:
                newPos[i] = 0
            newPos[i] -= mean_reversion_adjustment
    
    instrument_pairs = [27, 38]
    pair_adjustment = 50 # ?? can this be optimised
    returns = np.diff(prcSoFar, axis=1) / prcSoFar[:, :-1] * 100
    for i in instrument_pairs:
        if (nt < 300): 
            continue
        for j in instrument_pairs:
            if j <= i:
                continue
            instrument1 = i
            instrument2 = j

            moving_average1 = np.mean(returns[instrument1, :])
            moving_average2 = np.mean(returns[instrument2, :])

            spread = returns[instrument1, -1] - returns[instrument2, -1]
            spread_moving_average = moving_average1 - moving_average2
            spread_std_dev = np.std(returns[instrument1, :] - returns[instrument2, :])

            if spread < (spread_moving_average - 2 * spread_std_dev):
                # Instrument 1 is undervalued, Instrument 2 is overvalued
                if newPos[instrument1] <= 0:
                    newPos[instrument1] = 0
                if newPos[instrument2] >= 0:
                    newPos[instrument2] = 0
                newPos[instrument1] += pair_adjustment
                newPos[instrument2] -= pair_adjustment
            elif spread > (spread_moving_average + 2 * spread_std_dev):
                # Instrument 1 is overvalued, Instrument 2 is undervalued
                if newPos[instrument1] >= 0:
                    newPos[instrument1] = 0
                if newPos[instrument2] <= 0:
                    newPos[instrument2] = 0
                newPos[instrument1] -= pair_adjustment
                newPos[instrument2] += pair_adjustment
            elif spread_moving_average - spread_std_dev <= spread <= spread_moving_average + spread_std_dev:
                # Close positions when spread reverts to within one standard deviation of the mean spread
                newPos[instrument1] = 0
                newPos[instrument2] = 0

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
