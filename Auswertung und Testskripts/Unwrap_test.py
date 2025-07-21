                                                                                                                         #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 10 19:49:17 2025

@author: daniel
"""

#%% Initialisierung
import time
import sys
import os

sys.path.append("/home/daniel/Documents/Python/Bibliotheken/redpitaya_scpi")

from ltspice import Ltspice  # <-- das ist die richtige Klasse
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import redpitaya_scpi as scpi
import scipy.signal as sig

#%% Simulations Daten

l = Ltspice('./sim_data/schaltungsentwurf_no1.raw')
l.parse()
#print(l.variables)  # statt get_trace_names()

sim_freq = l.get_frequency()
LPF = l.get_data('v(/lpf)')
HPF = l.get_data('v(/hpf)')
BPF = l.get_data('v(/bpf)')
BSF = l.get_data('v(/bsf)')

# Magnitude
real_LPF_dB = 20 * np.log10(abs(LPF) + 1e-12)
real_HPF_dB = 20 * np.log10(abs(HPF) + 1e-12)
real_BPF_dB = 20 * np.log10(abs(BPF) + 1e-12)
real_BSF_dB = 20 * np.log10(abs(BSF) + 1e-12)

# Phase
phase_lp = np.degrees(np.angle(LPF))
phase_hp = np.degrees(np.angle(HPF))
phase_bp = np.degrees(np.angle(BPF))
phase_bs = np.degrees(np.angle(BSF))

sim_ampl = real_HPF_dB
sim_phase = phase_hp
#%% Redpitaya Settings
func = 'SINE'
ampl = 0.2
offset = 0.0
#freqs = np.linspace(50, 1000, 100)
freqs = np.arange(50,1000,10)
#%% SCPI Messung Import
DF_IN1 = pd.read_csv('./Komische_Phase_Ali/IN1_INT_IN.csv')
DF_IN2 = pd.read_csv('./Komische_Phase_Ali/IN2_INT_OUT.csv')

#DF_IN1 = DF_IN1.to_numpy()
#DF_IN2 = DF_IN2.to_numpy()

#%% Auswertung der Daten
#Phase läuft
w = 2 * np.pi * freqs
N = 16384  # length of data array, STEMlab buffer size
t = np.linspace(0, 8.389e-3, N)
ts = 8.389e-3 / N  # sampling time

MAG_dB = 20 * np.log10(np.abs(DF_IN2.std() / DF_IN1.std()))

PHASE_xcorr = np.empty((len(freqs)),dtype=float)

for i, freq in enumerate(freqs):
    corr = sig.correlate(DF_IN1[str(freq)].values, DF_IN2[str(freq)],method='fft')
    lags = sig.correlation_lags(len(DF_IN1[str(freq)]), len(DF_IN2[str(freq)]))
    phase_rad_xcorr = 2 * np.pi * freq * lags[np.argmax(corr)] * ts
    PHASE_xcorr[i] = phase_rad_xcorr
PHASE_deg = np.rad2deg(np.unwrap(PHASE_xcorr))
#%% Plot

plt.close('all')

# plt.figure(1,figsize = (12,9))
# plt.semilogx(sim_freq, real_LPF_dB,label = 'Lowpass')
# plt.semilogx(sim_freq, real_HPF_dB,label = 'Highpass')
# plt.semilogx(sim_freq, real_BPF_dB,label = 'Bandpass')
# plt.semilogx(sim_freq, real_BSF_dB,label = 'Bandstop')
# plt.xlabel("Frequenz [Hz]")
# plt.ylabel("Amplitude")
# plt.title('Filtertypen Simulation')
# plt.legend()
# plt.grid()
# plt.show()



plt.figure(2)
plt.subplot(3, 1, 1)
plt.semilogx(freqs, MAG_dB, label = 'Messung')
plt.semilogx(sim_freq, sim_ampl, label ='Simulation')
plt.title('Bode Plot: Magnitude')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Amplitude in dB")
plt.legend()
plt.grid()

plt.subplots_adjust(hspace=0.6)

plt.subplot(3, 1, 2)
plt.semilogx(freqs, np.rad2deg(PHASE_xcorr), label='Messung')
plt.semilogx(sim_freq, sim_phase, label='Simulation')
plt.title('Bode Plot: Phase vorher')
plt.xlabel("Frequenz [Hz]")
plt.ylabel("Phase in deg")
plt.legend()
plt.grid()

plt.subplots_adjust(hspace=0.6)
plt.subplot(3, 1, 3)
plt.semilogx(freqs, PHASE_deg, label='Messung')
plt.semilogx(sim_freq, sim_phase, label='Simulation')
plt.title('Bode Plot: Phase mit unwrap')
plt.xlabel('Frequenz [Hz]')
plt.ylabel('Phase in deg')
plt.legend()
plt.grid()























