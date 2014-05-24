__author__ = 'Галлям'

from encoding import encode
from decoding import decode
from additional import create_argument_parser

parser = create_argument_parser()
args = parser.parse_args()

if not args.encode is None:
    encode(args.encode[0], args.encode[1], args.encode[2],
           args.bit_count)
elif not args.decode is None:
    decode(args.decode[0], args.decode[1])
else:
    print("This feature isn't implemented yet")