import os
import numpy as np
import processingFunctions as pf
from matplotlib import pyplot as plt

# ------------------------------------------------------------------------------
# Define inputs, files, analysis type, plots, etc.
# ------------------------------------------------------------------------------
raw_data_file_dir = "G:\\Deployable Technologies\\4-Projects\\110005 MCHEG Phase II\\Technical Work\\Testing Results\\Flow Channel\\240815"
hasHallData = False
timeCol = 0
currCol = 1
volCol = 2
hall1Col = 3
hall2Col = 4

rollingAvgWindow = 75
plotAvgAPerSec = True
plotAvgVPerSec = True
plotRollAvgA = True
plotRollAvgV = True
plotPwr = True
# ------------------------------------------------------------------------------
# Begin script, file inport and preprocessing
# ------------------------------------------------------------------------------
#fileNames = os.listdir(raw_data_file_dir)
#fullFile = os.path.join(raw_data_file_dir, fileNames[0])
fullFile = 'G:\\Deployable Technologies\\4-Projects\\110005 MCHEG Phase II\\Technical Work\\Testing Results\\Flow Channel\\240815\\flowtest_0p5_4.6rps_012.csv'
rawData = np.loadtxt(fullFile, dtype='float', delimiter=',', skiprows=1)

timeData = rawData[:,timeCol]
currData = rawData[:,currCol]
volData = rawData[:, volCol]

if hasHallData:
    try:
        hall1Data = rawData[:,hall1Col]
        hall2Data = rawData[:,hall2Col]
    finally:
        print(fullFile)
        print('This file does not contain hall data')
        hasHallData = False

timeIndex = np.where(timeData == 0.1)
sampleRate = int(timeIndex[0][0] / 0.1)
testLen = int(timeData[-1])

# ------------------------------------------------------------------------------
# Begin data processing
# ------------------------------------------------------------------------------
timePerSecond = timeData[sampleRate::sampleRate]

if plotAvgAPerSec:
    avgAPerSec = pf.timeAvg(sampleRate, testLen, currData)
    print("Current time step average complete")
if plotAvgVPerSec:
    avgVPerSec = pf.timeAvg(sampleRate, testLen, volData)
    print("Voltage time step average complete")
if plotAvgAPerSec and plotAvgVPerSec:
    pwrPerSec = pf.pwrGen(avgAPerSec, avgVPerSec)

if plotRollAvgA:
    rollAvgA = pf.rollingAvg(rollingAvgWindow, currData)
    print("Current rolling average complete")
if plotRollAvgV:
    rollAvgV = pf.rollingAvg(rollingAvgWindow,volData)
    print("Voltage rolling average complete")

if plotRollAvgA and plotRollAvgV:
    pwrRolling = pf.pwrGen(rollAvgA, rollAvgV)

#AFreqResp, AFreqBins = pf.fft(currData, 1/sampleRate)
#VFreqResp, VFreqBins = pf.fft(volData, 1/sampleRate)
# ------------------------------------------------------------------------------
# Make output plots
# ------------------------------------------------------------------------------

if plotAvgAPerSec:
    plt.figure()
    plt.plot(timeData, currData)
    plt.plot(timePerSecond,avgAPerSec)
if plotAvgVPerSec:
    plt.figure()
    plt.plot(timeData, volData)
    plt.plot(timePerSecond,avgVPerSec)

if plotRollAvgA:
    plt.figure()
    plt.plot(timeData, currData)
    plt.plot(np.linspace(1,timeData[-1],len(rollAvgA)),rollAvgA)
if plotRollAvgV:
    plt.figure()
    plt.plot(timeData, volData)
    plt.plot(np.linspace(1,timeData[-1],len(rollAvgV)),rollAvgV)

if plotPwr:
    plt.figure()
    plt.legend(['Time Step Avg', 'Rolling Avg'])
    try:
        plt.plot(timePerSecond,pwrPerSec)
    except:
        plt.plot(np.linspace(1,timeData[-1],len(rollAvgV)),pwrRolling)
    finally:
        x=[]

plt.show()