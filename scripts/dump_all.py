#!/usr/bin/python3

import json
import pathlib
import asyncio
import pynayzr
from argparse import ArgumentParser
from PIL import Image


def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--bc', action='store', type=str)
    parser.add_argument('--dir', action='store', type=str, required=True)
    parser.add_argument('-i')
    return parser


def main():
    args = get_parser().parse_args()

    support_news = list(pynayzr.streams.support_news.keys())
    if args.bc:
        pynayzr.ocr.set_bing_credentials(args.bc)
        parser = pynayzr.ocr.parse_by_bing
        aparser = pynayzr.ocr.parse_by_async_bing
    else:
        parser = pynayzr.ocr.parse_by_async_tesseract
        aparser = None

    nm = asyncio.run(
        pynayzr.core.async_analyze(support_news,
                                   parser=parser,
                                   aparser=aparser,
                                   parse=True))

    w, h = nm['tvbs'].img.size
    im = Image.new('RGB', (w * 3, h * 3), '#FFFFFF')
    for index, v in enumerate(nm.items()):
        news, model = v
        r = index // 3
        c = index % 3
        im.paste(model.img, (c * w, r * h))

    # Make dir
    dir_path = pathlib.Path(args.dir)
    dir_path.mkdir(parents=True, exist_ok=True)

    # Dump all
    im.save(dir_path.joinpath('wall.jpg'))
    for news, model in nm.items():
        # Dump img
        model.save_all(dir_path.joinpath(f'{news}'))

        # Dump text json
        with open(dir_path.joinpath(f'{news}.json'), 'w') as f:
            f.write(model.to_json())


if __name__ == '__main__':
    main()
