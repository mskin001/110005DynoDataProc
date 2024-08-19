import numpy as np
import scipy as sp

def timeAvg(rate, len, data):
    avg = np.zeros((len,1))
    timeIter = 0
    for k in range(len):
        if k > 0:
            timeIter = rate*k + 1
        dt = timeIter+rate
        dtData = data[timeIter:dt]
        avg[k] = np.mean(dtData)
    return avg

def rollingAvg(window, data):
    iter = 0
    avg = []
    while iter < len(data) - window + 1:
        dataVals = data[iter:iter+window]
        avg.append(np.mean(dataVals))
        iter = iter + 1
    return np.array(avg)

def pwrGen(A, V):
    pwr = A * V
    return pwr

def fft(data, dt):
    freqResp = sp.fft.fftn(data, axes=0)
    freqBins = sp.fft.fftfreq(np.size(data[:,0]), d=dt)
    return freqResp, freqBins