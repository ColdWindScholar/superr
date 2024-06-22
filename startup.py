#!/usr/bin/env python3

import sys
import argparse
from collections import OrderedDict

func_dict = OrderedDict([
    ('unpack_img', 'partition.img'),
    ('pack_img', 'partition.img mode\n    MODE OPTIONS: raw, sparse, dat, lz4'),
    ('unpack_super', 'super.img'),
    ('pack_super',
     'part1.img [part2.img ...] mode\n    MODE OPTIONS: raw, sparse, dat, lz4'),
    ('deodex', ''),
    ('dmverity', ''),
    ('forcee', '\n ')
])


def do_parse():
    def Formatter(prog):
        return argparse.RawTextHelpFormatter(prog, max_help_position=7)

    def req_check(argr):
        for i in argr:
            if '--'+i in sys.argv or '-'+i[0] in sys.argv:
                return True
        return False

    parser = argparse.ArgumentParser(
        description="SuperR's Kitchen functions from the command line.",
        formatter_class=Formatter,
        epilog='*If no arguments are provided, the interactive kitchen will launch.*',
        add_help=False
    )

    optional = parser.add_argument_group('Optional')

    optional.add_argument(
        '--mainram',
        nargs='*',
        help=argparse.SUPPRESS
    )
    optional.add_argument(
        '--otherfile',
        nargs='*',
        help=argparse.SUPPRESS
    )
    optional.add_argument(
        '-f', '--function',
        required=req_check(['project']),
        nargs='+',
        metavar=('FUNCTION', 'ARGS'),
        help='\nFUNCTION OPTIONS/EXAMPLES:\n'
        + '-'.ljust(26, '-')+'\n-f '
        + '\n-f '.join([i+' '+func_dict[i] for i in func_dict])
    )
    optional.add_argument(
        '-p', '--project',
        required=req_check(['function']),
        metavar='DIRECTORY',
        help='\nEXAMPLE:\n'+'-'.ljust(8, '-')+'\n-p superr_Name\n '
    )
    optional.add_argument(
        '-h', '--help',
        action='help',
        help='\nShow this help message and exit'
    )

    return parser.parse_args()


def main(j, mfunc):
    args = do_parse()

    if args.function:
        srkcli = mfunc(sys._MEIPASS+'/srkcli')
        srkcli.main(j, args, func_dict)
    elif args.mainram:
        syslen = len(args.mainram)

        filetype = action = extra = ''
        base = args.mainram[0]
        func = args.mainram[1]

        if syslen > 2:
            romname = args.mainram[2]

            if syslen > 3:
                filetype = args.mainram[3]

            if syslen > 4:
                action = args.mainram[4]

            if syslen > 5:
                extra = args.mainram[5]
        else:
            print('ramdisk cannot be run outside the kitchen')
            sys.exit(1)

        mainram = mfunc(base+'/tools/source/mainram')
        mainram.ramdisk(j, base, func, romname, filetype, action, extra)
    elif args.otherfile:
        otherfile = mfunc(args.otherfile[0])
        otherfile.main(j, *args.otherfile[1:])
    else:
        mainsrk = mfunc(sys._MEIPASS+'/mainsrk')
        mainsrk.superr(j, mfunc)
