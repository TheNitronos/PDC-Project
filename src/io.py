import bitarray

def read_file(filename):
    read_bytes = None

    with open(filename, mode="rb") as file:
        read_bytes = file.read()

    list_of_booleans = bitarray.bitarray()
    list_of_booleans.frombytes(read_bytes)
    list_of_booleans = list_of_booleans.tolist()

    return list_of_booleans

def write_file(list_of_booleans, filename):
    binary_text_to_save = bitarray.bitarray(list_of_booleans).tobytes()

    with open(filename, mode="wb") as file:
        file.write(binary_text_to_save)
