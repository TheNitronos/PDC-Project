
def read_file(filename):
    read_text = None

    with open(filename, mode="r") as file:
        read_text = file.read()

    encoded_text = read_text.encode("utf-8")
    list_of_booleans = []

    for byte in encoded_text:
        for bit in bin(byte)[2:]:
            if bit == "0":
                list_of_booleans.append(True)
            elif  bit == "1":
                list_of_booleans.append(False)
            else:
                raise Exception("Bits should have value 0 or 1, found : {}".format(bit))

    return list_of_booleans

def write_file(list_of_booleans, filename):
    return
