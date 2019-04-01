# -*- coding: utf-8 -*-

from PIL import Image
import subprocess
import tempfile


support_news = {
    'pts': 'https://www.youtube.com/watch?v=_isseGKrquc',
    'ttv': 'https://www.youtube.com/watch?v=yk2CUjbyyQY',
    'set': 'https://www.youtube.com/watch?v=4ZVUmEUFwaY',
    'cti': 'https://www.youtube.com/watch?v=wUPPkSANpyo',
    'ebc': 'https://www.youtube.com/watch?v=dxpWqjvEKaM',
    'ftv': 'https://www.youtube.com/watch?v=XxJKnDLYZz4',
    'ctv': 'https://www.youtube.com/watch?v=DVOHYy_m_qU',
    'cts': 'https://www.youtube.com/watch?v=TL8mmew3jb8',
    'tvbs': 'https://www.youtube.com/watch?v=Hu1FkdAOws0'
}


def get(news):
    """Get Livestream frame by news media.

    Args:
        news (str): news media list in support_news
    Returns:
        Image.Image: PIL Image instance
    """
    if news not in support_news:
        raise KeyError

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
