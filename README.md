![pynayzr logo](https://github.com/pynayzr/pynayzr/blob/master/README/logo.png)

# PyNayzr - Taiwan TV-Media Analyzer

This project want to analysis Taiwan TV news media content, using Python,
tesseract and AI to analyze news content by live stream with frame.

## Requirements

Please install these package before you start to use news analyzer

* ffmpeg
* tesseract

## Apply for OCR API Keys

* Google Cloud Vision API: https://cloud.google.com/vision/
* Microsoft Computer Vision API: https://www.microsoft.com/cognitive-services/en-us/computer-vision-api

Please note: Google Cloud Vision API key MUST use Service Account Credentials
(服務帳戶金鑰) with JSON type, and Microsoft Computer Vision API key MUST use
plain text key

## Basic Usage and Example

```bash
usage: pynayzr [-h] [--bc BC] [--gc GC] [-n NEWS] [-i INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  --bc BC, --bing-credentials BC
                        Specific Bing Computer Vision API credentials key
  --gc GC, --google-credentials GC
                        Specific Google API credentials json filename
  -n NEWS, --news NEWS  Specific which news to analyze
  -i INPUT, --input INPUT
                        input image filename
  -o OUTPUT, --output-name OUTPUT
                        Specific image output place
```

### Analyze TVBS live, and using Google OCR

You must use json server side key to enable Google OCR API

```bash
$ pynayzr --gc key.json -n tvbs
{"title": "天外飛萊輪胎砸甲車 駕駛,乘客驚聲尖叫\n", "subpoint": null, "subtitle": "7天禁宰-送運松村滷味鴨賞恐缺貨衝擊\n", "type": "news", "source": null, "news": "tvbs", "timestamp": "2017-02-17 12:54:12"}
```

### Analyze TVBS, and save the image

The options `-o` should only indicate directory, not including filename

```bash
$ pynayzr --gc key.json -n tvbs -o .
{"title": "天外飛萊輪胎砸甲車 駕駛,乘客驚聲尖叫\n", "subpoint": null, "subtitle": "7天禁宰-送運松村滷味鴨賞恐缺貨衝擊\n", "type": "news", "source": null, "news": "tvbs", "timestamp": "2017-02-17 12:54:12"}
$ ls
tvbs.jpg
```

### Reanalyze from image

You can reanalyze the image if you update the core, or want to use another OCR
method to get the text. Note that you should also indicate the news source, so
that pynayzr can parse in correct news cropper

```bash
$ pynayzr --bc xxxxxxxxxxxxxxxx -n tvbs -i tvbs.jpg
{"title": "林佑璇", "subpoint": null, "subtitle": "你們要幹嘛﹗借皇簑的反違尋仇 店面全砸爛", "type": "news", "source": null, "news": "tvbs", "timestamp": "2017-02-17 12:58:47"}
```

## Capture live stream to image in command line

```bash
livestreamer -O https://www.youtube.com/watch\?v\=VsvZqiB2y1o 720p | ffmpeg -i - -f image2 -updatefirst 1 -r 1/5 out.jpg
```

## List of News

* PTS 公共電視 網路直播 PTS Live: https://www.youtube.com/watch?v=zjGR32QyTkQ
* TTV 台視新聞台HD直播: https://www.youtube.com/watch?v=yk2CUjbyyQY
* SET 三立新聞直播: https://www.youtube.com/watch?v=TgGyBF-7w8M
* CTI 中天新聞24小時HD新聞直播: https://www.youtube.com/watch?v=VsvZqiB2y1o
* EBC 東森新聞 51 頻道 24 小時線上直播: https://www.youtube.com/watch?v=yzE3bRtXIrI
* FTV 台灣民視新聞HD直播: https://www.youtube.com/watch?v=XxJKnDLYZz4
* CTV 中視新聞台 LIVE直播: https://www.youtube.com/watch?v=b3QIfgD--_E
* CTS 華視新聞HD直播: https://www.youtube.com/watch?v=1I6fxNSmQh4

## Reference

* 驗證資料來源: https://www.ptt.cc/bbs/Gossiping/M.1487052389.A.1E9.html
* 論文分析：[台灣電視媒體國際新聞之內容分析與產製研究 - 2003](http://www.comm.fju.edu.tw/journal/sites/default/files/data/mc01001.pdf)
