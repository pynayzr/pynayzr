# -*- coding: utf-8 -*-
#
# file: ocr.py
# description: ocr.py provide an interface for image translate to text.
#
# API:
#    parse_by_provider(img)
# Args:
#    img (Image.Image): Python PIL Image instance
#
# Returns:
#    str: The text in the img
#

import aiohttp
import requests
from PIL import Image

# Tesseract
import pyocr
import pyocr.builders
import async_pyocr

# Google Vision API
import io
import base64
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

# Tesseract Settings
tools = pyocr.get_available_tools()
tool = tools[0]
async_tools = async_pyocr.get_available_tools()
async_tool = async_tools[0]
lang = 'chi_tra'

# Google Vision Settings
credentials = None
service = None

# Bing Computer Vision Settings
bing_api = ('https://japaneast.api.cognitive.microsoft.com/vision/v1.0/ocr?'
            'language=zh-Hant&detectOrientation=false')
bing_credentials = None


def set_bing_credentials(key):
    global bing_credentials
    bing_credentials = key


def set_google_credentials(file_path):
    global credentials, service
    credentials = ServiceAccountCredentials.from_json_keyfile_name(file_path)
    service = discovery.build('vision', 'v1', credentials=credentials)


def get_google_credentials():
    return credentials, service


def parse_by_tesseract(img):
    return tool.image_to_string(img.convert('L'), lang=lang,
                                builder=pyocr.builders.TextBuilder())


async def parse_by_async_tesseract(img):
    return await async_tool.image_to_string(img.convert('L'), lang=lang)


def merge_imgs(imgs):
    wa = [img.size[0] for img in imgs]
    ha = [img.size[1] for img in imgs]
    w = max(wa)
    h = sum(ha) + 10 * len(ha)

    im = Image.new('RGB', (w, h), '#000000')
    for index, img in enumerate(imgs):
        im.paste(img, (0, sum(ha[:index]) + 10 * index))
    return im


def parse_by_bing(imgs: list):
    if not bing_credentials:
        raise ValueError('Set Bing Computer Vision API Credentials first')

    one_img = False
    if isinstance(imgs, Image.Image) or len(imgs) == 1:
        one_img = True
        img = imgs[0] if isinstance(imgs, list) else imgs

        # Check if image size have 50x50
        w, h = img.size
        if w < 50 or h < 50:
            if w < 50:
                w = 50
            if h < 50:
                h = 50
        im = Image.new('RGB', (w, h), '#000000')
        im.paste(img, (0, 0))
        img = im
    else:
        img = merge_imgs(imgs)

    b = io.BytesIO()
    img.save(b, format='PNG')
    image_content = b.getvalue()
    r = requests.post(url=bing_api, data=image_content,
                      headers={'Content-Type': 'application/octet-stream',
                               'Ocp-Apim-Subscription-Key': bing_credentials})
    try:
        if one_img:
            return ''.join([i['text'] for i in r.json()['regions'][0]['lines'][0]['words']])
        else:
            return [''.join(i['text'] for i in line['words'])
                    for line in r.json()['regions'][0]['lines']], r.json()
    except Exception:
        return ''


async def parse_by_async_bing(img):
    if not bing_credentials:
        raise ValueError('Set Bing Computer Vision API Credentials first')

    # Check if image size have 50x50
    w, h = img.size
    if w < 50 or h < 50:
        if w < 50:
            w = 50
        if h < 50:
            h = 50
        im = Image.new('RGB', (w, h), '#000000')
        im.paste(img, (0, 0))
        img = im

    b = io.BytesIO()
    img.save(b, format='PNG')
    image_content = b.getvalue()
    async with aiohttp.ClientSession() as session:
        async with session.post(url=bing_api, data=image_content,
                                headers={
                                    'Content-Type': 'application/octet-stream',
                                    'Ocp-Apim-Subscription-Key': bing_credentials}) as resp:
            try:
                j = await resp.json()
                return ''.join([i['text'] for i in j['regions'][0]['lines'][0]['words']])
            except Exception:
                return ''


def parse_by_google(img):
    if not service:
        raise ValueError('Set Google Vision API Credentials first')

    b = io.BytesIO()
    img.save(b, format='PNG')
    image_content = base64.b64encode(b.getvalue())
    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
            },
            'features': [{
                'type': 'TEXT_DETECTION',
            }]
        }]
    })

    response = service_request.execute()
    try:
        return response['responses'][0]['textAnnotations'][0]['description']
    except KeyError:
        return ''
