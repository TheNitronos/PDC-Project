import numpy as np

from numpy.fft    import rfft, irfft, rfftfreq
from random       import choice

Fs = 22050
Ts = 1/Fs

A = 1
K = 15
W = 2000

FREQUENCY_1 = 2000
FREQUENCY_2 = 4000
FREQUENCY_3 = 6000
FREQUENCY_4 = 8000

def frequencies(signal_length):
    return rfftfreq(signal_length, Ts)

def passband_filter(signal_length, omega):
    passband_frequencies = frequencies(signal_length)
    filter               = np.zeros(passband_frequencies.size)
    for i in np.argwhere(passband_frequencies-omega <= W/2):
        filter[i] = 1
    return filter

def cos_modulator(signal_length, omega):
    return np.array([np.cos(2*np.pi*omega*a*Ts) for a in range(signal_length)])

def cos_demodulator(signal, omega):
    signal_length      = len(signal)
    signal_frequencies = rfft(signal) * passband_filter(signal_length, omega)
    demodulated_signal = irfft(signal_frequencies) * cos_modulator(signal_length, omega)
    demodulated_signal_frequencies = rfft(demodulated_signal) * passband_filter(signal_length, 0)
    return irfft(demodulated_signal_frequencies)

def modulator(signal_length):
    return (cos_modulator(signal_length, FREQUENCY_1) + \
            cos_modulator(signal_length, FREQUENCY_2) + \
            cos_modulator(signal_length, FREQUENCY_3) + \
            cos_modulator(signal_length, FREQUENCY_4)) / 4

def demodulator(signal):
    return 2 * 4/3 * (cos_demodulator(signal, FREQUENCY_1) + \
                      cos_demodulator(signal, FREQUENCY_2) + \
                      cos_demodulator(signal, FREQUENCY_3) + \
                      cos_demodulator(signal, FREQUENCY_4))

def random_detection_sequence(length):
    return [choice([True, False]) for _ in range(length)]

def find_signal(signal, sent_signal_length, detection_sequence):
    encoded_detection_sequence = encoder(detection_sequence)
    correlation = np.correlate(signal, encoded_detection_sequence)
    i = np.argmax(correlation)
    return signal[i:i+sent_signal_length+len(detection_sequence)]

def encoder(bits):
    signal        = np.repeat([A if b else -A for b in bits], K)
    signal_length = len(signal)
    signal        = irfft(rfft(signal)*passband_filter(signal_length, 0))
    return modulator(signal_length) * signal

def decoder(received_signal, detection_sequence, sent_signal_length):
    signal_input  = demodulator(find_signal(received_signal, sent_signal_length, detection_sequence))
    signal_output = []

    for i in range(sent_signal_length//K):
        acc = 0
        for j in range(K):
            acc += signal_input[i * K + j]
        if (acc//K < 0):
            signal_output.append(False)
        else:
            signal_output.append(True)

    return signal_output

def check_successful_transmission(input_filename, output_filename):
    with open(input_filename, mode="rb") as input_file:
        with open(output_filename, mode="rb") as output_file:
            if (input_file.read() == output_file.read()):
                print("The transmission was successful ! :)")
            else:
                print("The transmission failed miserably ! :(")
