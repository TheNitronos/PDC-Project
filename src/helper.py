def read_file(filename):
    text = None

    with open(filename, mode="rt", encoding="utf-8") as file:
        text = file.read()

    return text
