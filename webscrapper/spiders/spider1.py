import scrapy
from multiprocessing import Process
from twisted.internet import reactor
from scrapy import signals
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from threading import Lock, Event
from scrapy.utils.project import get_project_settings
import os

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open("text.txt","a") as file:
            for quote in response.css('div.quote'):
                file.write(quote.css('span.text::text').extract_first())
                file.write("\n")

def execute_crawling():
    runner = CrawlerRunner()
    d = runner.crawl(QuotesSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() 

def run_spider(keyword):
    p = Process(target=execute_crawling)
    p.start()
    p.join()

