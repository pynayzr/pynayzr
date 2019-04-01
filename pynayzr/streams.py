# -*- coding: utf-8 -*-

from PIL import Image
import subprocess
import tempfile


support_news = {
    'pts': 'https://www.youtube.com/watch?v=zjGR32QyTkQ',
    'ttv': 'https://www.youtube.com/watch?v=yk2CUjbyyQY',
    'set': 'https://www.youtube.com/watch?v=15IKxpj1gQA',
    'cti': 'https://www.youtube.com/watch?v=wUPPkSANpyo',
    'ebc': 'https://www.youtube.com/watch?v=E07WI7WxVZY',
    'ftv': 'https://www.youtube.com/watch?v=XxJKnDLYZz4',
    'ctv': 'https://www.youtube.com/watch?v=qIa-L8URVBI',
    'cts': 'https://www.youtube.com/watch?v=7UF21-RF0pY',
    'tvbs': 'https://bcsecurelivehls-i.akamaihd.net/hls/live/510708/4862438529001/playlistTVBS-N-HD-CH1-M.m3u8'
}


def tvbs():
    """Return TVBS livestream frame
    # NOTE: Not sure tvbs link will expire or not
    """
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
    """Get Livestream frame by news media.

    Args:
        news (str): news media list in support_news
    Returns:
        Image.Image: PIL Image instance
    """
    if news not in support_news:
        raise KeyError

    # TVBS not using youtube
    if news.startswith('tvbs'):
        return tvbs()

    # Other news using youtube
    with tempfile.TemporaryDirectory() as temp_dir:
        streamlink = [
            'streamlink',
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

        p1 = subprocess.Popen(streamlink, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(ffmpeg, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, stdin=p1.stdout)
        p1.stdout.close()
        p2.communicate()

        return Image.open('%s/out.jpg' % (temp_dir))
