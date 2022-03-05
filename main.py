import argparse

from pathlib import Path

from features.AndroGuard import AndroGuardWrapper
from features.LIEF import LIEFWrapper
from core.Constants import BASE_PROTO_CLASS


"""
Usage:

python main.py -i my.apk -o classes.txt [--base 'Lcom/google/protobuf/GeneratedMessageLite;']
"""

def arg_parser():
    parser = argparse.ArgumentParser(description='Android app static analyser')

    parser.add_argument('-i', '--input',    help='Input android file',                                        required=True)
    parser.add_argument('-o', '--output',   help='Output file',                                               required=True)
    parser.add_argument('--base',           help='Base class',                    default=BASE_PROTO_CLASS,   required=False)
    parser.add_argument('-s',               help='TODO: Get strings from binary', default=False,              required=False, type=bool)
    
    
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = arg_parser()

    assert Path(args.input).exists(), f'The file doesn\'t exist: {args.input}'
    assert Path(args.output).parent.exists(), f'The parent directory for output doesn\'t exist: {args.output}'

    # Input
    path = Path(args.input)
    output = Path(args.output)

    isGetStrings = args.s
    baseClassSmaliName = args.base

    # Set up AndroGuard
    AndroGuard = AndroGuardWrapper()
    AndroGuard.load(path)
    AndroGuard = AndroGuard.analyse()

    # Get class extends for base class
    res = AndroGuard.extendClassNameList(
        AndroGuard.classAnalysis(
            baseClassSmaliName
        )
    )

    # Save data to the output file
    with output.open(mode='w') as out_stream:
        out_stream.write('\n'.join(res))

    # print('Hello world')