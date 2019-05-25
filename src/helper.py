import numpy as np

from random import choice

Fs = 22050
Ts = 1/Fs

A = 1
K = 14
W = 1575

def random_detection_sequence(length):
    return [choice([True, False]) for _ in range(length)]

def find_signal(signal, sent_signal_length, detection_sequence):
    encoded_detection_sequence = encode(detection_sequence)
    convolution = np.correlate(signal, encoded_detection_sequence)
    i = np.argmax(convolution)
    return signal[i:i+sent_signal_length]


def cos_modulation(frequency, signal_length):
    return np.array([np.cos(2*np.pi*frequency*a*Ts) for a in range(signal_length)])

def modulation(length):
    return (cos_modulation(2000, length) + \
            cos_modulation(4000, length) + \
            cos_modulation(6000, length) + \
            cos_modulation(8000, length)) / 4

def encode(list_of_booleans):
    bits   = [A if b else -A for b in list_of_booleans]
    signal = np.repeat(bits, K)

    return modulation(len(signal))*signal

def decode(received_signal, detection_sequence, sent_signal_length):
    signal_input  = find_signal(received_signal, sent_signal_length, detection_sequence)/modulation(sent_signal_length)
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
