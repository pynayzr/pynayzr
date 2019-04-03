#!/usr/bin/python

import argparse
import glob
import os
import pathlib
import statistics
import pynayzr
import imgcompare
from PIL import Image, ImageDraw


# Based on 240p
REFERENCE_BOX = {
    'tvbs': (50, 50, 150, 63),
    'ftv': (80, 43, 89, 63),
    'cti': (90, 40, 100, 60)
}


def get_time(t):
    return f'{t // 60:02d}:{t % 60:02d}'


def get_frame_time(filename):
    return int(os.path.splitext(os.path.basename(filename))[0].split('_')[0])


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--news', type=str, required=True)
    parser.add_argument('-d', '--dir', type=str, required=True)
    parser.add_argument('-o', '--output', type=str, required=True)
    parser.add_argument('--reference', nargs='+', type=int)
    parser.add_argument('--threshold', type=int, default=10)
    return parser


def main():
    args = get_parser().parse_args()
    news = args.news
    dir_path = args.dir
    out_dir = pathlib.Path(args.output)

    if not out_dir.exists():
        out_dir.mkdir()
    for i in sorted(glob.glob(f'{dir_path}/*.jpg')):
        nm = pynayzr.NewsModel(news, image_path=i)
        filename = os.path.splitext(os.path.basename(i))[0]
        nm.save_all(out_dir.joinpath(filename))

    images = sorted(glob.glob(f'{out_dir}/*_title.jpg'))
    bottoms = sorted(glob.glob(f'{out_dir}/*_bottom.jpg'))

    # Compare base
    current = images[0]
    current_i = 0

    # Unique title, (start, end), duration
    uniq = []
    times = []
    durations = []

    # Static part's box
    # NOTE: This will compare with "bottom", not title
    if args.reference:
        cp_box = args.reference
    elif news in REFERENCE_BOX:
        cp_box = REFERENCE_BOX[news]
    else:
        # XXX: Should warn user?
        cp_box = (0, 0, 1, 1)
    cp = Image.open(bottoms[0]).crop(cp_box)

    # Couting for continuous frame
    continuous = 0

    # Compare the images
    prev = current
    for index, i in enumerate(images[1:]):
        continuous += 1
        if not imgcompare.is_equal(current, i, 12):
            if continuous > args.threshold:
                im = Image.open(bottoms[current_i + 1])
                if imgcompare.is_equal(cp, im.crop(cp_box), 3):
                    uniq.append(prev)
                    times.append((get_frame_time(current),
                                  get_frame_time(i)))
                    durations.append(times[-1][1] - times[-1][0])
            current = i
            current_i = index
            continuous = 0
        prev = i

    # Print the information
    print(len(images), len(uniq),
          f'mean: {statistics.mean(durations):.2f}, '
          f'stdev: {statistics.stdev(durations):.2f}, '
          f'median: {statistics.median(durations)}')

    # Output
    TIME_DURATION_SPACE = 100
    w, h = Image.open(uniq[0]).size
    w += TIME_DURATION_SPACE  # Give some space for time
    im = Image.new('RGB', (w, h * len(uniq)), '#FFFFFF')
    for index, i in enumerate(uniq):
        duration = ' ~ '.join(
            [get_time(times[index][0]),get_time(times[index][1] - 1)])
        im.paste(Image.open(i), (0, h * index))
        ImageDraw.Draw(im).text(
            (w - (TIME_DURATION_SPACE - 10), h * index + 10),
            duration,
            (0, 0, 0))
    im.save('out.jpg')


if __name__ == '__main__':
    main()
