from src.helper import *

import os
import argparse
import pathlib

import numpy as np

TEXT_FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Text-Files/")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Read/Write bytes from .txt file",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--input_file', type=str, required=True,
                        help='.txt file containing bytes to transmit.')

    parser.add_argument('--output_file', type=str, required=True,
                        help='.txt file containing transmitted bytes.')

    args = parser.parse_args()

    args.input_file  = pathlib.Path(TEXT_FILES_PATH+"Inputs/" +args.input_file ).resolve(strict=True)
    args.output_file = pathlib.Path(TEXT_FILES_PATH+"Outputs/"+args.output_file).resolve(strict=False)

    if not (args.input_file.is_file() and
            (args.input_file.suffix == '.txt')):
        raise ValueError('Parameter[input_file] is not a .txt file.')

    if not (args.output_file.suffix == '.txt'):
        raise ValueError('Parameter[output_file] is not a .txt file.')

    temp = read_file(args.input_file)
    #temp is a list of booleans
    write_file(temp, args.output_file)

    check_successful_transmission(args.input_file, args.output_file)
