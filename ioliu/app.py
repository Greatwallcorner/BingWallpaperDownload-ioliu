# -*- coding: utf-8 -*-
"""
heatdesert
"""
import argparse

from core import ioliudownload

parser = argparse.ArgumentParser(prog='bingwp', description='download bing wallpaper')
parser.add_argument('o', '--output', type=str, help='file output path')
parser.add_argument('-p', '--pack', action='store_true', help='pack file')
args = parser.parse_args()


def main():
    """

    """
    path = None
    whether_pack = False

    if args.output is not None:
        path = args.output
    else:
        raise Exception('output is None')

    if args.pack is True:
        whether_pack = True

    ioliudownload(path, whether_pack)


if __name__ == '__main__':
    main()