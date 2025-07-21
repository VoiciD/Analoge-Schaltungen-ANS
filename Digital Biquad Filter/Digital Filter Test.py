#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  8 23:32:26 2025

@author: daniel
"""

import pyaudio 
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt

from scipy.fftpack import fft
import scipy.signal as signal


R = 1000
C = 1*10**(-6)
w_0 = 1/(R*C)       #3-dB Grenzfrequenz
# fc = 1000
# w_0 = 2*np.pi*fc
Q = 1               #Güte
H = 1               #Verstärkungsfaktor

fs = 44100          #Sampling Rate

w0_prewarp =  2*np.arctan(w_0)


#%% Analoge Biquads
den = np.array([1/(w_0)**2,1/(w_0*Q),1])

num_LP = np.array([H])
num_HP = np.array([H/(w_0**2),0,0])
num_BS = np.array([-H/(w_0**2),0,-H])
num_BP = np.array([(-H/w_0),0])

#%% Bilinear Transformation
num_LP_dig,den_LP_dig = signal.bilinear(num_LP,den,fs)
num_HP_dig,den_HP_dig = signal.bilinear(num_HP,den,fs)
num_BS_dig,den_BS_dig = signal.bilinear(num_BS,den,fs)
num_BP_dig,den_BP_dig = signal.bilinear(num_BP,den,fs)

#%% Frequenzantworten
wz_LP,hz_LP = signal.freqz(num_LP_dig,den_LP_dig,worN = 512,fs=fs)
wz_HP,hz_HP = signal.freqz(num_HP_dig,den_HP_dig,worN = 512,fs=fs)
wz_BS,hz_BS = signal.freqz(num_BS_dig,den_BS_dig,worN = 512,fs=fs)
wz_BP,hz_BP = signal.freqz(num_BP_dig,den_BP_dig,worN = 512,fs=fs)
#%% SOS Strukturen

sos_dig_LP = signal.tf2sos(num_LP_dig,den_LP_dig)
print("Digital LP SOS:",sos_dig_LP)
sos_dig_HP = signal.tf2sos(num_HP_dig,den_HP_dig)
print("Digital HP SOS:",sos_dig_HP)
sos_dig_BS = signal.tf2sos(num_BS_dig,den_BS_dig)
print("Digital BS SOS:",sos_dig_BS)
sos_dig_BP = signal.tf2sos(num_BP_dig,den_BP_dig)
print("Digital BP SOS:",sos_dig_BP)

#%% Filterauswahl
chosing_ftype = True
while chosing_ftype == True:
    ftype = input("Filtertype:")
    
    if ftype == 'LP':
        filtertype = sos_dig_LP
        wz = wz_LP
        hz = hz_LP
        lbl = 'Lowpass'
        chosing_ftype = False
    elif ftype == 'HP':
        filtertype = sos_dig_HP
        wz = wz_HP
        hz = hz_HP
        lbl = 'Highpass'
        chosing_ftype = False
    elif ftype == 'BS':
        filtertype = sos_dig_BS
        wz = wz_BS
        hz = hz_BS
        lbl = 'Bandstop'
        chosing_ftype = False
    elif ftype == 'BP':
        filtertype = sos_dig_BP
        wz = wz_BP
        hz = hz_BP
        lbl = 'Bandpass'
        chosing_ftype = False
    else:
        print("No matching Filter found")
        
#%% Audiostream

p = pyaudio.PyAudio()



for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(i, info['name'], "Max Input Channels:", info['maxInputChannels'])
monitor_index_number = int(input("Input Device:",))


info_monitor = p.get_device_info_by_index(monitor_index_number)


CHUNK = 1024 * 4                                    # samples per frame
FORMAT = pyaudio.paInt16                            # audio format (bytes per sample?)
CHANNELS = 1                                        # single channel for microphone
RATE = 44100                                        # samples per second

stream = p.open(
    output_device_index=monitor_index_number,
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)
#%% Canvas
%matplotlib qt5
plt.figure(1)
plt.title("Filterkurve")
plt.plot(wz,20*np.log10(hz))


fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(15, 7))
# variable for plotting
x = np.arange(0, 2 * CHUNK, 2)       # samples (waveform)
xf = np.linspace(0, RATE, CHUNK)     # frequencies (spectrum)

# create a line object with random data
line, = ax1.plot(x, np.random.rand(CHUNK), '-', lw=1)

# create semilogx line for spectrum
line_fft, = ax2.plot(xf, np.random.rand(CHUNK), '-', lw=1)
# create semilogx line for spectrum
line_fft_filt, = ax3.plot(xf, np.random.rand(CHUNK), '-', lw=1)
# Signal range is -32k to 32k for 16bit
AMPLITUDE_LIMIT = 32000

plt.plot(wz, 20*np.log10(abs(hz)), label = lbl)
plt.grid(True)
plt.title('Digitale Biquad Frequenzgänge')
plt.xlabel('Frequenz in [Hz]')
plt.ylabel('Amplitude in [dB]')
plt.xlim([0, 4000])
plt.ylim([-30, 15])
plt.legend(loc='lower right')

# format waveform axes
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.grid()
ax1.set_ylim(-AMPLITUDE_LIMIT, AMPLITUDE_LIMIT)
ax1.set_xlim(0, 2 * CHUNK)
plt.subplots_adjust(hspace=0.6)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[-AMPLITUDE_LIMIT, 0, AMPLITUDE_LIMIT])
plt.grid()
# format spectrum axes
ax2.set_title("FFT unfiltered")
ax2.set_xlabel('Frequenz in [Hz]')
ax2.set_ylabel('Amplitude in [dB]')
ax2.set_xlim(20, RATE / 8)
ax2.grid()
ax2.set_ylim(-100, 40)
plt.subplots_adjust(hspace=0.6)
ax3.set_xlim(20, RATE / 8)
ax3.grid()
ax3.set_ylim(-100, 40)

print('stream started')

while True:
    
    # binary data
    data = stream.read(CHUNK, exception_on_overflow=False)   

    data_np = np.frombuffer(data, dtype='h')
    
    line.set_ydata(data_np)
    # compute FFT and update line
    data_np_filt = signal.sosfiltfilt(filtertype,data_np)
    #data_np_filt = signal.sosfiltfilt(filtertype,data_np_filt)

    
    yf = fft(data_np)
    yf_filt = fft(data_np_filt)
    
    line_fft.set_ydata(20*np.log10(np.abs(yf[0:CHUNK])  / (512 * CHUNK)))
    line_fft_filt.set_ydata(20*np.log10(np.abs(yf_filt[0:CHUNK])  / (512 * CHUNK)))
    
    fig.canvas.draw()
    fig.canvas.flush_events()








