"""
Main module for all program
"""
__author__ = 'Галлям'

from src.encoding import encode
from src.decoding import decode
from src.additional import create_argument_parser

parser = create_argument_parser()
args = parser.parse_args()

if not args.encode is None:
    encode(args.encode[0], args.encode[1], args.encode[2],
           args.bit_count)
elif not args.decode is None:
    decode(args.decode[0], args.decode[1])
else:
    print("This feature isn't implemented yet")
