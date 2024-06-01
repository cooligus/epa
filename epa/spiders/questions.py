import scrapy
import os.path
import urllib.request

class QuestionsSpider(scrapy.Spider):
    name = "questions"
    start_urls = [
        "https://www.praktycznyegzamin.pl/inf03ee09e14/teoria/wszystko/",
    ]

    def parse(self, response):
        for quote in response.css(".question"):
            imageName = None

            imageSrc = quote.css("div.image > img::attr(src)").get()
            if imageSrc != None:
                imageName = os.path.split(imageSrc)[-1]
            else:
                imageSrc = quote.css("div.image > video > source::attr(src)").get()
                if imageSrc != None:
                    imageName = os.path.split(imageSrc)[-1]

            answer = ""
            answers = []
            for htmlAnswer in quote.css("div.answer"):
                possibleAnswer = htmlAnswer.css("div::text").get()
                answers.append(possibleAnswer)
                good = htmlAnswer.css(".correct").extract_first()
                if good:
                    answer += "1 "
                    correctAnswer = possibleAnswer
                else:
                    answer += "0 "
            yield {
                "Question": quote.css("div.title::text").get(),
                "QType": '2',
                "Q_1": answers[0],
                "Q_2": answers[1],
                "Q_3": answers[2],
                "Q_4": answers[3],
                "Answers": answer,
                "CorrectAnswer": correctAnswer,
                "ImageSrc": imageSrc,
                "ImageName": imageName,
            }

