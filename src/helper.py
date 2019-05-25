import numpy as np

from numpy.fft    import fft, ifft, fftfreq
from random       import choice

Fs = 22050
Ts = 1/Fs

A = 1
K = 15
W = 2000

BITS_PER_BYTE    = 8
NUMBERS_OF_BYTES = 10
NUMBER_OF_BITS   = NUMBERS_OF_BYTES * BITS_PER_BYTE
SIGNAL_LENGTH    = NUMBER_OF_BITS * K

FREQUENCY_1 = 2000
FREQUENCY_2 = 4000
FREQUENCY_3 = 6000
FREQUENCY_4 = 8000

t = np.linspace(0, Ts*NUMBER_OF_BITS, SIGNAL_LENGTH)
f = fftfreq(SIGNAL_LENGTH, Ts)

def encoder(bits):
    signal_temp = np.repeat([A if b else -A for b in bits], K)
    return signal_temp * modulator(len(signal_temp))

def cos_demodulator(signal, omega):
    signal_frequencies = fft(signal) * passband_filter(f, omega, W)
    demodulated_signal_frequencies = fft(ifft(signal_frequencies) * cos_modulator(omega)) * passband_filter(f, 0, W)
    return ifft(demodulated_signal_frequencies)

def demodulator(signal):
    return 2 * 4/3 * (cos_demodulator(signal, FREQUENCY_1) + cos_demodulator(signal, FREQUENCY_2) + cos_demodulator(signal, FREQUENCY_3) + cos_demodulator(signal, FREQUENCY_4))


def passband_filter(frequencies, omega, width):
    filter = np.zeros(frequencies.size)
    for i in np.argwhere(abs(abs(frequencies)-omega) <= width/2):
        filter[i] = 1
    return filter

def decoder(signal_input):
    signal_output = []

    for i in range(NUMBER_OF_BITS):
        acc = 0
        for j in range(K):
            acc += signal_input[i * K + j]
        signal_output.append(acc//K)

    return signal_output

def cos_modulator(signal_length, omega):
    return np.array([np.cos(2*np.pi*omega*a*Ts) for a in range(signal_length)])

def modulator(signal_length):
    return (cos_modulator(signal_length, FREQUENCY_1) + \
            cos_modulator(signal_length, FREQUENCY_2) + \
            cos_modulator(signal_length, FREQUENCY_3) + \
            cos_modulator(signal_length, FREQUENCY_4)) / 4

def random_detection_sequence(length):
    return [choice([True, False]) for _ in range(length)]

def find_signal(signal, sent_signal_length, detection_sequence):
    encoded_detection_sequence = encoder(detection_sequence)
    convolution = np.correlate(signal, encoded_detection_sequence)
    i = np.argmax(convolution)
    return signal[i:i+sent_signal_length]

def decode(received_signal, detection_sequence, sent_signal_length):
    signal_input  = demodulator(find_signal(received_signal, sent_signal_length, detection_sequence))
    signal_output = []

    for i in range(sent_signal_length//K-len(detection_sequence)):
        acc = 0
        for j in range(K):
            acc += signal_input[len(detection_sequence) + i * K + j]
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

# import numpy as np
#
# from random import choice
#
# Fs = 22050
# Ts = 1/Fs
#
# A = 1
# K = 14
# W = 1575
#
# def random_detection_sequence(length):
#     return [choice([True, False]) for _ in range(length)]
#
# def find_signal(signal, sent_signal_length, detection_sequence):
#     encoded_detection_sequence = encode(detection_sequence)
#     convolution = np.correlate(signal, encoded_detection_sequence)
#     i = np.argmax(convolution)
#     return signal[i:i+sent_signal_length]
#
#
# def cos_modulation(frequency, signal_length):
#     return np.array([np.cos(2*np.pi*frequency*a*Ts) for a in range(signal_length)])
#
# def modulation(length):
#     return (cos_modulation(2000, length) + \
#             cos_modulation(4000, length) + \
#             cos_modulation(6000, length) + \
#             cos_modulation(8000, length)) / 4
#
# def encode(list_of_booleans):
#     bits   = [A if b else -A for b in list_of_booleans]
#     signal = np.repeat(bits, K)
#
#     return modulation(len(signal))*signal
#
# def decode(received_signal, detection_sequence, sent_signal_length):
#     signal_input  = find_signal(received_signal, sent_signal_length, detection_sequence)/modulation(sent_signal_length)
#     signal_output = []
#
#     for i in range(sent_signal_length//K-len(detection_sequence)):
#         acc = 0
#         for j in range(K):
#             acc += signal_input[len(detection_sequence) + i * K + j]
#         if (acc//K < 0):
#             signal_output.append(False)
#         else:
#             signal_output.append(True)
#
#     return signal_output
