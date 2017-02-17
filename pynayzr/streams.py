# -*- coding: utf-8 -*-

from PIL import Image
import subprocess
import tempfile

TIMEOUT = 1

support_news = {
    'pts': 'https://www.youtube.com/watch?v=zjGR32QyTkQ',
    'ttv': 'https://www.youtube.com/watch?v=yk2CUjbyyQY',
    'set': 'https://www.youtube.com/watch?v=TgGyBF-7w8M',
    'cti': 'https://www.youtube.com/watch?v=VsvZqiB2y1o',
    'ebc': 'https://www.youtube.com/watch?v=yzE3bRtXIrI',
    'ftv': 'https://www.youtube.com/watch?v=XxJKnDLYZz4',
    'ctv': 'https://www.youtube.com/watch?v=b3QIfgD--_E',
    'cts': 'https://www.youtube.com/watch?v=1I6fxNSmQh4',
    'tvbs': 'http://bcoveliveios-i.akamaihd.net/hls/live/255252/4005328949001_13/playlistTVBS-N-HD-CH1-M.m3u8'
}


def tvbs():
    # NOTE: Not sure tvbs link will expire or not
    with tempfile.TemporaryDirectory() as temp_dir:
        ffmpeg = [
            'ffmpeg',
            '-i',
            support_news['tvbs'],
            '-f',
            'image2',
            '-vframes',
            '1',
            '%s/out.jpg' % (temp_dir)
        ]

        p2 = subprocess.Popen(ffmpeg,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
        p2.communicate()

        return Image.open('%s/out.jpg' % (temp_dir))


def get(news):
    if news not in support_news:
        raise KeyError

    # TVBS not using youtube
    if news.startswith('tvbs'):
        return tvbs()

    # Other news using youtube
    with tempfile.TemporaryDirectory() as temp_dir:
        livestream = [
            'livestreamer',
            '-O',
            support_news[news],
            '720p'
        ]

        ffmpeg = [
            'ffmpeg',
            '-i',
            '-',
            '-f',
            'image2',
            '-vframes',
            '1',
            '%s/out.jpg' % (temp_dir)
        ]

        p1 = subprocess.Popen(livestream, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(ffmpeg, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, stdin=p1.stdout)
        p1.stdout.close()
        p2.communicate()

        return Image.open('%s/out.jpg' % (temp_dir))
