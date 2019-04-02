import asyncio
import pynayzr
from PIL import Image


support_news = list(pynayzr.streams.support_news.keys())
print('Support News:')
print(support_news)

images = asyncio.run(pynayzr.streams.aget_all())

w, h = images['pts'].size
im = Image.new('RGB', (w * 3, h * 3), '#FFFFFF')

for index, v in enumerate(images.items()):
    news, image = v
    r = index // 3
    c = index % 3
    im.paste(image, (c * w, r * h))

im.show()
