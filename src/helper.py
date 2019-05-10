import numpy as np

def read_file(filename):
    read_chars_in_bits = None

    with open(filename, mode="rb") as file:
        read_chars_in_bits = file.read()

    read_chars_in_bits_length = len(read_chars_in_bits)

    np_array_of_bytes = np.empty(read_chars_in_bits_length, dtype=np.int8)

    for i in range(read_chars_in_bits_length):
        np_array_of_bytes[i] = read_chars_in_bits[i]

    return np_array_of_bytes
