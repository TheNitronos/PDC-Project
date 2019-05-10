from src.helper import *

import os
import argparse
import pathlib

import numpy as np

TEXT_FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Text-Files/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Read bytes from .txt file containing characters",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--input_file', type=str, required=True,
                        help='.txt file containing chararacters.')

    args = parser.parse_args()
    args.input_file = pathlib.Path(TEXT_FILES_PATH+args.input_file).resolve(strict=True)

    if not (args.input_file.is_file() and
            (args.input_file.suffix == '.txt')):
        raise ValueError('Parameter[input_file] is not a .txt file.')

    print(read_file(args.input_file))
