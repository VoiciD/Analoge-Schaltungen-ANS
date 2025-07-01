#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 08:33:21 2025

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

R = 1000
C = 1*10**(-6)
w_0 = 1/(R*C)       #3-dB Grenzfrequenz

Q = 1               #Güte
H = 1               #Verstärkungsfaktor

fs = 10000          #Sampling Rate



#%% Der Nenner ist für alle Übertragungsfunktionen gleich
den = np.array([1/(w_0)**2,1/(w_0*Q),1])
#%% Analog Lowpass
num_LP = np.array([H])

zeros_analog_LP,poles_analog_LP,k_analog_LP = signal.tf2zpk(num_LP,den)
zeros_digital_LP,poles_digital_LP,k_digital_LP = signal.bilinear_zpk(zeros_analog_LP,poles_analog_LP,k_analog_LP,fs)

ws_LP,hs_LP = signal.freqs_zpk(zeros_analog_LP,poles_analog_LP,k_analog_LP)
wz_LP,hz_LP = signal.freqz_zpk(zeros_digital_LP,poles_digital_LP,k_digital_LP)

#%% Analog Highpass
num_HP = np.array([H/(w_0**2),0,0])

zeros_analog_HP,poles_analog_HP,k_analog_HP = signal.tf2zpk(num_HP,den)
zeros_digital_HP,poles_digital_HP,k_digital_HP = signal.bilinear_zpk(zeros_analog_HP,poles_analog_HP,k_analog_HP,fs)

ws_HP,hs_HP = signal.freqs_zpk(zeros_analog_HP,poles_analog_HP,k_analog_HP)
wz_HP,hz_HP = signal.freqz_zpk(zeros_digital_HP,poles_digital_HP,k_digital_HP)

#%% Analog Bandstop
num_BS = np.array([H/(w_0**2),0,H])

zeros_analog_BS,poles_analog_BS,k_analog_BS = signal.tf2zpk(num_BS,den)
zeros_digital_BS,poles_digital_BS,k_digital_BS = signal.bilinear_zpk(zeros_analog_BS,poles_analog_BS,k_analog_BS,fs)

ws_BS,hs_BS = signal.freqs_zpk(zeros_analog_BS,poles_analog_BS,k_analog_BS)
wz_BS,hz_BS = signal.freqz_zpk(zeros_digital_BS,poles_digital_BS,k_digital_BS)


#%% Analog Bandpass
num_BP = np.array([(-H/w_0),0])


zeros_analog_BP,poles_analog_BP,k_analog_BP = signal.tf2zpk(num_BP,den)

zeros_digital_BP,poles_digital_BP,k_digital_BP = signal.bilinear_zpk(zeros_analog_BP,poles_analog_BP,k_analog_BP,fs)
ws_BP,hs_BP = signal.freqs_zpk(zeros_analog_BP,poles_analog_BP,k_analog_BP)
wz_BP,hz_BP = signal.freqz_zpk(zeros_digital_BP,poles_digital_BP,k_digital_BP)


#%% Plot

fig, ax = plt.subplots(2, 2, constrained_layout=True)
ax[0,0].plot(ws_LP/(2*np.pi), 20*np.log(abs(hs_LP)), label="analog")
ax[0,0].plot(wz_LP*fs/(2*np.pi), 20*np.log(abs(hz_LP)), label="digital")
ax[0,0].set_ylim([-100,10])
ax[0,0].set_xlim([0,1000])
ax[0,0].set_title("Lowpass")
ax[0,0].set_ylabel("Magnitude [dB]")
ax[0,0].set_xlabel("Frequency [Hz]")
ax[0,0].grid()
ax[0,0].legend()
ax[0,1].plot(ws_HP/(2*np.pi), 20*np.log(abs(hs_HP)), label="analog")
ax[0,1].plot(wz_HP*fs/(2*np.pi), 20*np.log(abs(hz_HP)), label="digital")
ax[0,1].set_ylim([-100,10])
ax[0,1].set_xlim([0,1000])
ax[0,1].set_title("Highpass")
ax[0,1].set_ylabel("Magnitude [dB]")
ax[0,1].set_xlabel("Frequency [Hz]")
ax[0,1].grid()
ax[0,1].legend()
ax[1,0].plot(ws_BP/(2*np.pi), 20*np.log(abs(hs_BP)), label="analog")
ax[1,0].plot(wz_BP*fs/(2*np.pi), 20*np.log(abs(hz_BP)), label="digital")
ax[1,0].set_ylim([-100,10])
ax[1,0].set_xlim([0,1000])
ax[1,0].set_title("Bandpass")
ax[1,0].set_ylabel("Magnitude [dB]")
ax[1,0].set_xlabel("Frequency [Hz]")
ax[1,0].grid()
ax[1,0].legend()
ax[1,1].plot(ws_BS/(2*np.pi), 20*np.log(abs(hs_BS)), label="analog")
ax[1,1].plot(wz_BS*fs/(2*np.pi), 20*np.log(abs(hz_BS)), label="digital")
ax[1,1].set_ylim([-100,10])
ax[1,1].set_xlim([0,1000])
ax[1,1].set_title("Bandsperre")
ax[1,1].set_ylabel("Magnitude [dB]")
ax[1,1].set_xlabel("Frequency [Hz]")
ax[1,1].grid()
ax[1,1].legend()
plt.show()

unit_circle = plt.Circle((0,0),color="r",radius = 1,fill = False)
unit_circle1 = plt.Circle((0,0),color="r",radius = 1,fill = False)
unit_circle2 = plt.Circle((0,0),color="r",radius = 1,fill = False)
unit_circle3 = plt.Circle((0,0),color="r",radius = 1,fill = False)


fig, ax = plt.subplots(2,2, constrained_layout=True)
ax[0,0].scatter(np.real(zeros_digital_LP),np.imag(zeros_digital_LP),marker="o")
ax[0,0].scatter(np.real(poles_digital_LP),np.imag(poles_digital_LP),marker="x")
ax[0,0].add_patch(unit_circle)
ax[0,0].set_title("Pole/Zero Plot Lowpass")
ax[0,0].grid()
ax[0,1].scatter(np.real(zeros_digital_HP),np.imag(zeros_digital_HP),marker="o")
ax[0,1].scatter(np.real(poles_digital_HP),np.imag(poles_digital_HP),marker="x")
ax[0,1].add_patch(unit_circle1)
ax[0,1].set_title("Pole/Zero Plot Highpass")
ax[0,1].grid()
ax[1,0].scatter(np.real(zeros_digital_BP),np.imag(zeros_digital_BP),marker="o")
ax[1,0].scatter(np.real(poles_digital_BP),np.imag(poles_digital_BP),marker="x")
ax[1,0].add_patch(unit_circle2)
ax[1,0].set_title("Pole/Zero Plot Bandpass")
ax[1,0].grid()
ax[1,1].scatter(np.real(zeros_digital_BS),np.imag(zeros_digital_BS),marker="o")
ax[1,1].scatter(np.real(poles_digital_BS),np.imag(poles_digital_BS),marker="x")
ax[1,1].add_patch(unit_circle3)
ax[1,1].set_title("Pole/Zero Plot Bandstop")
ax[1,1].grid()
plt.show()
