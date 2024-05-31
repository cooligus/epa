from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import os
import requests

if __name__ == "__main__":
    ITEMS = 'tmp/items.json'
    BASE_URL = 'https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/wszystko/'
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
    
    confirm = input()
    if confirm == True:
        with open(ITEMS) as f:
            d = json.load(f)
            for elem in d:
                if elem['imageSrc'] == None:
                    continue
                print(elem)
                imageUrl = os.path.join(BASE_URL, elem['imageSrc'])
                img_data = requests.get(imageUrl).content
                with open(os.path.join('tmp' + elem['imageName']), 'wb') as handler:
                    handler.write(img_data)
