import asyncio
import pynayzr
from PIL import Image


support_news = list(pynayzr.streams.support_news.keys())
print('Support News:')
print(support_news)

nm = asyncio.run(
    pynayzr.core.async_analyze(support_news, parse=False))

w, h = nm['tvbs'].img.size
im = Image.new('RGB', (w * 3, h * 3), '#FFFFFF')

for index, v in enumerate(nm.items()):
    news, model = v
    r = index // 3
    c = index % 3
    im.paste(model.img, (c * w, r * h))

im.show()
