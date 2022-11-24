import scrapy
from ..items import NewsItem
import json
import parse
import sys
from ..utils import url_generator as ug
from datetime import datetime, timedelta

table_cols=[
    "origin",
    "end",
    "distance",
    "time",
    "elevation",
]
import os
print(os.getcwd())

class NewsSpider(scrapy.Spider):
    name="news"

    keywords=ug.get_keywords()

    url_lists=[ug.get_urls_for_keyword(kw) for kw in keywords]

    start_urls = []
    for sublist in url_lists:
        start_urls.extend(sublist)

    
    def parse(self, response, **kwargs):

        search_url=response.url

        results=response.css(".left-column")

        for i, article in enumerate(results.css(".article-block")):

            item=NewsItem()

            title=article.css(".article-title::text").extract_first()
            link=article.css(".article-link::attr(href)").extract_first()
            date=article.css(".article-date::text").extract_first()

            

            item["search_url"]=search_url
            item["title"]=title
            item["link"]=response.urljoin(link)
            item["date"]=date

            date=date.lower()

            if "órája" in date or "perce" in date or "tegnap" in date:
                yield item
                
            else:
                date_obj = datetime. strptime(date, '%Y.%m.%d. %H:%M')     

                if datetime.now()-timedelta(days=1) < date_obj:
                    yield item

if __name__ == '__main__':
    keywords=ug.get_keywords()

    url_lists=[ug.get_urls_for_keyword(kw) for kw in keywords]

    start_urls = []
    for sublist in url_lists:
        start_urls.extend(sublist)

    print(start_urls)