#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:13:01 2019

@author: Ericson Josep
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as spio
from scipy import signal
from scipy.fftpack import fft
import bitstring as bs

NBYTES = 16
NSAMPLE = 160 * NBYTES

#tpsignal = np.load('signal.npy')
tpsignal = np.load('signalLowSNR.npy')
tppulse =  np.load('pulse.npy')

print("Signal size: {} samples".format(len(tpsignal)))
numBits = len(tpsignal)/20
print("Data size:   {} bits , {} Bytes".format(numBits, (len(tpsignal)/20)/8))
print("Pulse size:  {}".format(len(tppulse)))

plt.close()
#plt.plot(tppulse)
# plt.show()

a = [1,1,0]

#a = [0.01884,
#0.007588,
#-0.01759,
#-0.04624,
#-0.04184,
#0.02415,
#0.1413,
#0.256,
#0.3037,
#0.256,
#0.1413,
#0.02415,
#-0.04184,
#-0.04624,
#-0.01759,
#0.007588,
#0.01884]

b = np.zeros(len(a))
b[0] = 1

#filtered_ecg = signal.filtfilt(a,b,tpsignal[0:NSAMPLE])
filtered_ecg = signal.filtfilt(np.flip(tppulse),1,tpsignal[0:NSAMPLE])

#a = [1,1,0]
#b = [1,0,0]

#filtered_ecg = signal.filtfilt(a,b,tpsignal[0:NSAMPLE])

plt.plot(tpsignal[:NSAMPLE], 'k-', label='tpsignal')
plt.plot(filtered_ecg[:NSAMPLE], 'b-', linewidth=1, label='filtered_ecg')
plt.legend(loc='best')
# plt.show()

sig_mean = np.mean(filtered_ecg)+0.1
print("Mean filter signal: {}".format(sig_mean))

numBits = int(NSAMPLE/20) 
bitstream = []
bytestream = []
byteCount = 0
bites = []

for i in range(numBits):
    sample =  filtered_ecg[(i*20) + 1]
    byteCount += 1
    if (sample > sig_mean):
        bitstream.append(1)
        bites.append(1)
    else:
        bitstream.append(0)
        bites.append(0)
        
    if(byteCount == 8):
        bytestream.append(np.array(bites))
        bites = []
        byteCount = 0
        
for data in bytestream:    
    byte = bs.BitArray(data)
    print("0x{} 0b{}".format(str(byte.hex),str(byte.bin)))  


# Make Histogram
    
byteHeader = [1, 0, 1, 0, 1, 1, 0, 0]
onesList  = []
zerosList = []
byteCount = 0

for i in range(numBits):
    sample =  filtered_ecg[(i*20) + 1]
    if(byteHeader[byteCount] == 1):
        onesList.append(sample)
    else:
        zerosList.append(sample)
    byteCount += 1
    if(byteCount == 8):
        byteCount = 0
        
   
plt.figure()
histRange =  np.arange(0, 2, 0.1) 
plt.hist(onesList, bins=histRange, alpha=0.6, label='my label')
plt.hist(zerosList, bins=histRange, alpha=0.6, label='0 bits')
plt.title("Histogram")
plt.show()

print("---------------------------")

onesHist, bins = np.histogram(onesList, bins=histRange)
zerosHist, bins = np.histogram(zerosList, bins=histRange)
print(onesHist)
print(zerosHist)
print(bins)

print("---------------------------")

bitstream = []
bytestream = []
byteCount = 0
bites = []
for i in range(numBits):
    sample =  filtered_ecg[(i*20) + 1]
    
    if (sample > 1.6):
        bitstream.append(1)
        bites.append(1)
    elif(sample < 1.4):
        bitstream.append(0)
        bites.append(0)
    else:
        if(byteHeader[byteCount] == 1):
            bitstream.append(1)
            bites.append(1)
        else:
            bitstream.append(0)
            bites.append(0)
       
    byteCount += 1
    if(byteCount == 8):
        bytestream.append(np.array(bites))
        bites = []
        byteCount = 0
        
for data in bytestream:    
    byte = bs.BitArray(data)
    print("0x{} 0b{}".format(str(byte.hex),str(byte.bin)))