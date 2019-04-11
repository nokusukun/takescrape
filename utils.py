import os
from io import BytesIO

import requests
from PIL import Image
import parse

def extractor(mapping):
    return parse.parse("i:{sx:d},{sy:d}+{sxoff:d},{syoff:d}>{dx:d},{dy:d}", mapping)

def unscrambler(source, usmap):
    unscrambled = Image.new('RGB', (usmap['width'], usmap['height']))
    for mapping in usmap['coords']:
        m = extractor(mapping)
        unscrambled.paste(
            source.crop((
                m['sx'], 
                m['sy'], 
                m['sx'] + m['sxoff'], 
                m['sy'] + m['syoff']
            )),
            (m['dx'], m['dy'])
        )
    return unscrambled


def processImage(imageBinary, usJson):
    scrambled = Image.open(imageBinary)
    unscrambled = unscrambler(scrambled, usJson['views'][0])
    return unscrambled


def getPage(manga, chapter, page):
    print(f'Downloading {manga}/{chapter}/{page}')
    urlTemp = "http://webcomicgamma.takeshobo.co.jp/manga/{manga}/_files/{chapter:03}/data/{page:04}.{fmt}"
    image = requests.get(urlTemp.format(
        manga=manga, 
        chapter=int(chapter), 
        page=int(page), 
        fmt='jpg'))
    if image.status_code != 200:
        return None
    ptimg = requests.get(urlTemp.format(
        manga=manga, 
        chapter=int(chapter), 
        page=int(page), 
        fmt='ptimg.json')).json()
    return processImage(BytesIO(image.content), ptimg)


def getChapter(manga, chapter):
    folder = os.path.join(manga, f"{int(chapter):03}")
    os.makedirs(folder,exist_ok=True)

    page_no = 1
    page = getPage(manga, chapter, page_no)
    if not page:
        return False
    
    while page:
        page.save(os.path.join(folder, f"{page_no:03}.png"))
        page_no += 1
        page = getPage(manga, chapter, page_no)
    
    return True
