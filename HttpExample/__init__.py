import logging
from webscrapper.spiders.spider1 import QuotesSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process
import azure.functions as func
import os


# Execute crawler in a new thread
def execute_crawling():
    runner = CrawlerRunner()
    d = runner.crawl(QuotesSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run() 

# Create a new thread to run spider
def run_spider():
    p = Process(target=execute_crawling)
    p.start()
    p.join()



# Http triggered azure function
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(type(QuotesSpider))
    run_spider()
    
    text = ""
    # Read from a file
    f = open("text.txt", "r")
    for x in f:
        text = text + x
    
    # Delete a file 
    os.remove("text.txt")
    
    return func.HttpResponse(f"Hello, {text}. This HTTP triggered function executed successfully.")
    

