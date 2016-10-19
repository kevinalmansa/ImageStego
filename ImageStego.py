#!/usr/bin/env python3
import argparse
import os
from StegoImage import LSBStego


def verify_dirs(paths):
    for verif_dir in paths:
        if verif_dir is not None:
            if not os.path.isdir(verif_dir):
                print("Error: " + verif_dir + " does not exist.")
                return False
            if not os.access(verif_dir, os.W_OK):
                print("Error: " + verif_dir + " is not writable")
                return False
    return True


def verify_stores(paths):
    for verify_file in paths:
        if verify_file is not None:
            if not os.path.isfile(verify_file):
                print("Error: " + verify_file + " does not exist.")
                return False
            if not os.access(verify_file, os.W_OK):
                print("Error: " + verify_file + " is not writable")
                return False
    return True


def main():
    parser = argparse.ArgumentParser(description='Steganography Demonstration of LSB',
                                     epilog='Created by Kevin Almansa')
    # parser.add_argument('-a', '--algo', help='Algorithm to use', default='lsb', type=str, choices=["lsb", "dct"],
    #                     required=True)
    parser.add_argument('-p', '--planes', help='Number of bitplanes to use', type=int, default=3, required=True)
    parser.add_argument('-s', '--store', metavar='path', help='Data to store', type=str)
    parser.add_argument('-e', '--extract', metavar='path', help='Path for extracted data', type=str)
    parser.add_argument('-si', '--storeimage', metavar='path', help='Image to store', type=str)
    parser.add_argument('-ei', '--extractimage', metavar='path', help='Path for extracted image', type=str)
    parser.add_argument('-o', '--outdir', metavar='path', help='Output Directory for new Images or Data', type=str,
                        default='misc/Stego/', required=True)
    parser.add_argument('-b', '--bitplanes', metavar='path', help='Path for bitplanes to be extracted to', type=str)
    parser.add_argument('-g', '--debug', metavar='path', help='Path to output debug information', type=str)
    parser.add_argument('inputfile', metavar='path', type=str)
    args = parser.parse_args()
    print(args)
    if not verify_dirs((args.outdir, args.bitplanes, args.debug)):
        return None
    if not os.path.isfile(args.inputfile) and os.access(args.inputfile, os.R_OK):
        return None
    if not verify_stores((args.storeimage, args.store)):
        return None
    if args.planes < 1 or args.planes > 8:
        print("Error: Planes value must be between 1 and 8")
        return None

    stegoApplication = LSBStego.LSBStego(args.outdir, args.bitplanes, args.debug)
    if args.storeimage is not None:
        stegoApplication.insert_image(args.inputfile, args.storeimage, args.planes)
    if args.extractimage is not None:
        stegoApplication.extract_image(args.inputfile, args.extractimage, args.planes)
    if args.store is not None:
        stegoApplication.insert_binary(args.inputfile, args.store, args.planes)
    if args.extract is not None:
        stegoApplication.extract_binary(args.inputfile, args.extract, args.planes)


if __name__ == '__main__':
    main()
