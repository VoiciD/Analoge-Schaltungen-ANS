# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ltspice as lts

meas_data_bs_q1 = pd.read_csv("../Chap4/freq_sweep_bs_Q1.csv")
freq = meas_data_bs_q1['Frequency [Hz]']
mag = meas_data_bs_q1[' Amplitude [dB]']
phase = meas_data_bs_q1[' Phase [deg]']


plt.figure()
plt.plot(freq,mag,color = "blue",label="Magnitude[dB]")
plt.plot(freq,phase,color="green",label="Phase [deg]")
plt.xscale('log')
plt.title("Messung Bandsperre Q=1")
plt.xlabel("Frequenz [Hz]")
plt.legend()
plt.grid()