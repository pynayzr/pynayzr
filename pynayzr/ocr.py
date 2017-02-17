# -*- coding: utf-8 -*-

import requests

# Tesseract
import pyocr
import pyocr.builders

# Google Vision API
import io
import base64
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

# Tesseract Settings
tools = pyocr.get_available_tools()
tool = tools[0]
lang = 'chi_tra'

# Google Vision Settings
credentials = None
service = None

# Bing Computer Vision Settings
bing_api = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/ocr?language=zh-Hant&detectOrientation=false'
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


def parse_by_bing(img):
    if not bing_credentials:
        raise ValueError('Set Bing Computer Vision API Credentials first')

    b = io.BytesIO()
    img.save(b, format='PNG')
    image_content = b.getvalue()
    r = requests.post(url=bing_api, data=image_content,
                      headers={'Content-Type': 'application/octet-stream',
                               'Ocp-Apim-Subscription-Key': bing_credentials})

    try:
        return ''.join([i['text'] for i in r.json()['regions'][0]['lines'][0]['words']])
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
