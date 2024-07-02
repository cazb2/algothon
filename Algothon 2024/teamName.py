
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

# Function to clean and load signals from a text file
# def load_signals(file_path):
#     with open(file_path, 'r') as file:
#         content = file.read()

#     # Remove any unwanted characters and split by spaces/newlines
#     cleaned_content = content.replace('[', '').replace(']', '').replace(',', ' ').replace('\n', ' ')
#     cleaned_content = ' '.join(cleaned_content.split())  # Ensure single spaces
#     signal_list = cleaned_content.split(' ')

#     # Convert the list of strings to a list of floats
#     signals = np.array([float(signal) for signal in signal_list if signal])
#     return signals

nInst = 50
currentPos = np.zeros(nInst)
position_size = 1000
# first_500_signals = load_signals('signals.txt')
window = 20
# signal_history = list(first_500_signals[-window:])  # Initialize as a list

def getMyPosition(prcSoFar):
    global currentPos, signal_history
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
    pair_adjustment = 50

    log_inst_A = np.log(prcSoFar[instrument_pairs[0], -(1 + window):])
    log_inst_B = np.log(prcSoFar[instrument_pairs[1], -(1 + window):])
    y = log_inst_A[:-1]
    X = log_inst_B[:-1]
    # X = sm.add_constant(X) # Should we add a constant?

    model = sm.OLS(y, X).fit()
    n = model.params[0]
    spread = log_inst_A[-1] - n * log_inst_B[-1]
    residuals = model.resid
    if adfuller(residuals)[1] >= 0.05:
        # print(f'Not stationary for day:  + {nt}')
        currentPos = newPos
        return newPos
    residual_std_dev = np.std(residuals, ddof=1)  # ddof=1 for sample standard deviation

    if spread < -2 * residual_std_dev:
        # Instrument 1 is undervalued, Instrument 2 is overvalued
        newPos[instrument_pairs[0]] += pair_adjustment
        newPos[instrument_pairs[1]] -= pair_adjustment
    elif spread > 2 * residual_std_dev:
        # Instrument 2 is undervalued, Instrument 1 is overvalued
        newPos[instrument_pairs[1]] += pair_adjustment
        newPos[instrument_pairs[0]] -= pair_adjustment














    # log_returns = np.log(prcSoFar[:, 1:] / prcSoFar[:, :-1])
    # pair_adjustment = 50 # ?? can this be optimised

    # y = log_returns[instrument_pairs[0], -window:]
    # X = log_returns[instrument_pairs[1], -window:]
    # X = sm.add_constant(X)  # Add a constant term for the intercept

    # # Fit the OLS model
    # model = sm.OLS(y, X).fit()
    # beta = model.params[1]  # Slope coefficient

    # # Calculate the signal
    # signal = log_returns[instrument_pairs[0], -1] - beta * log_returns[instrument_pairs[1], -1]

    # signal_history.append(signal)
    # if len(signal_history) > window:
    #     signal_history.pop(0)

    # # if len(signal_history) < 20:
    # #     currentPos = newPos
    # #     return newPos
    
    # signal_std_dev = np.std(signal_history)

    # if signal < -2 * signal_std_dev:
    #     # Instrument 1 is undervalued, Instrument 2 is overvalued
    #     newPos[instrument_pairs[0]] += pair_adjustment
    #     newPos[instrument_pairs[1]] -= pair_adjustment
    # elif signal > 2 * signal_std_dev:
    #     # Instrument 2 is undervalued, Instrument 1 is overvalued
    #     newPos[instrument_pairs[1]] += pair_adjustment
    #     newPos[instrument_pairs[0]] -= pair_adjustment


    # pair_adjustment = 50 # ?? can this be optimised
    # returns = np.diff(prcSoFar, axis=1) / prcSoFar[:, :-1] * 100
    # for i in instrument_pairs:
    #     if (nt < 300): 
    #         continue
    #     for j in instrument_pairs:
    #         if j <= i:
    #             continue
    #         instrument1 = i
    #         instrument2 = j

    #         moving_average1 = np.mean(returns[instrument1, :])
    #         moving_average2 = np.mean(returns[instrument2, :])

    #         spread = returns[instrument1, -1] - returns[instrument2, -1]
    #         spread_moving_average = moving_average1 - moving_average2
    #         spread_std_dev = np.std(returns[instrument1, :] - returns[instrument2, :])

    #         if spread < (spread_moving_average - 2 * spread_std_dev):
    #             # Instrument 1 is undervalued, Instrument 2 is overvalued
    #             if newPos[instrument1] <= 0:
    #                 newPos[instrument1] = 0
    #             if newPos[instrument2] >= 0:
    #                 newPos[instrument2] = 0
    #             newPos[instrument1] += pair_adjustment
    #             newPos[instrument2] -= pair_adjustment
    #         elif spread > (spread_moving_average + 2 * spread_std_dev):
    #             # Instrument 1 is overvalued, Instrument 2 is undervalued
    #             if newPos[instrument1] >= 0:
    #                 newPos[instrument1] = 0
    #             if newPos[instrument2] <= 0:
    #                 newPos[instrument2] = 0
    #             newPos[instrument1] -= pair_adjustment
    #             newPos[instrument2] += pair_adjustment
    #         elif spread_moving_average - spread_std_dev <= spread <= spread_moving_average + spread_std_dev:
    #             # Close positions when spread reverts to within one standard deviation of the mean spread
    #             newPos[instrument1] = 0
    #             newPos[instrument2] = 0

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
