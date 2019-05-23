import numpy as np

from random import choice

Fs = 22050
Ts = 1/Fs

A = 1
K = 14
W = 1575

def random_detection_sequence(length):
    return [choice([True, False]) for _ in range(length)]

def cos_modulation(frequency, signal_length):
    return np.array([np.cos(2*np.pi*frequency*a*Ts) for a in range(signal_length)])

def encode(list_of_booleans):
    bits   = [A if b else -A for b in list_of_booleans]
    signal = np.repeat(bits, K)

    signal_length = len(signal)

    modulation = cos_modulation(2000, signal_length) + \
                 cos_modulation(4000, signal_length) + \
                 cos_modulation(6000, signal_length) + \
                 cos_modulation(8000, signal_length)

    return modulation*signal/4

def decode(received_signal, sent_signal_length):
    signal_input  = received_signal[-sent_signal_length:]
    signal_output = []

    for i in range(sent_signal_length//K):
        acc = 0
        for j in range(K):
            acc += signal_input[i * K + j]
        signal_output.append(acc//K)

    return signal_output

def check_successful_transmission(input_filename, output_filename):
    with open(input_filename, mode="rb") as input_file:
        with open(output_filename, mode="rb") as output_file:
            if (input_file.read() == output_file.read()):
                print("The transmission was successful ! :)")
            else:
                print("The transmission failed miserably ! :(")
