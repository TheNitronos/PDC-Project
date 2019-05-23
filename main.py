from src.helper import *

import os
import argparse
import pathlib

import numpy as np

TEXT_FILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Text-Files/")

def parse_args():
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

    return args

if __name__ == '__main__':
    args = parse_args()

    INPUT_FILENAME  = args.input_file
    OUTPUT_FILENAME = args.output_file

    SENT_SIGNAL_FILENAME     = str(args.input_file)[:-4]  + "-sent-signal.txt"
    RECEIVED_SIGNAL_FILENAME = str(args.output_file)[:-4] + "-received-signal.txt"

    booleans = read_file(INPUT_FILENAME)

    ## TODO: turn the booleans (binary representation of INPUT_FILENAME content) into the signal to send and
    ##       save it in SENT_SIGNAL_FILENAME file

    server_command = """python ext/client.py \
                        --input_file {} \
                        --output_file {} \
                        --srv_hostname iscsrv72.epfl.ch \
                        --srv_port 80""".format(SENT_SIGNAL_FILENAME,
                                                RECEIVED_SIGNAL_FILENAME)

    os.system(server_command)

    ## TODO: use the received signal in RECEIVED_SIGNAL_FILENAME file to recover the binary representation of
    ##       the received message and affect it to output_message variable (uncomment and complete the following lines)

    # output_message = #todo
    # write_file(output_message)

    # check_successful_transmission(INPUT_FILENAME, OUTPUT_FILENAME)
