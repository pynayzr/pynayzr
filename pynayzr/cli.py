#! /usr/bin/python3
# -*- coding: utf-8 -*-

import pynayzr
from pynayzr import ocr
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('--bc', '--bing-credentials',
                        action='store',
                        type=str,
                        help='Specific Bing Computer Vision API credentials key')
    parser.add_argument('--gc', '--google-credentials',
                        action='store',
                        type=str,
                        help='Specific Google API credentials json filename')
    parser.add_argument('-n', '--news',
                        action='store',
                        type=str,
                        dest='news',
                        help='Specific which news to analyze')
    parser.add_argument('-i', '--input', action='store', type=str,
                        help='input image filename')
    parser.add_argument('-o', '--output-name',
                        action='store',
                        type=str,
                        dest='output',
                        help='Specific image output place')

    args = parser.parse_args()

    # Settings for API Crednetials
    parser = ocr.parse_by_tesseract
    if args.bc:
        pynayzr.set_bing_credentials(args.bc)
        parser = ocr.parse_by_bing
    if args.gc:
        pynayzr.set_google_credentials(args.gc)
        parser = ocr.parse_by_google

    # Parse News, and select image source (from live or local image)
    analyze = None
    if args.news:
        if args.input:
            analyze = pynayzr.NewsModel(args.news,
                                        image_path=args.input, parser=parser,
                                        _async=False)
        else:
            analyze = pynayzr.analyze(args.news, parser=parser,
                                      _async=False)
        print(analyze.to_json())

    if args.output and analyze:
            analyze.save_all(args.output)


if __name__ == '__main__':
    main()
