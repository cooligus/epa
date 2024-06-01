from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import os
import requests
import html
import genanki

if __name__ == "__main__":
    MODEL_ID = 1739533466
    DECK_ID = 1990990076
    BUILD = 'tmp'
    ITEMS = os.path.join(BUILD, 'items.json')
    ANKI_DECK = 'dest/egzaminpraktyczny.apkg'
    BASE_URL = 'https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/wszystko/'

    print("Do you want to download questions? [y/n]")
    confirm = input()
    if confirm == "y":
        try:
            os.remove(ITEMS)
        except OSError:
            pass

        spider = 'questions'
        settings = get_project_settings()
        settings["FEEDS"] = {
            ITEMS: {"format": "json"}
        }
        process = CrawlerProcess(settings)
        process.crawl(spider, start_urls = [BASE_URL])
        process.start()
    
    print("Do you want to download images? [y/n]")
    confirm = input()
    if confirm == "y":
        with open(ITEMS) as f:
            d = json.load(f)
            for elem in d:
                if elem['ImageSrc'] == None:
                    continue
                print(elem)
                imageUrl = os.path.join(BASE_URL, elem['ImageSrc'])
                img_data = requests.get(imageUrl).content
                with open(os.path.join('tmp', elem['ImageName']), 'wb') as handler:
                    handler.write(img_data)

    my_deck = genanki.Deck(
      DECK_ID,
      'Egzamin praktyczny')

    my_model = genanki.Model(
      MODEL_ID,
      'Pole jednokrotnego wyboru',
      fields=[
        {'name': 'Question'},
        {'name': 'QType'},
        {'name': 'Q_1'},
        {'name': 'Q_2'},
        {'name': 'Q_3'},
        {'name': 'Q_4'},
        {'name': 'Answers'},
        {'name': 'CorrectAnswer'},
        {'name': 'Image'},
      ],
      templates=[
        {
          'name': 'Pole jednokrotnego wyboru',
          'qfmt': '{{Question}}<hr>{{Q_1}}<br><br>{{Q_2}}<br><br>{{Q_3}}<br><br>{{Q_4}}<br><br>{{Image}}',
          'afmt': '{{FrontSide}}<hr id="answer">{{CorrectAnswer}}',
        },
      ])

    my_package = genanki.Package(my_deck)
    my_package.media_files = []

    with open(ITEMS) as f:
        d = json.load(f)
        for elem in d:
            ids = ['Question', 'QType', 'Q_1', 'Q_2', 'Q_3', 'Q_4', 'Answers', 'CorrectAnswer']
            data = []
            for id in ids:
                data.append(html.escape(elem[id]))

            image = ''
            if elem['ImageName'] != None:
                if elem['ImageName'][-3:] == 'mp4':
                    image = '<video src="{}">'.format(elem['ImageName'])
                else:
                    image = '<img src="{}">'.format(elem['ImageName'])
            data.append(image)
            my_note = genanki.Note(
                model=my_model,
                fields=data
            )
            if elem['ImageSrc'] != None:
                my_package.media_files.append(os.path.join(BUILD, elem['ImageName']))

            my_deck.add_note(my_note)

    try:
        os.mkdir('dest')
    except OSError:
        pass
    my_package.write_to_file(ANKI_DECK)