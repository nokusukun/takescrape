import sys

import utils

if __name__ == "__main__":
    try:
        manga, chapter = sys.argv[1:]
        utils.getChapter(manga, chapter)

    except ValueError:
        print('Usage: takescrape.py manga(url manga name) chapter(omit for all chapters)')
        print('Ex: py takescrape.py bokudun 1')
        print('-- Note --')
        print('Takeshobo now secures their image server and restricts access to chapters that aren\'t visible on the site.')