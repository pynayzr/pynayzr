# -*- coding: utf-8 -*-
import os
import asyncio
import subprocess
import tempfile
from PIL import Image


support_news = {
    'ttv': 'https://www.youtube.com/watch?v=yk2CUjbyyQY',
    'ctv': 'https://www.youtube.com/watch?v=hVNbIZYi1nI',
    'cts': 'https://www.youtube.com/watch?v=TL8mmew3jb8',
    'pts': 'https://www.youtube.com/watch?v=_isseGKrquc',
    'ebc': 'https://www.youtube.com/watch?v=dxpWqjvEKaM',
    'cti': 'https://www.youtube.com/watch?v=wUPPkSANpyo',
    'ftv': 'https://www.youtube.com/watch?v=XxJKnDLYZz4',
    'set': 'https://www.youtube.com/watch?v=4ZVUmEUFwaY',
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


async def aget(news):
    """Async get livestream frame by news media.

    Args:
        news (str): news media list in support_news
    Returns:
        Image.Image: PIL Image instance
    """
    if news not in support_news:
        raise KeyError

    # Other news using youtube
    with tempfile.TemporaryDirectory() as temp_dir:
        streamlink = ' '.join([
            'streamlink',
            '-O',
            support_news[news],
            '720p'
        ])

        ffmpeg = ' '.join([
            'ffmpeg',
            '-i',
            '-',
            '-f',
            'image2',
            '-vframes',
            '1',
            '%s/out.jpg' % (temp_dir)
        ])

        read, write = os.pipe()
        p1 = await asyncio.create_subprocess_shell(
            streamlink,
            stdout=write,
            stderr=asyncio.subprocess.DEVNULL)
        os.close(write)
        p2 = await asyncio.create_subprocess_shell(
            ffmpeg,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
            stdin=read)
        os.close(read)
        await p1.communicate()
        await p2.communicate()
        return Image.open('%s/out.jpg' % (temp_dir))


async def aget_all():
    async def mark(key, coro):
        return key, await coro
    d = {news: aget(news) for news in support_news}
    return {
        key: result
        for key, result in await asyncio.gather(
                *(mark(key, coro) for key, coro in d.items()))
        }
